import os
import sys
import json
import yaml
import signal
import argparse
from typing import Optional
from threading import Thread
from unidecode import unidecode
from flask import Flask, render_template, request, jsonify, url_for, redirect
from queue import Empty as EmptyQueue
from python import speech, language, utils, curriculum, structured_course, dictionary_verbs
from python.memory import Memory
from python.config import Config
from python.chatbot import Chatbot
from python.app_cache import AppCache
from python.consts import TEMP_DIR_NAME, TEMP_DIR, LTM_DIR, SAVED_SESSION_FILE, MALE_TUTORS, FEMALE_TUTORS, INPUT_LANGUAGES


app = Flask(__name__)

config: Optional[Config] = None
memory: Optional[Memory] = None
chatbot: Optional[Chatbot] = None
app_cache = AppCache()
voices_by_features = dict()
audio_queue_reject_remaining_fragments = False


@app.template_filter('convert_special')
def convert_special_letters(input_str):
    return unidecode(input_str)


@app.route('/')
def home():
    """
    Homepage of web UI
    """
    global memory, chatbot, config

    should_restart = bool(request.args.get('restart', 0))
    if should_restart:
        restart()

    memory = Memory()
    try:
        chatbot = Chatbot(config=config, memory=memory)
        languages = [config.language.learning, config.language.native, 'A']
        auto_send_recording = int(config.behavior.auto_send_recording)
        user_profile_img = config.user.image
        bot_profile_img = config.bot.image
    except Exception as e:
        languages = ['A']
        auto_send_recording = 0
        app_cache.server_errors.append(utils.get_error_message_from_exception(e))
        user_profile_img = ''
        bot_profile_img = ''

    if os.path.exists(TEMP_DIR):
        for f in os.listdir(TEMP_DIR):
            os.remove(os.path.join(TEMP_DIR, f))
    else:
        os.makedirs(TEMP_DIR)

    if not os.path.exists(LTM_DIR):
        os.makedirs(LTM_DIR)

    return render_template('index.html', languages=languages, auto_send_recording=auto_send_recording,
                           user_profile_img=user_profile_img, bot_profile_img=bot_profile_img)


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """
    Web page, setup page
    """
    if request.method == 'POST':
        filename = request.form.get('filename')
        app_cache.config_file = filename
        data = {
            "model": {
                "name": request.form.get('model-name'),
                "temperature": float(request.form.get('temperature'))
            },
            "user": {
                "name": request.form.get('user-name'),
                "image": request.form.get('profile-img-url'),
                "gender": request.form.get('gender')
            },
            "bot": {
                "name": request.form.get('tutor').split("-")[0],
                "image": f"/static/bots_profile/{unidecode(request.form.get('tutor').split('-')[0].lower())}.png",
                "gender": request.form.get('tutor').split("-")[1].lower(),
                "voice": request.form.get('voices-dropdown')
            },
            "language": {
                "native": request.form.get('user-lang-dropdown').lower(),
                "learning": request.form.get('tutor-lang-dropdown').split("-")[0].lower(),
                "level": request.form.get('lang-level')
            },
            "behavior": {
                "auto_send_recording": bool(request.form.get('auto-send-switch'))
            }
        }
        api_key = (request.form.get('gemini-api-key') or '').strip()
        if api_key:
            with open(os.path.join(os.getcwd(), 'keys.yml'), 'w') as keyfile:
                yaml.dump({'gemini': {'api_key': api_key}}, keyfile, allow_unicode=True)
        with open(os.path.join(os.getcwd(), filename), 'w') as outfile:
            yaml.dump(data, outfile, allow_unicode=True)
        return jsonify({'status': 'success'})

    else:
        return render_template('setup.html', males=MALE_TUTORS, females=FEMALE_TUTORS,
                               input_languages_codes_and_names=[[language.language_name_to_iso6391(lang), lang]
                                                                for lang in INPUT_LANGUAGES],
                               output_languages_locales_and_names=[[k, language.locale_code_to_language(k, name_in_same_language=True)]
                                                                   for k in voices_by_features.keys()]
                               )

@app.route("/get_next_from_audio_queue", methods=['GET'])
def get_next_from_audio_queue():
    try:
        filename = app_cache.play_recordings_queue.get(timeout=1)
        filename = url_for('static', filename=f'{TEMP_DIR_NAME}/{filename.split("/")[-1]}')
        empty = False
    except EmptyQueue:
        filename = None
        empty = True
    return jsonify({'file_url': filename, 'empty': int(empty)})


