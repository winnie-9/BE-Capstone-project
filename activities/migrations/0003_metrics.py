# Generated by Django 5.1.2 on 2024-10-17 17:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_activity_history'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year')], max_length=5)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('total_duration', models.IntegerField()),
                ('total_distance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total_calories_burned', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'period', 'start_date'], name='activities__user_id_a0fa08_idx')],
                'unique_together': {('user', 'period', 'start_date')},
            },
        ),
    ]
