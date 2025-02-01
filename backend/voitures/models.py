from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
class Marque(models.Model):
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom

class Voiture(models.Model):
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    modele = models.CharField(max_length=100)
    annee = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='voitures_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.annee})"

from django.db import models

class AdminSite(models.Model):
    email = models.EmailField(unique=True)
    motdepasse = models.CharField(max_length=255)  # Pas de hachage ici
    
    def __str__(self):
        return self.email  # Vous pouvez retourner l'email ou un autre attribut

    
class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.nom

class Achat(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    date_achat = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.client.nom} - {self.voiture} - {self.date_achat}"

class Panier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.voiture.modele} - {self.quantite}"