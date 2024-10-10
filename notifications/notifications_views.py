from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from notifications.models import Notification

@login_required
def notifications_page(request):
    """Vue pour afficher la page des notifications."""
    return render(request, './pages/dashboard.html')

@login_required
def mark_as_read(request, notification_id):
    """Vue pour marquer une notification spécifique comme lue."""
    notification = Notification.objects.get(id=notification_id)
    if request.user == notification.recipient:
        notification.mark_as_read()
    return JsonResponse({'status': 'success'})

@login_required
def mark_all_as_read(request):
    """Vue pour marquer toutes les notifications de l'utilisateur comme lues."""
    request.user.notifications.mark_all_as_read()
    return JsonResponse({'status': 'success'})