# Generated by Django 3.1.5 on 2021-03-14 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peticions', '0016_slug_juntes_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='junta',
            name='latest_export',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]