@app.route("/clear_audio_queue", methods=['GET'])
def clear_audio_queue():
    global audio_queue_reject_remaining_fragments
    audio_queue_reject_remaining_fragments = True
    app_cache.play_recordings_queue.queue.clear()
    return jsonify({'message': 'Audio cache cleared'})


def put_in_audio_queue(filename: str) -> bool:
    """
    Helper function to put filename in audio queue

    :param filename: filename to put in queue
    """
    global audio_queue_reject_remaining_fragments
    if audio_queue_reject_remaining_fragments:
        fragment_index = int(filename.split('_')[-1].split('.')[0])
        if fragment_index > 0:
            return False
        else:
            audio_queue_reject_remaining_fragments = False
    app_cache.play_recordings_queue.put(filename)
    return True


@app.route('/upload_recording', methods=['POST'])
def upload_recording():
    return_json = dict()
    if 'file' in request.files:
        file = request.files['file']
        raw_recording_filename = os.path.join(TEMP_DIR, "raw_recording")
        file.save(raw_recording_filename)
        try:
            mp3_filename = os.path.join(TEMP_DIR, f"user_recording_{len(memory)}_0.mp3")
            utils.convert_file_and_save_as_mp3(raw_recording_filename, mp3_filename)
            app_cache.user_recording = mp3_filename
        except Exception as e:
            app_cache.server_errors.append(utils.get_error_message_from_exception(e))
            mp3_filename = None
        return_json['filename'] = mp3_filename
    else:
        return_json['filename'] = None
    return jsonify(return_json)


@app.route('/get_language_voices', methods=['POST'])
def get_language_voices():
    """
    Get supported voices by TTS
    """
    lang_locale = request.form['language']
    gender = request.form['gender'].lower()
    voices = voices_by_features.get(lang_locale, {}).get(gender, [])
    return jsonify({'voices': voices})


@app.route('/play_bot_test_text', methods=['POST'])
def play_bot_test_text():
    """
    Play testing text-to-speech text from setup page
    """
    text = request.form['text']
    lang_code = request.form['lang']
    voice_name = request.form['voice']
    voice = speech.get_voice_object(voice_name=voice_name, language_code=lang_code)
    filename = utils.bot_text_to_speech(text, 0, 0, voice=voice)
    return jsonify({'file_url': url_for('static', filename=f'{TEMP_DIR_NAME}/{filename.split("/")[-1]}')})


@app.route('/get_response', methods=['POST'])
def get_response():
    """
    Get response from chatbot
    """
    global audio_queue_reject_remaining_fragments
    audio_queue_reject_remaining_fragments = False
    error_message = None
    first_message = ''
    try:
        is_initial_message = bool(int(request.form['is_initial_message']))
        app_cache.message_generator = chatbot.get_response(is_initial_message)
        app_cache.last_sentence = ''
        app_cache.sentences_counter = 0
        app_cache.bot_recordings = list()
        first_message = next(app_cache.message_generator)
        app_cache.generated_message = first_message
    except Exception as e:
        error_message = utils.get_error_message_from_exception(e)
    finally:
        return jsonify({'message': first_message,
                        'message_index': len(memory),
                        'error': error_message})


@app.route('/get_next_message', methods=['POST'])
def get_next_message():
    """
    Helper endpoint for '/get_response', to handle the generator yielded by the chatbot.
    It returns the next characters in generator till it is consumed, then queues the full response for TTS.
    """
    index = int(request.form['message_index'])
    if app_cache.message_generator is None:
        return jsonify({'message': None})
    try:
        next_message = next(app_cache.message_generator)
        app_cache.generated_message += next_message
        return jsonify({'message': app_cache.generated_message})
    except StopIteration:
        full_message = app_cache.generated_message.strip()
        if full_message != '':
            app_cache.text2speech_queue.put({"text": full_message,
                                             "counter": 0,
                                             "message_index": index})
        store_message(sender="assistant", message=app_cache.generated_message)
        app_cache.message_generator = None
        app_cache.generated_message = ''
        return jsonify({'message': None})


