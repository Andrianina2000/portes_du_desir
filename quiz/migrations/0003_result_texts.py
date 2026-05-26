# Generated manually for editable result texts
from django.db import migrations

RESULT_TEXTS = [
    ('mental', 'Porte Mentale', 'Quand le desir s\'ouvre par l\'esprit', 'Votre porte dominante actuelle semble etre la porte Mentale', "Pour vous, l'intimite commence bien avant le corps : elle nait quand le mental se sent intrigue, compris, stimule. Vous vous activez par les mots, les descriptions, les scenarios, l'imaginaire. Ce besoin n'est pas une complication : c'est une porte de securite qui permet de s'ouvrir sans forcer.", "Comprendre avant de se livrer, sentir une intention claire, jouer avec l'imaginaire, se sentir relie(e) par la pensee et le langage.", 'Parlez avec precision et delicatesse. Le cadre clair vous securise et vous permet de vous ouvrir pleinement.', "Je veux comprendre avant d'avancer."),
    ('emotionnel', 'Porte Emotionnelle', "Quand le desir nait d'un sentiment", 'Votre porte dominante actuelle semble etre la porte Emotionnelle', "Pour vous, le desir durable ne depend pas d'un geste, mais de l'emotion que ce geste active. Vous avez besoin de vous sentir vu(e), choisi(e), reconnu(e). Quand ce besoin est nourri, l'emotion partagee devient un vrai facteur d'intimite profonde.", "Etre vu(e) et reconnu(e), recevoir de l'admiration et de la tendresse, pouvoir etre vulnerable sans se fermer, sentir que le lien compte vraiment.", 'Commencez par le lien avant toute invitation intime. La securite affective est votre cle d\'ouverture.', "J'ai besoin de me sentir relie(e)."),
    ('energetique', 'Porte Energetique', "Quand l'intimite devient connexion subtile", 'Votre porte dominante actuelle semble etre la porte Energetique', "Vous entrez dans l'intimite par une connexion profonde, subtile, silencieuse. Vous ressentez l'energie de l'autre, anticipez ses besoins, vous synchronisez dans une meme pulsation. La presence, la respiration et l'intuition comptent plus que les mots.", "Sentir une presence vraie, vivre une synchronisation profonde, percevoir l'autre au-dela des mots.", 'Prenez un temps de presence partagee. Posez une intention, respirez ensemble, laissez la connexion se construire sans accelerer.', 'Je sens une connexion qui depasse les mots.'),
    ('sensoriel', 'Porte Sensorielle', 'Quand le plaisir se savoure avec presence', 'Votre porte dominante actuelle semble etre la porte Sensorielle', "Vous entrez dans le desir par les sens : la lenteur, l'ambiance, les textures, les odeurs, la voix. Le plaisir n'est pas un resultat mais une experience a savourer. Vous aimez les micro-sensations et avez besoin d'une presence fine et attentive.", "Le plaisir de sentir, une presence au corps, de la curiosite sans pression, un espace securisant d'exploration.", 'Ralentissez. Goutez chaque sensation. Variez les textures et les rythmes. Nommez ce qui est ressenti.', "J'ai besoin de douceur, de nuances, de lenteur."),
    ('physique', 'Porte Physique', 'Quand le corps devient la voie directe du desir', 'Votre porte dominante actuelle semble etre la porte Physique', "Votre desir s'ouvre par le corps : l'excitation, le mouvement, l'action, la puissance incarnee. Vous lisez les signaux corporels de l'autre avec finesse et aimez une approche directe et assumee. Le corps est votre intelligence premiere.", 'Sentir le corps vivant et present, agir, bouger, explorer, vivre une intensite incarnee et ajustee.', "Restez a l'ecoute du rythme et des signaux de l'autre. L'intensite modulee est plus juste qu'une initiative trop directe.", "Mon corps s'allume d'abord."),
]


def create_result_texts(apps, schema_editor):
    SiteText = apps.get_model('quiz', 'SiteText')
    for code, label, title, subtitle, description, besoins, conseil, phrase in RESULT_TEXTS:
        rows = [
            (f'result_{code}_label', f'Résultat {label} — libellé', label),
            (f'result_{code}_title', f'Résultat {label} — titre', title),
            (f'result_{code}_subtitle', f'Résultat {label} — sous-titre', subtitle),
            (f'result_{code}_description', f'Résultat {label} — description', description),
            (f'result_{code}_besoins', f'Résultat {label} — besoins', besoins),
            (f'result_{code}_conseil', f'Résultat {label} — conseil', conseil),
            (f'result_{code}_phrase', f'Résultat {label} — phrase', phrase),
        ]
        for key, title_label, content in rows:
            SiteText.objects.get_or_create(key=key, defaults={'title': title_label, 'content': content, 'is_active': True})


def remove_result_texts(apps, schema_editor):
    SiteText = apps.get_model('quiz', 'SiteText')
    keys = []
    for code, *_ in RESULT_TEXTS:
        for field in ['label','title','subtitle','description','besoins','conseil','phrase']:
            keys.append(f'result_{code}_{field}')
    SiteText.objects.filter(key__in=keys).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_sitetext'),
    ]

    operations = [
        migrations.RunPython(create_result_texts, remove_result_texts),
    ]
