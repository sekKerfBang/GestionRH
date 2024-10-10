# Generated by Django 5.0.6 on 2024-09-10 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0002_alter_abscence_type_abscence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abscence',
            name='type_abscence',
            field=models.CharField(choices=[('cgMt', 'Conge Maternite'), ('cgM', 'Conge Maladie'), ('cgE', 'Conge Entreprise')], max_length=4, verbose_name="Type d'abscence"),
        ),
        migrations.AlterField(
            model_name='employe',
            name='contrat_employe',
            field=models.CharField(choices=[('CDD', 'Contrat a dure determiner'), ('CDI', 'Contrat a dure indetermine')], max_length=3, verbose_name='Contrat'),
        ),
        migrations.AlterField(
            model_name='employe',
            name='poste_employe',
            field=models.CharField(choices=[('RF', 'Responsable Financier'), ('DEV', 'Developpeur'), ('DT', 'Directeur Technique'), ('DG', 'Directeur Generale'), ('RH', 'Gestion Humaine')], max_length=3, verbose_name='Poste'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='type_paiement',
            field=models.CharField(choices=[('CHECK', 'Cheque'), ('prime', 'Prime'), ('remboursement', 'Remboursement'), ('CASH', 'Espece')], max_length=13, verbose_name='Type de Paiement '),
        ),
    ]
