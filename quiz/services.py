import logging
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from .formatting import render_email_markdown

logger = logging.getLogger(__name__)

COMMON_EMAIL_FOOTER = """## 🌿 Une dernière chose importante...

Votre résultat met en lumière votre porte dominante du désir aujourd'hui. Cela signifie qu'à cet instant de votre vie, c'est généralement par cette voie que votre désir s'éveille le plus naturellement.

Cependant, le désir humain est vivant, évolutif et multidimensionnel.

En réalité, nous possédons tous les cinq portes :

- 🧠 La porte mentale
- ❤️ La porte émotionnelle
- ✨ La porte énergétique
- 🌿 La porte sensorielle
- 🔥 La porte physique

Aucune n'est meilleure qu'une autre. Elles participent toutes à la richesse de votre vie intime et relationnelle.

Selon les périodes de vie, les expériences traversées, l'état du couple, le niveau de sécurité émotionnelle, le stress, la fatigue ou encore les transformations personnelles, certaines portes peuvent devenir plus présentes tandis que d'autres se mettent momentanément en retrait.

Votre résultat n'est donc pas une étiquette.

C'est une photographie de votre fonctionnement actuel, une invitation à mieux comprendre ce qui nourrit votre désir aujourd'hui.

> Votre porte dominante vous montre par où le désir entre aujourd'hui. Les autres portes vous révèlent tout ce qu'il peut devenir.
"""

