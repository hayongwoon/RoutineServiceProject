# Generated by Django 4.0.3 on 2022-07-30 03:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('routine_result', '0002_alter_routineresult_routine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routineresult',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 30, 3, 41, 34, 224391, tzinfo=utc)),
        ),
    ]
