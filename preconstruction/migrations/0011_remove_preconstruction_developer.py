# Generated by Django 3.1.6 on 2024-07-23 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0010_auto_20240723_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preconstruction',
            name='developer',
        ),
    ]