RESULT_CONTENT = {
    'mental': {
        'label': 'Porte Mentale',
        'emoji': '🧠',
        'title': "Quand le désir commence dans l'imaginaire",
        'subtitle': "Votre porte dominante actuelle semble être la porte Mentale",
        'description': (
            "Votre désir ne naît pas d'abord dans le corps. Il commence souvent bien avant, "
            "dans votre esprit. Les mots, les idées, les conversations et l'imaginaire jouent "
            "un rôle important dans votre façon d'entrer en relation."
        ),
        'besoins': "Comprendre, imaginer, anticiper, explorer, sentir une stimulation intellectuelle et émotionnelle.",
        'conseil': "Nourrissez les conversations de qualité et laissez de la place à la spontanéité sans tout analyser.",
        'phrase': "Je me sens attiré(e) lorsque mon esprit se sent compris, stimulé et profondément relié à l'autre.",
        'couleur': '#6b7dbf',
        'email_content': """## Ce qui nourrit votre désir

Votre désir s'éveille lorsque vous ressentez :

- une connexion intellectuelle forte ;
- des conversations authentiques et stimulantes ;
- de la curiosité mutuelle ;
- de la créativité dans la relation ;
- des échanges qui sortent de la routine ;
- le sentiment d'être compris(e) dans votre profondeur.

Vous êtes particulièrement sensible à ce qui crée du sens.

Un simple échange peut parfois éveiller davantage votre désir qu'un geste pourtant considéré comme romantique par d'autres.

## Ce qui peut freiner votre désir

Votre désir peut se refermer lorsque :

- la relation devient trop mécanique ;
- la routine s'installe durablement ;
- les échanges deviennent superficiels ;
- vous avez l'impression de ne plus être compris(e) ;
- vous vous sentez intellectuellement seul(e) dans la relation.

Vous pouvez également avoir tendance à beaucoup réfléchir. Parfois, votre mental cherche à tout comprendre, tout anticiper ou tout maîtriser, ce qui peut rendre plus difficile l'accès au lâcher-prise.

## Votre défi amoureux

Votre plus belle force est votre richesse intérieure.

Votre défi consiste parfois à accepter que tout ne passe pas toujours par la compréhension. Le désir possède une part de mystère, d'imprévu et de spontanéité.

## Comment prendre soin de votre Porte Mentale

Pour nourrir cette dimension de votre désir, vous pouvez :

- cultiver des conversations de qualité ;
- partager vos rêves, vos projets et vos inspirations ;
- lire ou découvrir ensemble de nouveaux univers ;
- prendre du temps pour vous surprendre mutuellement ;
- créer des moments d'échange sans distraction ni écran.

> Votre désir s'épanouit lorsque votre esprit se sent libre, stimulé et connecté.
""",
        'email_footer': COMMON_EMAIL_FOOTER,
    },
    'emotionnel': {
        'label': 'Porte Émotionnelle',
        'emoji': '❤️',
        'title': "Quand le désir naît du lien affectif",
        'subtitle': "Votre porte dominante actuelle semble être la porte Émotionnelle",
        'description': (
            "Pour vous, le désir durable ne dépend pas seulement d'un geste. Il naît surtout "
            "du sentiment d'être vu(e), choisi(e), reconnu(e) et accueilli(e) avec délicatesse."
        ),
        'besoins': "Sécurité affective, reconnaissance, tendresse, confiance, authenticité et profondeur du lien.",
        'conseil': "Commencez par nourrir le lien. Lorsque le cœur se sent en sécurité, le désir peut s'ouvrir plus naturellement.",
        'phrase': "Je me sens attiré(e) lorsque je me sens choisi(e), reconnu(e) et émotionnellement en sécurité.",
        'couleur': '#bf6b7d',
        'email_content': """## Ce qui nourrit votre désir

Votre désir s'éveille lorsque vous ressentez :

- une sécurité émotionnelle ;
- une attention sincère ;
- une parole qui rassure ;
- le sentiment d'être important(e) pour l'autre ;
- une tendresse présente et régulière ;
- une relation où vous pouvez être vrai(e).

Pour vous, l'intimité commence souvent par le cœur.

Lorsque vous vous sentez pleinement accueilli(e), votre désir peut devenir profond, vivant et confiant.

## Ce qui peut freiner votre désir

Votre désir peut se refermer lorsque :

- vous ne vous sentez pas écouté(e) ;
- la relation manque de tendresse ;
- vous vous sentez négligé(e) ;
- les mots ou les gestes semblent froids ;
- vous avez peur de ne pas compter réellement.

## Votre défi amoureux

Votre grande force est votre capacité à aimer avec profondeur.

Votre défi consiste parfois à ne pas attendre que tout soit parfaitement sécurisé pour vous autoriser à vous ouvrir. Le lien se construit aussi par petites étapes.

## Comment prendre soin de votre Porte Émotionnelle

Pour nourrir cette dimension de votre désir, vous pouvez :

- exprimer ce qui vous touche ;
- demander clairement ce qui vous rassure ;
- cultiver des moments de qualité ;
- valoriser les gestes tendres ;
- créer un espace où chacun peut dire ce qu'il ressent.

> Votre désir grandit lorsque votre cœur se sent vu, respecté et accueilli.
""",
        'email_footer': COMMON_EMAIL_FOOTER,
    },
    'energetique': {
        'label': 'Porte Énergétique',
        'emoji': '✨',
        'title': "Quand l'intimité devient connexion subtile",
        'subtitle': "Votre porte dominante actuelle semble être la porte Énergétique",
        'description': (
            "Vous entrez dans l'intimité par une connexion profonde, subtile et silencieuse. "
            "La présence, l'intuition, le rythme et la qualité d'attention comptent beaucoup pour vous."
        ),
        'besoins': "Présence vraie, synchronisation, attention fine, rythme juste et sensation de connexion profonde.",
        'conseil': "Prenez le temps de créer une présence partagée. Laissez la connexion se construire sans précipitation.",
        'phrase': "Je sens une connexion qui dépasse les mots.",
        'couleur': '#7dbf6b',
        'email_content': """## Ce qui nourrit votre désir

Votre désir s'éveille lorsque vous ressentez :

- une présence profonde ;
- une connexion silencieuse ;
- une qualité d'attention ;
- une respiration commune ;
- un rythme partagé ;
- une sensation d'alignement avec l'autre.

Vous percevez souvent ce qui se joue au-delà des mots.

Pour vous, l'intimité commence lorsque deux personnes entrent dans un même espace émotionnel et énergétique.

## Ce qui peut freiner votre désir

Votre désir peut se fermer lorsque :

- l'autre est physiquement présent mais émotionnellement absent ;
- le rythme devient trop rapide ;
- vous sentez une tension non exprimée ;
- l'ambiance paraît lourde ou confuse ;
- vous ne ressentez plus la connexion.

## Votre défi amoureux

Votre sensibilité est une richesse.

Votre défi consiste parfois à ne pas attendre que l'énergie soit parfaite pour vous ouvrir. Une connexion peut aussi se construire dans le dialogue, l'ajustement et la confiance progressive.

## Comment prendre soin de votre Porte Énergétique

Pour nourrir cette dimension de votre désir, vous pouvez :

- ralentir le rythme ;
- créer des moments de présence sans distraction ;
- respirer ensemble ;
- écouter vos ressentis ;
- mettre des mots simples sur ce que vous percevez ;
- privilégier la qualité de présence à la performance.

> Votre désir s'épanouit lorsque la présence devient plus forte que les mots.
""",
        'email_footer': COMMON_EMAIL_FOOTER,
    },
    'sensoriel': {
        'label': 'Porte Sensorielle',
        'emoji': '🌿',
        'title': "Quand le plaisir se savoure avec présence",
        'subtitle': "Votre porte dominante actuelle semble être la porte Sensorielle",
        'description': (
            "Vous entrez dans le désir par les sens : la lenteur, l'ambiance, les textures, "
            "les odeurs, la voix et les nuances. Le plaisir est pour vous une expérience à savourer."
        ),
        'besoins': "Lenteur, douceur, ambiance rassurante, attention aux sensations et présence fine.",
        'conseil': "Ralentissez. Accordez de l'importance aux détails, aux sensations et à l'atmosphère.",
        'phrase': "J'ai besoin de douceur, de nuances et de lenteur.",
        'couleur': '#bf9b6b',
        'email_content': """## Ce qui nourrit votre désir

Votre désir s'éveille lorsque vous ressentez :

- une ambiance agréable ;
- une lumière douce ;
- une voix posée ;
- des gestes attentifs ;
- un rythme lent ;
- une présence aux sensations.

Pour vous, le plaisir n'est pas seulement un résultat. C'est une expérience à vivre avec attention.

## Ce qui peut freiner votre désir

Votre désir peut se refermer lorsque :

- tout va trop vite ;
- l'ambiance est stressante ;
- les gestes manquent de finesse ;
- vous ne vous sentez pas pleinement présent(e) ;
- la pression remplace le plaisir.

## Votre défi amoureux

Votre grande force est votre capacité à goûter les nuances.

Votre défi consiste parfois à exprimer clairement ce qui vous fait du bien, sans attendre que l'autre le devine.

## Comment prendre soin de votre Porte Sensorielle

Pour nourrir cette dimension de votre désir, vous pouvez :

- ralentir volontairement ;
- soigner l'ambiance ;
- prendre soin des détails ;
- écouter ce que votre corps ressent ;
- exprimer ce qui est agréable ;
- créer des rituels de présence.

> Votre désir s'épanouit lorsque vos sens se sentent libres, respectés et éveillés.
""",
        'email_footer': COMMON_EMAIL_FOOTER,
    },
    'physique': {
        'label': 'Porte Physique',
        'emoji': '🔥',
        'title': "Quand le corps devient la voie directe du désir",
        'subtitle': "Votre porte dominante actuelle semble être la porte Physique",
        'description': (
            "Votre désir s'ouvre par le corps : le mouvement, l'élan, la présence incarnée "
            "et les signaux corporels. Le corps est votre intelligence première."
        ),
        'besoins': "Corps vivant, présence incarnée, mouvement, spontanéité, énergie et intensité ajustée.",
        'conseil': "Gardez votre élan, tout en restant à l'écoute du rythme de l'autre et de la qualité du consentement.",
        'phrase': "Mon corps s'allume d'abord.",
        'couleur': '#bf6b6b',
        'email_content': """## Ce qui nourrit votre désir

Votre désir s'éveille lorsque vous ressentez :

- une présence corporelle claire ;
- un élan vivant ;
- une énergie assumée ;
- une spontanéité dans la relation ;
- une intensité qui reste ajustée ;
- le sentiment que le corps peut s'exprimer librement.

Pour vous, le corps parle souvent avant les mots.

## Ce qui peut freiner votre désir

Votre désir peut se refermer lorsque :

- la relation devient trop contrôlée ;
- l'élan est constamment retenu ;
- vous sentez une distance corporelle ;
- l'intensité manque de réciprocité ;
- vous ne pouvez pas exprimer votre énergie naturellement.

## Votre défi amoureux

Votre grande force est votre présence incarnée.

Votre défi consiste parfois à ralentir assez pour écouter les nuances, les émotions et le rythme de l'autre. L'intensité devient plus belle lorsqu'elle reste reliée à la présence et au respect mutuel.

## Comment prendre soin de votre Porte Physique

Pour nourrir cette dimension de votre désir, vous pouvez :

- bouger davantage ensemble ;
- laisser plus de place à la spontanéité ;
- écouter les signaux du corps ;
- créer un cadre clair et rassurant ;
- ajuster l'intensité selon le rythme de chacun ;
- associer énergie, attention et respect.

> Votre désir s'épanouit lorsque le corps peut être vivant, libre et pleinement respecté.
""",
        'email_footer': COMMON_EMAIL_FOOTER,
    },
}


