# Generated by Django 4.1.5 on 2023-01-03 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectFourGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grid', models.CharField(max_length=42)),
                ('current_player', models.CharField(max_length=1)),
                ('winner', models.CharField(blank=True, max_length=1, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
