import csv
from io import BytesIO

import qrcode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import StartForm
from .models import LeadParticipant, Question, QuestionChoice, QuizAnswer, QuizSession
from .services import RESULT_CONTENT, compute_result


@require_http_methods(["GET"])
def home(request):
    return render(request, 'quiz/home.html')


@require_http_methods(["GET", "POST"])
def start_quiz(request):
    if request.method == 'POST':
        form = StartForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            consent = form.cleaned_data['consent']
            participant, _ = LeadParticipant.objects.get_or_create(
                email=email,
                defaults={'consent_given': consent, 'consent_date': timezone.now(), 'source': 'QR / Web'}
            )
            participant.consent_given = consent
            participant.consent_date = timezone.now()
            participant.source = 'QR / Web'
            participant.save()
            session = QuizSession.objects.create(participant=participant)
            request.session['quiz_session_id'] = session.id
            return redirect('quiz_questions')
    else:
        form = StartForm()
    return render(request, 'quiz/start.html', {'form': form})


@require_http_methods(["GET", "POST"])
def quiz_questions(request):
    session_id = request.session.get('quiz_session_id')
    if not session_id:
        messages.error(request, "Veuillez commencer le test avant de continuer.")
        return redirect('start_quiz')
    session = get_object_or_404(QuizSession, id=session_id)
    questions = Question.objects.filter(is_active=True).prefetch_related('choices')

    if request.method == 'POST':
        QuizAnswer.objects.filter(session=session).delete()
        for question in questions:
            field_name = f'question_{question.id}'
            value = request.POST.get(field_name, '').strip()
            if question.question_type == 'single' and value:
                choice = QuestionChoice.objects.filter(id=value, question=question).first()
                if choice:
                    QuizAnswer.objects.create(session=session, question=question, choice=choice)
            elif question.question_type == 'text':
                QuizAnswer.objects.create(session=session, question=question, answer_text=value)

        result_data = compute_result(session)
        # Email désactivé pour l'instant
        return redirect('quiz_result', session_id=session.id)

    return render(request, 'quiz/quiz.html', {'session': session, 'questions': questions})


@require_http_methods(["GET"])
def quiz_result(request, session_id):
    """Vue personnelle du patient — son résultat uniquement."""
    session = get_object_or_404(QuizSession, id=session_id)
    result_data = RESULT_CONTENT.get(session.result_code)

    total = (session.total_score_mental + session.total_score_emotionnel +
             session.total_score_energetique + session.total_score_sensoriel +
             session.total_score_physique) or 1

    def pct(v): return round(v * 100 / total)

    scores = [
        {'code': 'mental', 'label': 'Mentale', 'score': session.total_score_mental, 'pct': pct(session.total_score_mental), 'color': '#6b7dbf'},
        {'code': 'emotionnel', 'label': 'Emotionnelle', 'score': session.total_score_emotionnel, 'pct': pct(session.total_score_emotionnel), 'color': '#bf6b7d'},
        {'code': 'energetique', 'label': 'Energetique', 'score': session.total_score_energetique, 'pct': pct(session.total_score_energetique), 'color': '#7dbf6b'},
        {'code': 'sensoriel', 'label': 'Sensorielle', 'score': session.total_score_sensoriel, 'pct': pct(session.total_score_sensoriel), 'color': '#bf9b6b'},
        {'code': 'physique', 'label': 'Physique', 'score': session.total_score_physique, 'pct': pct(session.total_score_physique), 'color': '#bf6b6b'},
    ]
    scores_sorted = sorted(scores, key=lambda x: x['score'], reverse=True)

    return render(request, 'quiz/result.html', {
        'session': session,
        'result': result_data,
        'scores': scores_sorted,
    })


@require_http_methods(["GET"])
def qr_code_page(request):
    start_url = request.build_absolute_uri(reverse('start_quiz'))
    return render(request, 'quiz/qr_code.html', {'start_url': start_url})


@require_http_methods(["GET"])
def qr_code_image(request):
    start_url = request.build_absolute_uri(reverse('start_quiz'))
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=4)
    qr.add_data(start_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='#1a0a12', back_color='#fdf8f2')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')


@require_http_methods(["GET"])
def export_csv(request):
    if not request.user.is_staff:
        return redirect('home')
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="portes_du_desir_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Email', 'Consentement', 'Source', 'Porte dominante',
                     'Score Mental', 'Score Emotionnel', 'Score Energetique',
                     'Score Sensoriel', 'Score Physique', 'Date du test'])
    for session in QuizSession.objects.select_related('participant').order_by('-id'):
        writer.writerow([
            session.id, session.participant.email,
            'Oui' if session.participant.consent_given else 'Non',
            session.participant.source, session.result_label,
            session.total_score_mental, session.total_score_emotionnel,
            session.total_score_energetique, session.total_score_sensoriel,
            session.total_score_physique,
            session.completed_at.strftime('%d/%m/%Y %H:%M') if session.completed_at else '',
        ])
    return response


@login_required(login_url='/admin/login/')
@require_http_methods(["GET"])
def admin_dashboard(request):
    """Dashboard admin — réservé aux staff connectés."""
    if not request.user.is_staff:
        return redirect('home')

    sessions = QuizSession.objects.select_related('participant').order_by('-id')
    total_sessions = sessions.count()
    total_participants = LeadParticipant.objects.count()
    total_consents = LeadParticipant.objects.filter(consent_given=True).count()

    counts = {code: QuizSession.objects.filter(result_code=code).count()
              for code in ['mental', 'emotionnel', 'energetique', 'sensoriel', 'physique']}

    def pct(v): return round(v * 100 / total_sessions) if total_sessions > 0 else 0
    pcts = {k: pct(v) for k, v in counts.items()}

    dominant_code = max(counts, key=counts.get) if total_sessions > 0 else None
    dominant_label = RESULT_CONTENT[dominant_code]['emoji'] if dominant_code and counts[dominant_code] > 0 else '—'

    return render(request, 'quiz/dashboard.html', {
        'sessions': sessions[:200],
        'total_sessions': total_sessions,
        'total_participants': total_participants,
        'total_consents': total_consents,
        'counts': counts,
        'pcts': pcts,
        'dominant_label': dominant_label,
        'RESULT_CONTENT': RESULT_CONTENT,
    })
