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
