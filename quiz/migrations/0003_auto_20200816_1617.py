# Generated by Django 3.1 on 2020-08-16 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20200811_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersanswer',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.answer'),
        ),
    ]
