# Generated by Django 5.0.6 on 2024-09-17 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0012_alter_abscence_type_abscence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abscence',
            name='type_abscence',
            field=models.CharField(choices=[('cgMt', 'Conge Maternite'), ('cgE', 'Conge Entreprise'), ('cgM', 'Conge Maladie')], max_length=4, verbose_name="Type d'abscence"),
        ),
        migrations.AlterField(
            model_name='employe',
            name='genre_employe',
            field=models.CharField(choices=[('H', 'Homme'), ('F', 'Femme')], max_length=1, verbose_name='Genre'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='poste_employe',
            field=models.CharField(choices=[('RH', 'Gestion Humaine'), ('DG', 'Directeur Generale'), ('DEV', 'Developpeur'), ('RF', 'Responsable Financier'), ('DT', 'Directeur Technique')], max_length=3, verbose_name='Poste'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='status',
            field=models.CharField(choices=[('valider', 'Valider'), ('en cours ', 'En cours'), ('annuler', 'Annuler')], max_length=9, verbose_name='Statut '),
        ),
    ]
