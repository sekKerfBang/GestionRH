from django.shortcuts import get_object_or_404, redirect, render, HttpResponse # type: ignore
# from django.http import HttpResponse # type: ignore
from .models import Employe, Abscence, Paiement
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import EmployerForm, AbscenceForm, PaiementForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
from notifications.signals import notify
from notifications.models import Notification

# def index(request, *args):
#      return render(request,'index.html')
'''
user.has_perm("employer.view_employe")
'''


@login_required()
def tableau(request, *args):
    #employe = get_object_or_404(Employe, user=request.user)
    
    # Récupérer les notifications non lues pour l'utilisateur
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)
    context = {
        # 'empl' : get_object_or_404(Employe, user=request.user),
        # 'employe': employe,
        'notifications_unread': notifications_unread
    }
    

    return render(request, './pages/dashboard.html', context)

# def notification(request):
#     return render (request, './pages/notifications.html')
from accounts.models import User
#@permission_required('employer.view_employe', raise_exception=True)
@login_required()
def table(request, *args, **kwargs):
    is_manager = request.user.groups.filter(name='Manager_user').exists()
    if request.user.has_perm('employer.view_all_employes'):
        # Le manager voit tous les employés
        employe = Employe.objects.all()
    else:
        # L'utilisateur simple voit seulement ses propres informations
        try:
            employe = Employe.objects.filter(user=request.user)  
        except Employe.DoesNotExist:
            employe = None
    return render(request, './pages/tables.html', {'employe': employe, 'is_manager' : is_manager })


@permission_required('employer.view_employe', raise_exception=True)
def vuEmployer(request, employer_id, *args):
    context= {'employe' : get_object_or_404(Employe, pk= employer_id)}
    return render(request, './pages/vueEmploye.html', context) 

def vuPaiement(request, employer_id, *args):
    context= {'paiement' : get_object_or_404(Paiement, pk= employer_id)}
    return render(request, './pages/vuePaiement.html', context)


@permission_required('employer.add_employe', raise_exception=True)   
def add(request, *args):    
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employer enregistrer avec succes !')
            return redirect('employer:table')
    else:
        form = EmployerForm()
    return render(request, './pages/ajout_employe.html', {'form':form})   


@permission_required('employer.change_employe', raise_exception=True)
def edit(request, employer_id, *args, **kwargs):
    employer = Employe.objects.get(pk = employer_id)
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES, instance= employer)
        if form.is_valid():
            form.save()
            return redirect('employer:table')
    else:
        form = EmployerForm(instance= employer)      
    return render(request, "./pages/modif.html", {'form':form})


@permission_required('employer.view_employe', raise_exception=True)  
def remove(request, employer_id, *args):
    employer = Employe.objects.get(pk=employer_id)
    employer.delete()
    return redirect('employer:table')

def abscence(request, *args) :
    abscence = None
    is_manager = request.user.groups.filter(name='Manager_user').exists()
    if request.user.has_perm('employer.view_all_employes'):
        abscence = Abscence.objects.all()
    else:
        try:
            employe = Employe.objects.get(user=request.user)  # Trouver l'employé associé à l'utilisateur
            abscence = Abscence.objects.filter(employe=employe)
        except Abscence.DoesNotExist:
            abscence = None
    return render(request, './pages/conge.html', {'title' : 'Gestion Conge', 'abscence': abscence, 'is_manager' : is_manager})


