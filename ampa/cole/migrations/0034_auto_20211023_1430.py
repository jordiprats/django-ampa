# Generated by Django 3.1.5 on 2021-10-23 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0033_cleanup_hone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curs',
            options={'ordering': ['-curs']},
        ),
        migrations.AlterField(
            model_name='alumne',
            name='num_llista',
            field=models.IntegerField(default=0),
        ),
    ]