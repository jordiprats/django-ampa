from django.db import migrations, models

def forward(apps, schema_editor):
    Alumne = apps.get_model("cole", "Alumne")
    for alumne in Alumne.objects.all():
        if alumne.classes.count() == 0:
            alumne.delete()
        else:
            alumne.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0031_auto_20211003_1736'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
