# Generated by Django 3.0.5 on 2020-11-28 11:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0004_auto_20201121_1549'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='classe',
            unique_together=set(),
        ),
        migrations.RenameField(
            model_name='Classe',
            old_name='curs',
            new_name='alias',
        ),
    ]

