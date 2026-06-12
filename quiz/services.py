import logging
import os
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

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


def _editable_text(key, default=''):
    try:
        from .models import SiteText
        item = SiteText.objects.filter(key=key, is_active=True).first()
        if item and item.content != '':
            return item.content
    except Exception:
        pass
    return default



def _format_email_rich_text(text):
    """
    Transforme un texte saisi dans l'admin en HTML propre pour l'email.
    - conserve les paragraphes
    - transforme les petits titres en intertitres
    - transforme les listes apres une ligne qui finit par ':' en puces
    - met les citations en encadre
    Le texte est echappe pour eviter d'injecter du HTML non controle.
    Pour mettre un mot en gras dans l'admin, utiliser **mot en gras**.
    """
    import re

    raw = (text or '').replace('\r\n', '\n').replace('\r', '\n').strip()
    if not raw:
        return ''

    def fmt(line):
        safe = escape(line.strip())
        # Gras simple utilisable dans l'admin : **texte**
        safe = re.sub(r'\*\*(.+?)\*\*', r'<strong style="font-weight:700;color:#5A0E28;">\1</strong>', safe)
        return safe

    lines = [line.strip() for line in raw.split('\n')]
    html = []
    paragraph = []
    in_list = False
    bullet_mode = False

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            body = '<br>'.join(fmt(x) for x in paragraph if x.strip())
            if body:
                html.append(
                    '<p style="font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.85;'
                    'color:#342629;text-align:left;margin:0 0 18px;">' + body + '</p>'
                )
        paragraph = []

    def close_list():
        nonlocal in_list, bullet_mode
        if in_list:
            html.append('</ul>')
        in_list = False
        bullet_mode = False

    def is_title(line):
        clean = line.strip()
        if not clean:
            return False
        if clean.startswith('«') or clean.endswith(':'):
            return False
        # Gros titre type "🧠 PORTE MENTALE"
        if any(clean.startswith(e) for e in ['🧠', '❤️', '✨', '🌿', '🔥']) and len(clean) <= 80:
            return True
        # Intertitres courts sans point final
        if len(clean) <= 72 and not clean.endswith(('.', ';', ',', '!', '?', '»')):
            words = clean.split()
            if 2 <= len(words) <= 8:
                return True
        return False

    def is_bullet(line):
        clean = line.strip()
        if not clean:
            return False
        if len(clean) > 120:
            return False
        starters = (
            'un ', 'une ', 'des ', 'de ', 'du ', 'd’', "d'", 'le ', 'la ', 'les ',
            'cultiver ', 'partager ', 'lire ', 'prendre ', 'exprimer ', 'créer ', 'creer ',
            'vous ', '❤️', '🧠', '✨', '🌿', '🔥'
        )
        return clean.lower().startswith(starters) or clean.endswith(';')

    for line in lines:
        if not line:
            flush_paragraph()
            # On garde le mode liste apres une ligne vide, car les textes colles depuis Word
            # mettent souvent une ligne vide entre chaque puce.
            continue

        if line.startswith('«') and line.endswith('»'):
            flush_paragraph()
            close_list()
            html.append(
                '<div style="font-family:Georgia,serif;font-size:19px;line-height:1.65;color:#8C5A32;'
                'font-style:italic;text-align:center;margin:22px 0;padding:20px 22px;'
                'border-top:1px solid #E7D8CB;border-bottom:1px solid #E7D8CB;background:#FFF8F1;">'
                + fmt(line) + '</div>'
            )
            continue

        if bullet_mode and is_bullet(line):
            flush_paragraph()
            if not in_list:
                html.append('<ul style="margin:0 0 22px 22px;padding:0;font-family:Arial,Helvetica,sans-serif;color:#342629;text-align:left;">')
                in_list = True
            item = line.rstrip(' ;')
            html.append('<li style="font-size:16px;line-height:1.75;margin:0 0 8px;padding-left:4px;">' + fmt(item) + '</li>')
            continue

        if in_list:
            close_list()

        if is_title(line):
            flush_paragraph()
            if any(line.startswith(e) for e in ['🧠', '❤️', '✨', '🌿', '🔥']):
                html.append(
                    '<div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.5;'
                    'letter-spacing:2px;text-transform:uppercase;color:#5A0E28;font-weight:700;'
                    'text-align:center;margin:28px 0 10px;">' + fmt(line) + '</div>'
                )
            else:
                html.append(
                    '<h2 style="font-family:Georgia,serif;font-size:24px;line-height:1.25;color:#5A0E28;'
                    'font-weight:600;text-align:left;margin:30px 0 12px;">' + fmt(line) + '</h2>'
                )
            continue

        paragraph.append(line)
        if line.endswith(':'):
            flush_paragraph()
            bullet_mode = True

    flush_paragraph()
    close_list()

    return mark_safe(''.join(html))