def addConge(request, *args, **kwargs):
    if request.method == 'POST':
        form = AbscenceForm(request.POST)
        if form.is_valid():
            try:
                employe = Employe.objects.get(user=request.user)  # Récupérer l'employé correspondant à l'utilisateur
            except ObjectDoesNotExist:
                messages.error(request, "Votre profil d'employé n'existe pas. Veuillez contacter l'administrateur.")
                return redirect('employer:abscence')
                
            conge = form.save(commit=False)
            conge.employe = employe
            conge.save()

            # Préparation de la description
            description = f"Période : du {conge.date_debut} au {conge.date_fin}"
            # Notification pour les managers
            try:
                manager_group = Group.objects.get(name='Manager_user')
                manager_users = User.objects.filter(groups=manager_group)
                notify.send(
                    sender=employe.user,
                    recipient=manager_users,
                    verb='a soumis une demande de congé',
                    action_object=conge,
                    target=employe.user,
                    description=description
                )

                messages.success(request, "Votre demande de congé a été soumise avec succès.")
            except Group.DoesNotExist:
                messages.error(request, "Le groupe des managers n'existe pas. Veuillez contacter l'administrateur.")

            return redirect('employer:abscence')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = AbscenceForm()

    return render(request, 'pages/ajout_conge.html', {'form': form})


def paiement(request, *args):
    paiement = None
    is_manager = request.user.groups.filter(name='Manager_user').exists()
    if request.user.has_perm('employer.view_all_employes'):
        paiement = Paiement.objects.all()
    else:
        try:
            employe = Employe.objects.get(user=request.user)  # Trouver l'employé associé à l'utilisateur
            paiement = Paiement.objects.filter(employe_id=employe)
        except Abscence.DoesNotExist:
            paiement = None
    context = { 'paiement' : paiement, 'is_manager' : is_manager}
    return render(request, './pages/paiement.html', context)

def addPaiement(request, *args):
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            try:
                employe = Employe.objects.get(user=request.user)  # Récupérer l'employé correspondant à l'utilisateur
            except ObjectDoesNotExist:
                messages.error(request, "Votre profil d'employé n'existe pas. Veuillez contacter l'administrateur.")
                return redirect('employer:paiement')
                
            paiement = form.save(commit=False)
            paiement.employe_id = employe
            paiement.save()

            # Préparation de la description
            description = "type de paiement {} avec un montant de  {}".format(paiement.type_paiement, paiement.montant_total)
            # Notification pour les managers
            try:
                manager_group = Group.objects.get(name='Manager_user')
                manager_users = User.objects.filter(groups=manager_group)
                notify.send(
                    sender=employe.user,
                    recipient=manager_users,
                    verb='a soumis une demande de paiement',
                    action_object=paiement,
                    target=employe.user,
                    description=description
                )

                messages.success(request, "Votre demande de paiement a été soumise avec succès.")
            except Group.DoesNotExist:
                messages.error(request, "Le groupe des managers n'existe pas. Veuillez contacter l'administrateur.")

            return redirect('employer:paiement')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else :
        form = PaiementForm()
        
    return render(request, './pages/ajout_paiement.html', {'form' : form})        
    
from .tasks import somme

def test_task(request):
    result = somme.delay(2000, 1)
    return render(request, './pages/test_task.html', {'resultat' : result})

def result_task(request, task_id):
    result = somme.AsyncResult(task_id)
    if result.ready():
        return render(request, './pages/result_task.html', {'result' : result.result})
    return render(request, './pages/result_task.html', {'result' : 'result no yo ready'}) 

def is_manager(user):
    return user.groups.filter(name='Manager_user').exists()



