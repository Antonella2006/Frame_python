from rest_framework import serializers
from .models import Voiture

class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture
        fields = ['marque', 'modele', 'annee', 'prix', 'disponible', 'photo']
