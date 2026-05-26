from django.contrib import admin
from .models import LeadParticipant, Question, QuestionChoice, QuizAnswer, QuizSession, SiteText


class QuestionChoiceInline(admin.TabularInline):
    model = QuestionChoice
    extra = 1
    fields = (
        'order', 'label', 'value',
        'score_mental', 'score_emotionnel', 'score_energetique', 'score_sensoriel', 'score_physique',
    )
    ordering = ('order', 'id')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'question_type', 'is_active')
    list_display_links = ('title',)
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'question_type')
    search_fields = ('title', 'text')
    ordering = ('order', 'id')
    fields = ('order', 'is_active', 'question_type', 'title', 'text')
    inlines = [QuestionChoiceInline]


@admin.register(SiteText)
class SiteTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'key', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    search_fields = ('title', 'key', 'content')
    readonly_fields = ('updated_at',)
    ordering = ('title',)
    fieldsets = (
        ('Texte modifiable', {
            'fields': ('title', 'key', 'content', 'is_active')
        }),
        ('Informations', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )


@admin.register(LeadParticipant)
class LeadParticipantAdmin(admin.ModelAdmin):
    list_display = ('email', 'consent_given', 'consent_date', 'source', 'created_at')
    list_filter = ('consent_given', 'source')
    search_fields = ('email',)
    ordering = ('-created_at',)


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant', 'started_at', 'completed_at', 'result_label',
                    'total_score_mental', 'total_score_emotionnel', 'total_score_energetique',
                    'total_score_sensoriel', 'total_score_physique')
    list_filter = ('result_code', 'completed_at')
    search_fields = ('participant__email', 'result_label')
    ordering = ('-id',)


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'question', 'choice', 'answer_text')
    search_fields = ('session__participant__email', 'question__title', 'choice__label', 'answer_text')
