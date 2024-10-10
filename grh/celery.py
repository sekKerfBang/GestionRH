import os
from celery import Celery

# Définir les paramètres par défaut de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grh.settings')

# Créer l'application Celery
app = Celery('grh')


# Charger les paramètres de Celery depuis Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découvrir les tâches automatiquement
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request : {self.request!r}')