def get_result_content(code):
    base = RESULT_CONTENT.get(code, {}).copy()
    if not base:
        return base
    prefix = f'result_{code}_'
    for field in ['label', 'title', 'subtitle', 'description', 'besoins', 'conseil', 'phrase']:
        base[field] = _editable_text(prefix + field, base.get(field, ''))
    return base


def get_all_result_content():
    return {code: get_result_content(code) for code in RESULT_CONTENT.keys()}


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
    session.result_label = get_result_content(best_code)['label']
    session.completed_at = timezone.now()
    session.save()

    return get_result_content(best_code)


def _pct(score, total):
    return round(score * 100 / total) if total > 0 else 0


def get_instagram_url(result_code):
    mapping = {
        'mental': getattr(settings, 'INSTAGRAM_MENTAL_URL', ''),
        'emotionnel': getattr(settings, 'INSTAGRAM_EMOTIONNEL_URL', ''),
        'energetique': getattr(settings, 'INSTAGRAM_ENERGETIQUE_URL', ''),
        'sensoriel': getattr(settings, 'INSTAGRAM_SENSORIEL_URL', ''),
        'physique': getattr(settings, 'INSTAGRAM_PHYSIQUE_URL', ''),
    }
    return mapping.get(result_code) or getattr(settings, 'INSTAGRAM_URL', 'https://www.instagram.com/intimementtoi/')


def _find_illustration_path(filename):
    """
    Retrouve l'image dans les dossiers static possibles.
    Objectif : l'attacher directement dans l'email avec SendGrid inline CID,
    pour eviter que Gmail/Outlook bloque une image externe.
    """
    if not filename:
        return None

    # Recherche Django officielle dans les fichiers static.
    try:
        from django.contrib.staticfiles import finders
        found = finders.find(f'quiz/img/{filename}')
        if found and os.path.exists(found):
            return found
    except Exception:
        pass

    base_dir = getattr(settings, 'BASE_DIR', '')
    static_root = getattr(settings, 'STATIC_ROOT', '')

    candidates = []
    if base_dir:
        candidates.extend([
            os.path.join(base_dir, 'quiz', 'static', 'quiz', 'img', filename),
            os.path.join(base_dir, 'static', 'quiz', 'img', filename),
            os.path.join(base_dir, 'staticfiles', 'quiz', 'img', filename),
        ])
    if static_root:
        candidates.append(os.path.join(static_root, 'quiz', 'img', filename))

    for path in candidates:
        if path and os.path.exists(path):
            return path

    return None


def send_result_email(session, result_data):
    import base64
    import mimetypes
    import sendgrid
    from sendgrid.helpers.mail import (
        Attachment,
        Bcc,
        ContentId,
        Disposition,
        FileContent,
        FileName,
        FileType,
        Mail,
    )

    participant_email = session.participant.email
    admin_email = getattr(settings, 'ADMIN_RESULT_EMAIL', '')

    total = (session.total_score_mental + session.total_score_emotionnel +
             session.total_score_energetique + session.total_score_sensoriel +
             session.total_score_physique) or 1

    illustration_map = {
        'mental': 'porte_mental.jpg',
        'emotionnel': 'porte_emotionnel.jpg',
        'energetique': 'porte_energetique.jpg',
        'sensoriel': 'porte_sensoriel.jpg',
        'physique': 'porte_physique.jpg',
    }

    illustration_file = illustration_map.get(session.result_code, '')
    # Important Gmail / Outlook : on utilise une URL publique HTTPS.
    # Le CID / pièce jointe inline peut apparaître cassé dans Gmail, surtout en spam.
    # SITE_URL doit contenir le domaine Railway ou le domaine personnalisé, sans slash final.
    site_url = getattr(settings, 'SITE_URL', 'https://web-production-eb2eba.up.railway.app').rstrip('/')
    illustration_url = f"{site_url}/static/quiz/img/{illustration_file}" if illustration_file else ''

    ctx = {
        'result_code': session.result_code,
        'result_label': result_data['label'],
        'result_title': result_data['title'],
        'result_description': result_data['description'],
        'result_description_html': _format_email_rich_text(result_data.get('description', '')),
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
        'instagram_url': get_instagram_url(session.result_code),
    }

    html_body = render_to_string('quiz/email_result.html', ctx)
    text_body = "Votre resultat : " + result_data['label'] + "\n" + result_data['title']

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=participant_email,
        subject="Votre resultat - " + result_data['label'],
        html_content=html_body,
        plain_text_content=text_body,
    )

    # Pas de pièce jointe image ici : l'image est chargée depuis l'URL publique.

    if admin_email:
        message.add_bcc(Bcc(admin_email))

    response = sg.send(message)
    logger.info(f"Email SendGrid envoye a {participant_email} - status: {response.status_code}")
