from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Employe, Abscence, Paiement


# @receiver(post_save, sender=Employe)
# def notify_employe_creation(sender, instance, created, **kwargs):
#     if created:
#         # Notification pour la création d'un nouvel employé
#         notify.send(instance, recipient=instance, verb='Nouvel employé créé')
#     else:
#         # Notification pour la mise à jour d'un employé
#         notify.send(instance, recipient=instance, verb='Employé mis à jour')

# @receiver(post_save, sender=Abscence)
# def notify_absence_creation(sender, instance, created, **kwargs):   
#     notify.send(instance.employe.user, recipient=instance.employe.user, verb=f"Nouvelle demande d'absence: {instance.type_abscence}")

# @receiver(post_save, sender=Paiement)
# def notify_paiement_creation(sender, instance, created, **kwargs):
#     notify.send(instance.employe_id, recipient=instance.employe_id, verb=f"Paiement effectué de {instance.montant_total} pour {instance.type_paiement}")