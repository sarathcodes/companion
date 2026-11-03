import os
import json
from typing import Dict, Any, List, Optional
from python.consts import DEFAULT_FAST_MODEL, LTM_DIR

STARRED_WORDS_FILE = os.path.join(LTM_DIR, "starred_words.json")
DICT_CACHE_FILE = os.path.join(LTM_DIR, "dictionary_cache.json")

COMMON_DAILY_VERBS: List[Dict[str, Any]] = [
    {
        "verb": "être",
        "en": "to be",
        "category": "indispensables",
        "emoji": "🌟",
        "auxiliary": "avoir",
        "past_participle": "été",
        "tip": "Seule exception à l'imparfait (radical 'ét-' : j'étais). Au futur : je serai.",
        "tenses": {
            "Présent": ["je suis", "tu es", "il/elle est", "nous sommes", "vous êtes", "ils/elles sont"],
            "Passé Composé": ["j'ai été", "tu as été", "il/elle a été", "nous avons été", "vous avez été", "ils/elles ont été"],
            "Imparfait": ["j'étais", "tu étais", "il/elle était", "nous étions", "vous étiez", "ils/elles étaient"],
            "Futur Simple": ["je serai", "tu seras", "il/elle sera", "nous serons", "vous serez", "ils/elles seront"],
            "Conditionnel": ["je serais", "tu serais", "il/elle serait", "nous serions", "vous seriez", "ils/elles seraient"],
            "Impératif / Subjonctif": ["Sois ! Soyons ! Soyez !", "qu'il soit / que je sois"]
        },
        "examples": [
            {"fr": "Je suis très content d'habiter à Genève.", "en": "I am very happy to live in Geneva."},
            {"fr": "Quand j'étais petit, j'étais très curieux.", "en": "When I was little, I was very curious."}
        ]
    },
    {
        "verb": "avoir",
        "en": "to have (also used for age, hunger, thirst, pain)",
        "category": "indispensables",
        "emoji": "🎒",
        "auxiliary": "avoir",
        "past_participle": "eu",
        "tip": "Utilisé pour l'âge (J'ai 12 ans), avoir faim/soif/froid/chaud/mal/besoin de.",
        "tenses": {
            "Présent": ["j'ai", "tu as", "il/elle a", "nous avons", "vous avez", "ils/elles ont"],
            "Passé Composé": ["j'ai eu", "tu as eu", "il/elle a eu", "nous avons eu", "vous avez eu", "ils/elles ont eu"],
            "Imparfait": ["j'avais", "tu avais", "il/elle avait", "nous avions", "vous aviez", "ils/elles avaient"],
            "Futur Simple": ["j'aurai", "tu auras", "il/elle aura", "nous aurons", "vous aurez", "ils/elles auront"],
            "Conditionnel": ["j'aurais", "tu aurais", "il/elle aurait", "nous aurions", "vous auriez", "ils/elles auraient"],
            "Impératif / Subjonctif": ["Aie ! Ayons ! Ayez !", "qu'il ait / que j'aie"]
        },
        "examples": [
            {"fr": "Mon fils a douze ans et nous avons beaucoup de projets.", "en": "My son is twelve years old and we have many plans."},
            {"fr": "Hier, j'ai eu une réunion importante au bureau.", "en": "Yesterday, I had an important meeting at the office."}
        ]
    },
    {
        "verb": "aller",
        "en": "to go (+ Futur Proche: aller + infinitif)",
        "category": "indispensables",
        "emoji": "🚶",
        "auxiliary": "être",
        "past_participle": "allé(e)(s)",
        "tip": "Prend l'auxiliaire ÊTRE au passé composé (Je suis allé, elle est allée) !",
        "tenses": {
            "Présent": ["je vais", "tu vas", "il/elle va", "nous allons", "vous allez", "ils/elles vont"],
            "Passé Composé": ["je suis allé(e)", "tu es allé(e)", "il/elle est allé(e)", "nous sommes allé(e)s", "vous êtes allé(e)s", "ils/elles sont allé(e)s"],
            "Imparfait": ["j'allais", "tu allais", "il/elle allait", "nous allions", "vous alliez", "ils/elles allaient"],
            "Futur Simple": ["j'irai", "tu iras", "il/elle ira", "nous irons", "vous irez", "ils/elles iront"],
            "Conditionnel": ["j'irais", "tu irais", "il/elle irait", "nous irions", "vous iriez", "ils/elles iraient"],
            "Impératif / Subjonctif": ["Va ! (Vas-y !) Allons ! Allez !", "que j'aille / qu'il aille"]
        },
        "examples": [
            {"fr": "Dimanche dernier, nous sommes allés au bord du lac.", "en": "Last Sunday, we went to the lakeshore."},
            {"fr": "Demain, je vais aller à mon cours de français.", "en": "Tomorrow, I am going to go to my French class."}
        ]
    },
    {
        "verb": "faire",
        "en": "to do / to make (+ weather & sports)",
        "category": "indispensables",
        "emoji": "🛠️",
        "auxiliary": "avoir",
        "past_participle": "fait",
        "tip": "Attention à 'vous faites' et 'ils font' au présent ! Futur : je ferai.",
        "tenses": {
            "Présent": ["je fais", "tu fais", "il/elle fait", "nous faisons", "vous faites", "ils/elles font"],
            "Passé Composé": ["j'ai fait", "tu as fait", "il/elle a fait", "nous avons fait", "vous avez fait", "ils/elles ont fait"],
            "Imparfait": ["je faisais", "tu faisais", "il/elle faisait", "nous faisions", "vous faisiez", "ils/elles faisaient"],
            "Futur Simple": ["je ferai", "tu feras", "il/elle fera", "nous ferons", "vous ferez", "ils/elles feront"],
            "Conditionnel": ["je ferais", "tu ferais", "il/elle ferait", "nous ferions", "vous feriez", "ils/elles feraient"],
            "Impératif / Subjonctif": ["Fais ! Faisons ! Faites !", "que je fasse / qu'il fasse"]
        },
        "examples": [
            {"fr": "Le week-end, nous faisons les courses et du sport.", "en": "On the weekend, we do the grocery shopping and play sports."},
            {"fr": "Il faisait très beau hier quand j'ai fait du vélo.", "en": "The weather was very nice yesterday when I went cycling."}
        ]
    },
    {
        "verb": "prendre",
        "en": "to take / to have (food, drink, transport)",
        "category": "indispensables",
        "emoji": "☕",
        "auxiliary": "avoir",
        "past_participle": "pris",
        "tip": "Même famille : comprendre (compris), apprendre (appris). Pas de 'd' avec nous/vous/ils !",
        "tenses": {
            "Présent": ["je prends", "tu prends", "il/elle prend", "nous prenons", "vous prenez", "ils/elles prennent"],
            "Passé Composé": ["j'ai pris", "tu as pris", "il/elle a pris", "nous avons pris", "vous avez pris", "ils/elles ont pris"],
            "Imparfait": ["je prenais", "tu prenais", "il/elle prenait", "nous prenions", "vous preniez", "ils/elles prenaient"],
            "Futur Simple": ["je prendrai", "tu prendras", "il/elle prendra", "nous prendrons", "vous prendrez", "ils/elles prendront"],
            "Conditionnel": ["je prendrais", "tu prendrais", "il/elle prendrait", "nous prendrions", "vous prendriez", "ils/elles prendraient"],
            "Impératif / Subjonctif": ["Prends ! Prenons ! Prenez !", "que je prenne"]
        },
        "examples": [
            {"fr": "Tous les matins, je prends le tram et je prends un café.", "en": "Every morning, I take the tram and have a coffee."},
            {"fr": "Hier, nous avons pris le train pour aller à Zurich.", "en": "Yesterday, we took the train to go to Zurich."}
        ]
    },
    {
        "verb": "pouvoir",
        "en": "can / to be able to",
        "category": "indispensables",
        "emoji": "💪",
        "auxiliary": "avoir",
        "past_participle": "pu",
        "tip": "Participe passé très court : 'pu' (J'ai pu). Au conditionnel de politesse : 'Pourriez-vous... ?'",
        "tenses": {
            "Présent": ["je peux", "tu peux", "il/elle peut", "nous pouvons", "vous pouvez", "ils/elles peuvent"],
            "Passé Composé": ["j'ai pu", "tu as pu", "il/elle a pu", "nous avons pu", "vous avez pu", "ils/elles ont pu"],
            "Imparfait": ["je pouvais", "tu pouvais", "il/elle pouvait", "nous pouvions", "vous pouviez", "ils/elles pouvaient"],
            "Futur Simple": ["je pourrai", "tu pourras", "il/elle pourra", "nous pourrons", "vous pourrez", "ils/elles pourront"],
            "Conditionnel": ["je pourrais", "tu pourrais", "il/elle pourrait", "nous pourrions", "vous pourriez", "ils/elles pourraient"],
            "Impératif / Subjonctif": ["(Pas d'impératif)", "que je puisse / qu'il puisse"]
        },
        "examples": [
            {"fr": "Excusez-moi, pourriez-vous répéter plus lentement ?", "en": "Excuse me, could you repeat more slowly?"},
            {"fr": "À cause de mon travail, je n'ai pas pu venir mardi.", "en": "Because of my work, I couldn't come on Tuesday."}
        ]
    },
    {
        "verb": "vouloir",
        "en": "to want",
        "category": "indispensables",
        "emoji": "🎯",
        "auxiliary": "avoir",
        "past_participle": "voulu",
        "tip": "Utilisez 'Je voudrais' (conditionnel) pour demander poliment !",
        "tenses": {
            "Présent": ["je veux", "tu veux", "il/elle veut", "nous voulons", "vous voulez", "ils/elles veulent"],
            "Passé Composé": ["j'ai voulu", "tu as voulu", "il/elle a voulu", "nous avons voulu", "vous avez voulu", "ils/elles ont voulu"],
            "Imparfait": ["je voulais", "tu voulais", "il/elle voulait", "nous voulions", "vous vouliez", "ils/elles voulaient"],
            "Futur Simple": ["je voudrai", "tu voudras", "il/elle voudra", "nous voudrons", "vous voudrez", "ils/elles voudront"],
            "Conditionnel": ["je voudrais", "tu voudrais", "il/elle voudrait", "nous voudrions", "vous voudriez", "ils/elles voudraient"],
            "Impératif / Subjonctif": ["Veuillez (formel)", "que je veuille"]
        },
        "examples": [
            {"fr": "Je voudrais réserver une table pour trois personnes, s'il vous plaît.", "en": "I would like to book a table for three people, please."},
            {"fr": "Quand j'étais enfant, je voulais devenir pilote.", "en": "When I was a child, I wanted to become a pilot."}
        ]
    },
    {
        "verb": "devoir",
        "en": "must / to have to (+ tu devrais = you should)",
        "category": "indispensables",
        "emoji": "📋",
        "auxiliary": "avoir",
        "past_participle": "dû",
        "tip": "Participe passé avec accent circonflexe : 'dû' (J'ai dû travailler). Conditionnel = conseil ('Tu devrais').",
        "tenses": {
            "Présent": ["je dois", "tu dois", "il/elle doit", "nous devons", "vous devez", "ils/elles doivent"],
            "Passé Composé": ["j'ai dû", "tu as dû", "il/elle a dû", "nous avons dû", "vous avez dû", "ils/elles ont dû"],
            "Imparfait": ["je devais", "tu devais", "il/elle devait", "nous devions", "vous deviez", "ils/elles devaient"],
            "Futur Simple": ["je devrai", "tu devras", "il/elle devra", "nous devrons", "vous devrez", "ils/elles devront"],
            "Conditionnel": ["je devrais", "tu devrais", "il/elle devrait", "nous devrions", "vous devriez", "ils/elles devraient"],
            "Impératif / Subjonctif": ["(Rare)", "que je doive"]
        },
        "examples": [
            {"fr": "Hier, j'ai dû rester tard au bureau.", "en": "Yesterday, I had to stay late at the office."},
            {"fr": "Tu devrais écouter la radio en français tous les matins.", "en": "You should listen to French radio every morning."}
        ]
    },
    {
        "verb": "savoir",
        "en": "to know (a fact, or how to do something)",
        "category": "indispensables",
        "emoji": "🧠",
        "auxiliary": "avoir",
        "past_participle": "su",
        "tip": "Savoir + infinitif / que / où / comment (vs. Connaître + un nom de personne ou de ville).",
        "tenses": {
            "Présent": ["je sais", "tu sais", "il/elle sait", "nous savons", "vous savez", "ils/elles savent"],
            "Passé Composé": ["j'ai su", "tu as su", "il/elle a su", "nous avons su", "vous avez su", "ils/elles ont su"],
            "Imparfait": ["je savais", "tu savais", "il/elle savait", "nous savions", "vous saviez", "ils/elles savaient"],
            "Futur Simple": ["je saurai", "tu sauras", "il/elle saura", "nous saurons", "vous saurez", "ils/elles sauront"],
            "Conditionnel": ["je saurais", "tu saurais", "il/elle saurait", "nous saurions", "vous sauriez", "ils/elles sauraient"],
            "Impératif / Subjonctif": ["Sache ! Sachons ! Sachez !", "que je sache / qu'il sache"]
        },
        "examples": [
            {"fr": "Mon fils sait très bien nager et jouer aux échecs.", "en": "My son knows how to swim and play chess very well."},
            {"fr": "Je ne savais pas que le magasin était fermé le dimanche.", "en": "I didn't know that the shop was closed on Sundays."}
        ]
    },
    {
        "verb": "venir",
        "en": "to come (+ venir de = just did)",
        "category": "quotidien",
        "emoji": "🚆",
        "auxiliary": "être",
        "past_participle": "venu(e)(s)",
        "tip": "Prend ÊTRE au passé composé (Je suis venu). Même famille : devenir (devenu), revenir (revenu), tenir (tenu).",
        "tenses": {
            "Présent": ["je viens", "tu viens", "il/elle vient", "nous venons", "vous venez", "ils/elles viennent"],
            "Passé Composé": ["je suis venu(e)", "tu es venu(e)", "il/elle est venu(e)", "nous sommes venu(e)s", "vous êtes venu(e)s", "ils/elles sont venu(e)s"],
            "Imparfait": ["je venais", "tu venais", "il/elle venait", "nous venions", "vous veniez", "ils/elles venaient"],
            "Futur Simple": ["je viendrai", "tu viendras", "il/elle viendra", "nous viendrons", "vous viendrez", "ils/elles viendront"],
            "Conditionnel": ["je viendrais", "tu viendrais", "il/elle viendrait", "nous viendrions", "vous viendriez", "ils/elles viendraient"],
            "Impératif / Subjonctif": ["Viens ! Venons ! Venez !", "que je vienne / qu'il vienne"]
        },
        "examples": [
            {"fr": "Je viens de finir mes exercices de français.", "en": "I just finished my French exercises."},
            {"fr": "Mes parents sont venus nous rendre visite à Genève l'été dernier.", "en": "My parents came to visit us in Geneva last summer."}
        ]
    },
    {
        "verb": "partir",
        "en": "to leave / to depart",
        "category": "quotidien",
        "emoji": "🧳",
        "auxiliary": "être",
        "past_participle": "parti(e)(s)",
        "tip": "Verbe ADVENT → auxiliaire ÊTRE (Nous sommes partis à 8h). Même conjugaison que sortir et dormir.",
        "tenses": {
            "Présent": ["je pars", "tu pars", "il/elle part", "nous partons", "vous partez", "ils/elles partent"],
            "Passé Composé": ["je suis parti(e)", "tu es parti(e)", "il/elle est parti(e)", "nous sommes parti(e)s", "vous êtes parti(e)s", "ils/elles sont parti(e)s"],
            "Imparfait": ["je partais", "tu partais", "il/elle partait", "nous partions", "vous partiez", "ils/elles partaient"],
            "Futur Simple": ["je partirai", "tu partiras", "il/elle partira", "nous partirons", "vous partirez", "ils/elles partiront"],
            "Conditionnel": ["je partirais", "tu partirais", "il/elle partirait", "nous partirions", "vous partiriez", "ils/elles partiraient"],
            "Impératif / Subjonctif": ["Pars ! Partons ! Partez !", "que je parte"]
        },
        "examples": [
            {"fr": "D'habitude, je pars de la maison à sept heures et demie.", "en": "Usually, I leave the house at 7:30."},
            {"fr": "Nous sommes partis en vacances au mois d'août.", "en": "We left on vacation in August."}
        ]
    },
    {
        "verb": "sortir",
        "en": "to go out / to exit",
        "category": "quotidien",
        "emoji": "🚪",
        "auxiliary": "être",
        "past_participle": "sorti(e)(s)",
        "tip": "Prend ÊTRE (Hier soir, nous sommes sortis au restaurant).",
        "tenses": {
            "Présent": ["je sors", "tu sors", "il/elle sort", "nous sortons", "vous sortez", "ils/elles sortent"],
            "Passé Composé": ["je suis sorti(e)", "tu es sorti(e)", "il/elle est sorti(e)", "nous sommes sorti(e)s", "vous êtes sorti(e)s", "ils/elles sont sorti(e)s"],
            "Imparfait": ["je sortais", "tu sortais", "il/elle sortait", "nous sortions", "vous sortiez", "ils/elles sortaient"],
            "Futur Simple": ["je sortirai", "tu sortiras", "il/elle sortira", "nous sortirons", "vous sortirez", "ils/elles sortiront"],
            "Conditionnel": ["je sortirais", "tu sortirais", "il/elle sortirait", "nous sortirions", "vous sortiriez", "ils/elles sortiraient"],
            "Impératif / Subjonctif": ["Sors ! Sortons ! Sortez !", "que je sorte"]
        },
        "examples": [
            {"fr": "Il pleut, mais nous sortons quand même prendre l'air.", "en": "It's raining, but we're going out anyway to get some fresh air."}
        ]
    },
    {
        "verb": "mettre",
        "en": "to put / to put on (clothes) / to set (an alarm, the table)",
        "category": "quotidien",
        "emoji": "🧥",
        "auxiliary": "avoir",
        "past_participle": "mis",
        "tip": "Même famille : promettre (promis), permettre (permis), admettre (admis).",
        "tenses": {
            "Présent": ["je mets", "tu mets", "il/elle met", "nous mettons", "vous mettez", "ils/elles mettent"],
            "Passé Composé": ["j'ai mis", "tu as mis", "il/elle a mis", "nous avons mis", "vous avez mis", "ils/elles ont mis"],
            "Imparfait": ["je mettais", "tu mettais", "il/elle mettait", "nous mettions", "vous mettiez", "ils/elles mettaient"],
            "Futur Simple": ["je mettrai", "tu mettras", "il/elle mettra", "nous mettrons", "vous mettrez", "ils/elles mettront"],
            "Conditionnel": ["je mettrais", "tu mettrais", "il/elle mettrait", "nous mettrions", "vous mettriez", "ils/elles mettraient"],
            "Impératif / Subjonctif": ["Mets ! Mettons ! Mettez !", "que je mette"]
        },
        "examples": [
            {"fr": "J'ai oublié de mettre mon réveil hier soir !", "en": "I forgot to set my alarm last night!"},
            {"fr": "Mets ton manteau, il fait froid dehors.", "en": "Put on your coat, it's cold outside."}
        ]
    },
    {
        "verb": "voir",
        "en": "to see",
        "category": "quotidien",
        "emoji": "👀",
        "auxiliary": "avoir",
        "past_participle": "vu",
        "tip": "Futur et conditionnel prennent deux 'r' : je verrai / je verrais.",
        "tenses": {
            "Présent": ["je vois", "tu vois", "il/elle voit", "nous voyons", "vous voyez", "ils/elles voient"],
            "Passé Composé": ["j'ai vu", "tu as vu", "il/elle a vu", "nous avons vu", "vous avez vu", "ils/elles ont vu"],
            "Imparfait": ["je voyais", "tu voyais", "il/elle voyait", "nous voyions", "vous voyiez", "ils/elles voyaient"],
            "Futur Simple": ["je verrai", "tu verras", "il/elle verra", "nous verrons", "vous verrez", "ils/elles verront"],
            "Conditionnel": ["je verrais", "tu verrais", "il/elle verrait", "nous verrions", "vous verriez", "ils/elles verraient"],
            "Impératif / Subjonctif": ["Vois ! Voyons ! Voyez !", "que je voie"]
        },
        "examples": [
            {"fr": "Nous avons vu un très bon film français samedi soir.", "en": "We saw a very good French movie on Saturday night."}
        ]
    },
    {
        "verb": "dire",
        "en": "to say / to tell",
        "category": "quotidien",
        "emoji": "🗣️",
        "auxiliary": "avoir",
        "past_participle": "dit",
        "tip": "Attention à 'vous dites' au présent (comme 'vous faites') !",
        "tenses": {
            "Présent": ["je dis", "tu dis", "il/elle dit", "nous disons", "vous dites", "ils/elles disent"],
            "Passé Composé": ["j'ai dit", "tu as dit", "il/elle a dit", "nous avons dit", "vous avez dit", "ils/elles ont dit"],
            "Imparfait": ["je disais", "tu disais", "il/elle disait", "nous disions", "vous disiez", "ils/elles disaient"],
            "Futur Simple": ["je dirai", "tu diras", "il/elle dira", "nous dirons", "vous direz", "ils/elles diront"],
            "Conditionnel": ["je dirais", "tu dirais", "il/elle dirait", "nous dirions", "vous diriez", "ils/elles diraient"],
            "Impératif / Subjonctif": ["Dis-moi ! Disons ! Dites-moi !", "que je dise"]
        },
        "examples": [
            {"fr": "Mon collègue m'a dit que la réunion commençait à 10h.", "en": "My colleague told me that the meeting started at 10 AM."}
        ]
    },
    {
        "verb": "boire",
        "en": "to drink",
        "category": "quotidien",
        "emoji": "🥤",
        "auxiliary": "avoir",
        "past_participle": "bu",
        "tip": "Au pluriel du présent et à l'imparfait, le radical devient 'buv-' (nous buvons, je buvais) !",
        "tenses": {
            "Présent": ["je bois", "tu bois", "il/elle boit", "nous buvons", "vous buvez", "ils/elles boivent"],
            "Passé Composé": ["j'ai bu", "tu as bu", "il/elle a bu", "nous avons bu", "vous avez bu", "ils/elles ont bu"],
            "Imparfait": ["je buvais", "tu buvais", "il/elle buvait", "nous buvions", "vous buviez", "ils/elles buvaient"],
            "Futur Simple": ["je boirai", "tu boiras", "il/elle boira", "nous boirons", "vous boirez", "ils/elles boiront"],
            "Conditionnel": ["je boirais", "tu boirais", "il/elle boirait", "nous boirions", "vous boiriez", "ils/elles boiraient"],
            "Impératif / Subjonctif": ["Bois ! Buvons ! Buvez !", "que je boive"]
        },
        "examples": [
            {"fr": "En Inde, nous buvions du thé chaï tous les après-midis.", "en": "In India, we used to drink chai tea every afternoon."}
        ]
    },
    {
        "verb": "connaître",
        "en": "to know / be familiar with (a person, place, subject)",
        "category": "quotidien",
        "emoji": "🤝",
        "auxiliary": "avoir",
        "past_participle": "connu",
        "tip": "Toujours suivi d'un NOM (Je connais Genève, je connais ton voisin). Jamais suivi d'un verbe ou de 'que' !",
        "tenses": {
            "Présent": ["je connais", "tu connais", "il/elle connaît", "nous connaissons", "vous connaissez", "ils/elles connaissent"],
            "Passé Composé": ["j'ai connu", "tu as connu", "il/elle a connu", "nous avons connu", "vous avez connu", "ils/elles ont connu"],
            "Imparfait": ["je connaissais", "tu connaissais", "il/elle connaissait", "nous connaissions", "vous connaissiez", "ils/elles connaissaient"],
            "Futur Simple": ["je connaîtrai", "tu connaîtras", "il/elle connaîtra", "nous connaîtrons", "vous connaîtrez", "ils/elles connaîtront"],
            "Conditionnel": ["je connaîtrais", "tu connaîtrais", "il/elle connaîtrait", "nous connaîtrions", "vous connaîtriez", "ils/elles connaîtraient"],
            "Impératif / Subjonctif": ["Connais ! Connaissez !", "que je connaisse"]
        },
        "examples": [
            {"fr": "Tu connais quelqu'un dans cet immeuble ? — Non, je ne connais personne.", "en": "Do you know anyone in this building? — No, I don't know anyone."}
        ]
    },
    {
        "verb": "écrire",
        "en": "to write",
        "category": "quotidien",
        "emoji": "✍️",
        "auxiliary": "avoir",
        "past_participle": "écrit",
        "tip": "Au pluriel et à l'imparfait, on ajoute un 'v' : nous écrivons, j'écrivais.",
        "tenses": {
            "Présent": ["j'écris", "tu écris", "il/elle écrit", "nous écrivons", "vous écrivez", "ils/elles écrivent"],
            "Passé Composé": ["j'ai écrit", "tu as écrit", "il/elle a écrit", "nous avons écrit", "vous avez écrit", "ils/elles ont écrit"],
            "Imparfait": ["j'écrivais", "tu écrivais", "il/elle écrivait", "nous écrivions", "vous écriviez", "ils/elles écrivaient"],
            "Futur Simple": ["j'écrirai", "tu écriras", "il/elle écrira", "nous écrirons", "vous écrirez", "ils/elles écriront"],
            "Conditionnel": ["j'écrirais", "tu écrirais", "il/elle écrirait", "nous écririons", "vous écririez", "ils/elles écriraient"],
            "Impératif / Subjonctif": ["Écris-moi ! Écrivez !", "que j'écrive"]
        },
        "examples": [
            {"fr": "J'ai écrit un courriel à la régie immobilière ce matin.", "en": "I wrote an email to the property management agency this morning."}
        ]
    },
    {
        "verb": "se lever",
        "en": "to get up / stand up (Pronominal)",
        "category": "pronominaux",
        "emoji": "🌅",
        "auxiliary": "être",
        "past_participle": "levé(e)(s)",
        "tip": "Tous les verbes pronominaux ('se...') prennent ÊTRE au passé composé : Je me suis levé, je ne me suis pas levé.",
        "tenses": {
            "Présent": ["je me lève", "tu te lèves", "il/elle se lève", "nous nous levons", "vous vous levez", "ils/elles se lèvent"],
            "Passé Composé": ["je me suis levé(e)", "tu t'es levé(e)", "il/elle s'est levé(e)", "nous nous sommes levé(e)s", "vous vous êtes levé(e)s", "ils/elles se sont levé(e)s"],
            "Imparfait": ["je me levais", "tu te levais", "il/elle se levait", "nous nous levions", "vous vous leviez", "ils/elles se levaient"],
            "Futur Simple": ["je me lèverai", "tu te lèveras", "il/elle se lèvera", "nous nous lèverons", "vous vous lèverez", "ils/elles se lèveront"],
            "Conditionnel": ["je me lèverais", "tu te lèverais", "il/elle se lèverait", "nous nous lèverions", "vous vous lèveriez", "ils/elles se lèveraient"],
            "Impératif / Subjonctif": ["Lève-toi ! (Ne te lève pas !) Levons-nous ! Levez-vous !", "que je me lève"]
        },
        "examples": [
            {"fr": "La semaine, je me lève à 6h, mais dimanche je me suis levé à 9h.", "en": "On weekdays, I get up at 6 AM, but on Sunday I got up at 9 AM."}
        ]
    },
    {
        "verb": "se souvenir",
        "en": "to remember (+ DE quelque chose)",
        "category": "pronominaux",
        "emoji": "💭",
        "auxiliary": "être",
        "past_participle": "souvenu(e)(s)",
        "tip": "Se conjugue exactement comme 'venir' + DE : 'Je me souviens de mon enfance → Je m'en souviens !'",
        "tenses": {
            "Présent": ["je me souviens", "tu te souviens", "il/elle se souvient", "nous nous souvenons", "vous vous souvenez", "ils/elles se souviennent"],
            "Passé Composé": ["je me suis souvenu(e)", "tu t'es souvenu(e)", "il/elle s'est souvenu(e)", "nous nous sommes souvenu(e)s", "vous vous êtes souvenu(e)s", "ils/elles se sont souvenu(e)s"],
            "Imparfait": ["je me souvenais", "tu te souvenais", "il/elle se souvenait", "nous nous souvenions", "vous vous souveniez", "ils/elles se souvenaient"],
            "Futur Simple": ["je me souviendrai", "tu te souviendras", "il/elle se souviendra", "nous nous souviendrons", "vous vous souviendrez", "ils/elles se souviendront"],
            "Conditionnel": ["je me souviendrais", "tu te souviendrais", "il/elle se souviendrait", "nous nous souviendrions", "vous vous souviendriez", "ils/elles se souviendraient"],
            "Impératif / Subjonctif": ["Souviens-toi ! Souvenez-vous !", "que je me souvienne"]
        },
        "examples": [
            {"fr": "Je me souviens très bien du jour où nous sommes arrivés en Suisse.", "en": "I remember very well the day we arrived in Switzerland."}
        ]
    }
]


