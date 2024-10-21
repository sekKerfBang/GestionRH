from django.contrib import admin

#from .models import User

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from .forms import UserAdminCreationForm, UserAdminChangeForm
User = get_user_model() 

#Supprimer le modele de group de l'administrateur. Nous ne l'utilisons pas 
#admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    
    #Les formulaires d'ajout et de modification d'une instance d'un utilisateur
    model = User
    #Les champs a utiliser pour afficher le model user
    #Celles ci remplacent les definitions de la BaseUserAdmin
    #Qui font reference a des champs specifiques sur auth.User
    list_display = ['first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active',]
    list_filter = ['is_superuser', 'is_staff',]
    list_per_page = 10
    labels = { 'first_name' : 'Prenom ', 'last_name' : 'Nom ', 'email' : 'Email ', 'password' : 'Mot de Passe' }
    fieldsets = (
        (("Information Personnel"), {"fields": ("email", "first_name", "last_name", "password", 'matricule' ,'profile_user',)}),
        (("Permissions"), {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes' : ('wide'),
            'fields'  : ('email', 'first_name', 'last_name', 'matricule','password1', 'password2', 'is_staff', 'is_active', 'is_superuser')
        }),
    )
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm
    search_fields = ['email']
    ordering = ['email', 'is_staff']
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    
    
admin.site.register(User, UserAdmin)

    
# @admin.register(User)
# class AccountsAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ( 'Information Compte', {'fields' : ['first_name', 'last_name', 'email', 'password', 'staff', 'admin', 'is_active']}),
        
#         ]
#     list_filter = ['email', 'first_name']
#     list_display = ('first_name', 'last_name', 'email', 'password','staff', 'admin', 'is_active')
#     list_per_page = 5
#     labels = {'first_name' : 'Prenom'}

