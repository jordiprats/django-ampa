# Generated by Django 3.1.5 on 2021-01-30 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0011_auto_20210110_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]
