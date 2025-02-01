from django.http import HttpResponse
from voitures.models import Voiture,Marque, Panier
from voitures.forms import VoitureForm
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from voitures.serializers import VoitureSerializer
from rest_framework import viewsets
from django.contrib import messages
from django.contrib.auth import login, authenticate
from voitures.forms import AdminAuthForm
from django.contrib.auth.models import User
from voitures.models import AdminSite
from django.contrib.auth.decorators import login_required
def liste_voitures(request):
    voitures = Voiture.objects.all()
    context = {'voitures': voitures}
    return render(request, 'voitures/liste_voitures.html', context)

def accueil(request):
    voitures = Voiture.objects.all()  
    return render(request, 'accueil.html', {'voitures': voitures})

def about(request):
    return render(request, 'about.html')  


def ford(request):
    ford_marque = Marque.objects.get(nom='Ford')
    ford = Voiture.objects.filter(marque=ford_marque)
    return render(request, 'ford.html', {'voitures': ford})

def audi(request):
    audi_marque = Marque.objects.get(nom='Audi')
    audi = Voiture.objects.filter(marque=audi_marque)
    return render(request, 'Audi.html', {'voitures': audi})
    
def admin_home(request):
    return render(request, 'Voitures/liste_voitures.html')


def mercedes(request):
    mercedes_marque = Marque.objects.get(nom='Mercedes')
    mercedes = Voiture.objects.filter(marque=mercedes_marque)
    return render(request, 'Mercedes.html', {'voitures': mercedes})

def ajouter_voiture(request):
    if request.method == 'POST':
        form = VoitureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "La voiture a été ajoutée avec succès !")
            return redirect('liste_voitures')  
    else:
        form = VoitureForm()
    return render(request, 'voitures/ajouter_voiture.html', {'form': form})
def modifier_voiture(request, id):
    
    voiture = get_object_or_404(Voiture, id=id)
    
    if request.method == 'POST':
        form = VoitureForm(request.POST, request.FILES, instance=voiture)  
        if form.is_valid():
            form.save()  
            return redirect('liste_voitures')  
    else:
        form = VoitureForm(instance=voiture)  
    return render(request, 'voitures/modifier_voiture.html', {'form': form, 'voiture': voiture})

def supprimer_voiture(request, id):
    voiture = get_object_or_404(Voiture, id=id)
    
    if request.method == "POST":
        voiture.delete()
        return redirect('liste_voitures')  
    
    return render(request, 'voitures/supprimer_voiture.html', {'voiture': voiture})

class VoitureListCreate(generics.ListCreateAPIView):
    queryset = Voiture.objects.all()
    serializer_class = VoitureSerializer

class VoitureRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voiture.objects.all()
    serializer_class = VoitureSerializer
    queryset = Voiture.objects.all()
    serializer_class = VoitureSerializer


class VoitureViewSet(viewsets.ModelViewSet):
    queryset = Voiture.objects.all()
    serializer_class = VoitureSerializer

def recherche_voiture(request):
    query = request.GET.get('search', '') 
    voitures = Voiture.objects.all() 
    if query:
        voitures = voitures.filter(modele__icontains=query) 

    return render(request, 'accueil.html', {'voitures': voitures})

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Utilise get pour éviter l'exception
        password = request.POST.get('motdepasse')  # Utilise get pour éviter l'exception

        if email and password:
            try:
                admin = AdminSite.objects.get(email=email)
                if password == admin.motdepasse:
                    # Connexion réussie, rediriger vers une page d'admin ou autre
                    return redirect('admin_home')
                else:
                    return render(request, 'Voitures/adminconnex.html', {'error': 'Mot de passe incorrect'})
            except AdminSite.DoesNotExist:
                return render(request, 'Voitures/adminconnex.html', {'error': 'Email non trouvé'})
        else:
            return render(request, 'Voitures/adminconnex.html', {'error': 'Veuillez remplir tous les champs'})
    return render(request, 'Voitures/adminconnex.html')


def ajouter_panier(request, voiture_id):
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez vous connecter pour ajouter des articles au panier.")
        return redirect('admin_login')  # Redirige vers la page de connexion
    # Sinon, ajouter la voiture au panier
    voiture = Voiture.objects.get(id=voiture_id)
    panier = request.session.get('panier', [])
    panier.append(voiture.id)
    request.session['panier'] = panier
    messages.success(request, f"La voiture {voiture.marque} {voiture.modele} a été ajoutée à votre panier.")
    return redirect('panier')

@login_required
def panier_view(request):
    # Récupérer les objets du panier pour l'utilisateur authentifié
    panier = Panier.objects.filter(user=request.user)
    voitures = [item.voiture for item in panier]  # Extraire les voitures du panier
    return render(request, 'panier.html', {'voitures': voitures})


@login_required
def modifier_quantite(request, voiture_id):
    action = request.POST.get('action')
    voiture = Voiture.objects.get(id=voiture_id)
    panier_item = Panier.objects.get(user=request.user, voiture=voiture)

    if action == 'increase':
        panier_item.quantite += 1
    elif action == 'decrease' and panier_item.quantite > 1:
        panier_item.quantite -= 1

    panier_item.save()

    return redirect('panier')