# Generated by Django 3.1.5 on 2021-11-20 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peticions', '0021_issue_classes'),
        ('cole', '0045_mailing_nomes_plataforma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='representants',
            field=models.ManyToManyField(blank=True, default=None, related_name='mailings', to='peticions.Representant'),
        ),
    ]
