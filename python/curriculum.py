import os
import re
import json
import base64
from typing import Dict, Any, List, Optional
from python.consts import DEFAULT_FAST_MODEL, LTM_DIR

CUSTOM_CLASSES_FILE = os.path.join(LTM_DIR, "custom_classes.json")
PROGRESS_FILE = os.path.join(LTM_DIR, "study_progress.json")

DELF_B1_ROADMAP = {
    "target_date": "End of February 2027",
    "current_level": "A2+ (Bridge to B1 — Class 11 Completed)",
    "feasibility_verdict": "Highly Achievable (85–90% confidence with 2 classes/week + 25 min/day practice)",
    "feasibility_summary": (
        "You have already completed 11 classes covering the core A2→B1 bridge: Passé Composé (avoir, être & ADVENT, "
        "pronominal verbs, past participle agreement), L'Imparfait vs. Passé Composé, Complex Negation (ne...plus, "
        "pas encore, jamais, rien, personne, ni...ni, ne...que), L'Impératif with pronouns, Question Registers, and "
        "key B1 connectors (cependant, toutefois, du coup, quand même, grâce à, à cause de). Living in Geneva gives "
        "you daily exposure, and 2 classes/week gives you ~32 more structured lessons before the end of February."
    ),
    "exam_requirements": {
        "passing_score": "50 / 100 total (minimum 5 / 25 in each of the 4 sections)",
        "sections": [
            {
                "name": "1. Compréhension de l'oral (Listening)",
                "duration": "25 min",
                "points": "25 pts",
                "details": "3 audio recordings (everyday conversations, radio interviews, announcements) played twice."
            },
            {
                "name": "2. Compréhension des écrits (Reading)",
                "duration": "45 min",
                "points": "25 pts",
                "details": "2–3 texts: analyzing practical information (comparing options) and understanding an article/opinion piece."
            },
            {
                "name": "3. Production écrite (Writing)",
                "duration": "45 min",
                "points": "25 pts",
                "details": "Write a 160–180 word personal essay, email, or forum post expressing experiences and your opinion with logical connectors."
            },
            {
                "name": "4. Production orale (Speaking)",
                "duration": "15 min (+ 10 min prep for Part 3)",
                "points": "25 pts",
                "details": "Part 1: Entretien dirigé (2–3 min about yourself, Geneva, past/future). Part 2: Exercice en interaction (3–4 min roleplay solving a problem). Part 3: Expression d'un point de vue (5–7 min monologue on a short text)."
            }
        ]
    },
    "milestones": [
        {
            "month": "Month 1 (November) — Classes 1–15: Past Tenses, Negation & Daily Life Mastery",
            "status": "In Progress (11/15 classes done)",
            "topics": [
                "Master Passé Composé (avoir, être ADVENT, pronominal verbs) vs. Imparfait (habits, descriptions, memories)",
                "Complex negations (ne...plus, pas encore, jamais, rien, personne, ni...ni) & restriction (ne...que)",
                "Pronoms compléments COD / COI (le, la, les, lui, leur) and pronoms Y & EN",
                "DELF B1 Speaking Part 1: Presenting your life in Geneva, your work, family, and childhood memories"
            ]
        },
        {
            "month": "Month 2 (December) — Classes 16–23: Future, Conditional & Relative Pronouns",
            "status": "Upcoming",
            "topics": [
                "Le Futur Simple vs. Futur Proche (making plans and predictions)",
                "Le Conditionnel Présent (politeness, advice 'tu devrais...', wishes 'j'aimerais...', hypotheses with 'si + imparfait')",
                "Relative pronouns: qui, que, où, dont (connecting complex sentences naturally)",
                "DELF B1 Speaking Part 2: Roleplay interactions (negotiating, complaining politely, finding a solution)"
            ]
        },
        {
            "month": "Month 3 (January) — Classes 24–31: Subjunctive & B1 Argumentation",
            "status": "Upcoming",
            "topics": [
                "Le Subjonctif Présent (il faut que, bien que, pour que, je voudrais que, émotions)",
                "B1 Logical Connectors: Cause (puisque, comme), Consequence (donc, par conséquent, du coup), Opposition (cependant, toutefois, pourtant, malgré)",
                "Reported speech (Discours indirect) & Plus-que-parfait",
                "DELF B1 Speaking Part 3 & Writing: Structuring a 170-word opinion essay and 5-minute monologue"
            ]
        },
        {
            "month": "Month 4 (February) — Classes 32–39: Full DELF B1 Mock Exams & Fluency Polish",
            "status": "Target Exam Month",
            "topics": [
                "Timed 160–180 word writing drills with B1 connector checklists",
                "Full 3-part Oral Exam simulations with Renée (Entretien + Interaction + Point de vue)",
                "Listening & Reading timed practice tests"
            ]
        }
    ],
    "b1_speaking_simulators": [
        {
            "id": "b1-oral-1",
            "part": "Partie 1 : Entretien dirigé (2–3 min)",
            "title": "Présentez-vous, votre vie à Genève et vos souvenirs",
            "prompt_fr": (
                "Bonjour ! Pour commencer cet entretien, pouvez-vous vous présenter ? Parlez-moi de votre vie actuelle "
                "à Genève avec votre famille (depuis combien de temps vous y habitez, ce que vous aimez dans votre quartier), "
                "de vos loisirs, et comparez votre vie d'aujourd'hui avec votre enfance (en utilisant le passé composé et l'imparfait)."
            ),
            "tips": "Use: 'J'habite à Genève depuis...', 'D'un côté... de l'autre côté...', 'À proximité, il y a...', Imparfait for childhood habits ('Quand j'étais petit, je jouais...'), and Passé Composé for key events ('Je me suis installé à Genève...')."
        },
        {
            "id": "b1-oral-2",
            "part": "Partie 2 : Exercice en interaction (Roleplay)",
            "title": "Inscription à un cours d'escalade — Changement de créneau",
            "prompt_fr": (
                "Vous vous êtes inscrit à un cours d'escalade hebdomadaire avec votre fils, mais à cause de votre travail, "
                "vous ne pouvez plus venir au créneau du mardi soir. Expliquez le problème à l'entraîneur et essayez de trouver "
                "une solution ensemble (changer de créneau ou obtenir un remboursement)."
            ),
            "tips": "Use Class 3 & 7 vocab: 'les horaires d'ouverture', 'le créneau', 'hebdomadaire', 'à cause de mon travail', 'ne...plus', 'quand même', 'est-ce qu'il serait possible de...'."
        },
        {
            "id": "b1-oral-3",
            "part": "Partie 3 : Expression d'un point de vue (Monologue B1)",
            "title": "Faut-il vivre au centre-ville ou à la campagne ?",
            "prompt_fr": (
                "De plus en plus de familles hésitent entre habiter dans un immeuble au cœur de la ville ou s'installer "
                "à la campagne. Présentez les avantages et les inconvénients des deux modes de vie et donnez votre opinion personnelle avec des exemples."
            ),
            "tips": "Structure your monologue: 1) Introduction du thème, 2) D'un côté (avantages de la ville : transports, gagner du temps, à proximité), 3) Cependant / Toutefois (inconvénients : bruit, logement cher), 4) Conclusion personnelle."
        }
    ]
}

