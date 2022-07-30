# Generated by Django 4.0.3 on 2022-07-29 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('routine', '0005_alter_routine_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoutineResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('result', models.CharField(choices=[('NOT', 'NOT'), ('TRY', 'TRY'), ('DONE', 'DONE')], max_length=50, verbose_name='결과')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('routine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routine.routine', verbose_name='루틴 결과')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
