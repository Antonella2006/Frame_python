from django.urls import path,include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static   
from rest_framework.routers import DefaultRouter
from voitures.views import VoitureViewSet
from django.contrib.auth import views as auth_views 
router = DefaultRouter()
router.register(r'voitures', VoitureViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'), 
    path('voitures/', views.liste_voitures, name='liste_voitures'), 
    path('voitures/ajouter', views.ajouter_voiture, name='ajouter_voiture'), 
    path('voitures/modifier_voiture/<int:id>/', views.modifier_voiture, name='modifier_voiture'),
    path('voitures/supprimer_voiture/<int:id>/', views.supprimer_voiture, name='supprimer_voiture'),
    path('api/voitures/', views.VoitureListCreate.as_view(), name='voiture_list_create'),
    path('api/voitures/<int:id>/', views.VoitureRetrieveUpdateDestroy.as_view(), name='voiture_detail'),
    path('api/', include(router.urls)),
    path('about/', views.about, name='about'),
    path('ford/', views.ford, name='ford'),
    path('Mercedes/', views.mercedes, name='mercedes'),
    path('Audi/', views.audi, name='audi'),
    path('recherche/', views.recherche_voiture, name='recherche_voiture'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('connexion/', auth_views.LoginView.as_view(), name='connexion'),
    path('ajouter_panier/<int:voiture_id>/', views.ajouter_panier, name='ajouter_panier'),
    path('panier/', views.panier_view, name='panier'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)