def _editable_text(key, default=''):
    """Compatibilité avec l'ancien système SiteText."""
    try:
        from .models import SiteText
        item = SiteText.objects.filter(key=key, is_active=True).first()
        if item and item.content != '':
            return item.content
    except Exception:
        pass
    return default


def _result_content_from_db(code, base):
    """Charge le contenu depuis la nouvelle table ResultContent si elle existe."""
    try:
        from .models import ResultContent
        item = ResultContent.objects.filter(code=code, is_active=True).first()
        if not item:
            return base
        base.update({
            'label': item.label or base.get('label', ''),
            'title': item.title or base.get('title', ''),
            'subtitle': item.subtitle or base.get('subtitle', ''),
            'description': item.description or base.get('description', ''),
            'besoins': item.besoins or base.get('besoins', ''),
            'conseil': item.conseil or base.get('conseil', ''),
            'phrase': item.phrase or base.get('phrase', ''),
            'email_content': item.email_content or base.get('email_content', ''),
            'email_footer': item.email_footer or base.get('email_footer', ''),
        })
    except Exception as exc:
        # Pendant les migrations ou avant que la table existe, on garde les valeurs par défaut.
        logger.debug("ResultContent indisponible, fallback contenu code : %s", exc)
    return base


def get_result_content(code):
    base = RESULT_CONTENT.get(code, {}).copy()
    if not base:
        return base

    # Nouveau système : contenu complet modifiable depuis l'admin.
    base = _result_content_from_db(code, base)

    # Ancien système : garde les SiteText existants comme fallback si la nouvelle table n'a pas encore été remplie.
    prefix = f'result_{code}_'
    for field in ['label', 'title', 'subtitle', 'description', 'besoins', 'conseil', 'phrase']:
        base[field] = _editable_text(prefix + field, base.get(field, ''))

    base['description_html'] = render_email_markdown(base.get('description', ''))
    base['email_content_html'] = render_email_markdown(base.get('email_content', ''))
    base['email_footer_html'] = render_email_markdown(base.get('email_footer', ''))
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