CLASSES_DATA: List[Dict[str, Any]] = [
    {
        "id": "class-1",
        "number": 1,
        "date": "Sep 4",
        "title": "Articles (Jouer à/de), Genre des noms & Présenter sa ville",
        "cefr_level": "A2",
        "summary": "Mastering 'jouer à' (sports/games) vs 'jouer de' (instruments), partitive articles, noun gender rules by word endings (-age, -eau, -ment, -isme vs -tion, -ette, -ance, -ure), and describing your life in Geneva.",
        "concepts": [
            {
                "title": "1. Jouer à (Sports & Jeux) vs. Jouer de (Instruments) vs. Faire de",
                "explanation": "Use 'jouer à' (+ contracted article au, à la, à l', aux) for sports, board games, and video games. Use 'jouer de' (+ du, de la, de l', des) for musical instruments. Use 'faire de' (+ du, de la, de l', des) for any sport or activity.",
                "rules": [
                    "jouer + à + le = jouer au (ex: jouer au badminton, jouer au foot, jouer au tennis)",
                    "jouer + à + les = jouer aux (ex: jouer aux cartes, jouer aux échecs, jouer aux jeux-vidéo)",
                    "jouer + de + le = jouer du (ex: jouer du piano, jouer du violon)",
                    "jouer + de + la = jouer de la (ex: jouer de la guitare, jouer de la flûte)",
                    "Attention à la négation : 'Je fais du sport' → 'Je ne fais pas de sport' (du/de la/des deviennent 'de' après la négation)."
                ],
                "examples": [
                    {"fr": "Je joue au badminton et aux jeux-vidéo avec mon fils.", "en": "I play badminton and video games with my son."},
                    {"fr": "Elle joue de la guitare et du piano.", "en": "She plays the guitar and the piano."},
                    {"fr": "Mon fils fait de la natation deux fois par semaine.", "en": "My son does swimming twice a week."}
                ]
            },
            {
                "title": "2. Reconnaître le genre des noms (Masculin vs. Féminin)",
                "explanation": "In French, a noun's ending reliably predicts whether it is masculine (le/un) or feminine (la/une) ~90% of the time—just memorize the key exceptions from class!",
                "rules": [
                    "MASCULIN (-age) : le voyage, le paysage, le fromage, le ménage, le garage. ⚠️ Exceptions (5) : la plage, la page, la nage, l'image, la cage.",
                    "MASCULIN (-eau) : le bateau, le cadeau, le gâteau, le chapeau, le bureau. ⚠️ Exceptions : l'eau (f), la peau (f).",
                    "MASCULIN (-ment / -isme / -al) : le changement, le gouvernement, le tourisme, le réalisme, le journal, le cheval.",
                    "FÉMININ (-é / -ée) : la beauté, la liberté, la réalité, l'idée. ⚠️ Exception clé : le musée (m), le lycée (m).",
                    "FÉMININ (-ance / -ence) : la tolérance, la patience, la chance, la différence. ⚠️ Exception : le silence (m).",
                    "FÉMININ (-ette / -tion / -sion / -ure) : la baguette, la bicyclette, la nation, la télévision, la voiture, la nature, la peinture."
                ],
                "examples": [
                    {"fr": "J'adore le paysage autour du lac à Genève, surtout la plage en été.", "en": "I love the landscape around the lake in Geneva, especially the beach in summer."},
                    {"fr": "Nous avons visité le musée et admiré la peinture.", "en": "We visited the museum and admired the painting."}
                ]
            },
            {
                "title": "3. Distinctions clés : Visiter vs. Rendre visite à / Passer vs. Dépenser",
                "explanation": "Avoid classic English-to-French traps when talking about spending time/money or visiting places/people.",
                "rules": [
                    "Visiter + un lieu (place/city/museum) : 'Je visite Paris / le musée.'",
                    "Rendre visite à + une personne : 'Je rends visite à mes parents / à un ami.'",
                    "Passer du temps (to spend time) vs. Dépenser de l'argent (to spend money).",
                    "Expressions avec N'importe : n'importe quoi (anything/nonsense), n'importe où (anywhere), n'importe qui (anyone), n'importe quand (anytime)."
                ],
                "examples": [
                    {"fr": "J'aime passer du temps avec ma famille le week-end.", "en": "I like spending time with my family on the weekend."},
                    {"fr": "Nous allons rendre visite à nos amis à Lausanne.", "en": "We are going to visit our friends in Lausanne."},
                    {"fr": "Cependant, je préfère ne pas dépenser trop d'argent.", "en": "However, I prefer not to spend too much money."}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "cependant / toutefois", "en": "however / nonetheless", "note": "Formal B1 connectors"},
            {"fr": "passer le temps", "en": "to spend time", "note": "Never use 'dépenser' for time"},
            {"fr": "dépenser de l'argent", "en": "to spend money", "note": "Used for money/energy"},
            {"fr": "rendre visite à quelqu'un", "en": "to visit someone (a person)", "note": "vs. 'visiter un lieu'"},
            {"fr": "n'importe quoi / n'importe où", "en": "anything / anywhere", "note": "Also: n'importe qui, n'importe quel"},
            {"fr": "le paysage (m) / la plage (f)", "en": "the landscape / the beach", "note": "la plage is an exception to -age"},
            {"fr": "le musée (m) / la beauté (f)", "en": "the museum / the beauty", "note": "le musée is an exception to -é/-ée"},
            {"fr": "la randonnée", "en": "hiking", "note": "faire de la randonnée"}
        ],
        "homework": "Présentez votre ville : Racontez votre vie à Genève (depuis combien de temps vous y habitez, votre famille, votre quartier, les transports, et ce que vous aimez faire pendant votre temps libre).",
        "written_exercises": [
            {
                "id": "c1-ex1",
                "question": "Complétez avec 'au', 'aux', 'du' ou 'de la' : Mon fils joue ___ badminton le samedi, et ma femme joue ___ guitare.",
                "hint": "jouer à (sport) vs. jouer de (instrument)",
                "answer": "au, de la",
                "accepted_answers": ["au, de la", "au / de la", "au et de la"],
                "explanation": "Badminton is a sport ('jouer à + le = au badminton'), while guitar is an instrument ('jouer de + la = de la guitare')."
            },
            {
                "id": "c1-ex2",
                "question": "Choisissez l'article correct (le ou la) : ___ voyage, ___ plage, ___ musée, ___ télévision.",
                "hint": "Check the endings: -age (and its exception!), -ée (exception!), -sion.",
                "answer": "le, la, le, la",
                "accepted_answers": ["le, la, le, la", "le voyage, la plage, le musée, la télévision"],
                "explanation": "'-age' is masculine (le voyage) EXCEPT 'la plage'. '-é/-ée' is feminine EXCEPT 'le musée'. '-sion' is always feminine (la télévision)."
            },
            {
                "id": "c1-ex3",
                "question": "Traduisez ou corrigez l'erreur : 'Le week-end, je visite mes grands-parents et je dépense du temps avec eux.'",
                "hint": "Use 'rendre visite à' for people and 'passer du temps' for time!",
                "answer": "Le week-end, je rends visite à mes grands-parents et je passe du temps avec eux.",
                "accepted_answers": [
                    "Le week-end, je rends visite à mes grands-parents et je passe du temps avec eux.",
                    "Je rends visite à mes grands-parents et je passe du temps avec eux."
                ],
                "explanation": "For people, always say 'rendre visite à quelqu'un' (not visiter). For time, always say 'passer du temps' (not dépenser)."
            },
            {
                "id": "c1-ex4",
                "question": "Complétez avec 'aux' ou 'des' : Mon fils adore jouer ___ jeux-vidéo et aux échecs.",
                "hint": "jouer + à + les = ?",
                "answer": "aux",
                "accepted_answers": ["aux"],
                "explanation": "With games ('les jeux-vidéo', 'les échecs'), we use 'jouer à + les = aux'."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c1-sp1",
                "title": "Présentez votre vie à Genève (Homework Class 1)",
                "prompt_fr": "Parlez de votre vie à Genève : depuis combien d'années habitez-vous à Genève ? Avec qui ? Quels sports ou instruments pratiquez-vous en famille (utiliser 'jouer à', 'jouer de', 'faire de') ?",
                "target_structures": ["J'habite à Genève depuis...", "jouer au / aux", "jouer du / de la", "passer du temps", "cependant / toutefois"]
            },
            {
                "id": "c1-sp2",
                "title": "Vos week-ends et vos visites",
                "prompt_fr": "Que faites-vous le week-end ? Quels lieux aimez-vous visiter en Suisse, et à qui rendez-vous visite ?",
                "target_structures": ["visiter + lieu", "rendre visite à + personne", "le paysage", "la plage", "le musée"]
            }
        ]
    },
    {
        "id": "class-2",
        "number": 2,
        "date": "Sep 9",
        "title": "Connecteurs du quotidien & La Négation (Partie 1)",
        "cefr_level": "A2",
        "summary": "Natural spoken connectors (du coup, quand même, franchement, d'un côté, au cœur de, à proximité) and negative structures (ne...pas, ne...pas du tout, ne...plus, ne...jamais).",
        "concepts": [
            {
                "title": "1. La Négation : ne...pas, ne...pas du tout, ne...plus, ne...jamais",
                "explanation": "Instead of always saying 'ne...pas', B1 speakers choose the exact negative adverb that matches the affirmative idea.",
                "rules": [
                    "Affirmative normal → ne ... pas (Je travaille → Je ne travaille pas).",
                    "Un peu / beaucoup → ne ... pas du tout (not at all : Je n'aime pas du tout le froid).",
                    "Toujours / encore (still) → ne ... plus (not anymore / no longer : Je ne fume plus, il n'habite plus ici).",
                    "Souvent / parfois / toujours (always) → ne ... jamais (never : Je ne prends jamais le bus)."
                ],
                "examples": [
                    {"fr": "Tu travailles encore dans cette entreprise ? — Non, je n'y travaille plus.", "en": "Do you still work at that company? — No, I don't work there anymore."},
                    {"fr": "Il va souvent au cinéma ? — Non, il ne va jamais au cinéma.", "en": "Does he often go to the cinema? — No, he never goes to the cinema."}
                ]
            },
            {
                "title": "2. Connecteurs et expressions utiles pour parler de son quartier",
                "explanation": "These expressions from Class 2 immediately make your spoken French sound natural and structured.",
                "rules": [
                    "au cœur de la ville (in the heart of the city) / à proximité (nearby).",
                    "d'un côté ... de l'autre côté (on one hand ... on the other hand).",
                    "cela me permet de gagner du temps (that allows me to save time).",
                    "du coup / alors (so / as a result — very common in spoken French).",
                    "quand même (anyway / still / even so) & franchement (frankly / honestly)."
                ],
                "examples": [
                    {"fr": "Mon appartement est situé au cœur de Genève, à proximité des transports publics.", "en": "My apartment is located in the heart of Geneva, close to public transport."},
                    {"fr": "Cela me permet de gagner du temps le matin.", "en": "That allows me to save time in the morning."},
                    {"fr": "J'ai oublié de mettre un réveil, du coup j'ai raté le bus !", "en": "I forgot to set an alarm, so I missed the bus!"}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "au cœur de", "en": "in the heart of", "note": "au cœur de la ville"},
            {"fr": "à proximité (de)", "en": "nearby / close to", "note": "Great B1 alternative to 'près de'"},
            {"fr": "gagner du temps", "en": "to save time", "note": "cela me permet de gagner du temps"},
            {"fr": "du coup", "en": "so / therefore (spoken)", "note": "Very natural in oral French"},
            {"fr": "quand même", "en": "anyway / all the same / still", "note": "Il pleut, mais je sors quand même"},
            {"fr": "franchement", "en": "frankly / honestly", "note": "Franchement, c'est très pratique"},
            {"fr": "volontiers", "en": "gladly / with pleasure", "note": "Oui, volontiers !"},
            {"fr": "rater le bus / mettre un réveil", "en": "to miss the bus / to set an alarm", "note": "oublier de mettre un réveil"}
        ],
        "homework": "Décrivez les avantages de votre quartier en utilisant 'au cœur de', 'à proximité', 'cela me permet de gagner du temps', 'du coup' et 'quand même'.",
        "written_exercises": [
            {
                "id": "c2-ex1",
                "question": "Répondez à la forme négative : 'Tu habites encore à Lyon ?' → 'Non, je ___ habite ___ à Lyon.'",
                "hint": "What is the opposite of 'encore' (still)?",
                "answer": "n', plus",
                "accepted_answers": ["n', plus", "n'habite plus", "Non, je n'habite plus à Lyon."],
                "explanation": "The opposite of 'encore / toujours' (still) is 'ne ... plus' (not anymore)."
            },
            {
                "id": "c2-ex2",
                "question": "Répondez à la forme négative : 'Vous prenez souvent le taxi ?' → 'Non, je ___ prends ___ le taxi.'",
                "hint": "Opposite of 'souvent / toujours' (frequency)",
                "answer": "ne, jamais",
                "accepted_answers": ["ne, jamais", "ne prends jamais", "Non, je ne prends jamais le taxi."],
                "explanation": "The opposite of 'souvent' (often) is 'ne ... jamais' (never)."
            },
            {
                "id": "c2-ex3",
                "question": "Complétez avec l'expression de la classe 2 : 'J'ai oublié de mettre mon réveil, ___ j'ai raté le bus !'",
                "hint": "Spoken connector meaning 'so / as a result'",
                "answer": "du coup",
                "accepted_answers": ["du coup", "alors", "donc"],
                "explanation": "'Du coup' (or 'alors') expresses an immediate consequence in spoken French."
            },
            {
                "id": "c2-ex4",
                "question": "Complétez : 'J'habite à proximité de mon bureau, cela me permet de ___ du temps.'",
                "hint": "How do we say 'to save time' in natural French?",
                "answer": "gagner",
                "accepted_answers": ["gagner", "sauvegarder"],
                "explanation": "'Gagner du temps' means to save time."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c2-sp1",
                "title": "Les avantages de votre quartier à Genève",
                "prompt_fr": "Expliquez pourquoi votre quartier à Genève est pratique. Utilisez 'au cœur de', 'à proximité', 'cela me permet de gagner du temps', 'franchement' et 'quand même'.",
                "target_structures": ["au cœur de", "à proximité", "gagner du temps", "franchement", "quand même"]
            },
            {
                "id": "c2-sp2",
                "title": "Ce que vous ne faites plus / jamais",
                "prompt_fr": "Quelles sont deux choses que vous faisiez avant mais que vous ne faites plus aujourd'hui (ne...plus), et deux choses que vous ne faites jamais (ne...jamais) ?",
                "target_structures": ["ne ... plus", "ne ... jamais", "ne ... pas du tout", "du coup"]
            }
        ]
    },
    {
        "id": "class-3",
        "number": 3,
        "date": "Sep 16",
        "title": "Négation Complexe (Partie 2) & Les 3 Registres de Questions",
        "cefr_level": "A2 → B1",
        "summary": "Mastering ne...ni...ni, ne...pas encore, ne...rien, ne...personne, the 3 question registers (familier, standard, soutenu/formel), and vocabulary for registering for sports/activities.",
        "concepts": [
            {
                "title": "1. La Négation Complexe (Partie 2)",
                "explanation": "Each affirmative pronoun or adverb has a specific negative counterpart.",
                "rules": [
                    "déjà (already) → ne ... pas encore (not yet) : 'Tu as déjà dîné ? Non, je n'ai pas encore dîné.'",
                    "quelque chose / tout (something / everything) → ne ... rien (nothing) ou 'Rien ne...' (as subject).",
                    "quelqu'un / tout le monde (someone / everyone) → ne ... personne (no one) ou 'Personne ne...' (as subject).",
                    "... et ... / ... ou ... → ne ... ni ... ni ... (neither ... nor) : 'Je ne parle ni l'espagnol ni l'allemand.' (Note: partitive/indefinite articles drop after ni...ni: 'Je ne bois ni thé ni café')."
                ],
                "examples": [
                    {"fr": "Tu connais quelqu'un ici ? — Non, je ne connais personne.", "en": "Do you know anyone here? — No, I don't know anyone."},
                    {"fr": "Quelqu'un a appelé ? — Non, personne n'a appelé.", "en": "Did anyone call? — No, nobody called."},
                    {"fr": "Je ne prends ni sucre ni lait dans mon café.", "en": "I take neither sugar nor milk in my coffee."}
                ]
            },
            {
                "title": "2. Les 3 Registres de Questions (Familier, Standard, Soutenu)",
                "explanation": "In DELF B1, you need to recognize and use all three ways of asking a question depending on whether you are speaking to a friend (familier), in daily life (standard), or in a formal letter/interview (soutenu).",
                "rules": [
                    "1. Familier (Intonation, pas d'inversion) : 'Tu viens à la fête ?' / 'Tu vas où ?'",
                    "2. Standard (Est-ce que + Sujet + Verbe) : 'Est-ce que tu viens à la fête ?' / 'Où est-ce que tu vas ?'",
                    "3. Soutenu / Formel (Inversion Verbe-Sujet) : 'Viens-tu à la fête ?' / 'Où vas-tu ?' / 'Y a-t-il un créneau disponible ?'"
                ],
                "examples": [
                    {"fr": "Familier : Il y a quelqu'un ? | Standard : Est-ce qu'il y a quelqu'un ? | Soutenu : Y a-t-il quelqu'un ?", "en": "Is anyone there? (in all 3 registers)"},
                    {"fr": "Quels sont les horaires d'ouverture et quel créneau est disponible ?", "en": "What are the opening hours and which time slot is available?"}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "faire de l'escalade", "en": "to go climbing / rock climbing", "note": "Activity registration dialogue"},
            {"fr": "les horaires d'ouverture", "en": "opening hours", "note": "Essential for DELF B1 roleplays"},
            {"fr": "un créneau (horaire)", "en": "a time slot", "note": "Quel créneau préférez-vous ?"},
            {"fr": "l'entraîneur (m)", "en": "the coach / trainer", "note": "Sport vocabulary"},
            {"fr": "hebdomadaire / mensuel", "en": "weekly / monthly", "note": "un cours hebdomadaire, un abonnement mensuel"},
            {"fr": "ne ... pas encore", "en": "not yet", "note": "Opposite of 'déjà'"},
            {"fr": "ne ... ni ... ni ...", "en": "neither ... nor ...", "note": "Double negation"}
        ],
        "homework": "Transformez 5 phrases affirmatives avec 'déjà', 'quelqu'un', 'quelque chose', 'tout le monde' à la forme négative, et écrivez un dialogue pour inscrire votre fils à un cours d'escalade.",
        "written_exercises": [
            {
                "id": "c3-ex1",
                "question": "Transformez à la forme négative : 'Tu as déjà visité Berne ?' → 'Non, je ___ ai ___ visité Berne.'",
                "hint": "Opposite of 'déjà' in Passé Composé (place the adverb before the past participle).",
                "answer": "n', pas encore",
                "accepted_answers": ["n', pas encore", "n'ai pas encore", "Non, je n'ai pas encore visité Berne."],
                "explanation": "The opposite of 'déjà' is 'ne ... pas encore', placed around the auxiliary: 'Je n'ai pas encore visité'."
            },
            {
                "id": "c3-ex2",
                "question": "Transformez à la forme négative : 'Tu vois quelqu'un dans la salle ?' → 'Non, je ___ vois ___.'",
                "hint": "Opposite of 'quelqu'un'",
                "answer": "ne, personne",
                "accepted_answers": ["ne, personne", "ne vois personne", "Non, je ne vois personne."],
                "explanation": "'Quelqu'un' becomes 'ne ... personne' (placed after the past participle too: 'Je n'ai vu personne')."
            },
            {
                "id": "c3-ex3",
                "question": "Transformez avec 'ni...ni' : 'J'aime le fromage et le vin.' → 'Je ___ aime ___ le fromage ___ le vin.'",
                "hint": "Use ne ... ni ... ni ... (keep definite articles le/la/les!).",
                "answer": "n', ni, ni",
                "accepted_answers": ["n', ni, ni", "Je n'aime ni le fromage ni le vin."],
                "explanation": "With definite articles (le, la, les), keep them after 'ni': 'Je n'aime ni le fromage ni le vin.'"
            },
            {
                "id": "c3-ex4",
                "question": "Transformez cette question au registre soutenu (inversion) : 'Est-ce qu'il y a un créneau le mardi ?'",
                "hint": "Inversion of 'il y a' adds a '-t-'!",
                "answer": "Y a-t-il un créneau le mardi ?",
                "accepted_answers": ["Y a-t-il un créneau le mardi ?", "Y a-t-il un créneau le mardi"],
                "explanation": "In formal/soutenu register, 'Est-ce qu'il y a' becomes 'Y a-t-il ... ?'."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c3-sp1",
                "title": "Jeu de rôle : Inscription au cours d'escalade",
                "prompt_fr": "Vous appelez un club de sport à Genève pour inscrire votre fils à un cours d'escalade. Posez au moins 3 questions (les horaires d'ouverture, les créneaux hebdomadaires disponibles, le tarif mensuel).",
                "target_structures": ["les horaires d'ouverture", "un créneau", "hebdomadaire", "mensuel", "Est-ce que / inversion"]
            },
            {
                "id": "c3-sp2",
                "title": "Défi Négation Complexe",
                "prompt_fr": "Répondez à l'oral en utilisant : 1) une phrase avec 'ne...pas encore', 2) une phrase avec 'ne...ni...ni', et 3) une phrase avec 'ne...rien' ou 'ne...personne'.",
                "target_structures": ["ne ... pas encore", "ne ... ni ... ni", "ne ... rien", "ne ... personne"]
            }
        ]
    },
    {
        "id": "class-4",
        "number": 4,
        "date": "Sep 20",
        "title": "Passé Récent & Passé Composé avec Avoir (Partie 1)",
        "cefr_level": "A2",
        "summary": "Expressing immediate past with 'venir de + infinitif', building the Passé Composé with auxiliary 'avoir', regular & core irregular past participles, and avoiding key faux-amis (actuellement vs en fait, librairie).",
        "concepts": [
            {
                "title": "1. Le Passé Récent : Venir de + Infinitif",
                "explanation": "To say you 'just' did something a few minutes ago, conjugate 'venir' in the present tense + de/d' + infinitive.",
                "rules": [
                    "Je viens de finir mon travail (I just finished my work).",
                    "Tu viens de manger / Il vient d'arriver / Nous venons de comprendre / Ils viennent de partir."
                ],
                "examples": [
                    {"fr": "Je viens de terminer mon cours de français.", "en": "I just finished my French class."},
                    {"fr": "Nous venons de prendre un café.", "en": "We just had a coffee."}
                ]
            },
            {
                "title": "2. Le Passé Composé avec Avoir : Formation & Participes Irréguliers (Liste 1)",
                "explanation": "Passé Composé = Present of AVOIR (j'ai, tu as, il a, nous avons, vous avez, ils ont) + Participe Passé.",
                "rules": [
                    "Verbes réguliers : -ER → -é (parlé, mangé) | -IR → -i (fini, choisi) | -RE → -u (vendu, attendu, répondu).",
                    "Irréguliers en -IS : prendre → pris, apprendre → appris, comprendre → compris.",
                    "Irréguliers en -U : avoir → eu, boire → bu, croire → cru, voir → vu, pouvoir → pu, vouloir → voulu, falloir → fallu, courir → couru.",
                    "Autres essentiels : être → été, faire → fait, dire → dit, ouvrir → ouvert, offrir → offert, sourire → souri."
                ],
                "examples": [
                    {"fr": "La semaine dernière, j'ai appris beaucoup de nouveaux mots et j'ai tout compris.", "en": "Last week, I learned many new words and I understood everything."},
                    {"fr": "Hier, il a fallu travailler tard et je n'ai pas pu sortir.", "en": "Yesterday, it was necessary to work late and I couldn't go out."}
                ]
            },
            {
                "title": "3. Faux-amis & Expressions idiomatiques",
                "explanation": "Watch out for these false friends noted in Class 4!",
                "rules": [
                    "actuellement = currently / right now (NOT 'actually'!).",
                    "en fait = actually / in fact.",
                    "une librairie = a bookstore (whereas 'une bibliothèque' = a library).",
                    "se rendre compte de = to realize ('Je me suis rendu compte de mon erreur')."
                ],
                "examples": [
                    {"fr": "Actuellement, je travaille à Genève, mais en fait j'ai grandi en Inde.", "en": "Currently, I work in Geneva, but actually I grew up in India."}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "actuellement vs. en fait", "en": "currently vs. actually/in fact", "note": "Classic false friend!"},
            {"fr": "une librairie vs. une bibliothèque", "en": "a bookstore vs. a library", "note": "Acheter un livre à la librairie"},
            {"fr": "se rendre compte (de)", "en": "to realize", "note": "Je viens de me rendre compte que..."},
            {"fr": "la semaine dernière / le mois dernier", "en": "last week / last month", "note": "Triggers Passé Composé"},
            {"fr": "il a fallu / j'ai pu / j'ai voulu", "en": "it was necessary / I could / I wanted", "note": "falloir → fallu, pouvoir → pu, vouloir → voulu"}
        ],
        "homework": "Racontez 6 actions que vous avez faites la semaine dernière au passé composé (en utilisant au moins 4 participes passés irréguliers) et 2 phrases au passé récent (venir de).",
        "written_exercises": [
            {
                "id": "c4-ex1",
                "question": "Donnez le participe passé de ces verbes : prendre → ___, boire → ___, pouvoir → ___, ouvrir → ___.",
                "hint": "Check the irregular endings (-is, -u, -ert).",
                "answer": "pris, bu, pu, ouvert",
                "accepted_answers": ["pris, bu, pu, ouvert"],
                "explanation": "prendre → pris, boire → bu, pouvoir → pu, ouvrir → ouvert."
            },
            {
                "id": "c4-ex2",
                "question": "Complétez au Passé Récent (venir de) : 'Attention, le train ___ partir il y a deux minutes !'",
                "hint": "Conjugate 'venir' for 'le train' (il) + de",
                "answer": "vient de",
                "accepted_answers": ["vient de"],
                "explanation": "'Le train vient de partir' = The train just left."
            },
            {
                "id": "c4-ex3",
                "question": "Choisissez entre 'actuellement' et 'en fait' : 'On pense que le français est facile, mais ___ la grammaire demande de la pratique. ___ , j'ai deux cours par semaine.'",
                "hint": "'en fait' = actually/in fact; 'actuellement' = currently.",
                "answer": "en fait, Actuellement",
                "accepted_answers": ["en fait, Actuellement", "en fait, actuellement"],
                "explanation": "'En fait' means 'actually / in fact', whereas 'actuellement' means 'currently / at the moment'."
            },
            {
                "id": "c4-ex4",
                "question": "Conjuguez au passé composé : 'Hier, nous (avoir) ___ beaucoup de travail et nous (faire) ___ de notre mieux.'",
                "hint": "avoir → eu, faire → fait",
                "answer": "avons eu, avons fait",
                "accepted_answers": ["avons eu, avons fait"],
                "explanation": "With 'nous': 'nous avons eu' (avoir) and 'nous avons fait' (faire)."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c4-sp1",
                "title": "Votre semaine dernière au Passé Composé",
                "prompt_fr": "Qu'avez-vous fait la semaine dernière ? Utilisez au moins 5 verbes irréguliers au passé composé (par exemple : j'ai pris, j'ai vu, j'ai appris, j'ai bu, j'ai fait, j'ai pu).",
                "target_structures": ["La semaine dernière", "j'ai pris", "j'ai fait", "j'ai vu", "j'ai appris", "en fait"]
            },
            {
                "id": "c4-sp2",
                "title": "Qu'est-ce que vous venez de faire ?",
                "prompt_fr": "Dites trois choses que vous (ou votre famille) venez juste de faire aujourd'hui en utilisant le passé récent ('je viens de...').",
                "target_structures": ["Je viens de...", "Ma femme vient de...", "Nous venons de..."]
            }
        ]
    },
    {
        "id": "class-5",
        "number": 5,
        "date": "Sep 25",
        "title": "Passé Composé Irréguliers (Partie 2) & Parcours Professionnel",
        "cefr_level": "A2",
        "summary": "Completing the irregular past participle families (-is, -u, -it, -ert) and vocabulary for emails, savings, and professional background.",
        "concepts": [
            {
                "title": "1. Familles de Participes Passés Irréguliers (Partie 2)",
                "explanation": "Grouping irregular verbs by root family makes them effortless to remember!",
                "rules": [
                    "Famille METTRE (-is) : mettre → mis, admettre → admis, promettre → promis, permettre → permis.",
                    "Famille TENIR / VENIR (-enu) : tenir → tenu, obtenir → obtenu, venir → venu, devenir → devenu.",
                    "Famille -U : devoir → dû (avec accent circonflexe !), lire → lu, savoir → su, connaître → connu, vivre → vécu, recevoir → reçu.",
                    "Famille -IT / -EINT : écrire → écrit, conduire → conduit, construire → construit, traduire → traduit, éteindre → éteint.",
                    "Famille -ERT / -I : découvrir → découvert, suivre → suivi."
                ],
                "examples": [
                    {"fr": "J'ai écrit un courriel à mon collègue et j'ai suivi un cours de français.", "en": "I wrote an email to my colleague and I took a French course."},
                    {"fr": "Nous avons découvert un très bon restaurant et j'ai promis à mon fils d'y retourner.", "en": "We discovered a very good restaurant and I promised my son to go back there."}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "un courriel (un mail)", "en": "an email", "note": "J'ai écrit / envoyé un courriel"},
            {"fr": "économiser (de l'argent)", "en": "to save money", "note": "Contrast with 'dépenser'"},
            {"fr": "un parcours professionnel", "en": "a career path / professional background", "note": "Essential for DELF B1 Part 1"},
            {"fr": "parmi (les deux)", "en": "among (between the two)", "note": "parmi mes collègues"},
            {"fr": "éteindre (éteint) / allumer", "en": "to turn off / to turn on", "note": "J'ai éteint la lumière"},
            {"fr": "suivre un cours (suivi)", "en": "to take / follow a course", "note": "J'ai suivi un cours"}
        ],
        "homework": "Présentez votre parcours professionnel et vos études au passé composé en utilisant 'suivre', 'apprendre', 'connaître', 'découvrir', 'écrire' et 'devoir'.",
        "written_exercises": [
            {
                "id": "c5-ex1",
                "question": "Donnez le participe passé : mettre → ___, devoir → ___, connaître → ___, écrire → ___, suivre → ___.",
                "hint": "Remember the circumflex on devoir!",
                "answer": "mis, dû, connu, écrit, suivi",
                "accepted_answers": ["mis, dû, connu, écrit, suivi", "mis, du, connu, écrit, suivi"],
                "explanation": "mettre → mis, devoir → dû, connaître → connu, écrire → écrit, suivre → suivi."
            },
            {
                "id": "c5-ex2",
                "question": "Conjuguez au passé composé : 'Hier soir, j' (éteindre) ___ l'ordinateur après avoir (écrire) ___ trois courriels.'",
                "hint": "éteindre → éteint, écrire → écrit",
                "answer": "ai éteint, écrit",
                "accepted_answers": ["ai éteint, écrit", "j'ai éteint, écrit"],
                "explanation": "'J'ai éteint l'ordinateur après avoir écrit trois courriels.'"
            },
            {
                "id": "c5-ex3",
                "question": "Conjuguez au passé composé : 'Nous (découvrir) ___ une belle région et j' (conduire) ___ pendant trois heures.'",
                "hint": "découvrir → découvert, conduire → conduit",
                "answer": "avons découvert, ai conduit",
                "accepted_answers": ["avons découvert, ai conduit"],
                "explanation": "découvrir → découvert ('nous avons découvert'), conduire → conduit ('j'ai conduit')."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c5-sp1",
                "title": "Votre parcours professionnel (DELF B1 Partie 1)",
                "prompt_fr": "Racontez votre parcours professionnel : quelles études avez-vous suivies, dans quels pays avez-vous travaillé, qu'avez-vous appris et découvert ?",
                "target_structures": ["J'ai suivi...", "J'ai travaillé...", "J'ai dû...", "J'ai découvert...", "mon parcours professionnel"]
            }
        ]
    },
    {
        "id": "class-6",
        "number": 6,
        "date": "Sep 30",
        "title": "Passé Composé avec Être (Règle ADVENT) & Accord",
        "cefr_level": "A2 → B1",
        "summary": "The 14+ verbs of movement/state that take auxiliary ÊTRE in Passé Composé (ADVENT pairs), subject-participle agreement (-e, -s, -es), and 'tout / toute / tous / toutes'.",
        "concepts": [
            {
                "title": "1. Les Verbes avec ÊTRE au Passé Composé (A.D.V.E.N.T.)",
                "explanation": "While most verbs use 'avoir', 14 core verbs of movement/change of state (plus their derivatives like devenir, revenir, rentrer, retourner) use ÊTRE (je suis, tu es, il est, nous sommes, vous êtes, ils sont).",
                "rules": [
                    "A : Arriver (arrivé) ↔ Partir (parti)  |  Aller (allé) ↔ Venir (venu) / Devenir (devenu) / Revenir (revenu)",
                    "D : Descendre (descendu) ↔ Monter (monté)",
                    "E : Entrer (entré) / Rentrer (rentré) ↔ Sortir (sorti)",
                    "N : Naître (né) ↔ Mourir (mort)",
                    "T : Tomber (tombé) ↔ Rester (resté)  |  + Passer par (passé), Retourner (retourné)"
                ],
                "examples": [
                    {"fr": "Je suis né en Inde, puis je suis venu en Suisse et je suis resté à Genève.", "en": "I was born in India, then I came to Switzerland and stayed in Geneva."},
                    {"fr": "Hier soir, nous sommes sortis au restaurant et nous sommes rentrés à 22h.", "en": "Last night, we went out to the restaurant and came back home at 10 PM."}
                ]
            },
            {
                "title": "2. L'Accord du Participe Passé avec ÊTRE & Tout/Toute/Tous/Toutes",
                "explanation": "With auxiliary ÊTRE, the past participle ALWAYS agrees in gender and number with the subject!",
                "rules": [
                    "Masculin singulier : Il est allé / Je (Balu) suis parti.",
                    "Féminin singulier (+e) : Elle est allée / Ma femme est partie.",
                    "Masculin pluriel (+s) : Ils sont allés / Mon fils et moi, nous sommes partis.",
                    "Féminin pluriel (+es) : Elles sont allées.",
                    "Tout + masc. sg. (tout le temps) | Toute + fém. sg. (toute la journée) | Tous + masc. pl. (tous les jours) | Toutes + fém. pl. (toutes les semaines)."
                ],
                "examples": [
                    {"fr": "Ma femme est allée au travail tôt et elle est restée au bureau toute la journée.", "en": "My wife went to work early and stayed at the office all day."},
                    {"fr": "Mes amis sont arrivés hier et ils sont repartis ce matin.", "en": "My friends arrived yesterday and left again this morning."}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "naître (né) / mourir (mort)", "en": "to be born / to die", "note": "Je suis né(e), il est mort"},
            {"fr": "rester (resté) / tomber (tombé)", "en": "to stay / to fall", "note": "Uses ÊTRE in French! (Je suis resté)"},
            {"fr": "rentrer / retourner", "en": "to return home / to go back", "note": "Je suis rentré à la maison"},
            {"fr": "toute la journée / tous les jours", "en": "all day long / every day", "note": "Agreement of tout/toute/tous/toutes"}
        ],
        "homework": "Racontez un voyage ou un déplacement récent en utilisant au moins 6 verbes avec ÊTRE (aller, partir, arriver, rester, sortir, rentrer) en faisant bien l'accord du participe passé.",
        "written_exercises": [
            {
                "id": "c6-ex1",
                "question": "Conjuguez au passé composé (attention à l'auxiliaire et à l'accord !) : 'Ma femme (aller) ___ à Zurich et elle (rentrer) ___ à 19h.'",
                "hint": "'Ma femme' is feminine singular (+e with être).",
                "answer": "est allée, est rentrée",
                "accepted_answers": ["est allée, est rentrée"],
                "explanation": "'Aller' and 'rentrer' take ÊTRE, and since 'ma femme' is feminine singular, we add -e: 'est allée', 'est rentrée'."
            },
            {
                "id": "c6-ex2",
                "question": "Conjuguez au passé composé : 'Dimanche, nous (rester) ___ à la maison ___ la journée (tout/toute/tous/toutes).'",
                "hint": "Rester takes ÊTRE! And 'la journée' is feminine singular.",
                "answer": "sommes restés, toute",
                "accepted_answers": ["sommes restés, toute", "sommes restées, toute"],
                "explanation": "In French, 'rester' (to stay) takes ÊTRE: 'nous sommes restés'. And 'la journée' is feminine singular: 'toute la journée'."
            },
            {
                "id": "c6-ex3",
                "question": "Avoir ou Être ? Complétez : 'J'___ pris le train, je ___ arrivé à Lausanne à 10h, et j'___ visité le musée.'",
                "hint": "prendre (avoir), arriver (être), visiter (avoir).",
                "answer": "ai, suis, ai",
                "accepted_answers": ["ai, suis, ai"],
                "explanation": "'Prendre' and 'visiter' take AVOIR ('j'ai pris', 'j'ai visité'), while 'arriver' is an ADVENT verb taking ÊTRE ('je suis arrivé')."
            },
            {
                "id": "c6-ex4",
                "question": "Complétez avec tout, toute, tous ou toutes : 'Je travaille ___ les jours et je suis occupé ___ la semaine.'",
                "hint": "'les jours' (masc. pl.) vs. 'la semaine' (fém. sg.)",
                "answer": "tous, toute",
                "accepted_answers": ["tous, toute"],
                "explanation": "'Tous les jours' (masculine plural) and 'toute la semaine' (feminine singular)."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c6-sp1",
                "title": "Racontez votre dernier week-end ou voyage (Verbes avec Être)",
                "prompt_fr": "Où êtes-vous allé(e) le week-end dernier ou pendant vos dernières vacances ? Avec qui êtes-vous parti(e), à quelle heure êtes-vous arrivé(e), combien de temps êtes-vous resté(e), et quand êtes-vous rentré(e) ?",
                "target_structures": ["Je suis allé", "Nous sommes partis", "Nous sommes arrivés", "Nous sommes restés", "toute la journée"]
            }
        ]
    },
    {
        "id": "class-7",
        "number": 7,
        "date": "Oct 4",
        "title": "Les Verbes Pronominaux (Présent & Passé Composé) & Cause",
        "cefr_level": "A2 → B1",
        "summary": "Daily routine and emotion reflexive verbs (se réveiller, se lever, se dépêcher, s'amuser, se souvenir...) in Present and Passé Composé (always with ÊTRE!), plus 'grâce à' vs 'à cause de'.",
        "concepts": [
            {
                "title": "1. Les Verbes Pronominaux au Présent et au Passé Composé",
                "explanation": "All pronominal (reflexive) verbs ('se + verbe') ALWAYS use auxiliary ÊTRE in the Passé Composé!",
                "rules": [
                    "Pronoms réfléchis : je me, tu te, il/elle se, nous nous, vous vous, ils/elles se.",
                    "Passé Composé (Affirmative) : Sujet + me/te/se/nous/vous/se + ÊTRE + Participe Passé.",
                    "Exemple : 'Je me suis réveillé à 6h, ma femme s'est levée à 6h30, nous nous sommes préparés rapidement.'",
                    "Passé Composé (Négative) : Sujet + NE + pronom réfléchi + ÊTRE + PAS + Participe Passé.",
                    "Exemple : 'Je ne me suis pas couché tard.' / 'Elle ne s'est pas maquillée.' / 'Ils ne se sont pas parlé.'"
                ],
                "examples": [
                    {"fr": "Ce matin, je me suis réveillé à 6 heures, je me suis douché et je me suis habillé.", "en": "This morning, I woke up at 6 AM, showered, and got dressed."},
                    {"fr": "Hier soir, nous ne nous sommes pas couchés tard parce que nous étions fatigués.", "en": "Last night, we didn't go to bed late because we were tired."}
                ]
            },
            {
                "title": "2. Exprimer la cause : Grâce à (positif) vs. À cause de (négatif)",
                "explanation": "A favorite DELF B1 distinction: choose between 'grâce à' and 'à cause de' depending on whether the result is positive or negative.",
                "rules": [
                    "Grâce à (+ nom / pronom) = Thanks to (positive outcome) : 'Grâce à mes cours de français, je progresse vite.'",
                    "À cause de (+ nom / du / de la / des) = Because of (negative problem) : 'À cause de la pluie / du trafic, je suis arrivé en retard.'"
                ],
                "examples": [
                    {"fr": "J'ai réussi mon examen grâce à mon professeur.", "en": "I passed my exam thanks to my teacher."},
                    {"fr": "Je me suis dépêché à cause du retard du bus.", "en": "I hurried because of the bus delay."}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "se réveiller / se lever", "en": "to wake up / to get up", "note": "Je me suis réveillé, je me suis levé"},
            {"fr": "se brosser les dents / se raser", "en": "to brush one's teeth / to shave", "note": "Routine du matin"},
            {"fr": "s'habiller / se préparer", "en": "to get dressed / to get ready", "note": "Je me suis habillé"},
            {"fr": "se dépêcher", "en": "to hurry up", "note": "Je me suis dépêché"},
            {"fr": "se détendre / se reposer", "en": "to relax / to rest", "note": "Le soir, je me détends"},
            {"fr": "s'ennuyer / se fâcher / s'amuser", "en": "to get bored / to get angry / to have fun", "note": "Verbes pronominaux d'émotion"},
            {"fr": "se souvenir (de)", "en": "to remember", "note": "Je me souviens de mon enfance"},
            {"fr": "grâce à vs. à cause de", "en": "thanks to (+) vs. because of (-)", "note": "Key B1 connector pair"}
        ],
        "homework": "Racontez votre routine d'hier matin et d'hier soir au passé composé en utilisant au moins 6 verbes pronominaux (dont un à la forme négative) + 'grâce à' et 'à cause de'.",
        "written_exercises": [
            {
                "id": "c7-ex1",
                "question": "Conjuguez au passé composé : 'Ce matin, je (se réveiller) ___ à 6h et je (se dépêcher) ___.'",
                "hint": "Pronominal verbs always use ÊTRE: je me suis + participe passé.",
                "answer": "me suis réveillé, me suis dépêché",
                "accepted_answers": ["me suis réveillé, me suis dépêché", "me suis réveillée, me suis dépêchée"],
                "explanation": "With 'je': 'je me suis réveillé' and 'je me suis dépêché'."
            },
            {
                "id": "c7-ex2",
                "question": "Mettez à la forme négative au passé composé : 'Nous nous sommes reposés.' → 'Nous ___ reposés.'",
                "hint": "Keep 'nous sommes' together inside 'ne ... pas'!",
                "answer": "ne nous sommes pas",
                "accepted_answers": ["ne nous sommes pas", "Nous ne nous sommes pas reposés."],
                "explanation": "In negative Passé Composé for pronominal verbs, 'ne' goes before the reflexive pronoun and 'pas' goes after 'être': 'Nous ne nous sommes pas reposés'."
            },
            {
                "id": "c7-ex3",
                "question": "Complétez avec 'grâce à' ou 'à cause de' : '1) J'ai appris le français ___ cette application. 2) Je suis arrivé en retard ___ la grève des transports.'",
                "hint": "Positive outcome vs. negative outcome.",
                "answer": "grâce à, à cause de",
                "accepted_answers": ["grâce à, à cause de"],
                "explanation": "'Grâce à' is for a positive cause; 'à cause de' is for a negative problem."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c7-sp1",
                "title": "Votre routine d'hier au Passé Composé",
                "prompt_fr": "Racontez votre journée d'hier du matin au soir en utilisant les verbes pronominaux au passé composé (se réveiller, se lever, se préparer, se dépêcher, se reposer, se coucher) et utilisez 'grâce à' ou 'à cause de'.",
                "target_structures": ["Je me suis réveillé", "Je me suis levé", "Je me suis préparé", "Nous nous sommes couchés", "grâce à / à cause de"]
            }
        ]
    },
    {
        "id": "class-8",
        "number": 8,
        "date": "Oct 9",
        "title": "L'Impératif, Pronoms Toniques & Le Logement",
        "cefr_level": "A2 → B1",
        "summary": "Giving advice, instructions, and orders with L'Impératif (affirmative & negative, dropping -s for -er verbs, irregulars sois/aie, and attaching pronouns like Dépêche-toi / Vas-y / Allons-y), plus housing vocabulary.",
        "concepts": [
            {
                "title": "1. L'Impératif (Donner un conseil ou une instruction)",
                "explanation": "The imperative only exists for 3 persons: TU, NOUS, VOUS (without saying the subject pronoun).",
                "rules": [
                    "Règle d'or des verbes en -ER (et aller / ouvrir / offrir) : à la forme TU, on supprime le '-s' final !",
                    "Exemples : Tu parles → Parle ! | Tu fermes → Ferme la porte ! | Tu vas → Va ! | Tu ouvres → Ouvre !",
                    "Verbes des 2e/3e groupes gardent le '-s' : Prends soin de toi ! / Finis ton travail ! / Réponds-moi !",
                    "Irréguliers : ÊTRE → Sois, Soyons, Soyez (Sois patient !) | AVOIR → Aie, Ayons, Ayez (N'aie pas peur !)."
                ],
                "examples": [
                    {"fr": "Prends soin de toi et sois prudent sur la route !", "en": "Take care of yourself and be careful on the road!"},
                    {"fr": "Ferme la porte et écoute-moi bien.", "en": "Close the door and listen to me carefully."}
                ]
            },
            {
                "title": "2. L'Impératif avec les Pronoms (Affirmative vs. Négative)",
                "explanation": "In the affirmative imperative, attach the pronoun AFTER the verb with a hyphen (me → moi, te → toi). In the negative imperative, put the pronoun back BEFORE the verb!",
                "rules": [
                    "Affirmatif : Dépêche-toi ! / Calme-toi ! / Lève-toi ! / Réponds-moi ! / Donnez-moi un stylo ! / Suis-moi !",
                    "Avec Y : Vas-y ! (keep the -s before 'y' for pronunciation!) / Allons-y !",
                    "Négatif : Ne te dépêche pas ! / Ne t'inquiète pas ! / Ne me réponds pas comme ça !"
                ],
                "examples": [
                    {"fr": "Dépêche-toi, nous allons rater le bus ! — Mais non, calme-toi, ne t'inquiète pas !", "en": "Hurry up, we're going to miss the bus! — No, calm down, don't worry!"},
                    {"fr": "C'est une excellente opportunité, vas-y !", "en": "It's a great opportunity, go for it!"}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "Prends soin de toi !", "en": "Take care of yourself!", "note": "Very warm closing phrase"},
            {"fr": "Ne t'inquiète pas ! / Calme-toi !", "en": "Don't worry! / Calm down!", "note": "Reflexive imperative"},
            {"fr": "Vas-y ! / Allons-y !", "en": "Go ahead! / Let's go!", "note": "Imperative + y"},
            {"fr": "se loger / un logement", "en": "to find housing / accommodation", "note": "B1 housing theme"},
            {"fr": "un immeuble récent / ancien", "en": "a modern / old apartment building", "note": "Describing your building"},
            {"fr": "un ascenseur / l'escalier (m) / un étage", "en": "an elevator / the stairs / a floor", "note": "J'habite au troisième étage"},
            {"fr": "un placard", "en": "a closet / cupboard", "note": "Il y a des placards dans la chambre"}
        ],
        "homework": "Donnez 5 conseils à un ami qui vient s'installer et se loger à Genève en utilisant l'impératif (affirmatif et négatif) et le vocabulaire du logement.",
        "written_exercises": [
            {
                "id": "c8-ex1",
                "question": "Transformez à l'impératif (forme 'tu') : 1) Tu regardes → ___ ! 2) Tu prends → ___ ! 3) Tu es patient → ___ patient !",
                "hint": "-er drops the -s; -re keeps the -s; être -> sois.",
                "answer": "Regarde, Prends, Sois",
                "accepted_answers": ["Regarde, Prends, Sois", "regarde, prends, sois"],
                "explanation": "-ER verbs drop the '-s' in 'tu' (Regarde), -RE verbs keep '-s' (Prends), and 'être' is irregular (Sois)."
            },
            {
                "id": "c8-ex2",
                "question": "Transformez à l'impératif affirmatif puis négatif (forme 'tu') : 'Tu te dépêches' → (+) ___ ! / (-) ___ !",
                "hint": "(+) verb-toi; (-) Ne te verb pas (without -s!).",
                "answer": "Dépêche-toi, Ne te dépêche pas",
                "accepted_answers": ["Dépêche-toi, Ne te dépêche pas", "Dépêche-toi !, Ne te dépêche pas !"],
                "explanation": "Affirmative: 'Dépêche-toi !' Negative: 'Ne te dépêche pas !' (still no -s because it's an -er verb)."
            },
            {
                "id": "c8-ex3",
                "question": "Complétez : 'C'est ton tour, ___ (aller + y, forme tu) ! Ne ___ (s'inquiéter, forme tu) pas !'",
                "hint": "Keep the -s before 'y' in 'Vas-y'!",
                "answer": "vas-y, t'inquiète",
                "accepted_answers": ["vas-y, t'inquiète", "Vas-y, t'inquiète"],
                "explanation": "'Vas-y !' keeps the '-s' for liaison before 'y', and 'Ne t'inquiète pas !' drops the '-s'."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c8-sp1",
                "title": "Conseils à un ami qui cherche un logement à Genève",
                "prompt_fr": "Un ami indien vient s'installer à Genève et cherche un appartement. Donnez-lui au moins 5 conseils à l'impératif (par ex: cherche un immeuble avec un ascenseur, choisis un quartier à proximité du tram, ne t'inquiète pas, prends ton temps, appelle-moi !).",
                "target_structures": ["Cherche...", "Prends...", "Sois...", "Ne t'inquiète pas", "un immeuble", "un ascenseur", "un étage"]
            }
        ]
    },
    {
        "id": "class-9",
        "number": 9,
        "date": "Oct 16",
        "title": "La Restriction (Ne...que), Biographies & Passions",
        "cefr_level": "A2 → B1",
        "summary": "Expressing 'only' with 'ne...que', 'être en train de' (in the middle of doing), narrating a biography in Passé Composé (Omar Sy / Intouchables), and talking about hobbies & passions.",
        "concepts": [
            {
                "title": "1. La Restriction : Ne ... que (= Seulement)",
                "explanation": "'Ne ... que' looks like a negation, but it actually means 'ONLY' ('seulement'). Place 'ne' before the verb and 'que' right before the word you want to restrict!",
                "rules": [
                    "Il n'y a qu'un placard dans cette chambre (= Il y a seulement un placard).",
                    "Je n'ai que dix minutes (= J'ai seulement dix minutes).",
                    "Elle ne boit que de l'eau (= Elle boit seulement de l'eau)."
                ],
                "examples": [
                    {"fr": "Dans mon ancien appartement, il n'y avait qu'une petite chambre.", "en": "In my old apartment, there was only one small bedroom."},
                    {"fr": "Je ne travaille que quatre jours cette semaine.", "en": "I am only working four days this week."}
                ]
            },
            {
                "title": "2. L'Action en cours (Être en train de) & Raconter une Biographie",
                "explanation": "Use 'être en train de + infinitif' for 'to be in the middle of doing something right now', and use key biographical verbs in Passé Composé.",
                "rules": [
                    "Je suis en train de réviser mon français (I am in the middle of reviewing my French).",
                    "Verbes biographiques (exemple d'Omar Sy dans le cours) : naître à, faire la connaissance de, s'associer avec, sortir un film, recevoir un prix/un César, s'installer à."
                ],
                "examples": [
                    {"fr": "Omar Sy a reçu le César du meilleur acteur pour le film Intouchables, puis il s'est installé à Los Angeles.", "en": "Omar Sy received the César for Best Actor for Intouchables, then he moved to Los Angeles."},
                    {"fr": "La photographie et le badminton, ça me passionne !", "en": "Photography and badminton, I'm passionate about them!"}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "ne ... que (= seulement)", "en": "only", "note": "Il n'y a qu'un ascenseur"},
            {"fr": "être en train de + infinitif", "en": "to be in the middle of doing", "note": "Je suis en train d'étudier"},
            {"fr": "faire la connaissance de", "en": "to meet / get to know (for the first time)", "note": "J'ai fait la connaissance de..."},
            {"fr": "s'installer (à)", "en": "to settle / move into (a city/country)", "note": "Je me suis installé à Genève"},
            {"fr": "recevoir (reçu)", "en": "to receive", "note": "Il a reçu un prix"},
            {"fr": "Quels sont vos loisirs ? / Ça me passionne", "en": "What are your hobbies? / I'm passionate about it", "note": "Talking about passions"}
        ],
        "homework": "Racontez la biographie d'une personne que vous admirez (ou votre propre parcours vers Genève) avec 's'installer', 'faire la connaissance de', 'recevoir' et utilisez 'ne...que' au moins deux fois.",
        "written_exercises": [
            {
                "id": "c9-ex1",
                "question": "Transformez avec 'ne ... que' : 'J'ai seulement une sœur.' → 'Je ___ ai ___ une sœur.'",
                "hint": "ne -> n' before vowel; que -> qu' before vowel.",
                "answer": "n', qu'",
                "accepted_answers": ["n', qu'", "Je n'ai qu'une sœur."],
                "explanation": "'Seulement' is replaced by 'ne ... que': 'Je n'ai qu'une sœur.'"
            },
            {
                "id": "c9-ex2",
                "question": "Complétez au passé composé : 'Nous (s'installer) ___ à Genève il y a cinq ans et nous (faire) ___ la connaissance de nos voisins.'",
                "hint": "s'installer takes ÊTRE; faire takes AVOIR.",
                "answer": "nous sommes installés, avons fait",
                "accepted_answers": ["nous sommes installés, avons fait"],
                "explanation": "'Nous nous sommes installés' (pronominal -> être) and 'nous avons fait la connaissance de...' (avoir)."
            },
            {
                "id": "c9-ex3",
                "question": "Traduisez avec l'expression du cours : 'I am in the middle of practicing my French.' → 'Je ___ pratiquer mon français.'",
                "hint": "être en train de + infinitif",
                "answer": "suis en train de",
                "accepted_answers": ["suis en train de", "Je suis en train de pratiquer mon français."],
                "explanation": "'Être en train de + infinitif' expresses an ongoing action right now."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c9-sp1",
                "title": "Vos loisirs, vos passions et votre arrivée à Genève",
                "prompt_fr": "Expliquez quand vous vous êtes installé(e) à Genève, comment vous avez fait la connaissance de vos amis ici, et quels sont vos loisirs qui vous passionnent (utilisez aussi 'ne...que' dans une phrase !).",
                "target_structures": ["Je me suis installé(e)", "J'ai fait la connaissance de", "ça me passionne", "ne ... que"]
            }
        ]
    },
    {
        "id": "class-10",
        "number": 10,
        "date": "Oct 23",
        "title": "Expressions Orales, Récit d'une Journée & Introduction à l'Imparfait",
        "cefr_level": "A2 → B1",
        "summary": "Authentic everyday French reactions (C'était une catastrophe, Ça m'arrive, C'est pas mal, Bof, Quand même), adverbs of frequency, narrating a full day, and forming L'Imparfait from the 'nous' stem.",
        "concepts": [
            {
                "title": "1. Formation de L'Imparfait (La règle du 'NOUS')",
                "explanation": "L'Imparfait is the easiest tense to form in French! Take the 'NOUS' form of the present tense, drop '-ons', and add the Imparfait endings: -ais, -ais, -ait, -ions, -iez, -aient.",
                "rules": [
                    "Terminaisons : je -ais, tu -ais, il/elle/on -ait, nous -ions, vous -iez, ils/elles -aient (Note: -ais, -ais, -ait, -aient all sound identical!).",
                    "Prendre → nous prenons → radical 'pren-' → je prenais, tu prenais, il prenait, nous prenions, vous preniez, ils prenaient.",
                    "Faire → nous faisons → je faisais, nous faisions.",
                    "Boire → nous buvons → je buvais, nous buvions.",
                    "Étudier → nous étudions → j'étudiais, nous étudiions (deux 'i' avec nous/vous !).",
                    "SEULE EXCEPTION en français : ÊTRE → radical 'ét-' → j'étais, tu étais, il était, nous étions, vous étiez, ils étaient."
                ],
                "examples": [
                    {"fr": "Quand j'étais étudiant, je prenais le bus tous les matins et j'avais beaucoup d'amis.", "en": "When I was a student, I used to take the bus every morning and I had many friends."},
                    {"fr": "Nous comprenions bien le professeur et nous étudiions ensemble.", "en": "We understood the teacher well and we used to study together."}
                ]
            },
            {
                "title": "2. Expressions Orales Naturelles & Adverbes",
                "explanation": "Expressions from Class 10 that make you sound like a native speaker in Geneva.",
                "rules": [
                    "C'était une catastrophe ! (It was a disaster!) / Quel bordel ! (What a mess! — very informal, use with friends).",
                    "Ça m'arrive souvent (That happens to me often) / C'est pas mal ! (Not bad / pretty good!) / Bof... (Meh / so-so).",
                    "Adverbes : surtout (especially), parfois (sometimes), particulièrement (particularly), normalement (normally/usually)."
                ],
                "examples": [
                    {"fr": "Hier j'ai passé une excellente journée, surtout le soir avec ma famille.", "en": "Yesterday I had a great day, especially in the evening with my family."}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "C'était une catastrophe !", "en": "It was a disaster!", "note": "Great expressive reaction"},
            {"fr": "Ça m'arrive (souvent / parfois)", "en": "That happens to me (often / sometimes)", "note": "Natural spoken phrase"},
            {"fr": "C'est pas mal ! / Bof", "en": "Pretty good! / So-so (meh)", "note": "Everyday reactions"},
            {"fr": "surtout / particulièrement", "en": "especially / particularly", "note": "J'aime la Suisse, surtout en été"},
            {"fr": "je prenais / j'avais / je faisais", "en": "I used to take / I had / I used to do", "note": "Imparfait forms"}
        ],
        "homework": "Conjuguez 'prendre', 'comprendre', 'avoir', 'boire', 'faire' et 'être' à l'imparfait, et racontez une journée complète (du matin au soir).",
        "written_exercises": [
            {
                "id": "c10-ex1",
                "question": "Conjuguez à l'imparfait : 1) Je (prendre) ___, 2) Nous (boire) ___, 3) Ils (avoir) ___, 4) Tu (être) ___.",
                "hint": "nous prenons -> pren-ais; nous buvons -> buv-ions; nous avons -> av-aient; être -> ét-ais.",
                "answer": "prenais, buvions, avaient, étais",
                "accepted_answers": ["prenais, buvions, avaient, étais"],
                "explanation": "From 'nous' present stem: prenais, buvions, avaient, and the only irregular stem 'étais'."
            },
            {
                "id": "c10-ex2",
                "question": "Complétez avec l'adverbe qui convient (surtout / parfois / ça m'arrive) : 'J'aime tous les sports, mais ___ le badminton. ___ de jouer deux fois par semaine.'",
                "hint": "'especially' and 'it happens to me'",
                "answer": "surtout, Ça m'arrive",
                "accepted_answers": ["surtout, Ça m'arrive", "surtout, ça m'arrive"],
                "explanation": "'Surtout' means 'especially', and 'Ça m'arrive de + infinitif' means 'I sometimes happen to...'."
            },
            {
                "id": "c10-ex3",
                "question": "Conjuguez à l'imparfait : 'Avant, je (faire) ___ beaucoup de vélo et je (croire) ___ que c'était facile.'",
                "hint": "nous faisons -> faisais; nous croyons -> croyais",
                "answer": "faisais, croyais",
                "accepted_answers": ["faisais, croyais"],
                "explanation": "From 'nous faisons' → 'je faisais'; from 'nous croyons' → 'je croyais'."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c10-sp1",
                "title": "Racontez une excellente journée (ou une catastrophe !)",
                "prompt_fr": "Racontez une journée mémorable (excellente ou catastrophique) du matin au soir. Utilisez les expressions 'c'est pas mal', 'quand même', 'surtout', 'parfois' ou 'c'était une catastrophe'.",
                "target_structures": ["Hier, j'ai passé...", "surtout", "quand même", "c'est pas mal / c'était une catastrophe"]
            }
        ]
    },
    {
        "id": "class-11",
        "number": 11,
        "date": "Oct 30",
        "title": "L'Imparfait vs. Passé Composé & Les Souvenirs d'Enfance",
        "cefr_level": "B1",
        "summary": "The core B1 distinction between L'Imparfait (past habits, 'used to', memories, background descriptions) and Le Passé Composé (specific one-time completed events), plus memory & nostalgia vocabulary.",
        "concepts": [
            {
                "title": "1. L'Imparfait vs. Le Passé Composé : La Différence Clé (B1)",
                "explanation": "In Class 11, you compared two sentences that summarize the entire rule: 'Lundi dernier, j'ai joué au football' (Passé Composé) vs. 'Quand j'étais jeune, je jouais au basket avec mes amis' (Imparfait).",
                "rules": [
                    "PASSÉ COMPOSÉ = Action ponctuelle, datée, terminée (One-time completed event with a clear start/end) : 'Hier / Lundi dernier / Un jour / Soudain, j'ai joué au foot.'",
                    "IMPARFAIT = Habitude dans le passé ('used to'), description, souvenir d'enfance, décor/météo : 'Quand j'étais petit / Tous les étés / À cette époque, je vivais en Inde, je prenais le bus et je jouais au cricket avec mes amis.'",
                    "Combinaison dans la même phrase : L'Imparfait plante le décor (ce qui était en cours), et le Passé Composé exprime l'événement qui interrompt : 'Je marchais dans la rue (Imparfait) quand j'ai rencontré un ami (Passé Composé).'"
                ],
                "examples": [
                    {"fr": "Quand j'étais enfant, je jouais au basket tous les soirs avec mes amis.", "en": "When I was a child, I used to play basketball every evening with my friends. (Imparfait = habit)"},
                    {"fr": "Lundi dernier, j'ai joué au badminton pendant une heure.", "en": "Last Monday, I played badminton for an hour. (Passé Composé = specific one-time event)"},
                    {"fr": "Ma mère s'occupait de nous et nous accompagnait à l'école tous les matins.", "en": "My mother used to take care of us and accompanied us to school every morning."}
                ]
            },
            {
                "title": "2. Vocabulaire des Souvenirs : Se souvenir de vs. Se rappeler",
                "explanation": "Talking about memories and nostalgia is a classic DELF B1 Production Orale & Écrite topic.",
                "rules": [
                    "se souvenir DE quelque chose : 'Je me souviens de mon enfance / de mon école.'",
                    "se rappeler quelque chose (sans 'de' !) : 'Je me rappelle cette période / ce voyage.'",
                    "évoquer / raconter un souvenir (to evoke / tell a memory) | être nostalgique | avoir une bonne mémoire | effacer un souvenir | s'intéresser à / montrer de l'intérêt."
                ],
                "examples": [
                    {"fr": "Je me souviens très bien de mon enfance : nous vivions dans une grande maison et nous étions très heureux.", "en": "I remember my childhood very well: we lived in a big house and we were very happy."}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "le souvenir vs. la mémoire", "en": "a memory (specific) vs. memory (faculty)", "note": "avoir un bon souvenir / avoir une bonne mémoire"},
            {"fr": "se souvenir de (+ nom)", "en": "to remember", "note": "Je me souviens de mon premier vélo"},
            {"fr": "se rappeler (+ nom direct)", "en": "to remember / recall", "note": "Je me rappelle cette époque"},
            {"fr": "être nostalgique", "en": "to be nostalgic", "note": "Parfois, je suis un peu nostalgique"},
            {"fr": "raconter / évoquer un souvenir", "en": "to tell / evoke a memory", "note": "Class 11 vocabulary"},
            {"fr": "s'occuper de / accompagner", "en": "to take care of / to accompany", "note": "Mes parents s'occupaient de moi"},
            {"fr": "montrer de l'intérêt / s'intéresser à", "en": "to show interest / to be interested in", "note": "Je m'intéressais beaucoup aux sciences"}
        ],
        "homework": "Devoir de la Classe 11 : Racontez une période de votre enfance à l'imparfait (où vous viviez, ce que vous faisiez avec vos amis, qui s'occupait de vous, vos habitudes à l'école et un souvenir particulier).",
        "written_exercises": [
            {
                "id": "c11-ex1",
                "question": "Choisissez entre l'Imparfait et le Passé Composé : '1) Quand j'étais petit, je (jouer) ___ au cricket tous les week-ends. 2) Samedi dernier, je (jouer) ___ au badminton avec mon fils.'",
                "hint": "1 = childhood habit (Imparfait); 2 = specific past Saturday (Passé Composé).",
                "answer": "jouais, ai joué",
                "accepted_answers": ["jouais, ai joué", "jouais, j'ai joué"],
                "explanation": "'Quand j'étais petit... tous les week-ends' is a past habit → Imparfait ('je jouais'). 'Samedi dernier' is a one-time completed event → Passé Composé ('j'ai joué')."
            },
            {
                "id": "c11-ex2",
                "question": "Conjuguez à l'imparfait (verbes de la Classe 11) : 'À cette époque, nous (vivre) ___ en Inde, ma mère (s'occuper) ___ de nous et nous (boire) ___ du thé chaï.'",
                "hint": "nous vivons -> vivions; elle s'occupait; nous buvons -> buvions.",
                "answer": "vivions, s'occupait, buvions",
                "accepted_answers": ["vivions, s'occupait, buvions"],
                "explanation": "vivre → nous vivions; s'occuper → elle s'occupait; boire → nous buvions."
            },
            {
                "id": "c11-ex3",
                "question": "Combinez Imparfait (décor/action en cours) et Passé Composé (interruption) : 'Hier, il (faire) ___ beau et je (marcher) ___ au bord du lac quand soudain je (rencontrer) ___ un collègue.'",
                "hint": "Weather & ongoing walking = Imparfait; 'soudain' interruption = Passé Composé.",
                "answer": "faisait, marchais, ai rencontré",
                "accepted_answers": ["faisait, marchais, ai rencontré", "faisait, marchais, j'ai rencontré"],
                "explanation": "Background weather ('il faisait beau') and ongoing action ('je marchais') take Imparfait; the sudden event ('j'ai rencontré') takes Passé Composé."
            },
            {
                "id": "c11-ex4",
                "question": "Complétez : 'Je me souviens ___ mon école primaire et je m'intéressais ___ mathématiques.'",
                "hint": "se souvenir DE + s'intéresser À (à + les = aux)",
                "answer": "de, aux",
                "accepted_answers": ["de, aux"],
                "explanation": "'Se souvenir de quelque chose' and 's'intéresser à quelque chose' (à + les = aux mathématiques)."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c11-sp1",
                "title": "Devoir Classe 11 : Racontez une période de votre enfance (Imparfait)",
                "prompt_fr": "Racontez une période de votre enfance ! Où viviez-vous ? Comment était votre maison ou votre école ? Que faisiez-vous après l'école avec vos amis ? Qui s'occupait de vous ? Utilisez l'imparfait et le vocabulaire des souvenirs ('je me souviens de...').",
                "target_structures": ["Quand j'étais petit / enfant", "je vivais", "je jouais", "nous allions", "s'occupait de", "je me souviens de"]
            },
            {
                "id": "c11-sp2",
                "title": "Contraste Imparfait vs. Passé Composé : Un souvenir marquant",
                "prompt_fr": "Racontez une anecdote du passé en combinant l'imparfait (le décor, ce que vous faisiez d'habitude) et le passé composé (ce qui s'est passé ce jour-là en particulier : 'Un jour, alors que j'étais..., j'ai...').",
                "target_structures": ["Imparfait (décor)", "Passé Composé (événement)", "Un jour / Soudain", "C'était..."]
            }
        ]
    },
    {
        "id": "class-12",
        "number": 12,
        "date": "Nov 4",
        "title": "Imparfait vs. Passé Composé (Marqueurs, 'Avoir lieu' & Récit de Vacances)",
        "cefr_level": "B1",
        "summary": "Deep dive into time markers for Imparfait (d'habitude, de temps en temps, le lundi) vs. Passé Composé (soudain, tout à coup, un jour, d'abord/ensuite/enfin), the expression 'avoir lieu', FIDE descriptive adjectives, and narrating your last vacation.",
        "concepts": [
            {
                "title": "1. L'Imparfait : Circonstances, Descriptions, Émotions & Expressions d'Habitude",
                "explanation": "In Class 12 (Pages 1 & 2), you learned the 3 core pillars of L'Imparfait and the exact frequency expressions that trigger it.",
                "rules": [
                    "1) L'heure, la météo & toutes les circonstances extérieures (le décor) : 'Il faisait beau, il y avait des animations, des décorations et des lumières de Noël.'",
                    "2) L'âge, l'apparence physique, les vêtements, les attitudes, les sentiments ou émotions : 'Quand j'étais petit(e), j'étais très heureux/heureuse.'",
                    "3) Les habitudes (Habits) : 'Le lundi (= every Monday), je prenais du pain avec du beurre. Le soir, nous regardions la télé.' (Compare with 'Le 8 novembre' = specific date -> Passé Composé !).",
                    "Expressions d'habitude (Imparfait) : tous les / toutes les, d'habitude (usually), normalement, généralement, en général, rarement, parfois, de temps en temps (from time to time), toujours."
                ],
                "examples": [
                    {"fr": "Je suis allé(e) au marché : il y avait beaucoup de fruits et de légumes, et il y avait des animations, des décorations et des lumières de Noël.", "en": "I went to the market (PC = action): there were lots of fruits and vegetables, and there were events, decorations, and Christmas lights (Imparfait = scene description)."},
                    {"fr": "Le lundi, je prenais du pain avec du beurre. Le soir, nous regardions la télé.", "en": "On Mondays (every Monday), I used to have bread with butter. In the evening, we used to watch TV."},
                    {"fr": "De temps en temps, nous partions en vacances.", "en": "From time to time, we used to go on vacation."}
                ]
            },
            {
                "title": "2. Le Passé Composé : L'Intrigue, 'Avoir lieu' & Les Marqueurs Chronologiques",
                "explanation": "In Class 12 (Pages 3 & 4), Passé Composé describes the specific, independent actions that move the plot/story forward (l'intrigue / l'histoire).",
                "rules": [
                    "AVOIR LIEU = to take place : Présent ('Le Diwali a lieu le 8 novembre cette année'), Futur ('Quand aura lieu cette exposition ?'), Passé Composé ('En 2025, l'atelier de sculpture a eu lieu au mois d'octobre').",
                    "Action interrompue (Imparfait + Passé Composé) avec 'soudain / soudainement / tout à coup' : 'Lorsque je mangeais (Imparfait), le téléphone a sonné (Passé Composé).'",
                    "Connecteurs de séquence (Passé Composé) : D'abord / premièrement / en premier → Ensuite / après → Enfin / finalement → Tout de suite (right away) → Un jour (one day = 99% Passé Composé !).",
                    "Contraste clé : 'Quand j'étais petit(e), je passais mes vacances en Italie' (Imparfait = habitude) vs. 'L'année dernière, j'ai passé mes vacances en Italie' (Passé Composé = événement précis).",
                    "Rappel préposition : les cours DE français, les cours DE yoga."
                ],
                "examples": [
                    {"fr": "Je suis arrivé chez moi à 16h. J'ai mangé et j'ai pris une douche. J'ai vu mon frère et on a joué à un jeu vidéo.", "en": "I arrived home at 4 PM. I ate and took a shower. I saw my brother and we played a video game. (Series of completed actions = PC)"},
                    {"fr": "Lorsque je mangeais, soudain le téléphone a sonné.", "en": "While I was eating (Imparfait), suddenly the phone rang (Passé Composé)."},
                    {"fr": "L'année dernière, j'ai passé mes vacances en Italie.", "en": "Last year, I spent my vacation in Italy."}
                ]
            },
            {
                "title": "3. Objectif Examen FIDE : Adjectifs Indispensables pour Décrire (Vacances & Lieux)",
                "explanation": "Your teacher wrote a special boxed note on Page 2: 'Learn adjectives as much as possible for FIDE exam!' Using varied adjectives with 'c'était + adjectif masculin' or 'il y avait...' boosts your FIDE & B1 score immediately.",
                "rules": [
                    "Pour décrire un lieu / un paysage : magnifique (magnificent), splendide, pittoresque (picturesque), paisible / calme (peaceful), animé(e) (lively/bustling), bondé(e) (crowded).",
                    "Pour décrire la météo & l'ambiance : ensoleillé(e) (sunny), doux / douce (mild), chaleureux / chaleureuse (warm/welcoming), accueillant(e) (welcoming), féerique (magical).",
                    "Pour décrire la nourriture & les souvenirs : délicieux / délicieuse, savoureux / savoureuse (tasty), inoubliable (unforgettable), reposant(e) (relaxing), enrichissant(e) (enriching)."
                ],
                "examples": [
                    {"fr": "Le paysage était magnifique et l'ambiance était très chaleureuse et paisible.", "en": "The scenery was magnificent and the atmosphere was very warm and peaceful."}
                ]
            }
        ],
        "vocabulary": [
            {"fr": "à ce moment-là / ce jour-là", "en": "at that moment / on that day", "note": "Class 12 Page 1 time markers"},
            {"fr": "avoir lieu (a eu lieu / aura lieu)", "en": "to take place (took place / will take place)", "note": "Le Diwali a lieu le 8 novembre"},
            {"fr": "de temps en temps", "en": "from time to time", "note": "Imparfait habit marker"},
            {"fr": "d'habitude / en général", "en": "usually / in general", "note": "Imparfait habit marker"},
            {"fr": "soudain / tout à coup", "en": "suddenly / all of a sudden", "note": "Triggers Passé Composé!"},
            {"fr": "tout de suite", "en": "right away / immediately", "note": "Action immédiate"},
            {"fr": "d'abord ... ensuite ... enfin", "en": "first ... then ... finally", "note": "Chronological story connectors"},
            {"fr": "des animations et des lumières", "en": "events/entertainment and lights", "note": "Il y avait des animations au marché"},
            {"fr": "les cours de français / de yoga", "en": "French classes / yoga classes", "note": "cours DE + matière"},
            {"fr": "inoubliable / magnifique / paisible", "en": "unforgettable / magnificent / peaceful", "note": "FIDE exam adjectives"},
            {"fr": "chaleureux (chaleureuse) / animé(e)", "en": "warm & welcoming / lively", "note": "FIDE exam adjectives"},
            {"fr": "reposant(e) / délicieux (délicieuse)", "en": "relaxing / delicious", "note": "Des vacances reposantes"}
        ],
        "homework": "Devoir de la Classe 12 : Décrivez vos dernières vacances en combinant le Passé Composé (où vous êtes allé, ce que vous avez fait : d'abord, ensuite, enfin, un jour...) et l'Imparfait (la météo, le paysage, ce qu'il y avait, vos émotions et des adjectifs riches pour le FIDE).",
        "written_exercises": [
            {
                "id": "c12-ex1",
                "question": "Imparfait (habitude) ou Passé Composé (événement précis) ? '1) Quand j'étais petit, je (passer) ___ mes vacances en Italie. 2) L'année dernière, je (passer) ___ mes vacances en Italie.'",
                "hint": "Page 4 comparison: childhood habit vs. last year!",
                "answer": "passais, ai passé",
                "accepted_answers": ["passais, ai passé", "passais, j'ai passé"],
                "explanation": "'Quand j'étais petit' = childhood habit → Imparfait ('je passais'). 'L'année dernière' = specific completed trip → Passé Composé ('j'ai passé')."
            },
            {
                "id": "c12-ex2",
                "question": "Action en cours + Interruption (Page 4) : 'Lorsque je (manger) ___, soudain le téléphone (sonner) ___.'",
                "hint": "Ongoing action = Imparfait; sudden phone ring = Passé Composé.",
                "answer": "mangeais, a sonné",
                "accepted_answers": ["mangeais, a sonné"],
                "explanation": "'Lorsque je mangeais' (ongoing background action in Imparfait) was interrupted by 'le téléphone a sonné' (Passé Composé)."
            },
            {
                "id": "c12-ex3",
                "question": "Complétez avec l'expression 'avoir lieu' (Page 3) : '1) Le Diwali ___ le 8 novembre cette année (présent). 2) En 2025, l'atelier de sculpture ___ en octobre (passé composé).'",
                "hint": "avoir lieu -> il a lieu (présent) / il a eu lieu (passé composé)",
                "answer": "a lieu, a eu lieu",
                "accepted_answers": ["a lieu, a eu lieu"],
                "explanation": "'Avoir lieu' means 'to take place'. In present: 'a lieu'. In Passé Composé: 'a eu lieu'."
            },
            {
                "id": "c12-ex4",
                "question": "Complétez la description du marché (Page 1) : 'Hier, je (aller) ___ au marché : il y (avoir) ___ beaucoup de fruits et des lumières de Noël.'",
                "hint": "Going to the market = Passé Composé (être); describing what there was = Imparfait (il y avait).",
                "answer": "suis allé, avait",
                "accepted_answers": ["suis allé, avait", "suis allée, avait", "suis allé, il y avait"],
                "explanation": "'Je suis allé(e)' is the main action (Passé Composé), and 'il y avait' sets the scene/description (Imparfait)."
            },
            {
                "id": "c12-ex5",
                "question": "Traduisez l'expression d'habitude (Page 2) : '___ (From time to time), nous partions en vacances.'",
                "hint": "De ... en ...",
                "answer": "De temps en temps",
                "accepted_answers": ["De temps en temps", "de temps en temps"],
                "explanation": "'De temps en temps' means 'from time to time' and is followed by L'Imparfait for past habits."
            }
        ],
        "speaking_prompts": [
            {
                "id": "c12-sp1",
                "title": "Devoir Classe 12 : Décrivez vos dernières vacances (Passé Composé + Imparfait)",
                "prompt_fr": "Décrivez vos dernières vacances ! Où êtes-vous allé(e) et avec qui (Passé Composé) ? Comment étaient la météo, l'hôtel et le paysage (Imparfait + adjectifs FIDE : magnifique, paisible, chaleureux, délicieux) ? Racontez ce que vous avez fait avec 'd'abord', 'ensuite', 'un jour' et 'enfin' !",
                "target_structures": ["L'année dernière / Cet été, nous sommes allés...", "Il faisait beau / Il y avait...", "C'était magnifique / paisible / inoubliable", "D'abord... ensuite... enfin", "Un jour / Soudain"]
            },
            {
                "id": "c12-sp2",
                "title": "Une sortie au marché ou un événement qui a eu lieu à Genève",
                "prompt_fr": "Racontez une sortie récente au marché ou une fête qui a eu lieu à Genève (comme sur la Page 1 et 3 du cahier). Utilisez 'avoir lieu', 'il y avait' (Imparfait) pour décrire les décorations et l'ambiance, et le Passé Composé pour vos actions !",
                "target_structures": ["avoir lieu (a eu lieu)", "Je suis allé(e)...", "Il y avait beaucoup de...", "des animations / des lumières", "C'était très animé"]
            }
        ]
    }
]


def load_custom_classes() -> List[Dict[str, Any]]:
    if not os.path.exists(CUSTOM_CLASSES_FILE):
        return []
    try:
        with open(CUSTOM_CLASSES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_custom_class(new_class: Dict[str, Any]) -> List[Dict[str, Any]]:
    os.makedirs(LTM_DIR, exist_ok=True)
    classes = load_custom_classes()
    # Replace if same id exists, otherwise append
    classes = [c for c in classes if c.get("id") != new_class.get("id")]
    classes.append(new_class)
    with open(CUSTOM_CLASSES_FILE, "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)
    return classes


def get_all_classes() -> List[Dict[str, Any]]:
    return CLASSES_DATA + load_custom_classes()


def get_class_by_id(class_id: str) -> Optional[Dict[str, Any]]:
    for c in get_all_classes():
        if c["id"] == class_id:
            return c
    return None


def load_progress() -> Dict[str, Any]:
    if not os.path.exists(PROGRESS_FILE):
        return {"completed_exercises": [], "completed_speaking": [], "mastered_classes": []}
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"completed_exercises": [], "completed_speaking": [], "mastered_classes": []}


def save_progress_item(category: str, item_id: str) -> Dict[str, Any]:
    os.makedirs(LTM_DIR, exist_ok=True)
    progress = load_progress()
    if category not in progress:
        progress[category] = []
    if item_id not in progress[category]:
        progress[category].append(item_id)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    return progress


def _extract_interaction_text(interaction) -> str:
    if getattr(interaction, "output_text", None):
        return interaction.output_text.strip()
    for output in reversed(getattr(interaction, "outputs", []) or []):
        if getattr(output, "type", None) == "text" and getattr(output, "text", None):
            return output.text.strip()
    return ""


def _parse_json_safely(raw_text: str) -> Dict[str, Any]:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start : end + 1]
    return json.loads(cleaned)


def evaluate_answer_with_gemini(
    client,
    class_id: str,
    prompt_text: str,
    user_answer: str,
    expected_answer: str = "",
    mode: str = "speaking",
) -> Dict[str, Any]:
    """
    Use Gemini (gemini-3.5-flash-lite) to evaluate either a written grammar exercise or an oral speaking response.
    Returns structured JSON with corrections, explanation, B1 upgrade, score, and a short French voice coaching message.
    """
    cls = get_class_by_id(class_id)
    class_context = f"{cls['title']} ({cls['summary']})" if cls else "DELF B1 French Preparation"

    system_instruction = (
        "You are Renée, a warm, rigorous DELF B1 French teacher in Geneva coaching Balu (Sarath), who lives in Geneva "
        "with his wife Lakshmi and 12-year-old son and is preparing for the DELF B1 exam by the end of February. "
        "Respond ONLY with a valid JSON object matching this exact schema:\n"
        "{\n"
        '  "score": <integer from 1 to 10>,\n'
        '  "verdict": "<Excellent ! | Très bien ! | Presque ! | À retravailler>",\n'
        '  "corrected_french": "<the student\'s answer corrected into natural, grammatically accurate French>",\n'
        '  "explanation_en": "<clear, encouraging explanation in English of what was right, any grammar/conjugation/gender/negation mistakes, and why the rule works>",\n'
        '  "b1_upgrade_fr": "<a rich DELF B1 model version in French using connectors like cependant, du coup, grâce à, quand même, d\'un côté...>",\n'
        '  "spoken_feedback_fr": "<2 short, warm sentences in French that you will speak aloud to the student congratulating them and giving the key correction>"\n'
        "}"
    )

    user_input = (
        f"Class / Module Context: {class_context}\n"
        f"Exercise Mode: {mode}\n"
        f"Prompt / Question: {prompt_text}\n"
        f"{f'Expected / Reference Answer: {expected_answer}' if expected_answer else ''}\n"
        f"Student's Answer: {user_answer}\n\n"
        "Evaluate the student's answer now and return ONLY the JSON object."
    )

    interaction = client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=system_instruction,
        input=user_input,
        generation_config={"thinking_level": "minimal"},
        store=False,
    )
    raw = _extract_interaction_text(interaction)
    return _parse_json_safely(raw)


def generate_dynamic_exercises(client, class_id: str) -> Dict[str, Any]:
    """
    Generate 3 fresh written drills and 1 fresh speaking prompt for the selected class using Gemini.
    """
    cls = get_class_by_id(class_id)
    if not cls:
        raise ValueError(f"Unknown class_id: {class_id}")

    concepts_summary = "\n".join(
        f"- {c['title']}: {c['explanation']} ({'; '.join(c.get('rules', [])[:3])})"
        for c in cls.get("concepts", [])
    )
    vocab_summary = ", ".join(v["fr"] for v in cls.get("vocabulary", [])[:10])

    system_instruction = (
        "You are a French DELF B1 curriculum designer creating fresh, engaging exercises tailored to a student living "
        "in Geneva with his wife and 12-year-old son. Return ONLY valid JSON with this exact structure:\n"
        "{\n"
        '  "written_exercises": [\n'
        "    {\n"
        '      "id": "<unique-id>",\n'
        '      "question": "<clear exercise question in French>",\n'
        '      "hint": "<helpful grammar hint in English>",\n'
        '      "answer": "<ideal answer>",\n'
        '      "accepted_answers": ["<ideal answer>"],\n'
        '      "explanation": "<clear explanation of the grammar rule in English>"\n'
        "    }\n"
        "  ],\n"
        '  "speaking_prompt": {\n'
        '    "id": "<unique-id>",\n'
        '    "title": "<short title>",\n'
        '    "prompt_fr": "<engaging oral prompt in French>",\n'
        '    "target_structures": ["<structure 1>", "<structure 2>", "<structure 3>"]\n'
        "  }\n"
        "}"
    )

    user_input = (
        f"Generate 3 brand-new written exercises and 1 brand-new speaking prompt for Class {cls['number']}: {cls['title']}.\n"
        f"Concepts taught in this class:\n{concepts_summary}\n"
        f"Key vocabulary: {vocab_summary}\n"
        "Return ONLY the JSON object."
    )

    interaction = client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=system_instruction,
        input=user_input,
        generation_config={"thinking_level": "minimal"},
        store=False,
    )
    raw = _extract_interaction_text(interaction)
    return _parse_json_safely(raw)


def import_new_class_from_pdf_or_text(
    client,
    class_number: int,
    class_date: str,
    raw_notes: str = "",
    pdf_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    """
    Parse a newly uploaded class PDF or pasted notes from the user's twice-weekly French classes
    and turn it into a structured Class module with grammar rules, vocabulary, written drills, and speaking prompts.
    """
    system_instruction = (
        "You are an expert French DELF B1 curriculum extractor. Given a student's class notes (PDF or text) from their "
        "French lesson, extract all grammar concepts, verb conjugations, vocabulary, homework, and create 4 written "
        "exercises and 2 speaking prompts. Return ONLY a valid JSON object with this exact schema:\n"
        "{\n"
        f'  "id": "class-{class_number}",\n'
        f'  "number": {class_number},\n'
        f'  "date": "{class_date}",\n'
        '  "title": "<French & English topic title>",\n'
        '  "cefr_level": "B1",\n'
        '  "summary": "<1-2 sentence summary in English of everything covered>",\n'
        '  "concepts": [\n'
        "    {\n"
        '      "title": "<Concept title>",\n'
        '      "explanation": "<Clear English explanation>",\n'
        '      "rules": ["<rule 1>", "<rule 2>"],\n'
        '      "examples": [{"fr": "<French example>", "en": "<English translation>"}]\n'
        "    }\n"
        "  ],\n"
        '  "vocabulary": [{"fr": "<French term>", "en": "<English meaning>", "note": "<usage note>"}],\n'
        '  "homework": "<Homework prompt in French>",\n'
        '  "written_exercises": [\n'
        "    {\n"
        f'      "id": "c{class_number}-ex1",\n'
        '      "question": "<Question in French>",\n'
        '      "hint": "<Hint in English>",\n'
        '      "answer": "<Correct answer>",\n'
        '      "accepted_answers": ["<Correct answer>"],\n'
        '      "explanation": "<Why this answer is correct>"\n'
        "    }\n"
        "  ],\n"
        '  "speaking_prompts": [\n'
        "    {\n"
        f'      "id": "c{class_number}-sp1",\n'
        '      "title": "<Speaking drill title>",\n'
        '      "prompt_fr": "<Oral prompt in French>",\n'
        '      "target_structures": ["<structure 1>", "<structure 2>"]\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    inputs: List[Any] = []
    if pdf_bytes:
        b64_pdf = base64.b64encode(pdf_bytes).decode("ascii")
        inputs.append({"type": "document", "data": b64_pdf, "mime_type": "application/pdf"})
    prompt_msg = f"Extract Class {class_number} ({class_date}) into the required JSON schema."
    if raw_notes.strip():
        prompt_msg += f"\n\nClass Notes:\n{raw_notes.strip()}"
    inputs.append({"type": "text", "text": prompt_msg})

    interaction = client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=system_instruction,
        input=inputs,
        generation_config={"thinking_level": "minimal"},
        store=False,
    )
    raw = _extract_interaction_text(interaction)
    new_class = _parse_json_safely(raw)
    new_class["id"] = f"class-{class_number}"
    new_class["number"] = class_number
    new_class["date"] = class_date
    save_custom_class(new_class)
    return new_class


HOMEWORK_FILE = os.path.join(LTM_DIR, "homework_submissions.json")


def load_homework_submissions() -> List[Dict[str, Any]]:
    if not os.path.exists(HOMEWORK_FILE):
        return []
    try:
        with open(HOMEWORK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_homework_submission(entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    os.makedirs(LTM_DIR, exist_ok=True)
    submissions = load_homework_submissions()
    # Put newest first
    submissions = [s for s in submissions if s.get("id") != entry.get("id")]
    submissions.insert(0, entry)
    with open(HOMEWORK_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions[:50], f, ensure_ascii=False, indent=2)
    return submissions[:50]


def delete_homework_submission(submission_id: str) -> List[Dict[str, Any]]:
    os.makedirs(LTM_DIR, exist_ok=True)
    submissions = [s for s in load_homework_submissions() if s.get("id") != submission_id]
    with open(HOMEWORK_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)
    return submissions


def evaluate_homework_submission(
    client,
    class_id: str,
    custom_prompt: str,
    student_text: str,
) -> Dict[str, Any]:
    """
    Evaluate and correct a student's written homework for a specific French class (or custom assignment).
    Saves the corrected homework in ltm/homework_submissions.json so the student can review it before class.
    """
    import time

    cls = get_class_by_id(class_id) if class_id else None
    class_title = f"Cours {cls['number']} ({cls['date']}) — {cls['title']}" if cls else "Devoir Libre"
    homework_prompt = custom_prompt.strip() or (cls.get("homework", "") if cls else "Écriture libre en français")

    concepts_context = ""
    vocab_context = ""
    if cls:
        concepts_context = "\n".join(
            f"- {c['title']}: {c['explanation']} ({'; '.join(c.get('rules', [])[:3])})"
            for c in cls.get("concepts", [])
        )
        vocab_context = ", ".join(v["fr"] for v in cls.get("vocabulary", [])[:12])

    system_instruction = (
        "You are Renée, a warm, encouraging, yet rigorous French teacher in Geneva helping your student correct their "
        "French class homework (target: A2/B1 DELF & FIDE).\n"
        "Analyze the student's homework text carefully and return ONLY a valid JSON object with this exact schema:\n"
        "{\n"
        '  "score": <number from 1 to 10>,\n'
        '  "verdict": "<short encouraging French title, e.g. \'Excellent devoir ! 🌟\' or \'Très bon travail, attention à l\\\'imparfait !\'>",\n'
        '  "corrected_text": "<The student\'s full text corrected into natural, grammatically accurate French, keeping their exact personal story and ideas>",\n'
        '  "b1_upgraded_text": "<An enriched B1 version of their text adding 2-3 natural connectors (e.g. cependant, à cette époque, d\'ailleurs, surtout, du coup) so they can impress their teacher in class>",\n'
        '  "mistakes": [\n'
        "    {\n"
        '      "original": "<exact phrase with error from student text>",\n'
        '      "correction": "<corrected French phrase>",\n'
        '      "rule": "<clear, friendly explanation in English of the grammar/spelling/tense rule (e.g. why Imparfait vs Passé Composé, preposition de/à, gender agreement)>"\n'
        "    }\n"
        "  ],\n"
        '  "strengths": ["<1st thing the student did well (in English)>", "<2nd thing the student did well>"],\n'
        '  "teacher_tip": "<1 practical tip in English + French example for reading this homework aloud in their next class>"\n'
        "}\n"
        "If there are no mistakes at all, return an empty array [] for 'mistakes'."
    )

    user_input = (
        f"Class: {class_title}\n"
        f"Homework Assignment Prompt: {homework_prompt}\n"
        f"Class Grammar Concepts:\n{concepts_context}\n"
        f"Class Target Vocabulary: {vocab_context}\n\n"
        f"Student's Written Homework:\n\"\"\"\n{student_text.strip()}\n\"\"\"\n\n"
        "Correct this homework thoroughly and return ONLY the JSON object."
    )

    interaction = client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=system_instruction,
        input=user_input,
        generation_config={"thinking_level": "minimal"},
        store=False,
    )
    raw = _extract_interaction_text(interaction)
    result = _parse_json_safely(raw)

    submission_entry = {
        "id": f"hw-{int(time.time() * 1000)}",
        "timestamp": time.strftime("%d %b %Y • %H:%M"),
        "class_id": class_id or "custom",
        "class_title": class_title,
        "homework_prompt": homework_prompt,
        "student_text": student_text.strip(),
        "evaluation": result,
    }
    all_submissions = save_homework_submission(submission_entry)
    return {
        "submission": submission_entry,
        "history": all_submissions,
    }


SAVED_HOMEWORKS_DIR = os.path.join(LTM_DIR, "saved_homeworks")


def interactive_improve_homework_from_english(
    client,
    class_id: str,
    custom_prompt: str,
    current_french_text: str,
    english_instructions: str,
    chat_history: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """
    Interactive Homework Co-Writer & Improver:
    The student types in English (or French/mixed) what personal details, ideas, or changes they want to include
    in their homework. Renée builds or updates their French homework using the target class grammar & vocabulary,
    and explains every sentence so the student learns and can read it confidently in class.
    """
    cls = get_class_by_id(class_id) if class_id else None
    class_title = f"Cours {cls['number']} ({cls['date']}) — {cls['title']}" if cls else "Devoir de Français"
    homework_prompt = custom_prompt.strip() or (cls.get("homework", "") if cls else "Écriture en français")

    concepts_context = ""
    vocab_context = ""
    if cls:
        concepts_context = "\n".join(
            f"- {c['title']}: {c['explanation']} ({'; '.join(c.get('rules', [])[:3])})"
            for c in cls.get("concepts", [])
        )
        vocab_context = ", ".join(v["fr"] for v in cls.get("vocabulary", [])[:15])

    history_str = ""
    if chat_history:
        history_str = "\nPrevious interactive requests from student:\n" + "\n".join(
            f"- Student requested: {h.get('user_en', '')}" for h in chat_history[-5:]
        )

    system_instruction = (
        "You are Renée, an interactive French homework co-writer and DELF B1 / FIDE coach in Geneva.\n"
        "The student is telling you in ENGLISH (or a mix of English and French) what personal memories, ideas, or "
        "changes they want to include in their French class homework.\n"
        "Your job is to craft or update their homework in natural, authentic French that uses the target grammar and "
        "vocabulary from their class, while keeping it 100% faithful to their personal story.\n"
        "Return ONLY a valid JSON object with this exact schema:\n"
        "{\n"
        '  "coach_reply_en": "<Warm, encouraging 1-2 sentence response in English explaining how you wove their ideas into the French text and which grammar rules you applied>",\n'
        '  "improved_french_text": "<Clear, natural A2/B1 French homework text incorporating the existing draft + the student\'s new English instructions>",\n'
        '  "b1_plus_french_text": "<An enriched B1+ version of the same text with smooth connectors like \'à cette époque\', \'cependant\', \'d\\\'ailleurs\', \'surtout\', \'du coup\'>",\n'
        '  "key_phrases_added": [\n'
        '    {"en": "<English idea the student asked for>", "fr": "<How we say it in French in the text>"}\n'
        "  ],\n"
        '  "sentence_breakdown": [\n'
        "    {\n"
        '      "fr": "<French sentence from improved_french_text>",\n'
        '      "en": "<English meaning>",\n'
        '      "grammar_note": "<Short note in English explaining the verb tense or structure used, e.g. \'Imparfait (vivions) because it describes where you used to live\'>"\n'
        "    }\n"
        "  ],\n"
        '  "follow_up_suggestions_en": [\n'
        '    "<Short English suggestion 1 the student can click to add more detail>",\n'
        '    "<Short English suggestion 2 the student can click to add a specific event>",\n'
        '    "Make it shorter and easier to pronounce in class"\n'
        "  ]\n"
        "}"
    )

    user_input = (
        f"Class: {class_title}\n"
        f"Homework Assignment Prompt: {homework_prompt}\n"
        f"Target Class Grammar:\n{concepts_context}\n"
        f"Target Class Vocabulary: {vocab_context}\n"
        f"{history_str}\n\n"
        f"Current French Draft in Editor (may be empty if starting fresh):\n\"\"\"\n{current_french_text.strip()}\n\"\"\"\n\n"
        f"Student's New Request in English (what to include or change):\n\"\"\"\n{english_instructions.strip()}\n\"\"\"\n\n"
        "Return ONLY the JSON object."
    )

    interaction = client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=system_instruction,
        input=user_input,
        generation_config={"thinking_level": "minimal"},
        store=False,
    )
    raw = _extract_interaction_text(interaction)
    return _parse_json_safely(raw)


def save_homework_to_disk(
    class_id: str,
    custom_prompt: str,
    student_text: str,
    corrected_text: str = "",
    b1_upgraded_text: str = "",
    english_notes: str = "",
) -> Dict[str, Any]:
    """
    Save the student's homework both into ltm/homework_submissions.json AND as a standalone
    Markdown (.md) and Text (.txt) file inside ltm/saved_homeworks/ on disk.
    """
    import time

    os.makedirs(SAVED_HOMEWORKS_DIR, exist_ok=True)
    cls = get_class_by_id(class_id) if class_id else None
    class_title = f"Cours {cls['number']} ({cls['date']}) — {cls['title']}" if cls else "Devoir Libre"
    homework_prompt = custom_prompt.strip() or (cls.get("homework", "") if cls else "Écriture libre en français")
    timestamp_display = time.strftime("%d %b %Y • %H:%M")
    file_stamp = time.strftime("%Y-%m-%d_%H%M%S")
    safe_class_slug = re.sub(r"[^a-zA-Z0-9_-]+", "_", class_id or "devoir")
    filename = f"devoir_{safe_class_slug}_{file_stamp}.md"
    file_path = os.path.join(SAVED_HOMEWORKS_DIR, filename)

    final_corrected = corrected_text.strip() or student_text.strip()

    md_lines = [
        f"# ✍️ {class_title}",
        f"**Date :** {timestamp_display}",
        f"**Consigne :** {homework_prompt}",
        "",
        "## 🇫🇷 Mon Texte en Français",
        student_text.strip() or "(Vide)",
        "",
    ]
    if corrected_text.strip() and corrected_text.strip() != student_text.strip():
        md_lines.extend([
            "## ✅ Version Corrigée / Améliorée",
            corrected_text.strip(),
            "",
        ])
    if b1_upgraded_text.strip():
        md_lines.extend([
            "## 🚀 Version Niveau B1+ (Avec Connecteurs)",
            b1_upgraded_text.strip(),
            "",
        ])
    if english_notes.strip():
        md_lines.extend([
            "## 🇬🇧 Mes Idées en Anglais (What I included)",
            english_notes.strip(),
            "",
        ])

    md_content = "\n".join(md_lines)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # Also save/update in homework_submissions.json so it shows in the right-hand sidebar history
    submission_entry = {
        "id": f"hw-{int(time.time() * 1000)}",
        "timestamp": timestamp_display,
        "class_id": class_id or "custom",
        "class_title": class_title,
        "homework_prompt": homework_prompt,
        "student_text": student_text.strip() or final_corrected,
        "saved_file_path": file_path,
        "evaluation": {
            "score": 10 if corrected_text.strip() else 8,
            "verdict": "Devoir sauvegardé sur le disque 💾",
            "corrected_text": final_corrected,
            "b1_upgraded_text": b1_upgraded_text.strip(),
            "mistakes": [],
            "strengths": ["Saved to disk at " + file_path],
            "teacher_tip": "Relis ton texte à voix haute avec le bouton 🔊 Écouter avant ton prochain cours !",
        },
    }
    all_submissions = save_homework_submission(submission_entry)
    return {
        "submission": submission_entry,
        "history": all_submissions,
        "file_path": file_path,
        "filename": filename,
        "file_content": md_content,
    }


