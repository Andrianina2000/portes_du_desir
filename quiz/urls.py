from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('quiz/', views.quiz_questions, name='quiz_questions'),
    path('result/<int:session_id>/', views.quiz_result, name='quiz_result'),
    path('qr/', views.qr_code_page, name='qr_code_page'),
    path('qr/image/', views.qr_code_image, name='qr_code_image'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
