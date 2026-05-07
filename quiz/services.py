import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

RESULT_CONTENT = {
    'mental': {
        'label': 'Porte Mentale',
        'emoji': '\U0001f9e0',
        'title': "Quand le desir s'ouvre par l'esprit",
        'subtitle': "Votre porte dominante actuelle semble etre la porte Mentale",
        'description': (
            "Pour vous, l'intimite commence bien avant le corps : elle nait quand le mental se sent "
            "intrigue, compris, stimule. Vous vous activez par les mots, les descriptions, les scenarios, "
            "l'imaginaire. Ce besoin n'est pas une complication : c'est une porte de securite qui permet "
            "de s'ouvrir sans forcer."
        ),
        'besoins': "Comprendre avant de se livrer, sentir une intention claire, jouer avec l'imaginaire, se sentir relie(e) par la pensee et le langage.",
        'conseil': "Parlez avec precision et delicatesse. Le cadre clair vous securise et vous permet de vous ouvrir pleinement.",
        'phrase': "Je veux comprendre avant d'avancer.",
        'couleur': '#6b7dbf',
    },
    'emotionnel': {
        'label': 'Porte Emotionnelle',
        'emoji': '\U0001f49b',
        'title': "Quand le desir nait d'un sentiment",
        'subtitle': "Votre porte dominante actuelle semble etre la porte Emotionnelle",
        'description': (
            "Pour vous, le desir durable ne depend pas d'un geste, mais de l'emotion que ce geste active. "
            "Vous avez besoin de vous sentir vu(e), choisi(e), reconnu(e). Quand ce besoin est nourri, "
            "l'emotion partagee devient un vrai facteur d'intimite profonde."
        ),
        'besoins': "Etre vu(e) et reconnu(e), recevoir de l'admiration et de la tendresse, pouvoir etre vulnerable sans se fermer, sentir que le lien compte vraiment.",
        'conseil': "Commencez par le lien avant toute invitation intime. La securite affective est votre cle d'ouverture.",
        'phrase': "J'ai besoin de me sentir relie(e).",
        'couleur': '#bf6b7d',
    },
    'energetique': {
        'label': 'Porte Energetique',
        'emoji': '\u2728',
        'title': "Quand l'intimite devient connexion subtile",
        'subtitle': "Votre porte dominante actuelle semble etre la porte Energetique",
        'description': (
            "Vous entrez dans l'intimite par une connexion profonde, subtile, silencieuse. Vous ressentez "
            "l'energie de l'autre, anticipez ses besoins, vous synchronisez dans une meme pulsation. "
            "La presence, la respiration et l'intuition comptent plus que les mots."
        ),
        'besoins': "Sentir une presence vraie, vivre une synchronisation profonde, percevoir l'autre au-dela des mots.",
        'conseil': "Prenez un temps de presence partagee. Posez une intention, respirez ensemble, laissez la connexion se construire sans accelerer.",
        'phrase': "Je sens une connexion qui depasse les mots.",
        'couleur': '#7dbf6b',
    },
    'sensoriel': {
        'label': 'Porte Sensorielle',
        'emoji': '\U0001f33f',
        'title': "Quand le plaisir se savoure avec presence",
        'subtitle': "Votre porte dominante actuelle semble etre la porte Sensorielle",
        'description': (
            "Vous entrez dans le desir par les sens : la lenteur, l'ambiance, les textures, les odeurs, "
            "la voix. Le plaisir n'est pas un resultat mais une experience a savourer. Vous aimez "
            "les micro-sensations et avez besoin d'une presence fine et attentive."
        ),
        'besoins': "Le plaisir de sentir, une presence au corps, de la curiosite sans pression, un espace securisant d'exploration.",
        'conseil': "Ralentissez. Goutez chaque sensation. Variez les textures et les rythmes. Nommez ce qui est ressenti.",
        'phrase': "J'ai besoin de douceur, de nuances, de lenteur.",
        'couleur': '#bf9b6b',
    },
    'physique': {
        'label': 'Porte Physique',
        'emoji': '\U0001f525',
        'title': "Quand le corps devient la voie directe du desir",
        'subtitle': "Votre porte dominante actuelle semble etre la porte Physique",
        'description': (
            "Votre desir s'ouvre par le corps : l'excitation, le mouvement, l'action, la puissance incarnee. "
            "Vous lisez les signaux corporels de l'autre avec finesse et aimez une approche directe et assumee. "
            "Le corps est votre intelligence premiere."
        ),
        'besoins': "Sentir le corps vivant et present, agir, bouger, explorer, vivre une intensite incarnee et ajustee.",
        'conseil': "Restez a l'ecoute du rythme et des signaux de l'autre. L'intensite modulee est plus juste qu'une initiative trop directe.",
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
    # Si EMAIL_HOST_USER n'est pas configure, on skippe silencieusement
    email_user = os.environ.get('EMAIL_HOST_USER', '').strip()
    if not email_user:
        return

    participant_email = session.participant.email
    admin_email = getattr(settings, 'ADMIN_RESULT_EMAIL', '')

    total = (session.total_score_mental + session.total_score_emotionnel +
             session.total_score_energetique + session.total_score_sensoriel +
             session.total_score_physique) or 1

    # URL absolue de l'illustration selon la porte
    illustration_map = {
        'mental':      'porte_mental.png',
        'emotionnel':  'porte_emotionnel.png',
        'energetique': 'porte_energetique.png',
        'sensoriel':   'porte_sensoriel.png',
        'physique':    'porte_physique.png',
    }
    illustration_file = illustration_map.get(session.result_code, '')
    illustration_url = f"https://raw.githubusercontent.com/Andrianina2000/portes_du_desir/main/quiz/static/quiz/img/{illustration_file}"

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
        'illustration_url': illustration_url,
    }

    subject = "Votre resultat - " + result_data['label']
    text_body = "Votre resultat : " + result_data['label'] + "\n" + result_data['title']

    try:
        html_body = render_to_string('quiz/email_result.html', ctx)
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[participant_email],
            bcc=[admin_email] if admin_email else [],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=True)
    except Exception:
        pass
