# Generated by Django 2.2.7 on 2019-11-20 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_question_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answer',
        ),
        migrations.AddField(
            model_name='choice',
            name='is_correct',
            field=models.BooleanField(default=False, help_text='Mark right if this is the right choice'),
        ),
    ]
