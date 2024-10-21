from django import forms 
from django.contrib.auth import get_user_model
#from django.contrib.auth.forms import  ReadOnlyPasswordHashField
#from django.contrib import messages

from .models import User
#User = get_user_model()
    
class UserRegister(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Mot de passe ')
    password_2 = forms.CharField(label="Confirmer mot de passe ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    ROLE_CHOICES = {
        ('manager', 'Manager'),
        ('simple_user', 'Simple Utilisateur'),
    }

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label='Rôle', widget=forms.Select(attrs={'placeholder' : 'Choix d\'utilisateur', 'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['profile_user','email', 'first_name', 'last_name','matricule' , 'password' ]
        widgets = {
            'profile_user' : forms.FileInput(attrs={ 'class' : 'form-control'}),
            # 'email' : forms.TextInput()
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Prénom', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
            'matricule': forms.TextInput(attrs={'placeholder': 'Matricule', 'class': 'form-control'}),
        }
    
        def clean_email(self):
            """ verify email is available"""
            email = self.cleaned_data.get('email')
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("L'email est pris")
            return email
        
        def clean_password(self):
            """ verifie que les deux mot de passe correspondent  """
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            password_2 = cleaned_data.get('password_2')
            if password is not None and password != password_2 :
                self.add_error("Les deux mots e passes ne correspondent pas !")
            return cleaned_data    
            

# class UserAdminCreationForm(forms.ModelForm):
#     """ Un formulaire pour creer de nouveau utilisateur. Comprends tout le necessaire champ, plus un mot de passe repete. """    
#     password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
#     password_2 = forms.CharField(label='Confirmer mot de passe', widget=forms.PasswordInput)
    
#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name', "password"]
        
#         def clean_password(self):
#             """Verify que les deux mots de passe correspondent"""
#             cleaned_data = super().clean()
#             password = cleaned_data.get("password")
#             password_2 =cleaned_data.get('password_2')
#             if password is not None and password != password_2 :
#                 self.add_error("password_2", "your passwords must match")
#             return cleaned_data
        
#         def save(self, Commit=False):
#             #Enregistrer le mot de passe fourni au format hacher
#             user = super().save(Commit=False)
#             user.set_password(self.clean_password['password'])
#             if Commit:
#                 user.save()
#                 messages.success('Utilisateur créé avec succès.')
#             return user 
        
# class UserAdminChangeForm(forms.ModelForm):
#     """Un formulaire pour mettre a jour les utilisateurs. Inclut tous les champs sur l'utilisateur, mais remplace le champ du mot de passe par celui de l'administrateur, champ d'affichage du hachage du mot de passe 
#     """        
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name', 'is_active', 'admin', 'password',]
    
#     def clean(self):
#         # Independament de ce que l'utilisateur fournit, renvoie la valeur initial 
#         # Cela se fait ici, plutot que sur le terrain car le     
#         # champ n'a pas acces a la valeur i initial
#         #
#         return self.initial['password']
                    
class UserForm(forms.Form):
    email   = forms.CharField(label='E-mail ', widget=forms.TextInput(attrs={ 'placeholder':'Entrez votre e-mail'}))
    password   = forms.CharField(label='Mot de Passe ', widget=forms.PasswordInput(attrs={'placeholder' : 'Entrez mot de passe'}))
    
    error_messages = {
        'email' : {
            'required' : 'Veuillez saisir l\'email !',
        },
        'password' : {
            'required' : 'Veuillez saisir le mot de passe !',
        },
    }
    






