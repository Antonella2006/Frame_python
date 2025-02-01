from django.shortcuts import render
from django.http import HttpResponse
from voitures.models import Voiture
from django.shortcuts import render, redirect
from .forms import VoitureForm
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from .serializers import VoitureSerializer
from rest_framework import viewsets


def liste_voitures(request):
    voitures = Voiture.objects.all()
    context = {'voitures': voitures}
    return render(request, 'voitures/liste_voitures.html', context)

def accueil(request):
    return render(request, 'accueil.html')  

def ajouter_voiture(request):
    if request.method == 'POST':
        form = VoitureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
