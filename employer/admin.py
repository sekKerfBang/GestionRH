from django.contrib import admin
from .models import Employe, Abscence, Paiement

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information utilisateur', {'fields': ['name_employe', 'prenom_employe', 'date_naiss_employe', 'poste_employe', 'genre_employe', 'image_employe', 'diplome_employe', 'contrat_employe', 'service_employe', 'user', 'matricule']}),
        ('Information Contact ', {'fields': ['tel_employe', 'adresse_employe', 'email_employe']}) 
        ]        
    list_display = ('name_employe', 'prenom_employe', 'date_naiss_employe', 'adresse_employe', 'email_employe', 'tel_employe', 'poste_employe', 'genre_employe', 'image_employe', 'diplome_employe', 'contrat_employe', 'service_employe')
    list_filter = ['email_employe']
    list_per_page = 10
    
    
# @admin.register(Contrat)
# class ContratAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Information Contrat', {'fields' : ['type_contrat', 'date_debut', 'date_fin']})
#     ]    
#     list_display = ('type_contrat', 'date_debut', 'date_fin')

# @admin.register(Poste)
# class PosteAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Information Poste', {'fields' : ['intitule', 'description', 'salaire', 'competences_requises']})
#     ]
#     list_display = ('intitule', 'description', 'salaire', 'competences_requises')
    
# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Information Service', {'fields': ['nom', 'nom_directeur', 'description']})
#     ]  
#     list_display = ('nom', 'nom_directeur', 'description')
    
@admin.register(Abscence)
class AbscenceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information Abscence', {'fields' : ['type_abscence', 'date_debut', 'date_fin', 'motif', 'employe']} )
    ]    
    list_display = ('employe', 'type_abscence', 'date_debut', 'date_fin', 'motif')
    list_per_page = 10
    
@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
        fieldsets = [
            ('Information Paiement', {'fields' : ['employe_id', 'date_paiement', 'montant_total', 'type_paiement', 'status']})
        ]
        list_display = ('employe_id', 'date_paiement', 'montant_total', 'type_paiement', 'status')
        list_per_page = 10
# Register your models here.
#admin.site.register(Employer, EmployerAdmin)