from notifications.signals import notify

def send_user_creation_notification(user):
    notify.send(user, verb='Votre compte a ete creer avec succes.')