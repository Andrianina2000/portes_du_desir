# Generated manually for editable site texts
from django.db import migrations, models


def create_default_texts(apps, schema_editor):
    SiteText = apps.get_model('quiz', 'SiteText')
    defaults = [
        ('site_tagline', 'Header — phrase sous le logo', "Découvrez votre porte d'entrée dans l'intimité"),
        ('home_eyebrow', 'Accueil — petite phrase', 'Test de connexion intime'),
        ('home_title', 'Accueil — grand titre', "Quelle est votre<br>porte d'entrée<br>dans <em>l'intimité</em>&nbsp;?"),
        ('home_description', 'Accueil — description', 'Un questionnaire immersif et confidentiel pour révéler votre dynamique dominante et comprendre comment vous vous connectez vraiment.'),
        ('home_button', 'Accueil — bouton principal', "Commencer l'exploration"),
        ('home_quote', 'Accueil — citation', "« L'intimité n'est pas ce que l'on partage,<br>c'est la porte par laquelle on entre. »"),
        ('home_feature_1_title', 'Accueil — bloc 1 titre', 'Rapide'),
        ('home_feature_1_desc', 'Accueil — bloc 1 description', '5 à 7 minutes pour un résultat profond et personnalisé'),
        ('home_feature_2_title', 'Accueil — bloc 2 titre', '5 portes'),
        ('home_feature_2_desc', 'Accueil — bloc 2 description', 'Cinq dynamiques distinctes, nuancées et bienveillantes'),
        ('home_feature_3_title', 'Accueil — bloc 3 titre', 'Par email'),
        ('home_feature_3_desc', 'Accueil — bloc 3 description', 'Votre résultat complet envoyé immédiatement'),
        ('home_doors_title', 'Accueil — titre des 5 portes', "Les cinq portes de l'intimité"),
        ('start_step', 'Début — étape', 'Étape 1 sur 3'),
        ('start_title', 'Début — titre', 'Avant de<br><em>commencer</em>'),
        ('start_description', 'Début — description', 'Votre résultat vous sera envoyé par email. Vos réponses restent confidentielles.'),
        ('start_email_label', 'Début — label email', 'Votre adresse email'),
        ('start_button', 'Début — bouton', 'Accéder au questionnaire'),
        ('quiz_step', 'Quiz — étape', 'Étape 2 sur 3 — Le questionnaire'),
        ('quiz_title', 'Quiz — titre', 'Vos <em>réponses</em>'),
        ('quiz_submit_button', 'Quiz — bouton final', 'Découvrir ma porte'),
        ('quiz_submit_note', 'Quiz — note sous bouton', 'Votre résultat complet vous sera envoyé par email'),
        ('result_step', 'Résultat — étape', 'Étape 3 sur 3 — Votre résultat'),
        ('result_eyebrow', 'Résultat — petite phrase', 'Résultat personnalisé'),
        ('result_needs_label', 'Résultat — label besoins', 'Ce dont vous avez besoin'),
        ('result_partner_label', 'Résultat — label conseil partenaire', 'Conseil pour votre partenaire'),
        ('result_note', 'Résultat — note', "<strong>N.B.</strong> Ce résultat est une photographie de votre fonctionnement à l'instant où vous avez répondu. Il ne vous enferme pas dans une case. Nous portons tous en nous les cinq portes de l'intimité, mais certaines sont plus présentes selon les périodes de vie, les cycles, l'état émotionnel et la qualité du lien."),
        ('result_cta_title', 'Résultat — titre CTA', 'Aller plus loin'),
        ('result_cta_subtitle', 'Résultat — description CTA', 'Découvrez nos séminaires et accompagnements pour approfondir votre connexion intime.'),
        ('result_instagram_button', 'Résultat — bouton Instagram', 'Découvrir la suite sur Instagram'),
        ('dashboard_title', 'Dashboard — titre', 'Suivi des <em>participants</em>'),
        ('dashboard_badge', 'Dashboard — badge', '✦ Tableau de bord'),
    ]
    for key, title, content in defaults:
        SiteText.objects.get_or_create(key=key, defaults={'title': title, 'content': content, 'is_active': True})


def remove_default_texts(apps, schema_editor):
    SiteText = apps.get_model('quiz', 'SiteText')
    SiteText.objects.filter(key__in=[
        'site_tagline','home_eyebrow','home_title','home_description','home_button','home_quote',
        'home_feature_1_title','home_feature_1_desc','home_feature_2_title','home_feature_2_desc',
        'home_feature_3_title','home_feature_3_desc','home_doors_title','start_step','start_title',
        'start_description','start_email_label','start_button','quiz_step','quiz_title','quiz_submit_button',
        'quiz_submit_note','result_step','result_eyebrow','result_needs_label','result_partner_label',
        'result_note','result_cta_title','result_cta_subtitle','result_instagram_button','dashboard_title',
        'dashboard_badge'
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField(help_text='Identifiant technique utilisé dans les pages. Ne pas le modifier une fois créé.', max_length=100, unique=True)),
                ('title', models.CharField(help_text="Nom lisible dans l'administration.", max_length=255)),
                ('content', models.TextField(blank=True, default='', help_text='Texte affiché sur le site. Vous pouvez le modifier librement.')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Texte du site',
                'verbose_name_plural': 'Textes du site',
                'ordering': ['title'],
            },
        ),
        migrations.RunPython(create_default_texts, remove_default_texts),
    ]