@app.route('/transcribe_recording', methods=['POST'])
def transcribe_recording():
    """
    Transcribe user recording using speech-to-text service
    """
    recorded_text = None
    error_message = None
    filename = request.form['filename']
    try:
        recorded_text = speech.speech2text(filename, language=app_cache.language)
    except Exception as e:
        error_message = utils.get_error_message_from_exception(e)
    finally:
        return jsonify({'recorded_text': recorded_text,
                        'error': error_message})


@app.route('/store_message', methods=['POST'])
def store_message(sender: Optional[str] = None, message: Optional[str] = None):
    """
    Save message in memory

    :param sender: role of message creator ("system", "user" or "assistant")
    :param message: message text
    """
    sender = sender or request.form['sender']
    message = message or request.form['message']
    memory.add(role=sender, message=message, user_recording=app_cache.user_recording,
               recording=app_cache.bot_recordings if sender == "assistant" else [])
    app_cache.user_recording = None
    return jsonify({'status': 'success'})


@app.route('/user_message_info', methods=['POST'])
def user_message_info():
    """
    Get metadata regarding user message. This is required for tbe frontend.
    """
    error_message = None
    message = request.form['message']
    try:
        is_language_learning = language.is_text_of_language(message, config.language.learning)
    except Exception as e:
        is_language_learning = False
        error_message = utils.get_error_message_from_exception(e)
    return jsonify({'user_recording': app_cache.user_recording,
                    'is_language_learning': is_language_learning,
                    'error': error_message})


@app.route('/play_bot_recording', methods=['POST'])
def play_bot_message():
    """
    Play selected message's bot recording if exists. If not, send text to TTS and play audio
    """
    global audio_queue_reject_remaining_fragments
    audio_queue_reject_remaining_fragments = False
    index = int(request.form['message_id'].split('_')[1])
    recordings = memory[index]["recording"] if index < len(memory) else []
    existing_recordings = [r for r in (recordings or []) if r and os.path.exists(r)]
    if len(existing_recordings) == 0:
        app_cache.text2speech_queue.put({"text": request.form["text"], "counter": 0,
                                         "message_index": index, 'skip_cache': True})
    else:
        for r in existing_recordings:
            put_in_audio_queue(r)
    return jsonify({'message': 'Recordings inserted to queue'})


@app.route('/play_user_recording', methods=['POST'])
def play_user_message():
    """
    Play user recording if exists
    """
    message_id = int(request.form['message_id'].split('_')[1])
    user_recording = memory[message_id]['user_recording']
    if user_recording:
        put_in_audio_queue(user_recording)
    return jsonify({'message': 'User message played successfully'})


@app.route('/set_language', methods=['POST'])
def set_language():
    """
    Set user recording language
    """
    language = request.form['language']
    if language == 'A':
        language = None
    app_cache.language = language
    return jsonify({'message': f'Language set successfully to {request.form["language"]}'})


@app.route('/translate_text', methods=['POST'])
def translate_text():
    """
    Translate message
    """
    message = request.form["text"]
    sender = request.form["sender"]
    lang = config.language.native if sender == "assistant" else config.language.learning
    try:
        translated = language.translate(message, to=lang)
    except Exception as e:
        app_cache.server_errors.append(utils.get_error_message_from_exception(e))
        translated = None
    return jsonify({'message': translated})


@app.route('/save_session', methods=['GET'])
def save_session():
    """
    Save current session as file
    """
    data = list()
    for m in memory.get_chat_history()[1:]:
        data.append({"role": m["role"], "content": m["content"]})

    json_data = json.dumps(data, indent=4)  # Convert the list of dictionaries to JSON format

    with open(SAVED_SESSION_FILE, "w") as f:
        f.write(json_data)

    return jsonify({"success": True})


@app.route('/load_session', methods=['GET'])
def load_session():
    """
    Load session from file
    """
    global memory, chatbot
    if os.path.isfile(SAVED_SESSION_FILE):
        with open(SAVED_SESSION_FILE, 'r') as f:
            messages = json.load(f)

            memory = Memory()
            chatbot = Chatbot(config=config, memory=memory)

            for message in messages:
                memory.add(role=message["role"], message=message["content"])
                if message["role"] == "user":
                    try:
                        message["is_language_learning"] = language.is_text_of_language(message["content"], config.language.learning)
                    except Exception as e:
                        message["is_language_learning"] = False
                        app_cache.server_errors.append(utils.get_error_message_from_exception(e))
                else:
                    message["is_language_learning"] = True

    else:
        messages = []

    return jsonify({"messages": messages})


