# Gestion du contenu long des emails

Après déploiement et migration, aller dans :

`/admin/` → `Quiz` → `Résultats / emails personnalisables`

Il y a 5 fiches :

- Porte Mentale
- Porte Émotionnelle
- Porte Énergétique
- Porte Sensorielle
- Porte Physique

La cliente peut modifier :

- le libellé de la porte ;
- le titre ;
- le résumé court ;
- la phrase-clé ;
- le contenu long du mail ;
- le bloc final du mail.

## Mise en forme acceptée

Dans le champ `email_content` ou `email_footer`, elle peut écrire :

```txt
## Grand titre

### Sous-titre

Un paragraphe normal avec **du texte en gras** et *du texte en italique*.

- élément de liste
- autre élément de liste
- troisième élément

> citation encadrée

---

[lien visible](https://exemple.com)
```

Important : laisser une ligne vide entre deux paragraphes.

## Déploiement Railway

La commande de démarrage a été corrigée pour lancer automatiquement :

```bash
python manage.py migrate --noinput
```

Ne plus lancer `setup_app` automatiquement au démarrage, sinon les questions/textes modifiés par la cliente peuvent être écrasés.
