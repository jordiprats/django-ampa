# Generated by Django 3.1.5 on 2021-03-07 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peticions', '0013_auto_20210307_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='representant',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
