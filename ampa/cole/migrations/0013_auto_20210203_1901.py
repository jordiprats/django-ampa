# Generated by Django 3.1.5 on 2021-02-03 19:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0012_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('html_message', models.TextField(blank=True, default='', max_length=50000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modalitat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('ordre', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['ordre'],
            },
        ),
        migrations.AddIndex(
            model_name='modalitat',
            index=models.Index(fields=['ordre'], name='cole_modali_ordre_905b19_idx'),
        ),
        migrations.AddField(
            model_name='curs',
            name='modalitat',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cursos', to='cole.modalitat'),
        ),
    ]
