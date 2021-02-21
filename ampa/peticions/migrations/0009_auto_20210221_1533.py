# Generated by Django 3.1.5 on 2021-02-21 15:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('peticions', '0008_auto_20210220_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='Representant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='representant',
            index=models.Index(fields=['name'], name='peticions_r_name_d45a5b_idx'),
        ),
    ]
