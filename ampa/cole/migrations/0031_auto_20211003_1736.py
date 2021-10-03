from django.db import migrations, models

def forward(apps, schema_editor):
    Alumne = apps.get_model("cole", "Alumne")
    for alumne in Alumne.objects.all():
        alumne.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0030_auto_20210903_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumne',
            name='cognom1_unaccented',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='alumne',
            name='cognom2_unaccented',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='alumne',
            name='nom_unaccented',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.RunPython(forward)
    ]
