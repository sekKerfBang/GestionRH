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
from django.http import JsonResponse
import openpyxl
from django.core.paginator import Paginator

@login_required()
def index(request, *args):
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)
    is_manager = request.user.groups.filter(name='Manager_user').exists()
    return render(request,'index.html', {'notifications_unread' : notifications_unread, 'is_manager' : is_manager} )
'''
user.has_perm("employer.view_employe")
'''


@login_required()
def tableau(request, *args):
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
    
    context = {
        'notifications_unread': notifications_unread
    }
    

    return render(request, './pages/dashboard.html', context)

def all_notifications(request):
    # Récupérons toutes les notifications pour l'utilisateur puis ils seront  paginées
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
    all_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    paginator = Paginator(all_notifications, 10)  # Affiche 10 notifications par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'notifications_unread' :notifications_unread
    }
    
    return render(request, './pages/notifications_list.html', context)


# def notification(request):
#     return render (request, './pages/notifications.html')
from accounts.models import User
#@permission_required('employer.view_employe', raise_exception=True)
@login_required()
def table(request, *args, **kwargs):
    is_manager = request.user.groups.filter(name='Manager_user').exists()
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
    if request.user.has_perm('employer.view_all_employes'):
        # Le manager voit tous les employés
        employe = Employe.objects.all()
    else:
        # L'utilisateur simple voit seulement ses propres informations
        try:
            employe = Employe.objects.filter(user=request.user)  
        except Employe.DoesNotExist:
            employe = None
    return render(request, './pages/tables.html', {'employe': employe, 'is_manager' : is_manager, 'notifications_unread' : notifications_unread })


@permission_required('employer.view_employe', raise_exception=True)
def vuEmployer(request, employer_id, *args):
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
    context= {
        'employe' : get_object_or_404(Employe, pk= employer_id),
        'notifications_unread' : notifications_unread
        }
    return render(request, './pages/vueEmploye.html', context) 

def vuPaiement(request, employer_id, *args):
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
    context= {
        'paiement' : get_object_or_404(Paiement, pk= employer_id),
        'notifications_unread' : notifications_unread,
        }
    return render(request, './pages/vuePaiement.html', context)


@permission_required('employer.add_employe', raise_exception=True)   
def add(request, *args):    
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employer enregistrer avec succes !')
            return redirect('employer:table')
    else:
        form = EmployerForm()
    return render(request, './pages/ajout_employe.html', {'form':form, 'notifications_unread' : notifications_unread})   


@permission_required('employer.change_employe', raise_exception=True)
def edit(request, employer_id, *args, **kwargs):
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
    employer = Employe.objects.get(pk = employer_id)
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES, instance= employer)
        if form.is_valid():
            form.save()
            return redirect('employer:table')
    else:
        form = EmployerForm(instance= employer) 
    
    return render(request, "./pages/modif.html", {'form':form, 'notifications_unread' : notifications_unread})


@permission_required('employer.view_employe', raise_exception=True)  
def remove(request, employer_id, *args):
    employer = Employe.objects.get(pk=employer_id)
    employer.delete()
    return redirect('employer:table')

def abscence(request, *args) :
    abscence = None
    is_manager = request.user.groups.filter(name='Manager_user').exists()
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
    if request.user.has_perm('employer.view_all_employes'):
        abscence = Abscence.objects.all()
    else:
        try:
            employe = Employe.objects.get(user=request.user)  # Trouver l'employé associé à l'utilisateur
            abscence = Abscence.objects.filter(employe=employe)
        except Abscence.DoesNotExist:
            abscence = None
    return render(request, './pages/conge.html', {'title' : 'Gestion Conge', 'abscence': abscence, 'is_manager' : is_manager, 'notifications_unread' :notifications_unread })


def addConge(request, *args, **kwargs):
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
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

    return render(request, 'pages/ajout_conge.html', {'form': form, 'notifications_unread' : notifications_unread})


def paiement(request, *args):
    paiement = None
    is_manager = request.user.groups.filter(name='Manager_user').exists()
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
    if request.user.has_perm('employer.view_all_employes'):
        paiement = Paiement.objects.all()
    else:
        try:
            employe = Employe.objects.get(user=request.user)  # Trouver l'employé associé à l'utilisateur
            paiement = Paiement.objects.filter(employe_id=employe)
        except Abscence.DoesNotExist:
            paiement = None
    context = { 'paiement' : paiement,
            'is_manager' : is_manager,
            'notifications_unread' : notifications_unread
            }
    return render(request, './pages/paiement.html', context)

def addPaiement(request, *args):
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]
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
        
    return render(request, './pages/ajout_paiement.html', {'form' : form, 'notifications_unread' : notifications_unread})        
    
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
    # Récupérer l'employé associé à l'utilisateur
    employe = get_object_or_404(Employe, user=request.user)

    # Vérifier si l'utilisateur est dans le groupe "Manager"
    is_manager = request.user.groups.filter(name='Manager_user').exists()
    notifications_unread = Notification.objects.filter(recipient=request.user, unread=True)[:5]

    # Si l'utilisateur est manager, récupérer les demandes de congé et de paiement en attente
    demandes_conge = Abscence.objects.filter(status='PENDING') if is_manager else None
    demandes_paiement = Paiement.objects.filter(status='PENDING') if is_manager else None

    # Récupérer la notification
    notification = get_object_or_404(Notification, pk=notification_id)

    # Marquer la notification comme lue si elle est encore non lue
    if notification.unread:
        notification.mark_as_read()

    # Contexte à passer au template
    context = {
        'notifications_unread' : notifications_unread,
        'employe': employe,
        'demandes_paiement': demandes_paiement,
        'demandes_conge': demandes_conge,
        'notification': notification,
        'is_manager': is_manager,  # Pour utiliser dans le template
    }

    # Afficher la page de détail de la notification
    return render(request, './pages/notifications_detail.html', context)


def get_counts(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "GET":
        try:
            employe_count = Employe.objects.count()
            conge_count = Abscence.objects.filter(status='PENDING').count()
            paiement_count = Paiement.objects.filter(status='PENDING').count()
            user_count = User.objects.count()

            data = {
                'employe_count': employe_count,
                'conge_count': conge_count,
                'paiement_count': paiement_count,
                'user_count' : user_count
            }
            return JsonResponse(data)
        except Exception as e:
            print(f"Erreur dans get_counts: {e}")  # Cela affichera l'erreur dans la console
            return JsonResponse({'error': 'Une erreur est survenue'}, status=500)
        


def export_employers_to_excel(request):
    # Créer un nouveau fichier Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Employers"

    # Ajouter les en-têtes de colonnes
    columns = ["ID", "Nom", "Prénom", "Email", "Adresse", "Téléphone", "Service", "Contrat", "Poste"]
    ws.append(columns)

    # Ajouter les données des employeurs
    employers = Employe.objects.all()  # Ajustez selon votre modèle
    for employe in  employers:
        ws.append([
            str(employe.id),
            employe.name_employe,
            employe.prenom_employe,
            employe.email_employe,
            employe.adresse_employe,
            employe.tel_employe,
            employe.service_employe,
            employe.contrat_employe,
            employe.poste_employe
            
            if employe.service_employe else '',  # Si vous avez un champ relationnel pour le service
        ])

    # Générer la réponse HTTP avec le fichier Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employers.xlsx'
    wb.save(response)
    
    return response
        