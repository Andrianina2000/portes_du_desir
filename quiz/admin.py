from django import forms
from django.contrib import admin
from django.db import models as django_models

from .models import (
    LeadParticipant,
    Question,
    QuestionChoice,
    QuizAnswer,
    QuizSession,
    ResultContent,
    SiteText,
)


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


@admin.register(ResultContent)
class ResultContentAdmin(admin.ModelAdmin):
    """Admin pensé pour Audrey : gros champs de texte + aide Markdown."""

    list_display = ('label', 'code', 'is_active', 'updated_at')
    list_display_links = ('label',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'code')
    search_fields = ('label', 'title', 'subtitle', 'description', 'email_content', 'email_footer')
    readonly_fields = ('updated_at', 'aide_mise_en_forme')
    ordering = ('code',)

    formfield_overrides = {
        django_models.TextField: {
            'widget': forms.Textarea(attrs={
                'rows': 14,
                'style': 'font-family: Consolas, Monaco, monospace; font-size: 14px; line-height: 1.6; min-height: 220px;',
            })
        },
    }

    fieldsets = (
        ('Porte / titre', {
            'fields': ('code', 'label', 'title', 'subtitle', 'phrase', 'is_active')
        }),
        ('Résumé court', {
            'fields': ('description', 'besoins', 'conseil'),
            'description': "Ces champs restent courts. Ils servent au résumé du résultat et à la page web."
        }),
        ('Email long avec mise en forme', {
            'fields': ('aide_mise_en_forme', 'email_content', 'email_footer'),
            'description': "C'est ici qu'Audrey peut coller beaucoup de texte et gérer la mise en forme du mail."
        }),
        ('Informations', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )

    def aide_mise_en_forme(self, obj=None):
        return (
            "Mise en forme acceptée dans le contenu email :\n\n"
            "## Grand titre de section\n"
            "### Sous-titre\n"
            "**texte en gras**\n"
            "*texte en italique*\n"
            "- élément de liste\n"
            "- autre élément\n"
            "> citation encadrée\n"
            "---\n"
            "[texte du lien](https://exemple.com)\n\n"
            "Astuce : laissez une ligne vide entre deux paragraphes."
        )
    aide_mise_en_forme.short_description = "Aide mise en forme"


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
