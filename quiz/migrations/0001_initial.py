from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='LeadParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('consent_given', models.BooleanField(default=False)),
                ('consent_date', models.DateTimeField(blank=True, null=True)),
                ('source', models.CharField(blank=True, default='QR / Web', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('text', models.TextField(blank=True)),
                ('question_type', models.CharField(choices=[('single', 'Choix unique'), ('text', 'Texte')], default='single', max_length=20)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='QuestionChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=500)),
                ('value', models.CharField(blank=True, default='', max_length=100)),
                ('score_mental', models.IntegerField(default=0)),
                ('score_emotionnel', models.IntegerField(default=0)),
                ('score_energetique', models.IntegerField(default=0)),
                ('score_sensoriel', models.IntegerField(default=0)),
                ('score_physique', models.IntegerField(default=0)),
                ('order', models.PositiveIntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='quiz.question')),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='QuizSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('total_score_mental', models.IntegerField(default=0)),
                ('total_score_emotionnel', models.IntegerField(default=0)),
                ('total_score_energetique', models.IntegerField(default=0)),
                ('total_score_sensoriel', models.IntegerField(default=0)),
                ('total_score_physique', models.IntegerField(default=0)),
                ('result_code', models.CharField(blank=True, default='', max_length=50)),
                ('result_label', models.CharField(blank=True, default='', max_length=255)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='quiz.leadparticipant')),
            ],
        ),
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, default='')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.questionchoice')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.quizsession')),
            ],
        ),
    ]
