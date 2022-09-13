# What you need to run this projects

* Docker (https://docs.docker.com/engine/install/)
* Docker compose (https://docs.docker.com/compose/install/compose-plugin/)


# To start the project in docker (using bash)
```
docker-compose up -d --build
```

and then to see logs :

```
docker ps
docker logs -f <container_name>
```

# To run units tests ( inside the container )

```
docker exec -it <container_name> sh
cd TestTechnique/
python manage.py test --verbosity=2
```

# Test Technique

Un Programme immobilier est caractérisé par :
* Un nom de programme, (ex : Les terrasses de Jade, mais pour l’exercice un nom random est
ok programme xxx),
* Un ensemble d’appartements qui appartiennent à ce programme. (Un appartement ne peut
pas appartenir à deux programmes),
* Un attribut actif ou non pour rendre indisponible un programme. Chaque appartement est caractérisé par :
    * Une surface,
    * Un prix,
    * Un nombre de pièces,
    * Une liste de de caractéristiques : [proche station ski, piscine, jardin, cave, parking, …].

TACHE 1 : Créer le modèle puis créer jeu de données (10 programmes, 20 appartements par programme, 2 caractéristiques par appartement, les prix sont random entre 80k et 300k) pour
nourrir la base de données avec des valeurs aléatoires.
```
python manage.py loaddata sample.json
```

TACHE 2 : Vous devez créer une api pour permettre de :
* Créer un appartement pour un programme,
* Lister tous les appartements :
    * Id (appartement)
    * Id_programme
    * Nom du programme
    * Surface
    * Nombre de pièces
    * Caractéristiques.

TACHE 3 : Créer les fonctions qui permettent d’obtenir un Queryset : (il n’est pas nécessaire de faire une api pour ces fonctions) :

* Lister tous les appartements qui dont le programme est actif. (filtrer sur les relations)
* Lister tous les appartements qui ont un prix entre 100k et 180k. (utilisation de Q expressions)
* Lister tous les programmes qui ont au moins un appartement qui contient une piscine. (filtrer
sur les relations)
* Lister les appartements si le code promo « PERE NOEL » est passé en argument, le prix baisse
de 5% et le libellé du programme est complété de « PROMO SPECIALE » (utiliser les F
expressions + annotate)
* Lister les appartements en ordonnant la réponse en fonction de la saison (fonction de la date
de la requête).
* En hiver (décembre – mars) les appartements qui sont proches des stations de ski
apparaissent en premier, puis tri par prix décroissant, surface décroissante, 
* En été (juin – septembre) les appartements qui ont une piscine apparaissent en
premier, puis tri par prix décroissant, surface décroissante.
* Sinon, le tri est par prix décroissant, surface décroissante.

TACHE 4 : Vérifier que votre programme peut être mis en production (Docker, pytest, …)
Librairies: django, django_rest_framework, pytest + celles dont vous avez besoin. 