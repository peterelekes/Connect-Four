# Generated by Django 4.1.5 on 2023-01-04 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect4', '0002_remove_connectfourgame_date_created_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connectfourgame',
            old_name='current_player',
            new_name='next_player',
        ),
    ]
