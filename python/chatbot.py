from textwrap import dedent
from typing import Generator, Optional
from google import genai
from python.memory import Memory
from python.config import Config
from python.consts import DEFAULT_CHAT_MODEL
from python.language import iso6391_to_language_name

SYSTEM_PROMPT = """You are a {language} teacher named {teacher_name}, and you are a {bot_gender}. You are on a 1-on-1 
                   session with your student, {user_name}, who is a {user_gender}. {user_name}'s {language} level 
                   is: {level}. Your task is to assist your student in advancing their {language}.
                   * When the session begins, offer a suitable session for {user_name}, unless asked for 
                   something else.
                   * {user_name}'s native language is {user_language}. {user_name} might address you in their own
                   language when they feel their {language} is not good enough. When that happens, first translate their
                   message to {language}, and then reply.
                   * IMPORTANT: If your student makes any mistake, be it typo or grammar, you MUST first correct
                   your student and only then reply.
                   * Keep your responses concise, natural, and conversational (plain text, avoid markdown horizontal rules).
                   * You are only allowed to speak {language}."""

INITIAL_MESSAGE = """Start our session now: greet me warmly as my tutor and suggest 3 optional topics for our lesson 
                     suiting my level. Reply directly in {language} (do not translate this instruction)."""

TUTOR_INSTRUCTIONS = """
                     ---
                     IMPORTANT: 
                     * If I replied in {language} and made any mistakes (grammar, typos, etc), you must correct me 
                     before replying
                     * You must keep the session flow, your response cannot end the session. Try to avoid broad
                     questions like "what would you like to do", and prefer to provide me with related questions
                     and exercises. 
                     * You MUST reply in {language}.
                     """


def _resolve_gemini_model(configured_model: Optional[str]) -> str:
    """
    Ensure we always use a current Gemini model and replace legacy OpenAI or deprecated Gemini model strings.
    """
    if not configured_model:
        return DEFAULT_CHAT_MODEL
    lowered = configured_model.strip().lower()
    if lowered.startswith(("gpt-", "gemini-1.", "gemini-2.")):
        return DEFAULT_CHAT_MODEL
    return configured_model.strip()


class Chatbot:
    """
    This class is used to communicate with the tutor using the Gemini Interactions API
    """
    def __init__(self, config: Config, memory: Memory):
        self.client: genai.Client = config.gemini.client
        self._memory = memory
        self._model = _resolve_gemini_model(config.model.name)
        self._language = config.language.learning
        self._last_interaction_id: Optional[str] = None

        lang = iso6391_to_language_name(config.language.learning)
        user_lang = iso6391_to_language_name(config.language.native)
        self._language_name = lang
        self._system_prompt = dedent(SYSTEM_PROMPT.format(
            teacher_name=config.bot.name, user_name=config.user.name, language=lang, user_language=user_lang,
            level=config.language.level, user_gender=config.user.gender, bot_gender=config.bot.gender
        ))
        self._focus_context: Optional[str] = None
        self._memory.add("system", self._system_prompt)

    def set_focus_context(self, focus_context: Optional[str]) -> None:
        """
        Set an optional class or DELF B1 focus topic for the conversation session.
        """
        self._focus_context = focus_context
        self._last_interaction_id = None

    def get_response(self, is_initial_message: bool = False) -> Generator[str, None, None]:
        """
        Send message to Gemini Interactions API and receive a streamed response.

        :param is_initial_message: whether this is the initial greeting turn on app launch
        :return: Generator yielding streamed text chunks from Gemini
        """
        history = self._memory.get_chat_history()
        system_instruction = self._system_prompt
        if self._focus_context:
            system_instruction += f"\n\nCURRENT LESSON FOCUS:\n{self._focus_context}"

        if is_initial_message:
            self._last_interaction_id = None
            if self._focus_context:
                user_prompt = (
                    f"Start our session now focusing on: {self._focus_context}. "
                    f"Greet me warmly and ask me a first practice question on this topic in {self._language_name}."
                )
            else:
                user_prompt = dedent(INITIAL_MESSAGE.format(language=self._language_name))
        else:
            user_prompt = history[-1]["content"] + dedent(
                TUTOR_INSTRUCTIONS.format(language=self._language_name)
            )
            if self._last_interaction_id is None and len(history) > 2:
                past_turns = "\n".join(
                    f"{'Student' if m['role'] == 'user' else 'Tutor'}: {m['content']}"
                    for m in history[1:-1]
                )
                system_instruction = (
                    f"{self._system_prompt}\n\n"
                    f"Previous conversation history from loaded session:\n{past_turns}"
                )

        thinking_level = "minimal" if "lite" in self._model else "low"
        kwargs = {
            "model": self._model,
            "system_instruction": system_instruction,
            "input": user_prompt,
            "generation_config": {
                "thinking_level": thinking_level,
            },
            "stream": True,
        }
        if self._last_interaction_id is not None:
            kwargs["previous_interaction_id"] = self._last_interaction_id

        stream = self.client.interactions.create(**kwargs)
        return self._generate_response(stream)

    def _generate_response(self, stream) -> Generator[str, None, None]:
        """
        Helper generator that yields incremental text deltas and updates `_last_interaction_id`.
        """
        for event in stream:
            event_type = getattr(event, "event_type", None)
            if event_type in ("interaction.created", "interaction.completed"):
                interaction_obj = getattr(event, "interaction", None)
                if interaction_obj and getattr(interaction_obj, "id", None):
                    self._last_interaction_id = interaction_obj.id
            elif event_type == "step.delta":
                delta = getattr(event, "delta", None)
                if delta and getattr(delta, "type", None) == "text" and getattr(delta, "text", None):
                    yield delta.text
