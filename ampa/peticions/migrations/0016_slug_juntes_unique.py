# Generated by Django 3.1.5 on 2021-03-13 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peticions', '0015_slug_juntes_issues'),
    ]

    operations = [
        migrations.AlterField(
            model_name='junta',
            name='slug',
            field=models.SlugField(default='no-slug', max_length=256, unique=True),
            preserve_default=False,
        ),
    ]