from django import forms
from .models import Voiture, Client, Achat , AdminSite
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = ['marque', 'modele', 'annee', 'prix', 'disponible', 'photo']
        widgets = {
            'marque': forms.Select(),
            'modele': forms.TextInput(attrs={'placeholder': 'Ex: Modèle de voiture'}),
            'annee': forms.NumberInput(attrs={'placeholder': 'Ex: 2020'}),
            'prix': forms.NumberInput(attrs={'placeholder': 'Ex: 25000'}),
            'disponible': forms.CheckboxInput(),
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'email', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom du client'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'placeholder': 'Numéro de téléphone'}),
        }


class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['client', 'voiture', 'date_achat', 'montant']
        widgets = {
            'client': forms.Select(),
            'voiture': forms.Select(),
            'date_achat': forms.DateInput(attrs={'type': 'date'}),
            'montant': forms.NumberInput(attrs={'placeholder': 'Prix total'}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AuthClientForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class EvaluationForm(forms.Form):
    note = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)
    commentaire = forms.CharField(widget=forms.Textarea, required=False)


class AdminAuthForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Les informations d'identification sont incorrectes.")
            if not user.is_staff:  # Vérifier si l'utilisateur est bien un administrateur
                raise forms.ValidationError("Vous devez être un administrateur pour vous connecter.")
        return cleaned_data
