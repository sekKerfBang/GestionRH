# Generated by Django 5.0.6 on 2024-10-17 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0005_alter_abscence_type_abscence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abscence',
            name='type_abscence',
            field=models.CharField(choices=[('cgE', 'Conge Entreprise'), ('autre', 'AUTRE'), ('cgM', 'Conge Maladie'), ('cgMt', 'Conge Maternite')], max_length=5, verbose_name='Type de Conge'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='contrat_employe',
            field=models.CharField(choices=[('CONTRA_A_DURE_DETERMINER', 'Contrat a dure determiner'), ('autre', 'AUTRE'), ('CONTRA_A_DURE_INDETERMINER', 'Contrat a dure indetermine')], max_length=26, verbose_name='Contrat'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='genre_employe',
            field=models.CharField(choices=[('F', 'Femme'), ('autre', 'AUTRE'), ('H', 'Homme')], max_length=5, verbose_name='Genre'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='poste_employe',
            field=models.CharField(choices=[('DG', 'Directeur Generale'), ('DT', 'Directeur Technique'), ('RH', 'Gestion Humaine'), ('DEV', 'Developpeur'), ('autre', 'AUTRE'), ('RF', 'Responsable Financier')], max_length=5, verbose_name='Poste'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='service_employe',
            field=models.CharField(choices=[('SR', 'Service de Reseau'), ('SD', 'Service de Developpement'), ('autre', 'AUTRE'), ('SRH', 'Services de gestion humaine')], max_length=5, verbose_name='Service'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='status',
            field=models.CharField(choices=[('REJECTED', 'Rejetée'), ('PENDING', 'En attente'), ('APPROVED', 'Approuvée')], default='PENDING', max_length=9, verbose_name='Statut '),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='type_paiement',
            field=models.CharField(choices=[('remboursement', 'Remboursement'), ('CASH', 'Espece'), ('autre', 'AUTRE'), ('CHECK', 'Cheque'), ('prime', 'Prime')], max_length=13, verbose_name='Type de Paiement '),
        ),
    ]