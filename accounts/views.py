from django.shortcuts import redirect, render, HttpResponse #
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import UserForm, UserRegister
from django.contrib.auth.models import Group
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from notifications.signals import notify
from .models import User

def register_user(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserRegister(request.POST, request.FILES) 
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save() 
            
            # Récupérer le rôle sélectionné dans le formulaire
            role = form.cleaned_data['role']
            
            group = None  # Initialiser la variable group
            print(f"Valeur du rôle: {role}") 

            try:
                # Assigner l'utilisateur au groupe approprié
                if role == 'manager':
                    group = Group.objects.get(name='Manager_user')
                elif role == 'simple_user':
                    group = Group.objects.get(name='simple_user')
            except:
                    raise ValueError("Rôle is valid" + str(role))
            new_user.groups.add(group)
            
            # Notification pour les manager
            manager_group = Group.objects.get(name='Manager_user')
            manager_users = User.objects.filter(groups=manager_group)
            for manager in manager_users:
                notify.send(
                    sender=new_user,
                    recipient=manager,
                    verb='s\'est inscrit',
                    description=f"Un nouvel utilisateur {new_user.email} s'est inscrit."
                )
            
            messages.success(request, 'Utilisateur enregistrer avec succes !')
            return redirect('accounts:login')
    else:
        form = UserRegister()
    return render(request, './pages/sign-up1.html', {'form': form})


def login_user(request, *args, **kwargs):
    if request.method == 'POST':      
        form = UserForm(request.POST)
        if form.is_valid():
            email= form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email = email , password = password)
            if user is not None:
                login(request, user)
                
                # Notification pour les manager
                manager_group = Group.objects.get(name='Manager_user')
                manager_users = User.objects.filter(groups=manager_group)
                for manager in manager_users:
                    notify.send(
                    sender=user,
                    recipient=manager,
                    verb='s\'est Connecter',
                    description=f"Un nouvel utilisateur {user.email} s'est connecter."
                )
                messages.info(request, 'Connecter avec succes !')
                return redirect('employer:tableau')
            else:
                messages.info(request, 'Adresse e-mail ou mot de passe incorrect...')
    else:
        form =  UserForm()
    return render(request, './pages/sign-in.html', {'form': form})
    
    
def logout_user(request, *args,  **kwargs):
    logout(request)
   
    return redirect('accounts:login') 


# @staff_member_required
# def addToPermissionGroup(request):
#     group = Group.objects.get(name="")
#     request.user.groups.add(group)
#     return HttpResponse("<h1> a ete ajouter avec succes dans le group ? </h1>")
