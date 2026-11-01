import os
import json
from typing import Dict, Any, List, Optional
from python.consts import DEFAULT_FAST_MODEL, LTM_DIR

COURSE_PROGRESS_FILE = os.path.join(LTM_DIR, "structured_course_progress.json")

STRUCTURED_COURSE_LEVELS: List[Dict[str, Any]] = [
    {
        "level": "A1",
        "title": "Niveau A1 — Fondations & Survie Orale",
        "subtitle": "Parler au présent, poser des questions simples et se débrouiller dans les situations de base à Genève",
        "target_skill": "Oral A1 + Phrases simples",
        "modules": [
            {
                "id": "a1-m1",
                "code": "A1.1",
                "level": "A1",
                "theme": "Identité, Famille & Vie à Genève",
                "title": "Se présenter, parler de sa famille et poser des questions",
                "gemini_presentation": (
                    "Bienvenue dans le module A1.1 ! Pour parler naturellement dès le début, vous devez maîtriser "
                    "la différence entre ÊTRE (état, nationalité, profession : 'Je suis indien, je suis ingénieur') "
                    "et AVOIR (âge, possession : 'J'ai 38 ans, mon fils a 12 ans'). Attention : en français, on utilise "
                    "toujours AVOIR pour dire son âge !"
                ),
                "quick_refresher": {
                    "rule_title": "Être vs. Avoir & Adjectifs Possessifs",
                    "formula": "Être (je suis, tu es, il est, nous sommes, vous êtes, ils sont) | Avoir (j'ai, tu as, il a, nous avons, vous avez, ils ont) + l'âge",
                    "key_takeaway": "Use AVOIR for age ('J'ai 40 ans') and choose mon/ma/mes according to the gender of the noun possessed, not the owner!"
                },
                "concepts": [
                    {
                        "title": "1. Être vs. Avoir & Les Pièges de l'Âge",
                        "explanation": "Use ÊTRE for nationality, profession (without article!), and adjectives. Use AVOIR for age and family members.",
                        "rules": [
                            "Profession sans article : 'Je suis ingénieur' (et NON 'Je suis un ingénieur').",
                            "Âge avec AVOIR : 'Mon fils a douze ans' (et NON 'Mon fils est douze ans').",
                            "Depuis + Présent : 'J'habite à Genève depuis cinq ans' (action qui continue aujourd'hui)."
                        ],
                        "examples": [
                            {"fr": "Je m'appelle Balu, je suis d'origine indienne et j'habite à Genève avec ma femme et mon fils.", "en": "My name is Balu, I am of Indian origin and I live in Geneva with my wife and my son."},
                            {"fr": "Mon fils a douze ans et il est élève au cycle d'orientation.", "en": "My son is twelve years old and he is a middle school student."}
                        ]
                    },
                    {
                        "title": "2. Les Adjectifs Possessifs (mon/ma/mes, notre/nos, leur/leurs)",
                        "explanation": "In French, 'mon' or 'ma' depends on the noun that follows (masculine or feminine), NOT on whether the speaker is a man or a woman!",
                        "rules": [
                            "Masculin singulier : mon fils, ton travail, son appartement.",
                            "Féminin singulier : ma femme, ta ville, sa voiture (⚠️ 'mon' devant une voyelle : mon amie, mon école).",
                            "Pluriel : mes enfants, nos amis, leurs parents."
                        ],
                        "examples": [
                            {"fr": "Ma femme travaille à Genève et son bureau n'est pas loin de notre appartement.", "en": "My wife works in Geneva and her office is not far from our apartment."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "être d'origine (+ adj.)", "en": "to be of ... origin", "note": "Je suis d'origine indienne"},
                    {"fr": "avoir ... ans", "en": "to be ... years old", "note": "Toujours avec AVOIR"},
                    {"fr": "l'épouse (f) / la femme / le mari", "en": "wife / husband", "note": "Ma femme, mon épouse"},
                    {"fr": "le fils / la fille / l'enfant", "en": "son / daughter / child", "note": "Prononcer 'fis'"},
                    {"fr": "le canton / la commune", "en": "canton / municipality (Swiss)", "note": "Le canton de Genève"},
                    {"fr": "depuis (+ durée au présent)", "en": "for / since (+ present tense)", "note": "J'habite ici depuis 5 ans"}
                ],
                "oral_challenges": [
                    {
                        "id": "a1-m1-oc1",
                        "title": "Défi Oral Strict A1.1 : Présentation complète en 4 phrases",
                        "prompt_fr": "Présentez-vous à l'oral : dites votre nom, votre origine, votre profession (sans article !), depuis combien de temps vous habitez à Genève, et présentez votre femme et l'âge de votre fils.",
                        "mandatory_structures": ["je suis", "j'habite à Genève depuis", "ma femme", "mon fils a ... ans"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "a1-m2",
                "code": "A1.2",
                "level": "A1",
                "theme": "Routine Quotidienne, Horaires & Habitudes",
                "title": "Les verbes au présent, les verbes pronominaux et dire l'heure",
                "gemini_presentation": (
                    "Dans ce module A1.2, nous construisons votre capacité à raconter votre journée type au présent. "
                    "Vous allez pratiquer les verbes réguliers (-er, -ir, -re), les grands verbes irréguliers du quotidien "
                    "(prendre, faire, aller, partir, sortir) et les verbes pronominaux (se réveiller, se lever, s'habiller)."
                ),
                "quick_refresher": {
                    "rule_title": "Présent des verbes courants & Pronominaux",
                    "formula": "Je me lève, nous prenons (pas de 'd'), ils prennent (2 'n'), nous faisons, vous faites, ils font",
                    "key_takeaway": "Pronounce 'je prends / tu prends / il prend' identically (silent d), and double the 'n' in 'ils prennent'!"
                },
                "concepts": [
                    {
                        "title": "1. Les Verbes Clés du Quotidien au Présent (Prendre, Faire, Partir, Sortir)",
                        "explanation": "Master the pronunciation difference between singular and plural forms in the present tense.",
                        "rules": [
                            "PRENDRE : je prends, tu prends, il prend (son nasal 'pran'), nous prenons, vous prenez, ils prennent (son 'prènn').",
                            "FAIRE : je fais, tu fais, il fait, nous faisons ('fe-zon'), vous faites, ils font.",
                            "PARTIR / SORTIR : je pars, il part, nous partons, ils partent | je sors, il sort, nous sortons, ils sortent."
                        ],
                        "examples": [
                            {"fr": "Tous les matins, je me lève à six heures et je prends un café avec ma femme.", "en": "Every morning, I get up at 6 o'clock and have a coffee with my wife."},
                            {"fr": "Nous partons de la maison à huit heures moins le quart.", "en": "We leave the house at 7:45 AM."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "se réveiller / se lever", "en": "to wake up / to get up", "note": "Je me lève tôt"},
                    {"fr": "se préparer / s'habiller", "en": "to get ready / to get dressed", "note": "Verbes pronominaux"},
                    {"fr": "prendre le petit-déjeuner", "en": "to have breakfast", "note": "Ne pas dire 'avoir le petit-déjeuner'"},
                    {"fr": "partir au travail / rentrer à la maison", "en": "to leave for work / to come back home", "note": "Routine quotidienne"},
                    {"fr": "le matin / l'après-midi / le soir", "en": "in the morning / afternoon / evening", "note": "Sans préposition 'dans' !"},
                    {"fr": "tous les jours / d'habitude", "en": "every day / usually", "note": "Fréquence"}
                ],
                "oral_challenges": [
                    {
                        "id": "a1-m2-oc1",
                        "title": "Défi Oral Strict A1.2 : Votre journée type du matin au soir",
                        "prompt_fr": "Racontez votre routine d'un jour de semaine au présent : à quelle heure vous vous levez, ce que vous prenez au petit-déjeuner, comment vous allez au travail, et ce que vous faites le soir en famille.",
                        "mandatory_structures": ["je me lève", "je prends", "je pars / je vais", "le soir", "nous"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "a1-m3",
                "code": "A1.3",
                "level": "A1",
                "theme": "Gastronomie, Courses au Supermarché & Restaurant",
                "title": "Articles partitifs (du/de la/des), quantités et commander poliment",
                "gemini_presentation": (
                    "En Suisse comme en France, commander au restaurant ou faire ses courses à la Migros/Coop exige de maîtriser "
                    "les articles partitifs (du pain, de la viande, de l'eau, des légumes) et la règle absolue de la quantité : "
                    "après 'beaucoup de', 'un peu de', 'un kilo de' ou 'pas de', on utilise toujours 'DE' tout seul !"
                ),
                "quick_refresher": {
                    "rule_title": "Partitifs (du, de la, des) vs. Quantité / Négation (de / d')",
                    "formula": "Affirmatif : Je mange du riz / de la salade / des fruits → Quantité ou Négation : Je mange beaucoup DE riz / Je ne mange pas DE viande",
                    "key_takeaway": "After 'pas', 'beaucoup', 'peu', 'trop', 'assez', 'un verre', 'un kilo' → always use DE (never du/de la/des)!"
                },
                "concepts": [
                    {
                        "title": "1. Les Articles Partitifs & La Règle du 'DE' après Quantité/Négation",
                        "explanation": "Use du/de la/de l'/des for unspecified quantities, but switch to plain 'de / d'' after any quantity expression or negation!",
                        "rules": [
                            "Partitifs : du fromage (m), de la soupe (f), de l'eau (voyelle), des pâtes (pl).",
                            "Quantité précise ou adverbe : beaucoup de légumes (et NON 'beaucoup des légumes'), un peu de sucre, une bouteille d'eau.",
                            "Négation : Je ne bois pas de café / Il n'y a plus de lait."
                        ],
                        "examples": [
                            {"fr": "Au petit-déjeuner, je prends du thé, mais je ne prends pas de café.", "en": "For breakfast, I have tea, but I don't have coffee."},
                            {"fr": "J'achète beaucoup de fruits et un kilo de pommes au marché.", "en": "I buy a lot of fruit and a kilo of apples at the market."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "Je voudrais ... s'il vous plaît", "en": "I would like ... please", "note": "Politesse indispensable (Conditionnel)"},
                    {"fr": "faire les courses", "en": "to do grocery shopping", "note": "Faire les courses à la Coop"},
                    {"fr": "le plat du jour / l'addition (f)", "en": "dish of the day / the bill", "note": "L'addition, s'il vous plaît !"},
                    {"fr": "beaucoup de / un peu de / trop de", "en": "a lot of / a little / too much", "note": "Toujours suivi de 'de' sans article"},
                    {"fr": "payer par carte / en espèces", "en": "to pay by card / in cash", "note": "À la caisse"}
                ],
                "oral_challenges": [
                    {
                        "id": "a1-m3-oc1",
                        "title": "Défi Oral Strict A1.3 : Commander au restaurant & parler de son alimentation",
                        "prompt_fr": "1) Commandez poliment un repas complet dans un restaurant à Genève (entrée, plat, boisson, et demandez l'addition). 2) Expliquez ce que vous mangez beaucoup et ce que vous ne mangez jamais ou pas (en respectant la règle du 'de' !).",
                        "mandatory_structures": ["je voudrais", "du / de la / des", "beaucoup de / un peu de", "je ne mange pas de / je ne bois pas de"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "a1-m4",
                "code": "A1.4",
                "level": "A1",
                "theme": "Transports Publics (TPG / CFF) & Orientation en Ville",
                "title": "Aller à, Venir de, Prépositions de lieu et Demander son chemin",
                "gemini_presentation": (
                    "Se déplacer à Genève en tram, en bus ou en train CFF demande de bien distinguer les prépositions "
                    "de lieu et de transport : 'en bus / en train / en voiture' mais 'à pied / à vélo', et les contractions "
                    "avec 'à' (au, aux) et 'de' (du, des)."
                ),
                "quick_refresher": {
                    "rule_title": "Prépositions de Transport & Contractions (au/aux, du/des)",
                    "formula": "EN + transport fermé (en tram, en train, en avion) | À + transport ouvert (à pied, à vélo) | à côté DU parc, en face DE LA gare",
                    "key_takeaway": "Prepositions ending in 'de' (à côté de, en face de, près de, loin de) contract with le/les → du / des!"
                },
                "concepts": [
                    {
                        "title": "1. Se situer et se déplacer : Prépositions & Contractions",
                        "explanation": "Combine movement verbs (aller, venir, prendre, descendre) with accurate prepositions.",
                        "rules": [
                            "Aller à / habiter à + ville : 'J'habite à Genève, je vais à Lausanne.'",
                            "Aller + EN + pays féminin (en Suisse, en Inde, en France) | AU + pays masculin (au Japon, au Portugal) | AUX + pluriel (aux États-Unis).",
                            "Prépositions composées avec DE : près du lac (de+le), en face de la gare, à côté des écoles (de+les), au bout de la rue."
                        ],
                        "examples": [
                            {"fr": "Pour aller au bureau, je prends le tram à côté de chez moi et je descends en face de la gare Cornavin.", "en": "To go to the office, I take the tram next to my place and get off opposite Cornavin station."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "prendre une correspondance / changer de tram", "en": "to take a connection / transfer", "note": "Transports publics"},
                    {"fr": "descendre au prochain arrêt", "en": "to get off at the next stop", "note": "En bus ou en tram"},
                    {"fr": "en face de / à côté de / au bout de", "en": "opposite / next to / at the end of", "note": "Suivi de du / de la / des"},
                    {"fr": "tout droit / à gauche / à droite", "en": "straight ahead / on the left / on the right", "note": "Indiquer une direction"},
                    {"fr": "en retard / à l'heure / en avance", "en": "late / on time / early", "note": "Le train est à l'heure"}
                ],
                "oral_challenges": [
                    {
                        "id": "a1-m4-oc1",
                        "title": "Défi Oral Strict A1.4 : Expliquer un itinéraire dans Genève",
                        "prompt_fr": "Un touriste vous demande comment aller de votre quartier jusqu'à la gare Cornavin ou au bord du lac Léman. Expliquez-lui l'itinéraire complet à l'oral (quel transport prendre, où descendre, et où se trouve le lieu avec 'à côté de', 'en face de', 'tout droit').",
                        "mandatory_structures": ["prenez / allez", "en tram / en bus / à pied", "à côté du / de la", "en face de / tout droit"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "a1-m5",
                "code": "A1.5",
                "level": "A1",
                "theme": "Santé, Médecin & Projets du Week-end (Futur Proche)",
                "title": "Avoir mal à, Il faut + infinitif & Le Futur Proche",
                "gemini_presentation": (
                    "Ce dernier module A1 vous prépare à deux situations essentielles à l'oral : expliquer un problème de santé "
                    "chez le médecin ou à la pharmacie ('J'ai mal à la tête / au dos', 'Il faut prendre ce médicament') et "
                    "parler de vos projets proches avec 'aller + infinitif'."
                ),
                "quick_refresher": {
                    "rule_title": "Avoir mal à + Futur Proche (Aller + Infinitif)",
                    "formula": "avoir mal au dos (masc) / à la gorge (fém) / à l'estomac / aux dents (pl) | Je vais partir, nous n'allons pas sortir",
                    "key_takeaway": "In Futur Proche, negation wraps around ALLER: 'Je ne vais pas travailler demain'."
                },
                "concepts": [
                    {
                        "title": "1. Exprimer la douleur (Avoir mal à) et l'obligation (Il faut)",
                        "explanation": "Use 'avoir mal à' + contracted article and 'il faut + infinitif' for general rules or medical advice.",
                        "rules": [
                            "J'ai mal au ventre / au dos / au genou (masculin).",
                            "J'ai mal à la tête / à la gorge / à la jambe (féminin).",
                            "J'ai mal aux dents / aux yeux / aux oreilles (pluriel).",
                            "Futur proche : Présent du verbe ALLER + Infinitif ('Ce week-end, nous allons faire de la randonnée')."
                        ],
                        "examples": [
                            {"fr": "J'ai mal à la gorge et j'ai de la fièvre, donc je vais aller chez le médecin cet après-midi.", "en": "I have a sore throat and a fever, so I am going to go to the doctor this afternoon."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "avoir mal au dos / à la tête / à la gorge", "en": "to have a backache / headache / sore throat", "note": "Chez le médecin"},
                    {"fr": "avoir de la fièvre / être enrhumé(e)", "en": "to have a fever / to have a cold", "note": "Symptômes"},
                    {"fr": "une ordonnance / la pharmacie", "en": "a prescription / the pharmacy", "note": "Prendre un médicament"},
                    {"fr": "Il faut (+ infinitif)", "en": "It is necessary to / One must", "note": "Il faut se reposer"},
                    {"fr": "ce week-end / demain matin", "en": "this weekend / tomorrow morning", "note": "Marqueurs du futur proche"}
                ],
                "oral_challenges": [
                    {
                        "id": "a1-m5-oc1",
                        "title": "Défi Oral Strict A1.5 : Chez le médecin & Projets du week-end",
                        "prompt_fr": "1) Vous êtes chez le médecin à Genève : expliquez vos symptômes (utilisez 'avoir mal à' au moins deux fois) et dites ce qu'il faut faire. 2) Dites 3 choses que vous et votre famille allez faire le week-end prochain (au futur proche).",
                        "mandatory_structures": ["j'ai mal au / à la", "il faut", "je vais / nous allons + infinitif"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            }
        ]
    },
    {
        "level": "A2",
        "title": "Niveau A2 — Autonomie Orale & Compétence Écrite Cible A2",
        "subtitle": "Raconter au passé (Passé Composé & Imparfait), comparer, utiliser les pronoms et valider votre objectif d'Écrit A2",
        "target_skill": "Oral A2 solide + Écrit A2 (Courriels & Messages 60–80 mots)",
        "modules": [
            {
                "id": "a2-m1",
                "code": "A2.1",
                "level": "A2",
                "theme": "Voyages, Vacances & Événements Passés",
                "title": "Maîtrise complète du Passé Composé (Avoir, Être ADVENT & Pronominaux)",
                "gemini_presentation": (
                    "Au niveau A2, vous devez pouvoir raconter un événement passé à l'oral sans hésiter entre les auxiliaires "
                    "AVOIR et ÊTRE. Rappelez-vous : les 14 verbes de déplacement (ADVENT : aller/venir, arriver/partir, entrer/sortir, "
                    "monter/descendre, naître/mourir, tomber/rester + rentrer/retourner/devenir) et TOUS les verbes pronominaux "
                    "prennent l'auxiliaire ÊTRE !"
                ),
                "quick_refresher": {
                    "rule_title": "Passé Composé : Avoir vs. Être & Place de la Négation",
                    "formula": "Avoir : J'ai pris / Je n'ai pas pris | Être (ADVENT + Pronominaux) : Nous sommes partis / Je ne me suis pas levé tard",
                    "key_takeaway": "Short adverbs (pas, déjà, encore, jamais, rien, bien, beaucoup) go BETWEEN the auxiliary and the past participle: 'Je n'ai pas encore fini'."
                },
                "concepts": [
                    {
                        "title": "1. Choix de l'Auxiliaire & Place des Adverbes au Passé Composé",
                        "explanation": "Get the auxiliary and word order right every time when speaking about the past.",
                        "rules": [
                            "AVOIR (90% des verbes, y compris être -> j'ai été, avoir -> j'ai eu, pouvoir -> j'ai pu, devoir -> j'ai dû).",
                            "ÊTRE (14 verbes ADVENT + verbes pronominaux 'se...') avec accord du participe passé (-e, -s, -es).",
                            "Place de la négation et des adverbes : Sujet + NE + Auxiliaire + PAS/JAMAIS/PLUS/PAS ENCORE + Participe Passé ('Nous ne sommes pas sortis')."
                        ],
                        "examples": [
                            {"fr": "L'été dernier, nous sommes partis en Italie, nous avons visité Rome et nous nous sommes bien amusés.", "en": "Last summer, we left for Italy, visited Rome, and had a great time."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "il y a (+ durée : il y a deux ans)", "en": "ago (two years ago)", "note": "Action terminée au passé composé"},
                    {"fr": "séjourner / passer un séjour", "en": "to stay / spend a trip", "note": "Nous avons passé un beau séjour"},
                    {"fr": "réserver un billet / un hôtel", "en": "to book a ticket / hotel", "note": "Vocabulaire du voyage"},
                    {"fr": "visiter un monument vs. rendre visite à un ami", "en": "to visit a place vs. visit a person", "note": "Distinction essentielle"},
                    {"fr": "se promener / se détendre", "en": "to take a walk / to relax", "note": "Pronominaux au passé composé"}
                ],
                "oral_challenges": [
                    {
                        "id": "a2-m1-oc1",
                        "title": "Défi Oral Strict A2.1 : Raconter vos dernières vacances en famille",
                        "prompt_fr": "Racontez un voyage ou des vacances que vous avez passés avec votre famille. Vous DEVEZ utiliser à l'oral : au moins 3 verbes avec ÊTRE (ex: partir, aller, arriver, rester, rentrer), 3 verbes avec AVOIR (ex: prendre, visiter, voir, faire), 1 verbe pronominal (ex: se promener, se reposer) et 1 phrase négative au passé composé.",
                        "mandatory_structures": ["sommes allés / partis / restés", "avons pris / visité / fait", "nous nous sommes", "ne ... pas (au passé composé)"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": {
                    "id": "a2-m1-wt1",
                    "title": "Écrit Cible A2 : Carte postale / Message de vacances (50–70 mots)",
                    "prompt_fr": "Écrivez un court message (60 mots) à un ami francophone pour lui raconter votre week-end dernier en Suisse (où vous êtes allé, ce que vous avez fait, et quand vous êtes rentré)."
                }
            },
            {
                "id": "a2-m2",
                "code": "A2.2",
                "level": "A2",
                "theme": "Souvenirs d'Enfance, Changements de Vie & Météo",
                "title": "L'Imparfait vs. Le Passé Composé : Raconter une histoire complète",
                "gemini_presentation": (
                    "C'est le concept central de votre Classe 11 et de tout le niveau A2/B1 : quand faut-il utiliser l'Imparfait "
                    "et quand faut-il utiliser le Passé Composé ? Pensez au cinéma : l'Imparfait est le DÉCOR, l'ambiance et "
                    "les habitudes ('Il faisait beau, j'habitais en Inde, je jouais au cricket'), tandis que le Passé Composé "
                    "est l'ACTION précise qui fait avancer l'histoire ('Un jour, j'ai décidé de partir en Suisse')."
                ),
                "quick_refresher": {
                    "rule_title": "Imparfait (Habitude / Décor) vs. Passé Composé (Événement ponctuel)",
                    "formula": "Imparfait = radical de 'nous' au présent + -ais, -ais, -ait, -ions, -iez, -aient (exception : j'étais) | PC = événement daté/soudain",
                    "key_takeaway": "Words like 'd'habitude, tous les jours, quand j'étais petit' trigger Imparfait; 'hier, un jour, soudain, tout à coup' trigger Passé Composé."
                },
                "concepts": [
                    {
                        "title": "1. Combiner Imparfait et Passé Composé dans un récit oral",
                        "explanation": "To tell any story naturally in French, alternate between Imparfait (background/ongoing state) and Passé Composé (event).",
                        "rules": [
                            "Habitude passée vs Aujourd'hui : 'Avant, je vivais en Inde et je prenais ma voiture ; aujourd'hui, j'habite à Genève et je prends le tram.'",
                            "Action en cours interrompue : 'Je marchais dans la rue (Imparfait) quand tout à coup il a commencé à pleuvoir (Passé Composé).'",
                            "Cause/État à l'imparfait : 'Je ne suis pas sorti (PC) parce que j'étais fatigué et qu'il pleuvait (Imparfait).'"
                        ],
                        "examples": [
                            {"fr": "Quand j'avais dix ans, j'allais à l'école à pied tous les jours, mais un jour mon père m'a acheté un vélo.", "en": "When I was ten, I used to walk to school every day, but one day my father bought me a bike."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "à cette époque-là / autrefois", "en": "at that time / in the past", "note": "Déclenche l'imparfait"},
                    {"fr": "avoir l'habitude de (+ infinitif)", "en": "to be used to / in the habit of", "note": "J'avais l'habitude de..."},
                    {"fr": "tout à coup / soudain", "en": "all of a sudden / suddenly", "note": "Déclenche le passé composé"},
                    {"fr": "se souvenir de / se rappeler", "en": "to remember / to recall", "note": "Je me souviens de mon école"},
                    {"fr": "déménager / changer de vie", "en": "to move house / to change life", "note": "J'ai déménagé en Suisse"}
                ],
                "oral_challenges": [
                    {
                        "id": "a2-m2-oc1",
                        "title": "Défi Oral Strict A2.2 : Avant vs. Après votre arrivée en Suisse",
                        "prompt_fr": "Comparez à l'oral votre vie d'avant (en Inde ou pendant votre jeunesse, à l'IMPARFAIT) avec le moment où vous avez déménagé à Genève (au PASSÉ COMPOSÉ) et votre vie actuelle (au PRÉSENT).",
                        "mandatory_structures": ["Avant / Quand j'étais...", "imparfait (-ais/-ions)", "passé composé (je suis venu / je me suis installé)", "maintenant / aujourd'hui"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "a2-m3",
                "code": "A2.3",
                "level": "A2",
                "theme": "Logement, Immobilier & Comparaison Ville vs. Campagne",
                "title": "Les Comparatifs (plus, moins, aussi, meilleur vs. mieux) & Décrire son logement",
                "gemini_presentation": (
                    "Pour comparer deux appartements, deux villes ou deux modes de vie, vous devez maîtriser les comparatifs "
                    "et surtout ne jamais confondre MEILLEUR (comparatif de l'adjectif 'bon' : 'C'est un meilleur quartier') "
                    "et MIEUX (comparatif de l'adverbe 'bien' : 'On vit mieux ici')."
                ),
                "quick_refresher": {
                    "rule_title": "Comparatifs & Meilleur (adj.) vs. Mieux (adv.)",
                    "formula": "Adjectif : plus / moins / aussi + adj. + que | Nom : plus DE / moins DE / autant DE + nom + que | bon → meilleur(e) | bien → mieux",
                    "key_takeaway": "With nouns, use 'autant DE' (not 'aussi de')! Use 'meilleur' to describe a noun ('la vie est meilleure') and 'mieux' to modify a verb ('je parle mieux')."
                },
                "concepts": [
                    {
                        "title": "1. Comparer des qualités, des quantités et des actions",
                        "explanation": "Notice how the comparative word changes depending on whether you compare an adjective, a noun, or a verb.",
                        "rules": [
                            "Avec un adjectif : Genève est plus calme que Mumbai, mais le logement est plus cher.",
                            "Avec un nom : Il y a plus d'espaces verts et moins de bruit qu'au centre-ville, mais il n'y a pas autant de magasins.",
                            "Exceptions : bon(ne) → meilleur(e) ('La qualité de vie est meilleure') | bien → mieux ('Je dors mieux à la campagne')."
                        ],
                        "examples": [
                            {"fr": "Mon nouvel appartement est plus spacieux et plus lumineux que l'ancien, et le quartier est meilleur pour mon fils.", "en": "My new apartment is more spacious and brighter than the old one, and the neighborhood is better for my son."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "le loyer / les charges", "en": "the rent / utility charges", "note": "Le loyer est élevé à Genève"},
                    {"fr": "spacieux / lumineux / bruyant", "en": "spacious / bright / noisy", "note": "Adjectifs du logement"},
                    {"fr": "le rez-de-chaussée / au 3e étage", "en": "ground floor / on the 3rd floor", "note": "Immeuble avec ascenseur"},
                    {"fr": "autant de (+ nom) que", "en": "as much / as many ... as", "note": "Autant d'avantages que d'inconvénients"},
                    {"fr": "meilleur(e) vs. mieux", "en": "better (adjective) vs. better (adverb)", "note": "Un meilleur appartement / vivre mieux"}
                ],
                "oral_challenges": [
                    {
                        "id": "a2-m3-oc1",
                        "title": "Défi Oral Strict A2.3 : Comparer deux logements ou deux villes",
                        "prompt_fr": "Comparez à l'oral la vie à Genève avec une autre ville que vous connaissez (ou comparez votre appartement actuel avec votre ancien logement). Utilisez obligatoirement : 'plus...que', 'moins de...que', et 'meilleur' ou 'mieux'.",
                        "mandatory_structures": ["plus ... que", "moins de / plus de", "meilleur / meilleure / mieux"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "a2-m4",
                "code": "A2.4",
                "level": "A2",
                "theme": "Relations Sociales, Cadeaux & Services Quotidien",
                "title": "Les Pronoms Compléments COD (le, la, les) & COI (lui, leur)",
                "gemini_presentation": (
                    "Pour ne pas répéter les mêmes noms dans chaque phrase ('Je vois mon voisin, je parle à mon voisin'), "
                    "les francophones utilisent constamment les pronoms COD (le, la, l', les) et COI (lui, leur). "
                    "La règle clé : s'il y a la préposition 'À + une personne' (parler à, téléphoner à, demander à, offrir à, "
                    "rendre visite à), utilisez LUI (singulier, homme ou femme !) ou LEUR (pluriel, sans -s !)."
                ),
                "quick_refresher": {
                    "rule_title": "Pronoms COD (le, la, les) vs. COI (lui, leur)",
                    "formula": "Verbe direct (voir, appeler, inviter, écouter) → le, la, les | Verbe + À une personne (parler à, téléphoner à, écrire à, répondre à) → lui, leur",
                    "key_takeaway": "'Lui' means BOTH 'to him' and 'to her'! And 'leur' as a pronoun before a verb NEVER takes an -s ('Je leur parle')."
                },
                "concepts": [
                    {
                        "title": "1. Choisir entre LE/LA/LES (COD) et LUI/LEUR (COI) et bien les placer",
                        "explanation": "Place the pronoun right BEFORE the conjugated verb (or right before the infinitive if there are two verbs!).",
                        "rules": [
                            "COD (sans 'à') : 'Tu connais ce restaurant ? Oui, je le connais.' / 'Je vais l'inviter.'",
                            "COI ('à + personne') : 'Tu téléphones à ta mère ? Oui, je lui téléphone tous les dimanches.' / 'Tu parles à tes collègues ? Oui, je leur parle en français.'",
                            "Avec 2 verbes (vouloir/pouvoir/aller + infinitif), le pronom se place devant l'INFINITIF : 'Je vais lui envoyer un courriel.'"
                        ],
                        "examples": [
                            {"fr": "Mon fils adore ses grands-parents : il les appelle souvent et il leur raconte sa semaine.", "en": "My son loves his grandparents: he calls them often and tells them about his week."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "téléphoner à / répondre à quelqu'un", "en": "to call / to answer someone (COI → lui/leur)", "note": "Je lui réponds"},
                    {"fr": "expliquer / demander quelque chose à quelqu'un", "en": "to explain / ask someone (COI → lui/leur)", "note": "Je lui demande un conseil"},
                    {"fr": "prêter / offrir / conseiller à quelqu'un", "en": "to lend / offer / advise someone", "note": "Je leur conseille de venir"},
                    {"fr": "remercier / aider / inviter quelqu'un", "en": "to thank / help / invite someone (COD → le/la/les)", "note": "Sans 'à' en français ! Je l'aide"}
                ],
                "oral_challenges": [
                    {
                        "id": "a2-m4-oc1",
                        "title": "Défi Oral Strict A2.4 : Parler de vos proches avec le, la, les, lui, leur",
                        "prompt_fr": "Parlez à l'oral de vos relations avec votre famille en Inde, vos collègues ou vos voisins à Genève. Vous DEVEZ utiliser 'le/la/les' (COD) et 'lui/leur' (COI) pour éviter les répétitions (ex: 'Je leur téléphone', 'Je lui demande', 'Je les vois').",
                        "mandatory_structures": ["le / la / les (pronom COD)", "lui", "leur"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "a2-m5",
                "code": "A2.5",
                "level": "A2",
                "theme": "Travail, Rendez-vous Médicaux/Administratifs & Pronoms Relatifs",
                "title": "Devoir / Pouvoir / Vouloir & Relier ses phrases avec QUI, QUE, OÙ",
                "gemini_presentation": (
                    "Dans ce module A2.5, nous relions vos phrases simples pour créer des phrases fluides à l'oral grâce aux "
                    "trois pronoms relatifs indispensables : QUI (sujet : 'le collègue qui parle'), QUE (objet : 'le projet que "
                    "je prépare') et OÙ (lieu ou moment : 'l'entreprise où je travaille, le jour où je suis arrivé')."
                ),
                "quick_refresher": {
                    "rule_title": "Pronoms Relatifs : QUI (sujet) vs. QUE (objet) vs. OÙ (lieu/temps)",
                    "formula": "QUI + Verbe ('la personne qui m'aide') | QUE / QU' + Sujet + Verbe ('le livre que je lis') | OÙ = lieu ou temps ('la ville où j'habite')",
                    "key_takeaway": "Fast trick: if the word right after the gap is a conjugated verb, use QUI. If it's a subject pronoun/noun (je, tu, mon fils...), use QUE / QU'!"
                },
                "concepts": [
                    {
                        "title": "1. Relier deux phrases avec QUI, QUE (QU') et OÙ",
                        "explanation": "Never translate English 'who/which/that' blindly—check whether the relative pronoun is the subject or object of the next verb.",
                        "rules": [
                            "QUI (sujet, suivi d'un verbe) : 'J'ai un professeur qui explique très bien la grammaire.'",
                            "QUE / QU' (COD, suivi d'un sujet + verbe) : 'Voici les exercices que j'ai faits hier.'",
                            "OÙ (complément de lieu ou de temps) : 'Genève est une ville où il y a beaucoup d'organisations internationales.'"
                        ],
                        "examples": [
                            {"fr": "Le quartier où nous habitons a un parc que mon fils aime beaucoup et qui est très calme.", "en": "The neighborhood where we live has a park that my son likes a lot and which is very quiet."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "reporter / déplacer un rendez-vous", "en": "to postpone / reschedule an appointment", "note": "Vocabulaire administratif/pro"},
                    {"fr": "un empêchement / un contretemps", "en": "an unexpected hindrance / setback", "note": "J'ai un empêchement"},
                    {"fr": "être disponible / convenir", "en": "to be available / to suit", "note": "Est-ce que jeudi vous convient ?"},
                    {"fr": "une réunion / un dossier", "en": "a meeting / a file or project", "note": "Au bureau"}
                ],
                "oral_challenges": [
                    {
                        "id": "a2-m5-oc1",
                        "title": "Défi Oral Strict A2.5 : Décrire votre travail et déplacer un rendez-vous",
                        "prompt_fr": "1) Décrivez votre travail et votre quartier en utilisant au moins une phrase avec QUI, une avec QUE et une avec OÙ. 2) Appelez votre dentiste pour expliquer que vous avez un empêchement et demandez à déplacer votre rendez-vous.",
                        "mandatory_structures": ["qui", "que / qu'", "où", "rendez-vous / empêchement / disponible"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "a2-m6",
                "code": "A2.6",
                "level": "A2",
                "theme": "Validation de l'Objectif Écrit A2 (Courriels Formels & Informels)",
                "title": "Tout ce qu'il faut pour réussir l'Écrit A2 en Suisse (60–80 mots)",
                "gemini_presentation": (
                    "Puisque votre objectif écrit est le niveau A2 (tandis que votre objectif oral est B1), ce module regroupe "
                    "exactement les modèles et formules dont vous avez besoin pour obtenir 100% à l'épreuve écrite A2 : "
                    "1) écrire un courriel formel (école de votre fils, régie immobilière, administration) et "
                    "2) écrire un message informel (inviter un ami, remercier, raconter un événement)."
                ),
                "quick_refresher": {
                    "rule_title": "Formules Clés pour l'Écrit A2 (60–80 mots)",
                    "formula": "Formel : 'Madame, Monsieur, Je vous écris pour vous informer que... Dans l'attente de votre réponse, je vous prie d'agréer mes salutations distinguées.'",
                    "key_takeaway": "Memorize 3 blocks for A2 formal emails: Opening ('Madame, Monsieur,'), Purpose ('Je vous contacte car...'), and Closing ('Cordialement / Meilleures salutations')."
                },
                "concepts": [
                    {
                        "title": "1. Structure d'un Courriel Formel A2 (Régie, École, Administration)",
                        "explanation": "In Switzerland, ending a formal email with 'Meilleures salutations' or 'Cordialement' is clean, natural, and accepted everywhere at A2.",
                        "rules": [
                            "Ouverture : 'Madame, Monsieur,' (ou 'Chère Madame..., Cher Monsieur...').",
                            "Objet du message : 'Je vous écris pour vous informer que...' / 'Je vous contacte au sujet de...'",
                            "Demande polie : 'Pourriez-vous m'envoyer... ?' / 'Serait-il possible de reporter notre rendez-vous ?'",
                            "Formule finale suisse A2 : 'En vous remerciant d'avance, je vous adresse, Madame, Monsieur, mes meilleures salutations.'"
                        ],
                        "examples": [
                            {"fr": "Madame, Monsieur, Je vous écris pour vous informer que mon fils ne pourra pas assister au cours demain car il est malade. Meilleures salutations, Sarath Nair.", "en": "Dear Sir/Madam, I am writing to inform you that my son will not be able to attend class tomorrow because he is sick. Best regards, Sarath Nair."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "Je vous écris pour vous informer que...", "en": "I am writing to inform you that...", "note": "Début de courriel formel"},
                    {"fr": "au sujet de / concernant", "en": "regarding / about", "note": "Je vous contacte au sujet de..."},
                    {"fr": "En vous remerciant d'avance", "en": "Thanking you in advance", "note": "Avant la signature"},
                    {"fr": "Meilleures salutations / Cordialement", "en": "Best regards (Swiss standard) / Kind regards", "note": "Fin de courriel"},
                    {"fr": "la régie immobilière / le propriétaire", "en": "property management agency / landlord", "note": "Vocabulaire suisse"}
                ],
                "oral_challenges": [
                    {
                        "id": "a2-m6-oc1",
                        "title": "Défi Oral & Écrit A2.6 : Message à la régie immobilière ou à l'école",
                        "prompt_fr": "Dictez ou écrivez un courriel formel de 60 à 80 mots à votre régie immobilière à Genève : expliquez que le chauffage (ou l'ascenseur) de votre immeuble ne fonctionne plus depuis hier et demandez quand un technicien pourra venir réparer le problème.",
                        "mandatory_structures": ["Madame, Monsieur", "Je vous écris", "ne ... plus", "Meilleures salutations / Cordialement"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": {
                    "id": "a2-m6-wt1",
                    "title": "Épreuve Finale Écrit A2 : Courriel à l'enseignant de votre fils (60–80 mots)",
                    "prompt_fr": "Écrivez un courriel de 60–80 mots à l'enseignant de votre fils pour excuser son absence de deux jours (expliquez la raison, demandez les devoirs à faire à la maison et saluez poliment)."
                }
            }
        ]
    },
    {
        "level": "B1",
        "title": "Niveau B1 — Maîtrise Orale B1 (Focus 100% Speaking & Argumentation)",
        "subtitle": "Parler avec fluidité, faire des hypothèses, utiliser y/en/subjonctif, argumenter et réussir l'examen oral B1 d'ici fin février",
        "target_skill": "Oral B1 Certifié (Entretien, Interaction & Point de vue)",
        "modules": [
            {
                "id": "b1-m1",
                "code": "B1.1",
                "level": "B1",
                "theme": "Projets d'Avenir, Conseils & Hypothèses (Si j'avais...)",
                "title": "Le Futur Simple, le Conditionnel Présent & L'Hypothèse (Si + Imparfait)",
                "gemini_presentation": (
                    "Bienvenue au Niveau B1 ! Pour passer du niveau A2 au niveau B1 à l'oral, l'examinateur attend que vous "
                    "sachiez exprimer des projets certains (Futur Simple : 'L'année prochaine, je passerai mon examen'), "
                    "donner des conseils ou exprimer des souhaits (Conditionnel : 'Tu devrais..., j'aimerais...') et surtout "
                    "faire des hypothèses avec la formule reine du B1 : SI + IMPARFAIT → CONDITIONNEL PRÉSENT !"
                ),
                "quick_refresher": {
                    "rule_title": "Futur Simple, Conditionnel & Hypothèse en 'SI'",
                    "formula": "Futur = Infinitif + -ai, -as, -a, -ons, -ez, -ont | Conditionnel = Radical du Futur + terminaisons de l'Imparfait (-ais, -ais, -ait, -ions, -iez, -aient) | SI + Imparfait → Conditionnel",
                    "key_takeaway": "NEVER put Conditional right after 'SI' ('Les SI n'aiment pas les -RAIS')! Say: 'Si j'avais (imparfait) plus de temps, je voyagerais (conditionnel) davantage.'"
                },
                "concepts": [
                    {
                        "title": "1. Le Futur Simple & Le Conditionnel (Mêmes radicaux irréguliers !)",
                        "explanation": "Once you know the irregular stems for the Futur Simple, you automatically know the Conditionnel—just swap the endings!",
                        "rules": [
                            "Radicaux irréguliers (Futur & Conditionnel) : être → ser- (je serai / je serais), avoir → aur- (j'aurai / j'aurais), aller → ir- (j'irai / j'irais), faire → fer- (je ferai / je ferais), pouvoir → pourr-, devoir → devr-, venir → viendr-, voir → verr-.",
                            "Usages du Conditionnel à l'oral B1 : 1) Conseil ('À ta place, je choisirais ce créneau / Tu devrais...'), 2) Souhait ('J'aimerais bien habiter au bord du lac'), 3) Politesse ('Pourriez-vous m'expliquer... ?').",
                            "L'Hypothèse B1 : SI + Imparfait, + Conditionnel ('Si nous habitions à la campagne, nous aurions un grand jardin')."
                        ],
                        "examples": [
                            {"fr": "En février prochain, je passerai l'examen B1 et je serai très fier de réussir.", "en": "Next February, I will take the B1 exam and I will be very proud to succeed."},
                            {"fr": "Si j'avais plus de temps libre, je ferais du sport tous les jours et j'apprendrais une autre langue.", "en": "If I had more free time, I would play sports every day and learn another language."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "À ta place / À votre place, je...", "en": "In your place / If I were you, I would...", "note": "Suivi du conditionnel"},
                    {"fr": "Tu devrais / Vous devriez (+ infinitif)", "en": "You should...", "note": "Donner un conseil B1"},
                    {"fr": "au cas où (+ conditionnel)", "en": "just in case", "note": "Prends un parapluie au cas où il pleuvrait"},
                    {"fr": "envisager de / avoir l'intention de", "en": "to plan to / to intend to", "note": "Parler de ses projets"},
                    {"fr": "davantage", "en": "more (B1 synonym of 'plus')", "note": "Je pratiquerais davantage"}
                ],
                "oral_challenges": [
                    {
                        "id": "b1-m1-oc1",
                        "title": "Défi Oral Strict B1.1 : Projets futurs, Conseils & Hypothèses en 'Si'",
                        "prompt_fr": "Répondez à l'oral en 3 parties : 1) Que ferez-vous l'année prochaine (utilisez au moins 2 verbes au futur simple) ? 2) Quel conseil donneriez-vous à quelqu'un qui veut apprendre le français (utilisez 'tu devrais' ou 'à ta place') ? 3) Que feriez-vous si vous aviez un mois de vacances supplémentaires ('Si j'avais..., je...') ?",
                        "mandatory_structures": ["futur simple (passerai / ferai / irai / serai)", "devrais / à ta place", "si j'avais / si je pouvais + conditionnel"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "b1-m2",
                "code": "B1.2",
                "level": "B1",
                "theme": "Consommation, Écologie & Fluidité Orale",
                "title": "Les Pronoms Y et EN & Le Pronom Relatif DONT",
                "gemini_presentation": (
                    "Rien ne distingue mieux un candidat B1 à l'oral que l'utilisation naturelle de Y, EN et DONT ! "
                    "C'est très simple : Y remplace un lieu ou 'À + quelque chose' ('J'habite à Genève → J'y habite', "
                    "'Je m'intéresse au sport → Je m'y intéresse'), tandis que EN remplace une quantité, un partitif ou "
                    "'DE + quelque chose' ('Je bois du café → J'en bois', 'J'ai besoin de temps → J'en ai besoin')."
                ),
                "quick_refresher": {
                    "rule_title": "Pronoms Y (lieu / à + chose) vs. EN (quantité / de + chose) & DONT",
                    "formula": "À + lieu/chose → Y ('J'y vais, j'y pense') | DE + chose / quantité → EN ('J'en prends deux, j'en ai besoin, je m'en souviens') | DONT = verbe/nom avec DE",
                    "key_takeaway": "Keep numbers and quantity words at the end when using EN: 'Tu as des frères ? Oui, j'en ai un / j'en ai beaucoup !'"
                },
                "concepts": [
                    {
                        "title": "1. Maîtriser Y, EN et DONT à l'oral",
                        "explanation": "Use Y for 'à + thing/place', EN for 'de + thing/quantity', and DONT to connect sentences when the verb uses 'de' (parler de, avoir besoin de, se souvenir de, être fier de).",
                        "rules": [
                            "Y = Lieu ('Je vis à Genève depuis 5 ans → J'y vis depuis 5 ans') ou Verbe + À + chose ('Je pense à mon examen → J'y pense').",
                            "EN = Partitif/Quantité ('Vous prenez du sucre ? Non, je n'en prends pas') ou Verbe + DE + chose ('Tu te souviens de ce film ? Oui, je m'en souviens !').",
                            "DONT (remplace 'de') : 'C'est le livre dont je t'ai parlé' / 'Le certificat B1 est l'objectif dont j'ai besoin.'"
                        ],
                        "examples": [
                            {"fr": "Genève est une ville magnifique : j'y habite depuis cinq ans et j'en suis très content.", "en": "Geneva is a magnificent city: I have lived there for five years and I am very happy with it."},
                            {"fr": "Le français est une langue dont j'ai besoin tous les jours au travail.", "en": "French is a language that I need every day at work."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "avoir besoin de (→ j'en ai besoin / dont j'ai besoin)", "en": "to need", "note": "Construit avec DE !"},
                    {"fr": "avoir envie de (→ j'en ai envie)", "en": "to feel like / want", "note": "Construit avec DE !"},
                    {"fr": "se souvenir de / s'occuper de (→ je m'en souviens / je m'en occupe)", "en": "to remember / to take care of", "note": "Avec le pronom EN"},
                    {"fr": "s'intéresser à / réfléchir à (→ je m'y intéresse / j'y réfléchis)", "en": "to be interested in / to think about", "note": "Avec le pronom Y"},
                    {"fr": "le tri des déchets / le recyclage", "en": "waste sorting / recycling", "note": "Thème écologique suisse"}
                ],
                "oral_challenges": [
                    {
                        "id": "b1-m2-oc1",
                        "title": "Défi Oral Strict B1.2 : Parler de Genève et de vos habitudes avec Y, EN et DONT",
                        "prompt_fr": "Répondez à l'oral en utilisant obligatoirement : 1) une phrase avec 'Y' (ex: 'j'y habite', 'j'y vais', 'je m'y intéresse'), 2) deux phrases avec 'EN' (ex: 'j'en bois', 'j'en ai besoin', 'je m'en occupe'), et 3) une phrase avec 'DONT' (ex: 'une chose dont j'ai besoin / dont je me souviens').",
                        "mandatory_structures": ["y", "en", "dont"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "b1-m3",
                "code": "B1.3",
                "level": "B1",
                "theme": "Vie Citoyenne, Règles de Société & Émotions",
                "title": "Le Subjonctif Présent : Exprimer l'obligation, le but et les sentiments",
                "gemini_presentation": (
                    "À l'examen oral B1, placer 2 ou 3 subjonctifs bien choisis ('Il faut que je travaille', 'Pour que mon fils "
                    "puisse réussir', 'Bien que ce soit difficile', 'Je suis content que vous soyez là') impressionne "
                    "immédiatement les examinateurs ! Vous n'avez pas besoin de connaître des centaines de verbes : maîtrisez "
                    "les déclencheurs avec QUE et les 7 verbes irréguliers les plus fréquents."
                ),
                "quick_refresher": {
                    "rule_title": "Le Subjonctif Présent (Il faut que, Pour que, Bien que)",
                    "formula": "Radical de 'ILS' au présent + -e, -es, -e, -ions, -iez, -ent | 7 Irréguliers : être (soit), avoir (ait), faire (fasse), aller (aille), pouvoir (puisse), savoir (sache), vouloir (veuille)",
                    "key_takeaway": "Use Subjonctif only when there are TWO subjects separated by QUE ('Je veux que tu viennes') or after 'Il faut que / Bien que / Pour que'!"
                },
                "concepts": [
                    {
                        "title": "1. Quand et comment utiliser le Subjonctif à l'oral B1",
                        "explanation": "Learn the 4 key triggers of the Subjunctive and the 7 essential irregular verbs.",
                        "rules": [
                            "1. Obligation / Nécessité : Il faut que..., Il est important que..., Il est nécessaire que...",
                            "2. Souhait / Volonté (2 sujets différents) : Je voudrais que..., J'aimerais que mon fils fasse...",
                            "3. Émotion / Crainte : Je suis content que..., J'ai peur qu'il soit en retard.",
                            "4. Connecteurs B1 : Pour que (so that), Bien que (although : 'Bien que le français soit difficile...'), Avant que.",
                            "Les 7 irréguliers indispensables : que je sois (être), que j'aie (avoir), que je fasse (faire), que j'aille (aller), que je puisse (pouvoir), que je sache (savoir), que je prenne / vienne."
                        ],
                        "examples": [
                            {"fr": "Pour obtenir mon certificat en février, il faut que je pratique l'oral tous les jours.", "en": "To get my certificate in February, I have to practice speaking every day."},
                            {"fr": "Bien que la grammaire française soit exigeante, je suis ravi que mes collègues m'aident à progresser.", "en": "Although French grammar is demanding, I am delighted that my colleagues help me progress."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "Il faut que / Il est essentiel que (+ subj.)", "en": "It is necessary / essential that...", "note": "Déclencheur n°1 du subjonctif"},
                    {"fr": "pour que / afin que (+ subj.)", "en": "so that / in order that", "note": "Exprimer le but"},
                    {"fr": "bien que (+ subj.)", "en": "although / even though", "note": "Ex: Bien que ce soit cher..."},
                    {"fr": "que je sois / qu'il soit (être)", "en": "that I be / that it be", "note": "Subjonctif de être"},
                    {"fr": "que je fasse / que je puisse", "en": "that I do / that I can", "note": "Subjonctif de faire & pouvoir"}
                ],
                "oral_challenges": [
                    {
                        "id": "b1-m3-oc1",
                        "title": "Défi Oral Strict B1.3 : Vos objectifs et règles de vie au Subjonctif",
                        "prompt_fr": "Expliquez à l'oral ce qu'il faut faire pour bien s'intégrer en Suisse et réussir son examen de français. Vous DEVEZ utiliser : 1) 'Il faut que...' + subjonctif, 2) 'Pour que...' + subjonctif, et 3) 'Bien que...' + subjonctif (avec au moins deux verbes comme être/soit, faire/fasse, pouvoir/puisse ou aller/aille).",
                        "mandatory_structures": ["il faut que", "pour que", "bien que", "soit / sois / fasse / puisse / aille"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "b1-m4",
                "code": "B1.4",
                "level": "B1",
                "theme": "Télétravail, Nouvelles Technologies & Argumentation B1",
                "title": "Structurer un Monologue B1 avec les Connecteurs Logiques",
                "gemini_presentation": (
                    "Dans la Partie 3 de l'examen oral B1, vous devez présenter votre opinion pendant 3 à 5 minutes sur un sujet "
                    "de société (le télétravail, les écrans pour les enfants, les transports). Le secret pour obtenir une note "
                    "élevée est d'organiser votre discours avec des connecteurs de cause, de conséquence et d'opposition — dont "
                    "plusieurs que vous avez déjà vus dans vos Classes 1, 2 et 7 !"
                ),
                "quick_refresher": {
                    "rule_title": "Plan en 4 Étapes & Connecteurs Logiques B1",
                    "formula": "1) Tout d'abord / En premier lieu → 2) D'un côté... (Grâce à / En effet) → 3) Cependant / Toutefois / En revanche (À cause de / Malgré) → 4) En conclusion / Personnellement, j'estime que...",
                    "key_takeaway": "'Malgré' is followed directly by a NOUN ('Malgré la pluie'), whereas 'Bien que' is followed by SUBJONCTIF ('Bien qu'il pleuve')!"
                },
                "concepts": [
                    {
                        "title": "1. Les Connecteurs de Cause, Conséquence et Opposition (Niveau B1)",
                        "explanation": "Use these connectors to link every idea smoothly when giving your opinion.",
                        "rules": [
                            "Introduire son avis : À mon avis, Selon moi, Personnellement, j'estime que..., Je trouve que...",
                            "Cause : parce que, comme (en tête de phrase : 'Comme j'habite près du tram...'), puisque, grâce à (+ nom positif), à cause de (+ nom négatif).",
                            "Conséquence : donc, alors, du coup (oral), c'est pourquoi, par conséquent.",
                            "Opposition & Concession : mais, cependant, toutefois, pourtant, en revanche (on the other hand), malgré (+ nom : 'malgré le prix élevé')."
                        ],
                        "examples": [
                            {"fr": "D'un côté, le télétravail permet de gagner du temps grâce à l'absence de trajet. Cependant, en revanche, il peut créer un sentiment d'isolement.", "en": "On one hand, remote work saves time thanks to no commute. However, on the other hand, it can create a feeling of isolation."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "D'une part ... d'autre part", "en": "On one hand ... on the other hand", "note": "Structurer ses arguments"},
                    {"fr": "en revanche / par contre", "en": "on the other hand / by contrast", "note": "Opposition claire"},
                    {"fr": "cependant / toutefois / pourtant", "en": "however / nonetheless / yet", "note": "Connecteurs B1"},
                    {"fr": "c'est pourquoi / par conséquent", "en": "that is why / consequently", "note": "Conséquence B1"},
                    {"fr": "malgré (+ nom)", "en": "despite (+ noun)", "note": "Malgré les inconvénients"}
                ],
                "oral_challenges": [
                    {
                        "id": "b1-m4-oc1",
                        "title": "Défi Oral Strict B1.4 : Monologue argumenté sur le Télétravail ou les Écrans",
                        "prompt_fr": "Présentez à l'oral votre point de vue structuré sur l'un de ces deux thèmes : 1) 'Le télétravail est-il une bonne chose ?' OU 2) 'Faut-il limiter les écrans et jeux-vidéo pour les adolescents de 12 ans ?' Utilisez obligatoirement : 'D'un côté', 'grâce à' ou 'à cause de', 'cependant / en revanche', et 'c'est pourquoi / du coup'.",
                        "mandatory_structures": ["d'un côté / d'une part", "grâce à / à cause de", "cependant / toutefois / en revanche", "c'est pourquoi / du coup / donc"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "b1-m5",
                "code": "B1.5",
                "level": "B1",
                "theme": "Services Publics, Réclamations & Négociation (Interaction B1)",
                "title": "Gérer un imprévu, se plaindre poliment et négocier une solution à l'oral",
                "gemini_presentation": (
                    "Dans la Partie 2 de l'examen oral B1 (et dans la vie réelle en Suisse !), on vous met face à un problème "
                    "inattendu : un train annulé, une erreur de facture, un voisin bruyant ou un cours annulé. Vous devez "
                    "expliquer le problème clairement, refuser une première réponse insuffisante avec politesse, et proposer "
                    "un compromis."
                ),
                "quick_refresher": {
                    "rule_title": "Stratégies d'Interaction & Négociation Polie B1",
                    "formula": "1) Exposer les faits ('Il se trouve que...') → 2) Exprimer son désaccord poliment ('Je comprends, mais ce n'est pas normal que...') → 3) Proposer une solution ('Serait-il possible de... / Nous pourrions...')",
                    "key_takeaway": "Combine the Conditional of politeness ('Auriez-vous...', 'Serait-il possible de...') with firm connectors ('toutefois', 'quand même') to negotiate effectively!"
                },
                "concepts": [
                    {
                        "title": "1. Formules clés pour négocier et résoudre un problème à l'oral",
                        "explanation": "Use these phrases in any roleplay or real-life customer service situation in Geneva.",
                        "rules": [
                            "Expliquer le problème : 'Je viens vous voir car j'ai un souci avec...' / 'Il y a une erreur sur ma facture.'",
                            "Insister poliment : 'Je comprends votre situation, mais j'ai quand même payé mon abonnement.'",
                            "Proposer un compromis : 'Serait-il possible de trouver un arrangement ?' / 'Est-ce qu'on pourrait envisager un remboursement ou un échange ?'"
                        ],
                        "examples": [
                            {"fr": "Je comprends que le cours du mardi soit complet, mais comme je me suis inscrit le mois dernier, serait-il possible de me proposer un autre créneau ?", "en": "I understand that Tuesday's class is full, but since I registered last month, would it be possible to offer me another time slot?"}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "un remboursement / un échange", "en": "a refund / an exchange", "note": "Service client"},
                    {"fr": "trouver un compromis / un arrangement", "en": "to find a compromise / arrangement", "note": "Interaction B1"},
                    {"fr": "Serait-il possible de (+ infinitif) ?", "en": "Would it be possible to...?", "note": "Formule polie B1"},
                    {"fr": "Je comprends bien, mais...", "en": "I understand well, however...", "note": "Refuser sans être agressif"},
                    {"fr": "être déçu(e) / mécontent(e)", "en": "to be disappointed / dissatisfied", "note": "Exprimer son ressenti"}
                ],
                "oral_challenges": [
                    {
                        "id": "b1-m5-oc1",
                        "title": "Défi Oral Strict B1.5 : Jeu de rôle — Réclamation et Négociation",
                        "prompt_fr": "Vous avez réservé et payé un hôtel à Zermatt pour votre famille ce week-end, mais en arrivant, la réception vous dit qu'il n'y a qu'une toute petite chambre sans vue. Expliquez le problème à l'oral, dites pourquoi vous êtes déçu, et négociez une solution (changer de chambre ou obtenir une réduction/remboursement partiel).",
                        "mandatory_structures": ["je comprends / cependant / mais", "serait-il possible de / pourriez-vous", "déçu / remboursement / arrangement / solution"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            },
            {
                "id": "b1-m6",
                "code": "B1.6",
                "level": "B1",
                "theme": "Discours Indirect, Plus-que-parfait & Examen Blanc Oral B1",
                "title": "Rapporter des paroles (Il m'a dit que...) & Simulation Finale B1",
                "gemini_presentation": (
                    "Ce dernier module B1.6 complète votre boîte à outils orale avec le Discours Indirect ('Mon collègue m'a dit "
                    "qu'il était d'accord et m'a demandé si je viendrais') et le Plus-que-parfait ('J'avais déjà appris l'anglais "
                    "avant de venir en Suisse'). Vous êtes maintenant prêt pour l'épreuve orale finale !"
                ),
                "quick_refresher": {
                    "rule_title": "Discours Indirect au Passé & Plus-que-parfait",
                    "formula": "Il m'a dit que : Présent → Imparfait ('Il a dit qu'il était occupé') | Passé Composé → Plus-que-parfait ('Il a dit qu'il avait fini') | Futur → Conditionnel ('Il a dit qu'il viendrait')",
                    "key_takeaway": "For Yes/No questions in indirect speech, use SI: 'Il m'a demandé SI j'habitais à Genève'. For 'Qu'est-ce que', use CE QUE: 'Il m'a demandé CE QUE je faisais'!"
                },
                "concepts": [
                    {
                        "title": "1. Le Plus-que-parfait & Le Discours Indirect dans la conversation",
                        "explanation": "Use Plus-que-parfait (imparfait of avoir/être + past participle) for an action that happened BEFORE another past action.",
                        "rules": [
                            "Plus-que-parfait : 'Quand je suis arrivé à la gare (PC), le train était déjà parti (PQP).'",
                            "Rapporter une phrase : 'Ma femme m'a dit qu'elle rentrerait à 19h.'",
                            "Rapporter une question : 'L'examinateur m'a demandé si je parlais français au travail et ce que je pensais de la vie à Genève.'"
                        ],
                        "examples": [
                            {"fr": "Mon professeur m'a dit que j'avais fait beaucoup de progrès et m'a demandé si j'étais prêt pour l'examen B1.", "en": "My teacher told me that I had made a lot of progress and asked me if I was ready for the B1 exam."}
                        ]
                    }
                ],
                "vocabulary": [
                    {"fr": "Il m'a dit que / Il m'a expliqué que", "en": "He told me that / explained that", "note": "Discours indirect"},
                    {"fr": "Il m'a demandé si (+ imparfait)", "en": "He asked me if/whether...", "note": "Question fermée rapportée"},
                    {"fr": "Il m'a demandé ce que (+ imparfait)", "en": "He asked me what...", "note": "Remplace 'qu'est-ce que'"},
                    {"fr": "j'avais déjà fait / j'étais déjà allé(e)", "en": "I had already done / had already gone", "note": "Plus-que-parfait"}
                ],
                "oral_challenges": [
                    {
                        "id": "b1-m6-oc1",
                        "title": "Défi Oral Strict Final B1.6 : Synthèse B1 (Passé, Discours Indirect, Opinion & Futur)",
                        "prompt_fr": "C'est votre grand défi de validation B1 ! À l'oral : 1) Racontez ce que vous aviez fait avant de vous installer à Genève (plus-que-parfait), 2) Rapportez une conversation récente avec votre professeur ou un collègue ('Il/Elle m'a dit que... et m'a demandé si...'), et 3) Expliquez pourquoi l'obtention du certificat B1 en février est importante pour vous.",
                        "mandatory_structures": ["avais / étais + participe passé", "m'a dit que", "m'a demandé si / ce que", "pour que / il faut que / cependant"],
                        "min_score": 8
                    }
                ],
                "writing_task_a2": None
            }
        ]
    }
]


def get_all_course_modules() -> List[Dict[str, Any]]:
    modules: List[Dict[str, Any]] = []
    for lvl in STRUCTURED_COURSE_LEVELS:
        for m in lvl["modules"]:
            modules.append(m)
    return modules


def get_course_module_by_id(module_id: str) -> Optional[Dict[str, Any]]:
    for m in get_all_course_modules():
        if m["id"] == module_id:
            return m
    return None


def load_course_progress() -> Dict[str, Any]:
    if not os.path.exists(COURSE_PROGRESS_FILE):
        return {
            "mastered_modules": [],
            "module_scores": {},
            "attempts_count": {},
            "needs_review_modules": [],
            "completed_a2_writing": []
        }
    try:
        with open(COURSE_PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("mastered_modules", [])
            data.setdefault("module_scores", {})
            data.setdefault("attempts_count", {})
            data.setdefault("needs_review_modules", [])
            data.setdefault("completed_a2_writing", [])
            return data
    except Exception:
        return {
            "mastered_modules": [],
            "module_scores": {},
            "attempts_count": {},
            "needs_review_modules": [],
            "completed_a2_writing": []
        }


def save_course_progress(progress: Dict[str, Any]) -> Dict[str, Any]:
    os.makedirs(LTM_DIR, exist_ok=True)
    with open(COURSE_PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    return progress


def record_module_evaluation(module_id: str, score: int, passed: bool, is_writing_a2: bool = False) -> Dict[str, Any]:
    progress = load_course_progress()
    if is_writing_a2:
        if score >= 7 and module_id not in progress["completed_a2_writing"]:
            progress["completed_a2_writing"].append(module_id)
        return save_course_progress(progress)

    prev_best = progress["module_scores"].get(module_id, 0)
    if score > prev_best:
        progress["module_scores"][module_id] = score
    progress["attempts_count"][module_id] = progress["attempts_count"].get(module_id, 0) + 1

    if passed and score >= 8:
        if module_id not in progress["mastered_modules"]:
            progress["mastered_modules"].append(module_id)
        if module_id in progress["needs_review_modules"]:
            progress["needs_review_modules"].remove(module_id)
    else:
        if module_id not in progress["mastered_modules"] and module_id not in progress["needs_review_modules"]:
            progress["needs_review_modules"].append(module_id)

    return save_course_progress(progress)


def toggle_module_review_flag(module_id: str) -> Dict[str, Any]:
    progress = load_course_progress()
    if module_id in progress["needs_review_modules"]:
        progress["needs_review_modules"].remove(module_id)
    else:
        progress["needs_review_modules"].append(module_id)
    return save_course_progress(progress)


def _extract_text(interaction) -> str:
    if getattr(interaction, "output_text", None):
        return interaction.output_text.strip()
    for output in reversed(getattr(interaction, "outputs", []) or []):
        if getattr(output, "type", None) == "text" and getattr(output, "text", None):
            return output.text.strip()
    return ""


def _parse_json(raw_text: str) -> Dict[str, Any]:
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


def evaluate_strict_course_challenge(
    client,
    module_id: str,
    prompt_text: str,
    user_answer: str,
    mandatory_structures: List[str],
    is_writing_a2: bool = False,
) -> Dict[str, Any]:
    """
    Strictly evaluate the student's spoken response (or A2 writing response) for a Structured Course module.
    Requires >= 8/10 and accurate use of the target grammar & thematic vocabulary to pass!
    """
    mod = get_course_module_by_id(module_id)
    if not mod:
        raise ValueError(f"Unknown module_id: {module_id}")

    vocab_list = ", ".join(v["fr"] for v in mod.get("vocabulary", []))
    mandatory_str = ", ".join(mandatory_structures) if mandatory_structures else "All core rules from the module"

    system_instruction = (
        "You are Gemini, acting as a STRICT, rigorous, yet encouraging Swiss DELF/FIDE examiner coaching Balu in Geneva. "
        "His goal is B1 Speaking mastery and A2 Writing mastery by the end of February. "
        "You MUST grade strictly: to pass a module (passed = true, score >= 8), the student MUST:\n"
        "1. Answer the prompt completely in French (not just 3 words).\n"
        "2. Correctly apply the module's grammar concept and mandatory structures.\n"
        "3. Use appropriate vocabulary from the module's theme.\n"
        "If the student makes a major grammar error on the target concept, forgets one of the mandatory structures, "
        "or gives a too-short answer, give a score <= 7 and set 'passed': false so they must retry and truly master the concept!\n\n"
        "Respond ONLY with a valid JSON object matching this exact schema:\n"
        "{\n"
        '  "score": <integer from 1 to 10>,\n'
        '  "passed": <true if score >= 8 and target concept is mastered, else false>,\n'
        '  "verdict": "<Validé avec Brio ! (9-10) | Concept Validé ✅ (8) | Non validé — À corriger et réessayer ⚠️ (<8)>",\n'
        '  "structures_used_check": "<explicitly list which mandatory structures/vocab were used correctly and which were missing or wrong>",\n'
        '  "corrected_french": "<the student\'s answer corrected into natural, accurate French>",\n'
        '  "strict_explanation_en": "<direct, crystal-clear breakdown in English of every grammar mistake and why the rule works>",\n'
        '  "model_answer_fr": "<ideal B1 oral (or A2 written) model answer in French using the theme vocabulary>",\n'
        '  "follow_up_verification_question_fr": "<1 short oral follow-up question in French testing the exact rule they struggled with (or a deeper check if they passed)>",\n'
        '  "spoken_examiner_feedback_fr": "<2 sentences in French that you will speak aloud as the strict examiner: state the score, what was good or missing, and ask them to repeat or answer the follow-up>"\n'
        "}"
    )

    user_input = (
        f"Module: {mod['code']} ({mod['level']}) — {mod['title']} [Theme: {mod['theme']}]\n"
        f"Mode: {'A2 Writing Task (Target: A2 level)' if is_writing_a2 else 'Strict Oral Speaking Mastery (Target: B1 Oral fluency)'}\n"
        f"Challenge Prompt: {prompt_text}\n"
        f"Mandatory Structures Required: {mandatory_str}\n"
        f"Thematic Vocabulary Available: {vocab_list}\n"
        f"Student's Answer: {user_answer}\n\n"
        "Grade strictly now and return ONLY the JSON object."
    )

    interaction = client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=system_instruction,
        input=user_input,
        generation_config={"thinking_level": "minimal"},
        store=False,
    )
    evaluation = _parse_json(_extract_text(interaction))
    score = int(evaluation.get("score", 0))
    passed = bool(evaluation.get("passed", False)) and (score >= 7 if is_writing_a2 else score >= 8)
    evaluation["passed"] = passed
    record_module_evaluation(module_id=module_id, score=score, passed=passed, is_writing_a2=is_writing_a2)
    return evaluation