@app.route('/check_server_errors', methods=['GET'])
def check_server_errors():
    """
    Check for errors saved in `app_cache`, and display on web UI
    """
    server_errors = app_cache.server_errors.copy()
    app_cache.server_errors = []
    return jsonify({'server_errors': server_errors})


@app.route('/memory', methods=['GET'])
def print_memory():
    """
    Helper endpoint for debugging. Print memory.
    """
    return json.dumps(memory.list, indent=4)


@app.route('/memory/updates', methods=['GET'])
def print_memory_updates():
    """
    Helper endpoint for debugging. Print memory updates.
    """
    return json.dumps(memory.updates, indent=4)


@app.route('/api/curriculum', methods=['GET'])
def api_get_curriculum():
    """
    Return all structured class modules (Classes 1-11 + custom uploaded classes), DELF B1 roadmap, study progress, and saved homework.
    """
    return jsonify({
        'classes': curriculum.get_all_classes(),
        'roadmap': curriculum.DELF_B1_ROADMAP,
        'progress': curriculum.load_progress(),
        'homework_history': curriculum.load_homework_submissions(),
    })


@app.route('/api/evaluate_homework', methods=['POST'])
def api_evaluate_homework():
    """
    Evaluate and correct a student's written homework for a class or custom prompt, and save to homework history.
    """
    class_id = (request.form.get('class_id') or 'class-11').strip()
    custom_prompt = (request.form.get('custom_prompt') or '').strip()
    student_text = (request.form.get('student_text') or '').strip()
    if not student_text:
        return jsonify({'submission': None, 'error': 'Écris d\'abord ton devoir en français dans la zone de texte !'}), 400
    try:
        res = curriculum.evaluate_homework_submission(
            client=config.gemini.client,
            class_id=class_id,
            custom_prompt=custom_prompt,
            student_text=student_text,
        )
        return jsonify({
            'submission': res['submission'],
            'homework_history': res['history'],
            'error': None,
        })
    except Exception as e:
        return jsonify({'submission': None, 'error': utils.get_error_message_from_exception(e)}), 500


@app.route('/api/delete_homework', methods=['POST'])
def api_delete_homework():
    """
    Delete a saved homework submission by ID.
    """
    submission_id = (request.form.get('submission_id') or '').strip()
    history = curriculum.delete_homework_submission(submission_id) if submission_id else curriculum.load_homework_submissions()
    return jsonify({'homework_history': history, 'error': None})


@app.route('/api/speak_french', methods=['POST'])
def api_speak_french():
    """
    Synthesize any French phrase/sentence on demand and return the MP3 file URL for immediate browser playback.
    """
    import time
    text = (request.form.get('text') or '').strip()
    if not text:
        return jsonify({'file_url': None, 'error': 'Empty text'})
    try:
        os.makedirs(TEMP_DIR, exist_ok=True)
        stamp = int(time.time() * 1000) % 1000000
        filename = utils.bot_text_to_speech(text=text, message_index=999, counter=stamp)
        file_url = url_for('static', filename=f'{TEMP_DIR_NAME}/{os.path.basename(filename)}')
        return jsonify({'file_url': file_url, 'error': None})
    except Exception as e:
        return jsonify({'file_url': None, 'error': utils.get_error_message_from_exception(e)})


@app.route('/api/evaluate_exercise', methods=['POST'])
def api_evaluate_exercise():
    """
    Evaluate a user's written or spoken exercise response using Gemini and optionally synthesize spoken feedback.
    """
    import time
    class_id = request.form.get('class_id', 'class-11')
    item_id = request.form.get('item_id', '')
    prompt_text = request.form.get('prompt_text', '')
    user_answer = (request.form.get('user_answer') or '').strip()
    expected_answer = request.form.get('expected_answer', '')
    mode = request.form.get('mode', 'speaking')

    if not user_answer:
        return jsonify({'error': 'Please enter or record your answer in French first.'}), 400

    try:
        evaluation = curriculum.evaluate_answer_with_gemini(
            client=config.gemini.client,
            class_id=class_id,
            prompt_text=prompt_text,
            user_answer=user_answer,
            expected_answer=expected_answer,
            mode=mode,
        )
        if item_id and evaluation.get('score', 0) >= 6:
            category = 'completed_speaking' if mode == 'speaking' else 'completed_exercises'
            curriculum.save_progress_item(category, item_id)

        audio_url = None
        spoken_fr = evaluation.get('spoken_feedback_fr', '')
        if spoken_fr and mode == 'speaking':
            try:
                stamp = int(time.time() * 1000) % 1000000
                filename = utils.bot_text_to_speech(text=spoken_fr, message_index=998, counter=stamp)
                audio_url = url_for('static', filename=f'{TEMP_DIR_NAME}/{os.path.basename(filename)}')
            except Exception:
                audio_url = None

        return jsonify({
            'evaluation': evaluation,
            'audio_url': audio_url,
            'progress': curriculum.load_progress(),
            'error': None,
        })
    except Exception as e:
        return jsonify({'evaluation': None, 'error': utils.get_error_message_from_exception(e)})


