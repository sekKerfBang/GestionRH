from django.urls import path
from . import views

app_name = "employer"

urlpatterns = [
    #path('employerMenu/', views.index, name='indexOfMenu'),
    path('dashboard/', views.tableau, name='tableau'), # ch tableau de bord 
    path('table-employe/', views.table, name='table'), #ch vue de la table 
    path('profile/<int:employer_id>', views.vuEmployer, name='employerVu'), #chemin de la vue du profile
    path('bulletin/<int:employer_id>', views.vuPaiement, name='vuPaiement'),
    path('create-employe/', views.add, name= 'add'), # ajout d'employer
    path('update-employe/<int:employer_id>/', views.edit, name='edit'),
    path('delete-employe/<int:employer_id>/', views.remove, name='delete'), # ch suppression d'employer
    path('conge-employe/', views.abscence, name='abscence'),
    path('create-conge/', views.addConge,  name='addChange'),
    path('paiement-employe/', views.paiement, name='paiement'),
    path('create-paiement/', views.addPaiement, name='addPaiement'),
    path('test/', views.test_task, name='test_task'),
    path('result_task/<str:task_id>', views.result_task, name='result_task'),
    # path('abscence/process/<int:abscence_id>/', views.process_conge, name='process_abscence'),
    path('notification/accepter_conge/<int:conge_id>/', views.accepter_demande, name='accepter_demande'),
    path('notification/accepter_paiement/<int:paiement_id>/', views.accepter_paiement, name='accepter_paiement'),
    path('notification/<int:notification_id>/', views.notification_detail, name='notification_detail'),

    # # URL pour rejeter la demande
    # path('notification/rejeter/<int:notification_id>/', views.rejeter_demande, name='rejeter_demande'),
    # pour l'inscription
    # path('tableauBord/', views.TableauBord, 'tableauBord')
    # #path('employerTablePage/', views.table, name='tableOfEmployer')
    # path('employerDetail/<int:employer_id>/', views.vue, name='vue'), # url correspondant a la vue d'un employer par id
    # path('ajouter-employer/', views.add, name= 'add'), # url pour l'ajout des employers
    # path('modifier-employer/<int:employer_id>/', views.edit, name='edit'), # pour la modification d'un employer
    # path('supprimer-employer/<int:employer_id>/', views.remove, name='delete'), # pour la suppresion d'un employer
]