@login_required
def accepter_demande(request, conge_id):
    conge = get_object_or_404(Abscence, pk=conge_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            conge.status = 'APPROVED'
            messages.success(request, 'La demande a été approuvée.')
        elif action == 'reject':
            conge.status = 'REJECTED'
            messages.success(request, 'La demande a été rejetée.')  
        conge.save()

        # Envoyer une notification à l'employé concerné
        Notification.objects.create(
            recipient=conge.employe.user,
            actor=request.user,
            verb='Votre demande de congé a été ' + ('approuvée' if conge.status == 'APPROVED' else 'rejetée'),
            data={'url': '/employe/conges/'},
            description = 'Votre demande de congé a été' + (' accepter' if conge.status == 'APPROVED' else ' refuser')
        )
    return redirect('employer:tableau')


@login_required
def accepter_paiement(request, paiement_id):
    paiement = get_object_or_404(Paiement, pk=paiement_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            paiement.status = 'APPROVED'
            messages.success(request, 'La demande de paiement a été approuvée.')
        elif action == 'reject':
            paiement.status = 'REJECTED'
            messages.success(request, 'La demande de paiement a été rejetée.')
        paiement.save() 

        # Envoyer une notification à l'employé concerné
        Notification.objects.create(
            recipient=paiement.employe_id.user,
            actor=request.user,
            verb='Votre demande de paiement a été ' + ('approuvée' if paiement.status == 'APPROVED' else 'rejetée'),
            data={'url': '/employe/paiements/'},
            description = 'Votre demande de paiement a été ' + ( 'accepter' if paiement.status == 'APPROVED' else ' refuser' )
        )

    return redirect('employer:tableau')

def notification_detail(request, notification_id):
    employe = get_object_or_404(Employe, user=request.user)

    # Vérifier si l'utilisateur fait partie du groupe Manager
    is_manager = request.user.groups.filter(name='Manager_user').exists()

    # Récupérer les demandes de congé en attente si l'utilisateur est un manager
    demandes_conge = Abscence.objects.filter(status='PENDING') if is_manager else None
    demandes_paiement = Paiement.objects.filter(status='PENDING') if is_manager else None
    # Récupérer la notification par son ID
    notification = get_object_or_404(Notification, pk=notification_id)
    
    # Marquer la notification comme lue si elle ne l'est pas déjà
    if notification.unread:
        notification.mark_as_read()
    
    context = {
        'employe': employe,
        'demandes_paiement' : demandes_paiement,
        'demandes_conge': demandes_conge,
        'notification': notification,
        'is_manager': is_manager,  # Ajout de la variable is_manager au context
    }
    # Afficher la page de détail de la notification
    return render(request, './pages/notifications_detail.html', context)





    # notification = get_object_or_404(Notification, id=notification_id)
    
    # # Vérifie si l'objet action associé à la notification est une demande de congé
    # if notification.action_object and isinstance(notification.action_object, Abscence):
    #     abscence = notification.action_object
    #     abscence.status = 'APPROVED'
    #     abscence.save()
        
    #     # Notifier l'utilisateur que sa demande a été approuvée
    #     notify.send(
    #         sender=request.user,  # Le manager
    #         recipient=abscence.employe.user,  # L'utilisateur ayant soumis la demande
    #         verb='Demande approuvée',
    #         action_object=abscence,
    #         description="Votre demande de congé a été approuvée."
    #     )
        
    #     # Marque la notification initiale comme lue
    #     notification.mark_as_read()
        
    #     messages.success(request, "La demande a été approuvée et l'utilisateur a été notifié.")
    
    # return redirect('employer:tableau')


# def rejeter_demande(request, conge_id):
#     conge = get_object_or_404(Abscence, id=conge_id)
#     conge.status = 'REJECTED'
#     conge.save()

#     # Notifier l'utilisateur
#     notify.send(
#         sender=request.user,
#         recipient=conge.employe.user,
#         verb='Demande de congé rejetée',
#         description="Votre demande de congé du {} au {} a été rejetée.".format(conge.date_debut, conge.date_fin)
#     )

#     return redirect('employer:tableau')
    # notification = get_object_or_404(Notification, id=notification_id)
    
    # # Vérifie si l'objet action associé à la notification est une demande de congé
    # if notification.action_object and isinstance(notification.action_object, Abscence):
    #     abscence = notification.action_object
    #     abscence.status = 'REJECTED'
    #     abscence.save()
        
    #     # Notifier l'utilisateur que sa demande a été rejetée
    #     notify.send(
    #         sender=request.user,  # Le manager
    #         recipient=abscence.employe.user,  # L'utilisateur ayant soumis la demande
    #         verb='Demande rejetée',
    #         action_object=abscence,
    #         description="Votre demande de congé a été rejetée."
    #     )
        
    #     # Marque la notification initiale comme lue
    #     notification.mark_as_read()
        
    #     messages.success(request, "La demande a été rejetée et l'utilisateur a été notifié.")
    
    # return redirect('employer:tableau')
