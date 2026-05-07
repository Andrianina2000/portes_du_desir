from django.contrib import admin
from .models import LeadParticipant, Question, QuestionChoice, QuizAnswer, QuizSession

class QuestionChoiceInline(admin.TabularInline):
    model = QuestionChoice
    extra = 1
    fields = ('label', 'score_mental', 'score_emotionnel', 'score_energetique', 'score_sensoriel', 'score_physique', 'order')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'question_type', 'is_active')
    list_editable = ('is_active',)
    inlines = [QuestionChoiceInline]

@admin.register(LeadParticipant)
class LeadParticipantAdmin(admin.ModelAdmin):
    list_display = ('email', 'consent_given', 'consent_date', 'source', 'created_at')
    search_fields = ('email',)

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant', 'started_at', 'completed_at', 'result_label',
                    'total_score_mental', 'total_score_emotionnel', 'total_score_energetique',
                    'total_score_sensoriel', 'total_score_physique')
    search_fields = ('participant__email', 'result_label')

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'question', 'choice', 'answer_text')
