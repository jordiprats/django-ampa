# Generated by Django 3.1.5 on 2021-03-14 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peticions', '0017_junta_latest_export'),
    ]

    operations = [
        migrations.AddField(
            model_name='junta',
            name='peu_message',
            field=models.TextField(blank=True, default='', max_length=50000, null=True),
        ),
    ]
