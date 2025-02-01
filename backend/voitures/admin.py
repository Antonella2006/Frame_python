from django.contrib import admin
from .models import Marque, Voiture, Client, Achat, AdminSite, Panier

admin.site.register(Marque)
admin.site.register(Voiture)
admin.site.register(Client)
admin.site.register(Achat)
admin.site.register(AdminSite)
admin.site.register(Panier)