@app.route('/api/mark_progress', methods=['POST'])
def api_mark_progress():
    category = request.form.get('category', 'completed_exercises')
    item_id = request.form.get('item_id', '')
    progress = curriculum.save_progress_item(category, item_id) if item_id else curriculum.load_progress()
    return jsonify({'progress': progress})


@app.route('/api/generate_exercises', methods=['POST'])
def api_generate_exercises():
    """
    Generate fresh written and oral exercises for a selected class using Gemini.
    """
    class_id = request.form.get('class_id', 'class-11')
    try:
        generated = curriculum.generate_dynamic_exercises(client=config.gemini.client, class_id=class_id)
        return jsonify({'generated': generated, 'error': None})
    except Exception as e:
        return jsonify({'generated': None, 'error': utils.get_error_message_from_exception(e)})


@app.route('/api/import_class', methods=['POST'])
def api_import_class():
    """
    Import a new class module from an uploaded PDF file or pasted class notes using Gemini.
    """
    try:
        class_number = int(request.form.get('class_number', len(curriculum.get_all_classes()) + 1))
        class_date = request.form.get('class_date', 'New Class')
        raw_notes = request.form.get('notes', '')
        pdf_bytes = None
        if 'file' in request.files and request.files['file'].filename:
            pdf_bytes = request.files['file'].read()
        if not pdf_bytes and not raw_notes.strip():
            return jsonify({'new_class': None, 'error': 'Please upload a PDF or paste your class notes.'})
        new_class = curriculum.import_new_class_from_pdf_or_text(
            client=config.gemini.client,
            class_number=class_number,
            class_date=class_date,
            raw_notes=raw_notes,
            pdf_bytes=pdf_bytes,
        )
        return jsonify({'new_class': new_class, 'classes': curriculum.get_all_classes(), 'error': None})
    except Exception as e:
        return jsonify({'new_class': None, 'error': utils.get_error_message_from_exception(e)})


@app.route('/api/set_chat_focus', methods=['POST'])
def api_set_chat_focus():
    """
    Focus the live tutor chat on a specific class or DELF B1 oral exam task.
    """
    global memory, chatbot
    focus_id = request.form.get('focus_id', '')
    focus_context = None
    if focus_id.startswith('class-'):
        cls = curriculum.get_class_by_id(focus_id)
        if cls:
            vocab_list = ', '.join(v['fr'] for v in cls.get('vocabulary', [])[:8])
            concepts_list = '; '.join(c['title'] for c in cls.get('concepts', []))
            focus_context = (
                f"Class {cls['number']}: {cls['title']}. Summary: {cls['summary']} "
                f"Grammar concepts to practice: {concepts_list}. Key vocabulary to encourage: {vocab_list}. "
                f"Homework topic: {cls.get('homework', '')}"
            )
    elif focus_id.startswith('b1-oral-'):
        for sim in curriculum.DELF_B1_ROADMAP['b1_speaking_simulators']:
            if sim['id'] == focus_id:
                focus_context = (
                    f"DELF B1 Oral Exam Simulation — {sim['part']} ({sim['title']}). "
                    f"Examiner prompt: {sim['prompt_fr']}. Coaching tips: {sim['tips']}"
                )
                break
    elif focus_id.startswith(('a1-', 'a2-', 'b1-')):
        mod = structured_course.get_course_module_by_id(focus_id)
        if mod:
            vocab_list = ', '.join(v['fr'] for v in mod.get('vocabulary', []))
            focus_context = (
                f"Structured Course Module {mod['code']} ({mod['level']}) — {mod['title']} [Theme: {mod['theme']}]. "
                f"Be a strict oral coach verifying the student's mastery of: {mod['quick_refresher']['rule_title']}. "
                f"Key vocabulary to test: {vocab_list}."
            )

    memory = Memory()
    chatbot = Chatbot(config=config, memory=memory)
    chatbot.set_focus_context(focus_context)
    return jsonify({'status': 'success', 'focus_context': focus_context})


