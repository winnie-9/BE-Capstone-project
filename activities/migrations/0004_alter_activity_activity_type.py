# Generated by Django 5.1.2 on 2024-10-19 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_metrics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(choices=[('Running', 'Running'), ('Cycling', 'Cycling'), ('Weightlifting', 'Weightlifting'), ('sit-ups', 'sit-ups'), ('Swimming', 'Swimming'), ('Other', 'Other')], max_length=100),
        ),
    ]
