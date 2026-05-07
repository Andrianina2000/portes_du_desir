from django.core.management.base import BaseCommand
from quiz.models import Question, QuestionChoice

QUESTIONS = [
    {
        'title': "Je m'ouvre davantage au désir quand…",
        'choices': [
            {"label": "l'échange est intelligent et stimulant", "mental": 1},
            {"label": "je me sens choisi(e), reconnu(e), profondément touché(e)", "emotionnel": 1},
            {"label": "je sens une connexion subtile, une synchronisation", "energetique": 1},
            {"label": "l'ambiance, les sensations et la lenteur m'enveloppent", "sensoriel": 1},
            {"label": "le contact, le mouvement, l'élan corporel commencent vite", "physique": 1},
        ]
    },
    {
        'title': "Ce qui me met le plus en mouvement, c'est…",
        'choices': [
            {"label": "les mots, scénarios, idées, jeux d'esprit", "mental": 1},
            {"label": "l'admiration, la sécurité affective, la vulnérabilité", "emotionnel": 1},
            {"label": "la présence, le silence juste, l'intuition", "energetique": 1},
            {"label": "les textures, odeurs, voix, regard, peau", "sensoriel": 1},
            {"label": "l'action, l'excitation, l'initiative corporelle", "physique": 1},
        ]
    },
    {
        'title': "Quand je manque de ce qui me nourrit, je me ferme surtout parce que…",
        'choices': [
            {"label": "je m'ennuie ou je ne vois pas le sens", "mental": 1},
            {"label": "je me sens invisible ou peu important(e)", "emotionnel": 1},
            {"label": "je ne « sens » plus la connexion", "energetique": 1},
            {"label": "je ne ressens plus de plaisir fin ou de présence", "sensoriel": 1},
            {"label": "je ne me sens pas suffisamment stimulé(e) physiquement", "physique": 1},
        ]
    },
    {
        'title': "Le compliment ou le geste qui me touche le plus est…",
        'choices': [
            {"label": "\"j'aime ta façon de penser / parler\"", "mental": 1},
            {"label": "\"je te vois / je te choisis / tu comptes pour moi\"", "emotionnel": 1},
            {"label": "\"je me sens relié(e) à toi sans effort\"", "energetique": 1},
            {"label": "\"ta voix / ton parfum / ta peau m'attirent\"", "sensoriel": 1},
            {"label": "\"j'ai envie de te toucher / te prendre dans mes bras\"", "physique": 1},
        ]
    },
    {
        'title': "Quand l'intimité est bonne, j'ai surtout besoin de…",
        'choices': [
            {"label": "curiosité, jeu, imagination", "mental": 1},
            {"label": "chaleur, validation, profondeur", "emotionnel": 1},
            {"label": "fluidité, accord, ressenti partagé", "energetique": 1},
            {"label": "lenteur, présence aux sensations", "sensoriel": 1},
            {"label": "intensité, contact, engagement du corps", "physique": 1},
        ]
    },
    {
        'title': "Si quelqu'un veut m'approcher, je suis le plus réceptif(ve) quand il/elle…",
        'choices': [
            {"label": "m'éveille par les mots", "mental": 1},
            {"label": "m'ouvre par l'attention émotionnelle", "emotionnel": 1},
            {"label": "se règle sur mon rythme intérieur", "energetique": 1},
            {"label": "soigne l'atmosphère et les sensations", "sensoriel": 1},
            {"label": "passe à l'action avec netteté", "physique": 1},
        ]
    },
    {
        'title': "Ce qui me donne le plus envie de dire oui, c'est…",
        'choices': [
            {"label": "une proposition stimulante et imaginative", "mental": 1},
            {"label": "un sentiment de sécurité et de reconnaissance", "emotionnel": 1},
            {"label": "une impression de \"juste synchro\"", "energetique": 1},
            {"label": "une montée progressive des sens", "sensoriel": 1},
            {"label": "une présence physique directe et assumée", "physique": 1},
        ]
    },
    {
        'title': "Dans un moment idéal, je remarque d'abord…",
        'choices': [
            {"label": "les idées, les mots, le scénario", "mental": 1},
            {"label": "les émotions, le lien, la valeur que j'ai", "emotionnel": 1},
            {"label": "l'atmosphère, la résonance, la vibration", "energetique": 1},
            {"label": "les sensations fines du corps", "sensoriel": 1},
            {"label": "l'excitation, la chaleur, le mouvement", "physique": 1},
        ]
    },
    {
        'title': "Ce qui me coupe le plus vite du désir, c'est…",
        'choices': [
            {"label": "la banalité, l'absence de stimulation mentale", "mental": 1},
            {"label": "le sentiment de ne pas être vu(e)", "emotionnel": 1},
            {"label": "le décalage de rythme ou de présence", "energetique": 1},
            {"label": "la brutalité, le manque de finesse", "sensoriel": 1},
            {"label": "la retenue excessive ou l'absence d'élan corporel", "physique": 1},
        ]
    },
    {
        'title': "Si je devais choisir la porte d'entrée la plus naturelle, ce serait…",
        'choices': [
            {"label": "la tête d'abord", "mental": 1},
            {"label": "le cœur d'abord", "emotionnel": 1},
            {"label": "la connexion d'abord", "energetique": 1},
            {"label": "les sens d'abord", "sensoriel": 1},
            {"label": "le corps d'abord", "physique": 1},
        ]
    },
]


class Command(BaseCommand):
    help = 'Charge les 10 questions des Portes du Desir'

    def handle(self, *args, **options):
        Question.objects.all().delete()
        self.stdout.write('Questions existantes supprimées.')

        import random
        for i, q_data in enumerate(QUESTIONS, start=1):
            question = Question.objects.create(
                title=q_data['title'],
                text='',
                question_type='single',
                order=i,
                is_active=True,
            )
            choices = q_data['choices']
            random.shuffle(choices)  # Mélange aléatoire pour éviter les biais
            for j, c in enumerate(choices, start=1):
                QuestionChoice.objects.create(
                    question=question,
                    label=c['label'],
                    score_mental=c.get('mental', 0),
                    score_emotionnel=c.get('emotionnel', 0),
                    score_energetique=c.get('energetique', 0),
                    score_sensoriel=c.get('sensoriel', 0),
                    score_physique=c.get('physique', 0),
                    order=j,
                )
            self.stdout.write(f'  ✓ Question {i}: {q_data["title"][:50]}')

        self.stdout.write(self.style.SUCCESS(f'\n10 questions chargées avec succès !'))
