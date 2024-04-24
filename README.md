ADD Django Rest Framework a un projet

ajouter la dépendance à DRF dans notre fichier requirements.txt  :
> djangorestframework==3.12.4

> pip install -r requirements.txt

déclarer DRF dans la liste des applications installées du fichier  settings.py  du projet Django :
> INSTALLED_APPS = [
'rest_framework',
]

activer l’authentification fournie par DRF pour nous connecter. Éditons notre fichier  urls.py  :
> urlpatterns = [
    path('api-auth/', include('rest_framework.urls'))
]

> python manage.py makemigrations
> python manage.py migrate
> python manage.py createsuperuser

Démarrer serveur de développement et se connecter sur l'API à présent en place :
> python manage.py runserver

