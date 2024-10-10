from django.db import models 
from accounts.models import User

class Employe(models.Model): 
    name_employe = models.CharField(max_length=20, verbose_name='Nom', blank=False)
    prenom_employe = models.CharField(max_length=25, verbose_name='Prenom', blank=False)
    date_naiss_employe = models.DateField(verbose_name='Date de Naissance', blank=False)
    email_employe = models.EmailField(max_length=50, verbose_name='E-mail', blank=False)
    adresse_employe = models.CharField(max_length=20, verbose_name='Adresse', blank=False)
    tel_employe = models.CharField(max_length=9, verbose_name='Telephone', blank=False)
    image_employe = models.ImageField(upload_to='image_Employe/',  verbose_name='Image Employer', blank=False)
    gr = {
        ("H", "Homme"),
        ("F", "Femme")
    }
    genre_employe = models.CharField(max_length=1, choices=gr, verbose_name='Genre', blank=False)
    diplome_employe = models.ImageField(upload_to='image_diplome_employe/', verbose_name='Image Diplome', blank=False)
    
    p = {
        ('DEV', 'Developpeur'),
        ('RH', 'Gestion Humaine'),
        ('DG', 'Directeur Generale'),
        ('DT', 'Directeur Technique'),
        ('RF', 'Responsable Financier')
    }
    poste_employe = models.CharField(verbose_name='Poste', max_length=3, choices=p, blank=False)
    
    c = {
        ('CDD', 'Contrat a dure determiner'),
        ('CDI', 'Contrat a dure indetermine')
    }
    contrat_employe = models.CharField(max_length=3, choices=c, verbose_name='Contrat', blank=False)
    
    s = {
        ('SD', 'Service de Developpement'),
        ('SR', 'Service de Reseau'),
        ('SRH', 'Services de gestion humaine')
    }
    service_employe = models.CharField(max_length=3, choices=s, verbose_name='Service', blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name_employe
    
    def has_perm(self, perm, obj=None):
        """
        Surcharge le comportement par défaut pour vérifier les permissions des utilisateurs en fonction des rôles ou groupes.
        """
        # Implémenter votre logique de vérification des permissions ici (par exemple, en utilisant user.groups.has_perm(perm))
        return super().has_perm(perm, obj)
    def has_module_perms(self, app_label):
        """
        Surcharge le comportement par défaut pour vérifier les permissions des utilisateurs pour des applications spécifiques.
        """
        # Implémenter votre logique de vérification des permissions ici (par exemple, en utilisant user.is_staff)
        return super().has_module_perms(app_label)

    class Meta:
        verbose_name = 'Employe'
        verbose_name_plural = 'Employes'
        permissions = [
            ("view_all_employes", "Can view all employes"),  # Permission pour les managers
        ]
        
        
class Abscence(models.Model):
    t_a = {
        ('cgM', 'Conge Maladie'),
        ('cgMt', 'Conge Maternite'),
        ('cgE', 'Conge Entreprise'),
        
    }
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvée'),
        ('REJECTED', 'Rejetée'),
    )   
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    type_abscence = models.CharField(max_length=4, choices = t_a,  blank=False,verbose_name='Type de Conge')
    date_debut = models.DateField(verbose_name='Date de debut', blank=False)
    date_fin = models.DateField(verbose_name='Date de fin', blank=False)
    motif = models.TextField(verbose_name='Motif', blank=False)   
    
    def __str__(self):
        return f"{self.employe} - {self.motif} - {self.status}"   
    


class Paiement(models.Model):
    employe_id = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_paiement = models.DateField( verbose_name='Date de Paiement ',  blank=False)
    montant_total = models.DecimalField(verbose_name='Montant Total ', max_digits=10, decimal_places=2 ,blank=False)
    tp = {
        ('CASH', 'Espece'),
        ('CHECK', 'Cheque'),
        ('prime', 'Prime'),
        ('remboursement', 'Remboursement'),
    }
    type_paiement = models.CharField( max_length=13, blank=False,choices=tp, verbose_name='Type de Paiement ')
    st = {
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvée'),
        ('REJECTED', 'Rejetée'),
    }
    status = models.CharField(max_length=9, verbose_name='Statut ', default='PENDING',choices=st, blank=False)
    
    def __str__(self):
        return f"{self.employe_id} - {self.date_paiement} - {self.type_paiement} - {self.status}"  
    
    
