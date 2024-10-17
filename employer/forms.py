from django import forms 
from .models import Employe 
from accounts.models import User
from .models import Abscence, Paiement

class EmployerForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='User ', widget=forms.Select(attrs={'placeholder' : 'User_id', 'class' :'form-select'}))

    class Meta:
        model = Employe
        fields = ['user' ,'name_employe', 'prenom_employe', 'date_naiss_employe', 'email_employe', 'adresse_employe', 'tel_employe', 'image_employe', 'poste_employe', 'contrat_employe', 'service_employe', 'genre_employe', 'diplome_employe']
        labels =  { 'name_employe': 'Nom', 'prenom_employe': 'Prenom', 'date_naiss_employe' : ' Date ', 'email_employe': 'Email', 'adresse_employe': 'Adresse', 'tel_employe': 'Telephone', 'image_employe': 'Image', 'genre_employe': 'Genre', 'diplome_employe': 'Diplome'}
        widgets = {
            'name_employe' : forms.TextInput(attrs={'placeholder' : 'Votre Nom', 'class' :'form-control'}),
            'prenom_employe' : forms.TextInput(attrs={'placeholder' : 'Votre prenom', 'class' :'form-control'}),
            'email_employe' : forms.TextInput(attrs={'placeholder' : 'Votre Email', 'class' : 'form-control'}),
            'adresse_employe' : forms.TextInput(attrs={'placeholder' : 'Votre Adresse', 'class' :'form-control'}),
            'tel_employe' : forms.TextInput(attrs={'placeholder' : 'Votre Numero Telephone', 'class' : 'form-control'}),
            'date_naiss_employe' : forms.TextInput(attrs={'placeholder' : 'AAAA -MM  -jj', 'class' : 'form-control'}),
            'poste_employe' : forms.Select(attrs={'class' : 'form-select'}),
            'contrat_employe' : forms.Select(attrs={'class' : 'form-select'}),
            'service_employe' :  forms.Select(attrs={'class' : 'form-select'}),
            'genre_employe'  : forms.Select(attrs={'class' : 'form-select'}),
            'image_employe' : forms.FileInput(attrs={'class' : 'form-control'}),
            'diplome_employe' : forms.FileInput(attrs={'class' : 'form-control'})
        }
        error_messages = {
            'user': {
                'required': 'Veuillez specifier l\'email',
            },
            'name_employe': {
                'required': 'Veuillez saisir votre nom.',
            },
            'prenom_employe' : {
                'required' : 'Veuillez saisir votre prenom.',
            }, 
            'email_employe' : {
                'required' : 'Veuillez saisir votre email',
            },
            'adresse_employe' : {
                'required' : 'Veuillez saisir votre adresse',
            },
            'tel_employe' : {
                'required' : 'Veuillez saisir votre Numero de telephone',
            },
            'date_naiss_employe' : {
                'required' : 'Veuillez saisir votre date de naissance',
            },
            'poste_employe' : {
                'required' : 'Veuillez specifier votre poste',
            },
            'contrat_employe' : {
                'required' : 'Veuillez specifier votre contrat ',
            },
            'service_employe' : {
                'required' : 'Veuillez specifier votre service ',
            },
            'genre_employe' : {
                'required' : 'Veuillez specifier votre genre ',
            },
            'image_employe' : {
                'required' : 'Veuillez specifier votre image ',
            },
            'diplome_employe' : {
                'required' : 'Veuillez specifier votre diplome ',
            },
        }
        
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        # Masquer le champ 'user' si c'est une modification
        if instance:
            self.fields['user'].widget = forms.HiddenInput()    
        
    def clean_diplome_employe(self):
        file = self.cleaned_data.get('diplome_employe')
        if file:
            if file.size > 5 * 1024 * 1024:  # ne dois pas depasser 5 MB sinon une erreur est lever
                raise forms.ValidationError("Le fichier est trop volumineux (max 5 MB).")
        return file
        

class  AbscenceForm(forms.ModelForm):
    class Meta:
        model = Abscence
        fields = ['type_abscence', 'date_debut', 'date_fin', 'motif']
        widgets = {
            'type_abscence' : forms.Select(attrs={'class' : 'form-select' }),
            'date_debut' : forms.TextInput(attrs={'placeholder' : 'AAAA -MM  -jj', 'class' : 'form-control'}),
            'date_fin' : forms.TextInput(attrs={'placeholder' : 'AAAA -MM  -jj', 'class' : 'form-control'}),
            'motif' : forms.TextInput(attrs={'placeholder' : 'Votre Motif ici ', 'class' : 'form-control'}),
            # 'employe' : forms.Select(attrs={'class' : 'form-select'})
        }
        
        error_messages = {
            'type_abscence' :{ 
                'required' : 'Veuillez entrer le type de conge',
                    },
            'date_debut' :{ 
                'required' : 'Veuillez entrer la date de debut',
                    },
            'date_fin' :{ 
                'required' : 'Veuillez entrer la date de fin ',
                    },
            'motif' :{ 
                'required' : 'Veuillez entrer le motif de conge',
                    },
            # 'employe' :{ 
            #     'required' : 'Veuillez specifier l\'employe',
            #         },
        }
        
class PaiementForm(forms.ModelForm):
    class Meta: 
        model = Paiement
        fields = ['employe_id', 'date_paiement', 'montant_total', 'type_paiement']
        widgets = {
            'montant_total' : forms.TextInput(attrs={'placeholder' : 'Veuillez saisir le montant total', 'class' : 'form-control'}),
            'date_paiement' : forms.TextInput(attrs={'placeholder' : 'AAAA -MM  -jj', 'class' : 'form-control'}),
            'type_paiement' : forms.Select(attrs={'class' : 'form-select'}),
            'employe_id' : forms.Select(attrs={'class' : 'form-select'}),
            }
        
        error_messages = {
            'montant_total' : {
                "required" : 'veuillez entrer le montant total',
            },
            'date_paiement' :{ 
                'required' : 'Veuillez entrer la date de paiement',
                    },
            'type_paiement' :{ 
                'required' : 'Veuillez specifier le type de paiement',
                    },
            'employe_id' :{ 
                'required' : 'Veuillez specifier l\'employe',
                    },
        }