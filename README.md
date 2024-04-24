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

CMDS:
>GET : Permet la lecture d'informations.
Un peu comme un site Internet classique, les appels en GET renvoient des données qui sont généralement du HTML qui est lu et rendu dans le navigateur. Dans le cas d’une API, il s’agit de JSON.

>POST : Permet la création d’entités.
Alors que sur un site les appels en POST peuvent être utilisés pour modifier une entité, dans le cas d’une API, les POST permettent la création.

>PATCH : Permet la modification d’une entité.
PATCH permet la modification de tout ou partie des valeurs des attributs d’une entité pour une API, alors que pour un site classique, nous utilisons un formulaire et un POST.

>DELETE : Permet la suppression d’une entité.
DELETE permet la suppression d’une entité pour une API, alors que pour un site classique, nous utilisons un formulaire et généralement un POST.

>PUT : Permet également la modification d’une entité.
Il est peu utilisé en dehors de l’interface de DRF, que nous verrons ensuite. Pour un site classique, l’action de modification entière d’une entité passe également par un POST au travers d’un formulaire.


