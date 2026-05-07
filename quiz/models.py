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
