# Generated by Django 3.1.5 on 2021-03-07 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0025_auto_20210307_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitat',
            name='codi_registre',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='entitat',
            name='logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entitats', to='cole.fileupload'),
        ),
        migrations.AlterField(
            model_name='entitat',
            name='name',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]
