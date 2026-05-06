from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

RESULT_CONTENT = {
    'mental': {
        'label': 'Porte Mentale',
        'emoji': '🧠',
        'title': "Quand le désir s'ouvre par l'esprit",
        'subtitle': "Votre porte dominante actuelle semble être la porte Mentale",
        'description': (
            "Pour vous, l'intimité commence bien avant le corps : elle naît quand le mental se sent "
            "intrigué, compris, stimulé. Vous vous activez par les mots, les descriptions, les scénarios, "
            "l'imaginaire. Ce besoin n'est pas une complication : c'est une porte de sécurité qui permet "
            "de s'ouvrir sans forcer."
        ),
        'besoins': "Comprendre avant de se livrer, sentir une intention claire, jouer avec l'imaginaire, se sentir relié(e) par la pensée et le langage.",
        'conseil': "Parlez avec précision et délicatesse. Le cadre clair vous sécurise et vous permet de vous ouvrir pleinement.",
        'phrase': "Je veux comprendre avant d'avancer.",
        'couleur': '#6b7dbf',
    },
    'emotionnel': {
        'label': 'Porte Émotionnelle',
        'emoji': '💛',
        'title': "Quand le désir naît d'un sentiment",
        'subtitle': "Votre porte dominante actuelle semble être la porte Émotionnelle",
        'description': (
            "Pour vous, le désir durable ne dépend pas d'un geste, mais de l'émotion que ce geste active. "
            "Vous avez besoin de vous sentir vu(e), choisi(e), reconnu(e). Quand ce besoin est nourri, "
            "l'émotion partagée devient un vrai facteur d'intimité profonde."
        ),
        'besoins': "Être vu(e) et reconnu(e), recevoir de l'admiration et de la tendresse, pouvoir être vulnérable sans se fermer, sentir que le lien compte vraiment.",
        'conseil': "Commencez par le lien avant toute invitation intime. La sécurité affective est votre clé d'ouverture.",
        'phrase': "J'ai besoin de me sentir relié(e).",
        'couleur': '#bf6b7d',
    },
    'energetique': {
        'label': 'Porte Énergétique',
        'emoji': '✨',
        'title': "Quand l'intimité devient connexion subtile",
        'subtitle': "Votre porte dominante actuelle semble être la porte Énergétique",
        'description': (
            "Vous entrez dans l'intimité par une connexion profonde, subtile, silencieuse. Vous ressentez "
            "l'énergie de l'autre, anticipez ses besoins, vous synchronisez dans une même pulsation. "
            "La présence, la respiration et l'intuition comptent plus que les mots."
        ),
        'besoins': "Sentir une présence vraie, vivre une synchronisation profonde, percevoir l'autre au-delà des mots.",
        'conseil': "Prenez un temps de présence partagée. Posez une intention, respirez ensemble, laissez la connexion se construire sans accélérer.",
        'phrase': "Je sens une connexion qui dépasse les mots.",
        'couleur': '#7dbf6b',
    },
    'sensoriel': {
        'label': 'Porte Sensorielle',
        'emoji': '🌿',
        'title': "Quand le plaisir se savoure avec présence",
        'subtitle': "Votre porte dominante actuelle semble être la porte Sensorielle",
        'description': (
            "Vous entrez dans le désir par les sens : la lenteur, l'ambiance, les textures, les odeurs, "
            "la voix. Le plaisir n'est pas un résultat mais une expérience à savourer. Vous aimez "
            "les micro-sensations et avez besoin d'une présence fine et attentive."
        ),
        'besoins': "Le plaisir de sentir, une présence au corps, de la curiosité sans pression, un espace sécurisant d'exploration.",
        'conseil': "Ralentissez. Goûtez chaque sensation. Variez les textures et les rythmes. Nommez ce qui est ressenti.",
        'phrase': "J'ai besoin de douceur, de nuances, de lenteur.",
        'couleur': '#bf9b6b',
    },
    'physique': {
        'label': 'Porte Physique',
        'emoji': '🔥',
        'title': "Quand le corps devient la voie directe du désir",
        'subtitle': "Votre porte dominante actuelle semble être la porte Physique",
        'description': (
            "Votre désir s'ouvre par le corps : l'excitation, le mouvement, l'action, la puissance incarnée. "
            "Vous lisez les signaux corporels de l'autre avec finesse et aimez une approche directe et assumée. "
            "Le corps est votre intelligence première."
        ),
        'besoins': "Sentir le corps vivant et présent, agir, bouger, explorer, vivre une intensité incarnée et ajustée.",
        'conseil': "Restez à l'écoute du rythme et des signaux de l'autre. L'intensité modulée est plus juste qu'une initiative trop directe.",
        'phrase': "Mon corps s'allume d'abord.",
        'couleur': '#bf6b6b',
    },
}


def compute_result(session):
    scores = {
        'mental': 0, 'emotionnel': 0,
        'energetique': 0, 'sensoriel': 0, 'physique': 0,
    }
    for answer in session.answers.select_related('choice').all():
        if answer.choice:
            scores['mental'] += answer.choice.score_mental
            scores['emotionnel'] += answer.choice.score_emotionnel
            scores['energetique'] += answer.choice.score_energetique
            scores['sensoriel'] += answer.choice.score_sensoriel
            scores['physique'] += answer.choice.score_physique

    session.total_score_mental = scores['mental']
    session.total_score_emotionnel = scores['emotionnel']
    session.total_score_energetique = scores['energetique']
    session.total_score_sensoriel = scores['sensoriel']
    session.total_score_physique = scores['physique']

    best_code = max(scores, key=scores.get)
    session.result_code = best_code
    session.result_label = RESULT_CONTENT[best_code]['label']
    session.completed_at = timezone.now()
    session.save()

    return RESULT_CONTENT[best_code]


def _pct(score, total):
    return round(score * 100 / total) if total > 0 else 0


def send_result_email(session, result_data):
    participant_email = session.participant.email
    admin_email = getattr(settings, 'ADMIN_RESULT_EMAIL', '')

    total = (session.total_score_mental + session.total_score_emotionnel +
             session.total_score_energetique + session.total_score_sensoriel +
             session.total_score_physique) or 1

    ctx = {
        'result_code': session.result_code,
        'result_label': result_data['label'],
        'result_title': result_data['title'],
        'result_description': result_data['description'],
        'result_phrase': result_data.get('phrase', ''),
        'score_mental': session.total_score_mental,
        'score_emotionnel': session.total_score_emotionnel,
        'score_energetique': session.total_score_energetique,
        'score_sensoriel': session.total_score_sensoriel,
        'score_physique': session.total_score_physique,
        'mental_pct': _pct(session.total_score_mental, total),
        'emotionnel_pct': _pct(session.total_score_emotionnel, total),
        'energetique_pct': _pct(session.total_score_energetique, total),
        'sensoriel_pct': _pct(session.total_score_sensoriel, total),
        'physique_pct': _pct(session.total_score_physique, total),
        'participant_email': participant_email,
        'result_data': result_data,
    }

    subject = "Votre résultat — " + result_data['label']

    text_body = "\n".join([
        "Bonjour,",
        "",
        "Merci d'avoir complété le test Les Portes du Désir.",
        "",
        "Votre résultat : " + result_data['label'],
        result_data['title'],
        "",
        result_data['description'],
        "",
        "Phrase clé : " + result_data.get('phrase', ''),
        "",
        "À bientôt.",
    ])

    html_body = render_to_string('quiz/email_result.html', ctx)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[participant_email],
        bcc=[admin_email] if admin_email else [],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)
