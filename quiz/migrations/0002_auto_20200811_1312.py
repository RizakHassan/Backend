# Generated by Django 3.1 on 2020-08-11 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserAnswer',
            new_name='UsersAnswer',
        ),
    ]
