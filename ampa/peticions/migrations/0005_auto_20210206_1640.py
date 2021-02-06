# Generated by Django 3.1.5 on 2021-02-06 16:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('peticions', '0004_auto_20210203_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='dislikes',
            field=models.ManyToManyField(related_name='disliked_issues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='likes',
            field=models.ManyToManyField(related_name='liked_issues', to=settings.AUTH_USER_MODEL),
        ),
    ]