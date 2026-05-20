# Comment fonctionne Docker

## 1. Installer et lancer Docker Desktop

Docker Desktop doit être lancé avant d'utiliser les commandes Docker.

## 2. Depuis la racine du projet

docker build --no-cache -f api-devops/Dockerfile -t api-mlp .

3. Lancer le conteneur
docker run -p 8000:8000 api-mlp

4. Ouvrir l'API
http://localhost:8000

5. Ouvrir Swagger pour les GET et POST
http://localhost:8000/docs

6. Exemple de test dans Swagger

Dans `POST /predict`, cliquer sur `Try it out`, puis mettre :

{
  "heure": 8,
  "mois": 3,
  "jour_semaine": 0,
  "Temperature": 18,
  "Pluie_1h": 0,
  "est_vacances": 0,
  "cat_jour": "JOHV",
  "arret": "BECON"
}