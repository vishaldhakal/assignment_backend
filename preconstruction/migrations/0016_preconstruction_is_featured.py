# Generated by Django 3.1.6 on 2025-02-19 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0015_auto_20240826_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='preconstruction',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
