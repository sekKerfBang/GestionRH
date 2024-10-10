# from django.forms import ValidationError
# from django.test import TestCase
# from .models import Employer

# class EmployerModelTest(TestCase):
#     def test_create_employer(self):
#         employer = Employer(
#             name_employer="Doe",
#             prenom_employer="John",
#             date_naiss_employer="1990-01-01",
#             email_employer="john.doe@example.com",
#             adresse_employer="123 Main St",
#             tel_employer="1234567890",
#             poste_employer="Developer",
#             genre_employer="H"
#         )
#         employer.save()
#         self.assertIsInstance(employer, Employer)

#     def test_employer_str_representation(self):
#         employer = Employer(name_employer="Doe", prenom_employer="John")
#         self.assertEqual(str(employer), "Doe")
        
#     def test_employer_email_unique(self):
#         employer1 = Employer.objects.create(
#             name_employer="Doe",
#             prenom_employer="John",
#             date_naiss_employer="1990-01-01",
#             email_employer="john.doe@example.com",
#             adresse_employer="123 Main St",
#             tel_employer="1234567890",
#             poste_employer="Developer",
#             genre_employer="H"
#         )
#         employer2 = Employer(
#             name_employer="Doe",
#             prenom_employer="Jane",
#             date_naiss_employer="1990-01-01",
#             email_employer="john.doe@example.com",  # Duplication de l'email
#             adresse_employer="456 Main St",
#             tel_employer="9876543210",
#             poste_employer="Designer",
#             genre_employer="F"
#         )
#         with self.assertRaises(ValidationError):
#             employer2.full_clean()
    
#     def test_employer_genre_choices(self):
#         employer = Employer(
#             name_employer="Doe",
#             prenom_employer="John",
#             date_naiss_employer="1990-01-01",
#             email_employer="john.doe@example.com",
#             adresse_employer="123 Main St",
#             tel_employer="1234567890",
#             poste_employer="Developer",
#             genre_employer="X"  # Valeur invalide
#         )
#         with self.assertRaises(ValidationError):
#             employer.full_clean()