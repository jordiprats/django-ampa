from django.db import migrations, models

def forward(apps, schema_editor):
    Alumne = apps.get_model("cole", "Alumne")
    for alumne in Alumne.objects.all():
        alumne.telf_tutor1 = alumne.telf_tutor1.replace(" ", "")
        alumne.telf_tutor2 = alumne.telf_tutor2.replace(" ", "")
        alumne.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0032_cleanup.py'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