@app.route('/api/structured_course', methods=['GET'])
def api_get_structured_course():
    """
    Return the full A1 -> A2 -> B1 structured course presented by Gemini and user progress tracker.
    """
    return jsonify({
        'levels': structured_course.STRUCTURED_COURSE_LEVELS,
        'progress': structured_course.load_course_progress(),
    })


@app.route('/api/evaluate_course_challenge', methods=['POST'])
def api_evaluate_course_challenge():
    """
    Strictly evaluate a spoken or A2 written challenge in the Structured Course (requires >= 8/10 for oral mastery).
    """
    import time
    module_id = request.form.get('module_id', 'a1-m1')
    prompt_text = request.form.get('prompt_text', '')
    user_answer = (request.form.get('user_answer') or '').strip()
    mandatory_raw = request.form.get('mandatory_structures', '[]')
    is_writing_a2 = bool(int(request.form.get('is_writing_a2', '0')))

    if not user_answer:
        return jsonify({'error': 'Parlez au micro ou écrivez votre réponse complète en français d\'abord.'}), 400

    try:
        mandatory_list = json.loads(mandatory_raw) if mandatory_raw else []
    except Exception:
        mandatory_list = []

    try:
        evaluation = structured_course.evaluate_strict_course_challenge(
            client=config.gemini.client,
            module_id=module_id,
            prompt_text=prompt_text,
            user_answer=user_answer,
            mandatory_structures=mandatory_list,
            is_writing_a2=is_writing_a2,
        )
        audio_url = None
        spoken_fr = evaluation.get('spoken_examiner_feedback_fr', '')
        if spoken_fr:
            try:
                stamp = int(time.time() * 1000) % 1000000
                filename = utils.bot_text_to_speech(text=spoken_fr, message_index=997, counter=stamp)
                audio_url = url_for('static', filename=f'{TEMP_DIR_NAME}/{os.path.basename(filename)}')
            except Exception:
                audio_url = None

        return jsonify({
            'evaluation': evaluation,
            'audio_url': audio_url,
            'progress': structured_course.load_course_progress(),
            'error': None,
        })
    except Exception as e:
        return jsonify({'evaluation': None, 'error': utils.get_error_message_from_exception(e)})


@app.route('/api/toggle_course_review', methods=['POST'])
def api_toggle_course_review():
    module_id = request.form.get('module_id', '')
    progress = structured_course.toggle_module_review_flag(module_id) if module_id else structured_course.load_course_progress()
    return jsonify({'progress': progress})


@app.route('/api/verbs_and_starred', methods=['GET'])
def api_get_verbs_and_starred():
    """
    Return the common daily verbs conjugation list and the user's starred words.
    """
    return jsonify({
        'verbs': dictionary_verbs.COMMON_DAILY_VERBS,
        'starred_words': dictionary_verbs.load_starred_words(),
    })


@app.route('/api/dictionary_lookup', methods=['POST'])
def api_dictionary_lookup():
    """
    Look up any right-clicked French word: translation, multiple forms/conjugations, and example sentences.
    """
    word = (request.form.get('word') or '').strip()
    context = (request.form.get('context') or '').strip()
    if not word:
        return jsonify({'entry': None, 'error': 'Aucun mot sélectionné.'}), 400
    try:
        entry = dictionary_verbs.lookup_word_smart_dictionary(
            client=config.gemini.client,
            word=word,
            context_sentence=context,
        )
        starred_list = dictionary_verbs.load_starred_words()
        key = (entry.get('lemma') or entry.get('word') or '').strip().lower()
        is_starred = any((w.get('lemma') or w.get('word') or '').strip().lower() == key for w in starred_list)
        return jsonify({'entry': entry, 'is_starred': is_starred, 'error': None})
    except Exception as e:
        return jsonify({'entry': None, 'error': utils.get_error_message_from_exception(e)})


