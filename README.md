# Portes du Désir - MVP Django

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## URLs utiles

- Accueil: `/`
- Démarrage du test: `/start/`
- Questionnaire: `/quiz/`
- Résultat: `/result/<id>/`
- Admin Django: `/admin/`
- Export CSV: `/export/csv/`

## Ce que fait cette V1

- Collecte email + consentement
- Lance une session de quiz
- Affiche les questions stockées en base
- Calcule un résultat selon les scores
- Envoie le résultat par email
- Exporte les résultats en CSV

## Important

Avant de tester l'envoi d'email, configure les variables SMTP dans `portes_du_desir/settings.py`.

## Interface admin cliente

Après déploiement, lancer les migrations :

```bash
python manage.py migrate
```

Créer un compte administrateur si besoin :

```bash
python manage.py createsuperuser
```

La cliente peut ensuite aller sur `/admin/`.

Sections importantes :

- **Textes du site** : modifier les textes visibles sur le site, l'accueil, le quiz, le résultat et les phrases de résultat.
- **Questions** : ajouter, désactiver, supprimer ou réordonner les questions.
- **Choix de questions** : dans chaque question, ajouter ou retirer les réponses et ajuster les scores.

Ne pas modifier le champ technique `key` dans **Textes du site**, sauf si le code est adapté aussi.
