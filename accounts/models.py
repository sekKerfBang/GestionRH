from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    
    def create_superuser(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        """
        Crée et enregistre un super utilisateur avec les privilèges d'administrateur.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le super utilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le super utilisateur doit avoir is_superuser=True.')

        return self.create_user(email, password, first_name, last_name, **extra_fields)
    
    
    def create_staffuser(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        """
        Crée et enregistre un utilisateur du personnel avec l'email et le mot de passe donnés.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', False)  # Un utilisateur staff n'est pas superuser
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, first_name, last_name, **extra_fields)
   

    def create_user(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        """
        Crée et enregistre un utilisateur avec l'email, le mot de passe et d'autres champs supplémentaires.
        """
        if not email:
            raise ValueError('Les utilisateurs doivent avoir une adresse email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
  

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email adresse ', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='Prenom ',max_length=150, null=False, blank=False)
    last_name = models.CharField(verbose_name='Nom ', max_length=150, null=False, blank=False)
    profile_user = models.ImageField(upload_to='profile/', verbose_name='Image ', blank=False, null=False)
    # matricule = models.IntegerField(verbose_name='Matricule')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # Remarquez l'abscence de "champ password", c'est deja integrer pas besoin de preciser
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # par defaut l'email et le password sont requis 
    
        
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        #L'utilisateur est identifier par son adresse e-mail
        return self.email
    
    def short_name(self):
        #L'utilisateur est identifier par son adresse e-mail
        return self.email
    
    def has_perm(self, perm, obj=None):
        """
        Surcharge le comportement par défaut pour vérifier les permissions des utilisateurs en fonction des rôles ou groupes.
        """
        # Implémenter votre logique de vérification des permissions ici (par exemple, en utilisant user.groups.has_perm(perm))
        return super().has_perm(perm, obj)
    
    # def has_perm(self, perm, obj=None):
    #     "L'utilisateur dispose t-il des autorisations necessaires pour voir l'application"
    #     return True
    
    
    def has_module_perms(self, app_label):
        """
        Surcharge le comportement par défaut pour vérifier les permissions des utilisateurs pour des applications spécifiques.
        """
        # Implémenter votre logique de vérification des permissions ici (par exemple, en utilisant user.is_staff)
        return super().has_module_perms(app_label)
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural  = 'utilisateurs'
        permissions = [
            ("view_all_users", "Can view all users"),  # Ajoute une permission pour voir tous les utilisateurs
        ]
            
        
    objects = UserManager()
    
        




















