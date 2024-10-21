from django.urls import path
from . import views
from .views import get_counts

app_name = "employer"

urlpatterns = [
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
    path('notifications/', views.all_notifications, name='all_notifications'),
    path('get_counts/', get_counts, name='get_counts'), 
    path('downloads/excel/', views.export_employers_to_excel, name='export_employers_to_excel'),                                                                                                                      
    
]
