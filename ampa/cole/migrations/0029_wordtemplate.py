# Generated by Django 3.1.5 on 2021-05-09 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0028_auto_20210307_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordTemplate',
            fields=[
                ('fileattachment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cole.fileattachment')),
            ],
            bases=('cole.fileattachment',),
        ),
    ]