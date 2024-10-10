from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register_user, name='register'), # enregistrement nouvel utilisateur 
    path('login/', views.login_user, name='login'), #pour l'identification 
    path('logout/', views.logout_user, name='logout'),
    #path('password_change/', views.change_password, name='change_password'),
# path('MotDePasseOublier/', views.forgotPassword, name='forgotPassword'),
# path('update/', views.update_password, name='update')
]