@app.route('/api/toggle_star_word', methods=['POST'])
def api_toggle_star_word():
    """
    Star or unstar a word from the right-click dictionary popup or Starred Words section.
    """
    raw_entry = request.form.get('entry_json', '{}')
    try:
        entry = json.loads(raw_entry)
        res = dictionary_verbs.toggle_starred_word(entry)
        return jsonify({'starred': res['starred'], 'starred_words': res['starred_words'], 'error': None})
    except Exception as e:
        return jsonify({'starred': False, 'starred_words': dictionary_verbs.load_starred_words(), 'error': utils.get_error_message_from_exception(e)})


@app.route('/api/conjugate_verb', methods=['POST'])
def api_conjugate_verb():
    """
    Conjugate any custom French verb searched on the Verb Conjugation page.
    """
    verb_query = (request.form.get('verb') or '').strip()
    if not verb_query:
        return jsonify({'verb_data': None, 'error': 'Entrez un verbe.'}), 400
    try:
        verb_data = dictionary_verbs.conjugate_any_verb_with_gemini(client=config.gemini.client, verb_query=verb_query)
        return jsonify({'verb_data': verb_data, 'error': None})
    except Exception as e:
        return jsonify({'verb_data': None, 'error': utils.get_error_message_from_exception(e)})


def exit_graceful(signum, frame) -> None:
    """
    Stop threads when app terminates.

    :param signum: required by `signal.signal`
    :param frame: required by `signal.signal`
    """
    app_cache.stop_threads_event.set()
    if app_cache.text2speech_thread is not None:
        app_cache.text2speech_thread.join()
    sys.exit(0)


def restart() -> None:
    """
    Restart app
    """
    global config
    try:
        config = Config.from_yml_file(app_cache.config_file)
    except FileNotFoundError:
        app_cache.server_errors.append("Config file not found. Go to /setup to configure the app.")
        config = Config({'bot': {'voice': 'Kore'}})

    if app_cache.keys_file and os.path.exists(app_cache.keys_file):
        config.update_from_yml_file(app_cache.keys_file)
    elif os.path.exists("keys.yml"):
        config.update_from_yml_file("keys.yml")

    gemini_client = utils.init_gemini(config)
    if gemini_client is None:
        app_cache.server_errors.append(
            "Gemini API key not found. Set GEMINI_API_KEY in your terminal or enter it in /setup (Advanced options)."
        )
    config.update(gemini={'client': gemini_client})

    language.init_language(client=gemini_client)
    speech.init_speech(config=config, client=gemini_client)


def run(port: int = 5001) -> None:
    """
    Run app
    """
    global voices_by_features
    restart()
    voices_by_features = speech.voices_by_features()
    app_cache.text2speech_thread = Thread(target=bot_text_to_speech_queue_func, daemon=True)
    app_cache.text2speech_thread.start()

    app.run(host="0.0.0.0", port=port)


########## THREADS ##########

def bot_text_to_speech_queue_func():
    """
    This function is meant to run on a parallel thread.
    It is responsible to send texts to the TTS service, and then place the filename in a different queue,
    in order to be played
    """
    global config, memory, app_cache
    while not app_cache.stop_threads_event.is_set():
        try:
            item = app_cache.text2speech_queue.get(timeout=1)  # Wait for 1 second to get an item
            idx = item["message_index"]
            filename = utils.bot_text_to_speech(text=item['text'], message_index=idx, counter=item['counter'])
            if not filename or not os.path.exists(filename):
                continue
            if item.get('skip_cache', False):
                memory.update(idx, recording=[filename])
            else:
                app_cache.bot_recordings.append(filename)
                memory.update(idx, recording=app_cache.bot_recordings)
            put_in_audio_queue(filename)

        except EmptyQueue:
            continue
        except Exception as e:
            app_cache.server_errors.append(utils.get_error_message_from_exception(e))


#############################


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config_file', default='config.yml', help='A config yml file.')
    parser.add_argument('-k', '--keys', dest='keys_file', help='A keys yml file [optional].')
    parser.add_argument('-p', '--port', dest='port', type=int, default=5001, help='Port to run the server on (default: 5001).')
    args = parser.parse_args()
    signal.signal(signal.SIGINT, exit_graceful)
    signal.signal(signal.SIGTERM, exit_graceful)
    app_cache.config_file = args.config_file
    app_cache.keys_file = args.keys_file
    run(port=args.port)
