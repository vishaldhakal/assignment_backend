# Generated by Django 3.1.6 on 2024-08-03 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0012_remove_preconstruction_project_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='preconstruction',
            name='occupancy',
            field=models.IntegerField(default=2025),
        ),
    ]