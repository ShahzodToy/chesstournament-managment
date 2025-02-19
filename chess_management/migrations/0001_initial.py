# Generated by Django 5.0.7 on 2024-07-20 16:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('current_round', models.IntegerField(default=1)),
                ('participants', models.ManyToManyField(related_name='tournaments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.IntegerField()),
                ('result', models.CharField(blank=True, choices=[('player1', 'Player 1 Wins'), ('player2', 'Player 2 Wins'), ('draw', 'Draw')], max_length=20, null=True)),
                ('player1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1_matches', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2_matches', to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='chess_management.tournament')),
            ],
        ),
    ]
