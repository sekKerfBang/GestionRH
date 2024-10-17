# Generated by Django 5.0.6 on 2024-10-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0006_alter_abscence_type_abscence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abscence',
            name='type_abscence',
            field=models.CharField(choices=[('cgM', 'Conge Maladie'), ('cgMt', 'Conge Maternite'), ('cgE', 'Conge Entreprise'), ('autre', 'AUTRE')], max_length=5, verbose_name='Type de Conge'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='contrat_employe',
            field=models.CharField(choices=[('CONTRA_A_DURE_DETERMINER', 'Contrat a dure determiner'), ('CONTRA_A_DURE_INDETERMINER', 'Contrat a dure indetermine'), ('autre', 'AUTRE')], max_length=26, verbose_name='Contrat'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='genre_employe',
            field=models.CharField(choices=[('H', 'Homme'), ('F', 'Femme'), ('autre', 'AUTRE')], max_length=5, verbose_name='Genre'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='poste_employe',
            field=models.CharField(choices=[('DEV', 'Developpeur'), ('RH', 'Gestion Humaine'), ('DG', 'Directeur Generale'), ('DT', 'Directeur Technique'), ('RF', 'Responsable Financier'), ('autre', 'AUTRE')], max_length=5, verbose_name='Poste'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='service_employe',
            field=models.CharField(choices=[('SD', 'Service de Developpement'), ('SR', 'Service de Reseau'), ('SRH', 'Services de gestion humaine'), ('autre', 'AUTRE')], max_length=5, verbose_name='Service'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='status',
            field=models.CharField(choices=[('PENDING', 'En attente'), ('APPROVED', 'Approuvée'), ('REJECTED', 'Rejetée')], default='PENDING', max_length=9, verbose_name='Statut '),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='type_paiement',
            field=models.CharField(choices=[('CASH', 'Espece'), ('CHECK', 'Cheque'), ('prime', 'Prime'), ('remboursement', 'Remboursement'), ('autre', 'AUTRE')], max_length=13, verbose_name='Type de Paiement '),
        ),
    ]
