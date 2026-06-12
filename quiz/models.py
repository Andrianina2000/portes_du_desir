from django.db import models

RESULT_CHOICES = (
    ('mental', 'Porte Mentale'),
    ('emotionnel', 'Porte Emotionnelle'),
    ('energetique', 'Porte Energetique'),
    ('sensoriel', 'Porte Sensorielle'),
    ('physique', 'Porte Physique'),
)

class LeadParticipant(models.Model):
    email = models.EmailField(unique=True)
    consent_given = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True, default='QR / Web')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.email

class Question(models.Model):
    QUESTION_TYPE_CHOICES = (('single', 'Choix unique'), ('text', 'Texte'),)
    title = models.CharField(max_length=500)
    text = models.TextField(blank=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='single')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ['order', 'id']
    def __str__(self): return f"{self.order} - {self.title}"

class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    label = models.CharField(max_length=500)
    value = models.CharField(max_length=100, blank=True, default='')
    score_mental = models.IntegerField(default=0)
    score_emotionnel = models.IntegerField(default=0)
    score_energetique = models.IntegerField(default=0)
    score_sensoriel = models.IntegerField(default=0)
    score_physique = models.IntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['order', 'id']
    def __str__(self): return f"{self.question.title[:30]} - {self.label[:30]}"

class QuizSession(models.Model):
    participant = models.ForeignKey(LeadParticipant, on_delete=models.CASCADE, related_name='sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_score_mental = models.IntegerField(default=0)
    total_score_emotionnel = models.IntegerField(default=0)
    total_score_energetique = models.IntegerField(default=0)
    total_score_sensoriel = models.IntegerField(default=0)
    total_score_physique = models.IntegerField(default=0)
    result_code = models.CharField(max_length=50, choices=RESULT_CHOICES, blank=True, default='')
    result_label = models.CharField(max_length=255, blank=True, default='')
    def __str__(self): return f"Session #{self.id} - {self.participant.email}"

class QuizAnswer(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(QuestionChoice, on_delete=models.SET_NULL, null=True, blank=True)
    answer_text = models.TextField(blank=True, default='')
    def __str__(self): return f"Session {self.session_id} - Q{self.question_id}"


class ResultContent(models.Model):
    """Contenu éditable d'une porte de résultat.

    La cliente peut modifier ici les textes affichés sur la page résultat
    et surtout le contenu long envoyé par email. Le champ email_content
    accepte une mise en forme simple type Markdown.
    """

    code = models.CharField(
        max_length=50,
        choices=RESULT_CHOICES,
        unique=True,
        help_text="Porte concernée. Ne pas changer après création."
    )
    label = models.CharField(
        max_length=100,
        help_text="Exemple : Porte Mentale"
    )
    title = models.CharField(
        max_length=255,
        help_text="Sous-titre principal affiché sous la porte."
    )
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Petit texte de contexte affiché sur la page résultat."
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text="Résumé court affiché dans le mail et sur la page résultat."
    )
    besoins = models.TextField(
        blank=True,
        default='',
        help_text="Bloc court : besoins / ce qui nourrit cette porte."
    )
    conseil = models.TextField(
        blank=True,
        default='',
        help_text="Bloc court : conseil ou piste d'accompagnement."
    )
    phrase = models.CharField(
        max_length=500,
        blank=True,
        default='',
        help_text="Phrase-clé affichée en citation."
    )
    email_content = models.TextField(
        blank=True,
        default='',
        help_text=(
            "Contenu long du mail. Mise en forme acceptée : ## Titre, ### Sous-titre, "
            "**gras**, *italique*, - liste, > citation, --- séparation, [lien](https://...)."
        )
    )
    email_footer = models.TextField(
        blank=True,
        default='',
        help_text="Bloc final commun ou spécifique ajouté après le contenu long. Même mise en forme que le contenu email."
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        verbose_name = "Résultat / email personnalisable"
        verbose_name_plural = "Résultats / emails personnalisables"

    def __str__(self):
        return self.label or self.code


class SiteText(models.Model):
    key = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Identifiant technique utilisé dans les pages. Ne pas le modifier une fois créé."
    )
    title = models.CharField(
        max_length=255,
        help_text="Nom lisible dans l'administration."
    )
    content = models.TextField(
        blank=True,
        default='',
        help_text="Texte affiché sur le site. Vous pouvez le modifier librement."
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Texte du site"
        verbose_name_plural = "Textes du site"

    def __str__(self):
        return self.title
