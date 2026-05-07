from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz.models import Question, QuestionChoice
import random

QUESTIONS = [
    {
        'title': "Je m'ouvre davantage au désir quand\u2026",
        'choices': [
            {"label": "l'\u00e9change est intelligent et stimulant", "mental": 1},
            {"label": "je me sens choisi(e), reconnu(e), profond\u00e9ment touch\u00e9(e)", "emotionnel": 1},
            {"label": "je sens une connexion subtile, une synchronisation", "energetique": 1},
            {"label": "l'ambiance, les sensations et la lenteur m'enveloppent", "sensoriel": 1},
            {"label": "le contact, le mouvement, l'\u00e9lan corporel commencent vite", "physique": 1},
        ]
    },
    {
        'title': "Ce qui me met le plus en mouvement, c'est\u2026",
        'choices': [
            {"label": "les mots, sc\u00e9narios, id\u00e9es, jeux d'esprit", "mental": 1},
            {"label": "l'admiration, la s\u00e9curit\u00e9 affective, la vuln\u00e9rabilit\u00e9", "emotionnel": 1},
            {"label": "la pr\u00e9sence, le silence juste, l'intuition", "energetique": 1},
            {"label": "les textures, odeurs, voix, regard, peau", "sensoriel": 1},
            {"label": "l'action, l'excitation, l'initiative corporelle", "physique": 1},
        ]
    },
    {
        'title': "Quand je manque de ce qui me nourrit, je me ferme surtout parce que\u2026",
        'choices': [
            {"label": "je m'ennuie ou je ne vois pas le sens", "mental": 1},
            {"label": "je me sens invisible ou peu important(e)", "emotionnel": 1},
            {"label": "je ne \u00ab sens \u00bb plus la connexion", "energetique": 1},
            {"label": "je ne ressens plus de plaisir fin ou de pr\u00e9sence", "sensoriel": 1},
            {"label": "je ne me sens pas suffisamment stimul\u00e9(e) physiquement", "physique": 1},
        ]
    },
    {
        'title': "Le compliment ou le geste qui me touche le plus est\u2026",
        'choices': [
            {"label": "\"j'aime ta fa\u00e7on de penser / parler\"", "mental": 1},
            {"label": "\"je te vois / je te choisis / tu comptes pour moi\"", "emotionnel": 1},
            {"label": "\"je me sens reli\u00e9(e) \u00e0 toi sans effort\"", "energetique": 1},
            {"label": "\"ta voix / ton parfum / ta peau m'attirent\"", "sensoriel": 1},
            {"label": "\"j'ai envie de te toucher / te prendre dans mes bras\"", "physique": 1},
        ]
    },
    {
        'title': "Quand l'intimit\u00e9 est bonne, j'ai surtout besoin de\u2026",
        'choices': [
            {"label": "curiosit\u00e9, jeu, imagination", "mental": 1},
            {"label": "chaleur, validation, profondeur", "emotionnel": 1},
            {"label": "fluidit\u00e9, accord, ressenti partag\u00e9", "energetique": 1},
            {"label": "lenteur, pr\u00e9sence aux sensations", "sensoriel": 1},
            {"label": "intensit\u00e9, contact, engagement du corps", "physique": 1},
        ]
    },
    {
        'title': "Si quelqu'un veut m'approcher, je suis le plus r\u00e9ceptif(ve) quand il/elle\u2026",
        'choices': [
            {"label": "m'\u00e9veille par les mots", "mental": 1},
            {"label": "m'ouvre par l'attention \u00e9motionnelle", "emotionnel": 1},
            {"label": "se r\u00e8gle sur mon rythme int\u00e9rieur", "energetique": 1},
            {"label": "soigne l'atmosph\u00e8re et les sensations", "sensoriel": 1},
            {"label": "passe \u00e0 l'action avec nettet\u00e9", "physique": 1},
        ]
    },
    {
        'title': "Ce qui me donne le plus envie de dire oui, c'est\u2026",
        'choices': [
            {"label": "une proposition stimulante et imaginative", "mental": 1},
            {"label": "un sentiment de s\u00e9curit\u00e9 et de reconnaissance", "emotionnel": 1},
            {"label": "une impression de \"juste synchro\"", "energetique": 1},
            {"label": "une mont\u00e9e progressive des sens", "sensoriel": 1},
            {"label": "une pr\u00e9sence physique directe et assum\u00e9e", "physique": 1},
        ]
    },
    {
        'title': "Dans un moment id\u00e9al, je remarque d'abord\u2026",
        'choices': [
            {"label": "les id\u00e9es, les mots, le sc\u00e9nario", "mental": 1},
            {"label": "les \u00e9motions, le lien, la valeur que j'ai", "emotionnel": 1},
            {"label": "l'atmosph\u00e8re, la r\u00e9sonance, la vibration", "energetique": 1},
            {"label": "les sensations fines du corps", "sensoriel": 1},
            {"label": "l'excitation, la chaleur, le mouvement", "physique": 1},
        ]
    },
    {
        'title': "Ce qui me coupe le plus vite du d\u00e9sir, c'est\u2026",
        'choices': [
            {"label": "la banalit\u00e9, l'absence de stimulation mentale", "mental": 1},
            {"label": "le sentiment de ne pas \u00eatre vu(e)", "emotionnel": 1},
            {"label": "le d\u00e9calage de rythme ou de pr\u00e9sence", "energetique": 1},
            {"label": "la brutalit\u00e9, le manque de finesse", "sensoriel": 1},
            {"label": "la retenue excessive ou l'absence d'\u00e9lan corporel", "physique": 1},
        ]
    },
    {
        'title': "Si je devais choisir la porte d'entr\u00e9e la plus naturelle, ce serait\u2026",
        'choices': [
            {"label": "la t\u00eate d'abord", "mental": 1},
            {"label": "le c\u0153ur d'abord", "emotionnel": 1},
            {"label": "la connexion d'abord", "energetique": 1},
            {"label": "les sens d'abord", "sensoriel": 1},
            {"label": "le corps d'abord", "physique": 1},
        ]
    },
]


class Command(BaseCommand):
    help = 'Configure toute l app : superuser + questions'

    def handle(self, *args, **options):
        # 1. Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'andrianinarabary3@gmail.com', 'PortesDesir2024!')
            self.stdout.write(self.style.SUCCESS('Superuser admin cree'))
        else:
            self.stdout.write('Superuser admin existe deja')

        # 2. Questions
        Question.objects.all().delete()
        for i, q_data in enumerate(QUESTIONS, start=1):
            question = Question.objects.create(
                title=q_data['title'], text='', question_type='single', order=i, is_active=True,
            )
            choices = q_data['choices'][:]
            random.shuffle(choices)
            for j, c in enumerate(choices, start=1):
                QuestionChoice.objects.create(
                    question=question, label=c['label'],
                    score_mental=c.get('mental', 0),
                    score_emotionnel=c.get('emotionnel', 0),
                    score_energetique=c.get('energetique', 0),
                    score_sensoriel=c.get('sensoriel', 0),
                    score_physique=c.get('physique', 0),
                    order=j,
                )
            self.stdout.write(f'  Question {i} OK')

        self.stdout.write(self.style.SUCCESS('Setup complet !'))
