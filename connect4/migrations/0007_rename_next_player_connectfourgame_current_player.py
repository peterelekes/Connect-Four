# Generated by Django 4.1.5 on 2023-01-04 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect4', '0006_remove_connectfourgame_board'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connectfourgame',
            old_name='next_player',
            new_name='current_player',
        ),
    ]