def send_result_email(session, result_data):
    import sendgrid
    from sendgrid.helpers.mail import Bcc, Mail

    participant_email = session.participant.email
    admin_email = getattr(settings, 'ADMIN_RESULT_EMAIL', '')

    total = (session.total_score_mental + session.total_score_emotionnel +
             session.total_score_energetique + session.total_score_sensoriel +
             session.total_score_physique) or 1

    ctx = {
        'result_code': session.result_code,
        'result_label': result_data['label'],
        'result_title': result_data['title'],
        'result_description': result_data.get('description', ''),
        'result_description_html': result_data.get('description_html', ''),
        'result_email_content_html': result_data.get('email_content_html', ''),
        'result_email_footer_html': result_data.get('email_footer_html', ''),
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
        'instagram_url': get_instagram_url(session.result_code),
    }

    html_body = render_to_string('quiz/email_result.html', ctx)
    text_body = (
        f"Votre résultat : {result_data.get('label', '')}\n"
        f"{result_data.get('title', '')}\n\n"
        f"{result_data.get('description', '')}\n\n"
        f"{result_data.get('email_content', '')}\n\n"
        f"{result_data.get('phrase', '')}\n"
    )

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=participant_email,
        subject="Votre résultat — " + result_data['label'],
        html_content=html_body,
        plain_text_content=text_body,
    )

    if admin_email:
        message.add_bcc(Bcc(admin_email))

    response = sg.send(message)
    logger.info(f"Email SendGrid envoyé à {participant_email} - status: {response.status_code}")
