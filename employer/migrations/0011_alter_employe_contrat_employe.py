# Generated by Django 5.0.6 on 2024-10-17 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0010_alter_employe_genre_employe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='contrat_employe',
            field=models.CharField(choices=[('CONTRA_A_DURE_DETERMINER', 'Contrat a dure determiner'), ('CONTRA_A_DURE_INDETERMINER', 'Contrat a dure indetermine'), ('autre', 'AUTRE')], max_length=27, verbose_name='Contrat'),
        ),
    ]