def load_starred_words() -> List[Dict[str, Any]]:
    if not os.path.exists(STARRED_WORDS_FILE):
        return []
    try:
        with open(STARRED_WORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_starred_words(words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    os.makedirs(LTM_DIR, exist_ok=True)
    with open(STARRED_WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    return words


def toggle_starred_word(word_entry: Dict[str, Any]) -> Dict[str, Any]:
    words = load_starred_words()
    key = (word_entry.get("lemma") or word_entry.get("word") or "").strip().lower()
    existing_idx = next(
        (i for i, w in enumerate(words) if (w.get("lemma") or w.get("word") or "").strip().lower() == key),
        -1
    )
    if existing_idx != -1:
        words.pop(existing_idx)
        starred = False
    else:
        words.insert(0, word_entry)
        starred = True
    save_starred_words(words)
    return {"starred": starred, "starred_words": words}


def _load_dict_cache() -> Dict[str, Any]:
    if not os.path.exists(DICT_CACHE_FILE):
        return {}
    try:
        with open(DICT_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_dict_cache(cache: Dict[str, Any]) -> None:
    os.makedirs(LTM_DIR, exist_ok=True)
    with open(DICT_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


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


def _match_common_verb_any_form(clean_word: str) -> Optional[Dict[str, Any]]:
    """
    Check if `clean_word` matches the infinitive, past participle, or any conjugated form
    of our 20 pre-loaded COMMON_DAILY_VERBS.
    """
    for v in COMMON_DAILY_VERBS:
        if v["verb"] == clean_word or v["past_participle"].split("(")[0] == clean_word:
            return v
        for tense_lines in v.get("tenses", {}).values():
            for line in tense_lines:
                tokens = [t.strip("()!.,").lower() for t in line.replace("'", " ").replace("/", " ").split()]
                if clean_word in tokens:
                    return v
    return None


def _starts_with_vowel(s: str) -> bool:
    return bool(s) and s[0].lower() in "aeiouyàâäéèêëîïôöùûüœæh"


def _je_prefix(verb_form: str) -> str:
    return f"j'{verb_form}" if _starts_with_vowel(verb_form) else f"je {verb_form}"


def _build_5_tenses_in_python(
    infinitive: str,
    auxiliary: str,
    past_participle: str,
    present_6: List[str],
    imparfait_stem: str,
    futur_stem: str,
) -> Dict[str, List[str]]:
    """
    Deterministically build full 5-tense conjugation tables in Python from compact stems
    so Gemini never has to output verbatim Bescherelle tables (preventing any recitation block!).
    """
    inf = (infinitive or "").strip().lower()
    is_pronominal = inf.startswith("se ") or inf.startswith("s'")
    base_inf = inf[3:].strip() if inf.startswith("se ") else (inf[2:].strip() if inf.startswith("s'") else inf)

    # Fallback regular stems if not provided
    if not present_6 or len(present_6) < 6:
        if base_inf.endswith("er"):
            st = base_inf[:-2]
            present_6 = [f"{st}e", f"{st}es", f"{st}e", f"{st}ons", f"{st}ez", f"{st}ent"]
        elif base_inf.endswith("ir"):
            st = base_inf[:-2]
            present_6 = [f"{st}is", f"{st}is", f"{st}it", f"{st}issons", f"{st}issez", f"{st}issent"]
        elif base_inf.endswith("re"):
            st = base_inf[:-2]
            present_6 = [f"{st}s", f"{st}s", f"{st}", f"{st}ons", f"{st}ez", f"{st}ent"]
        else:
            st = base_inf
            present_6 = [st, st, st, f"{st}ons", f"{st}ez", f"{st}ent"]

    if not imparfait_stem:
        nous_form = present_6[3]
        imparfait_stem = nous_form[:-3] if nous_form.endswith("ons") else base_inf[:-2]

    if not futur_stem:
        futur_stem = base_inf[:-1] if base_inf.endswith("re") else base_inf

    pp = (past_participle or "").strip() or (
        f"{base_inf[:-2]}é" if base_inf.endswith("er") else f"{base_inf[:-2]}i"
    )
    aux = "être" if is_pronominal else ((auxiliary or "avoir").strip().lower())

    if is_pronominal:
        refl_v = ["me ", "te ", "se ", "nous ", "vous ", "se "]
        refl_el = ["m'", "t'", "s'", "nous ", "vous ", "s'"]
        subjects = ["je ", "tu ", "il/elle ", "nous ", "vous ", "ils/elles "]

        def _fmt_pron(idx: int, vform: str) -> str:
            r = refl_el[idx] if _starts_with_vowel(vform) else refl_v[idx]
            return f"{subjects[idx]}{r}{vform}"

        present_lines = [_fmt_pron(i, present_6[i]) for i in range(6)]
        imp_endings = ["ais", "ais", "ait", "ions", "iez", "aient"]
        imparfait_lines = [_fmt_pron(i, f"{imparfait_stem}{imp_endings[i]}") for i in range(6)]
        fut_endings = ["ai", "as", "a", "ons", "ez", "ont"]
        futur_lines = [_fmt_pron(i, f"{futur_stem}{fut_endings[i]}") for i in range(6)]
        cond_lines = [_fmt_pron(i, f"{futur_stem}{imp_endings[i]}") for i in range(6)]
        pc_lines = [
            f"je me suis {pp}(e)",
            f"tu t'es {pp}(e)",
            f"il/elle s'est {pp}(e)",
            f"nous nous sommes {pp}(e)s",
            f"vous vous êtes {pp}(e)s",
            f"ils/elles se sont {pp}(e)s",
        ]
    else:
        subjects_other = ["tu", "il/elle", "nous", "vous", "ils/elles"]
        present_lines = [_je_prefix(present_6[0])] + [f"{subjects_other[i-1]} {present_6[i]}" for i in range(1, 6)]

        imp_endings = ["ais", "ais", "ait", "ions", "iez", "aient"]
        imp_forms = [f"{imparfait_stem}{e}" for e in imp_endings]
        imparfait_lines = [_je_prefix(imp_forms[0])] + [f"{subjects_other[i-1]} {imp_forms[i]}" for i in range(1, 6)]

        fut_endings = ["ai", "as", "a", "ons", "ez", "ont"]
        fut_forms = [f"{futur_stem}{e}" for e in fut_endings]
        futur_lines = [_je_prefix(fut_forms[0])] + [f"{subjects_other[i-1]} {fut_forms[i]}" for i in range(1, 6)]

        cond_forms = [f"{futur_stem}{e}" for e in imp_endings]
        cond_lines = [_je_prefix(cond_forms[0])] + [f"{subjects_other[i-1]} {cond_forms[i]}" for i in range(1, 6)]

        if aux == "être":
            pc_lines = [
                f"je suis {pp}(e)",
                f"tu es {pp}(e)",
                f"il/elle est {pp}(e)",
                f"nous sommes {pp}(e)s",
                f"vous êtes {pp}(e)s",
                f"ils/elles sont {pp}(e)s",
            ]
        else:
            pc_lines = [
                f"j'ai {pp}",
                f"tu as {pp}",
                f"il/elle a {pp}",
                f"nous avons {pp}",
                f"vous avez {pp}",
                f"ils/elles ont {pp}",
            ]

    return {
        "Présent": present_lines,
        "Passé Composé": pc_lines,
        "Imparfait": imparfait_lines,
        "Futur Simple": futur_lines,
        "Conditionnel": cond_lines,
    }


def lookup_word_smart_dictionary(client, word: str, context_sentence: str = "") -> Dict[str, Any]:
    """
    Look up any right-clicked word in French: returns English translation, part of speech,
    multiple forms (full conjugation table if verb, or gender/plural forms if noun/adjective),
    and 2 everyday example sentences.
    Uses compact stem extraction + Python conjugation to avoid any Gemini recitation blocks.
    """
    clean_word = word.strip(" .,!?;:\"'()[]{}«»").lower()
    if not clean_word:
        raise ValueError("No word selected")

    # 1. Check if it matches any form of our 20 pre-loaded daily verbs first (0ms!)
    matched_verb = _match_common_verb_any_form(clean_word)
    if matched_verb:
        return {
            "word": word,
            "lemma": matched_verb["verb"],
            "part_of_speech": f"Verbe ({matched_verb['category']}) — Auxiliaire {matched_verb['auxiliary']}",
            "english_meaning": matched_verb["en"],
            "grammar_tip": matched_verb["tip"],
            "is_verb": True,
            "forms": {
                "infinitive": matched_verb["verb"],
                "auxiliary": matched_verb["auxiliary"],
                "past_participle": matched_verb["past_participle"],
                "tenses": {
                    "Présent": matched_verb["tenses"]["Présent"],
                    "Passé Composé": matched_verb["tenses"]["Passé Composé"],
                    "Imparfait": matched_verb["tenses"]["Imparfait"],
                    "Futur Simple": matched_verb["tenses"]["Futur Simple"],
                    "Conditionnel": matched_verb["tenses"]["Conditionnel"],
                },
            },
            "examples": matched_verb["examples"],
        }

    # 2. Check local dictionary cache
    cache = _load_dict_cache()
    if clean_word in cache:
        return cache[clean_word]

    # 3. Query Gemini for compact metadata + stems (never full 30-line tables, avoiding recitation!)
    system_instruction = (
        "You are an original French-English tutor creating a custom flashcard for Balu, who lives in Geneva "
        "with his wife Lakshmi and 12-year-old son. "
        "Given a clicked French word and its sentence context, return ONLY a valid JSON object with this schema:\n"
        "{\n"
        '  "word": "<clicked word>",\n'
        '  "lemma": "<infinitive if verb, masculine singular if noun/adjective>",\n'
        '  "part_of_speech": "<Verbe, Nom masculin, Nom féminin, Adjectif, Adverbe, Préposition, etc.>",\n'
        '  "english_meaning": "<English translation and meaning in this context>",\n'
        '  "grammar_tip": "<1 short original tip for a student in Geneva>",\n'
        '  "is_verb": <true if verb/conjugated verb/participle, else false>,\n'
        '  "verb_info": {\n'
        '    "infinitive": "<French infinitive>",\n'
        '    "auxiliary": "<avoir or être>",\n'
        '    "past_participle": "<past participle without auxiliary>",\n'
        '    "present_6": ["<1sg verb form without pronoun>", "<2sg>", "<3sg>", "<1pl>", "<2pl>", "<3pl>"],\n'
        '    "imparfait_stem": "<stem before -ais, e.g. parl, finiss, pren>",\n'
        '    "futur_stem": "<stem before -ai, e.g. parler, finir, prendr>"\n'
        '  },\n'
        '  "noun_adj_forms": {\n'
        '    "masculine_singular": "<masc sg form>",\n'
        '    "feminine_singular": "<fem sg form>",\n'
        '    "plural": "<plural form>",\n'
        '    "related_family": ["<related word 1>", "<related word 2>"]\n'
        '  },\n'
        '  "examples": [\n'
        '    {"fr": "<original French sentence set in Geneva using the word>", "en": "<English translation>"},\n'
        '    {"fr": "<second original French sentence about daily family/work life>", "en": "<English translation>"}\n'
        '  ]\n'
        "}"
    )

    user_input = f"Word: {word}\nContext: {context_sentence or 'General daily French'}\nReturn ONLY the JSON."
    interaction = client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=system_instruction,
        input=user_input,
        generation_config={"thinking_level": "minimal"},
        store=False,
    )
    raw_data = _parse_json(_extract_text(interaction))

    is_verb = bool(raw_data.get("is_verb", False))
    if is_verb:
        vinfo = raw_data.get("verb_info") or {}
        inf = vinfo.get("infinitive") or raw_data.get("lemma") or clean_word
        # If the lemma itself matches one of our 20 daily verbs, use its rich table!
        matched_by_lemma = _match_common_verb_any_form(inf.strip().lower())
        if matched_by_lemma:
            tenses_dict = {
                "Présent": matched_by_lemma["tenses"]["Présent"],
                "Passé Composé": matched_by_lemma["tenses"]["Passé Composé"],
                "Imparfait": matched_by_lemma["tenses"]["Imparfait"],
                "Futur Simple": matched_by_lemma["tenses"]["Futur Simple"],
                "Conditionnel": matched_by_lemma["tenses"]["Conditionnel"],
            }
            aux = matched_by_lemma["auxiliary"]
            pp = matched_by_lemma["past_participle"]
        else:
            aux = vinfo.get("auxiliary", "avoir")
            pp = vinfo.get("past_participle", "")
            tenses_dict = _build_5_tenses_in_python(
                infinitive=inf,
                auxiliary=aux,
                past_participle=pp,
                present_6=vinfo.get("present_6") or [],
                imparfait_stem=vinfo.get("imparfait_stem") or "",
                futur_stem=vinfo.get("futur_stem") or "",
            )
        forms_out = {
            "infinitive": inf,
            "auxiliary": aux,
            "past_participle": pp,
            "tenses": tenses_dict,
        }
    else:
        forms_out = raw_data.get("noun_adj_forms") or {
            "masculine_singular": raw_data.get("lemma", word),
            "feminine_singular": "",
            "plural": "",
            "related_family": [],
        }

    result = {
        "word": raw_data.get("word", word),
        "lemma": raw_data.get("lemma", word),
        "part_of_speech": raw_data.get("part_of_speech", "Mot"),
        "english_meaning": raw_data.get("english_meaning", ""),
        "grammar_tip": raw_data.get("grammar_tip", ""),
        "is_verb": is_verb,
        "forms": forms_out,
        "examples": raw_data.get("examples") or [],
    }
    cache[clean_word] = result
    _save_dict_cache(cache)
    return result


def conjugate_any_verb_with_gemini(client, verb_query: str) -> Dict[str, Any]:
    """
    Conjugate any custom French verb searched on the Verb Conjugation page using compact stem extraction
    + deterministic Python table construction (zero recitation risk).
    """
    clean_v = verb_query.strip().lower()
    matched = _match_common_verb_any_form(clean_v)
    if matched:
        return matched

    system_instruction = (
        "You are a French grammar assistant. Given a verb query (in French or English), identify the French "
        "infinitive and its conjugation stems, and write 2 original example sentences set in Geneva. "
        "Return ONLY a valid JSON object with this schema:\n"
        "{\n"
        '  "verb": "<French infinitive>",\n'
        '  "en": "<English meaning>",\n'
        '  "auxiliary": "<avoir or être>",\n'
        '  "past_participle": "<past participle>",\n'
        '  "tip": "<1 helpful tip about this verb>",\n'
        '  "present_6": ["<1sg verb form without pronoun>", "<2sg>", "<3sg>", "<1pl>", "<2pl>", "<3pl>"],\n'
        '  "imparfait_stem": "<stem before -ais>",\n'
        '  "futur_stem": "<stem before -ai>",\n'
        '  "imperative_subj": ["<Imperative forms>", "<Subjunctive que je ...>"],\n'
        '  "examples": [\n'
        '    {"fr": "<original French example in Geneva>", "en": "<English translation>"},\n'
        '    {"fr": "<second original French example>", "en": "<English translation>"}\n'
        '  ]\n'
        "}"
    )

    interaction = client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=system_instruction,
        input=f"Verb: {verb_query}",
        generation_config={"thinking_level": "minimal"},
        store=False,
    )
    raw = _parse_json(_extract_text(interaction))
    inf = raw.get("verb", verb_query)
    aux = raw.get("auxiliary", "avoir")
    pp = raw.get("past_participle", "")
    tenses = _build_5_tenses_in_python(
        infinitive=inf,
        auxiliary=aux,
        past_participle=pp,
        present_6=raw.get("present_6") or [],
        imparfait_stem=raw.get("imparfait_stem") or "",
        futur_stem=raw.get("futur_stem") or "",
    )
    tenses["Impératif / Subjonctif"] = raw.get("imperative_subj") or [f"que je {raw.get('present_6', [''])[0]}"]

    return {
        "verb": inf,
        "en": raw.get("en", ""),
        "category": "custom",
        "emoji": "⚡",
        "auxiliary": aux,
        "past_participle": pp,
        "tip": raw.get("tip", ""),
        "tenses": tenses,
        "examples": raw.get("examples") or [],
    }
