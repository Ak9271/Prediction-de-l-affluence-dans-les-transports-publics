#Importer les outils et lire les données

# importe les bibli
import pandas as pd # manip des tableaux de données
import matplotlib.pyplot as plt # dessiner les graphiques

# charge le fichier CSV dans tableau df
# précise sep=';' car colonnes de fichier sont séparées par ;
df = pd.read_csv('frequentation-gares.csv', sep=';')

# affiche les 5 premières lignes
df.head()



#Calculer et afficher l'évolution globale (2015 - 2024)
#Additionner tous les voyageurs de toutes les gares pour chaque année, et en fait une courbe.

# listes des années
annees = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

# crée nom exact des colonnes
colonnes_voyageurs = [f'Total Voyageurs {annee}' for annee in annees]

# calcule la somme de chaque colonne
evolution_globale = df[colonnes_voyageurs].sum()

# graphique en courbe
plt.figure(figsize=(10, 5))
plt.plot(annees, evolution_globale, marker='o', color='b', linewidth=2)
plt.title('Évolution de la fréquentation des gares en France (2015-2024)')
plt.xlabel('Années')
plt.ylabel('Nombre total de voyageurs')
plt.grid(True)
plt.show()



#Le Top 10 des gares en 2024

# trie le tableau , colonne 2024 ASC
top_10_2024 = df.sort_values(by='Total Voyageurs 2024', ascending=False).head(10)

# dessine un graphique en barres horizontales
plt.figure(figsize=(10, 6))
plt.barh(top_10_2024['Nom de la gare'], top_10_2024['Total Voyageurs 2024'], color='skyblue')

# inverse l'axe Y pour avoir le n°1 en haut
plt.gca().invert_yaxis()

plt.title('Top 10 des gares les plus fréquentées en 2024')
plt.xlabel('Nombre de voyageurs')
plt.ylabel('Nom de la gare')
plt.show()



#Concaténation csv trimestre1, 2, 3 et 4
#Ajout de 4 données semestrielles pour compléter les informations manquantes du csv principal (données de fréquentation journalières ou horaires)

import pandas as pd

# lit les 4 fichiers séparément
df_q1 = pd.read_csv('trimestre1.csv', sep=';')
df_q2 = pd.read_csv('trimestre2.csv', sep=';')
df_q3 = pd.read_csv('trimestre3.csv', sep=';')
df_q4 = pd.read_csv('trimestre4.csv', sep=';')

# empile pour créer l'année
df_2025_complet = pd.concat([df_q1, df_q2, df_q3, df_q4], ignore_index=True)

print(f"Le fichier final contient {len(df_2025_complet)} lignes d'historique de trafic.")

# affiche les 5 premières lignes
df_2025_complet.head()



#Lecture : func pd.read_csv() ouvre chaque trimestre séparément dans la mémoire Python
#Fusion : func pd.concat() prend la liste des 4 tableaux et les colle les uns en dessous des autres pour continuer après fin du trimestre.
#Vérification : print(len(...)) donne le nombre total de lignes du tableau.
#Fait une DB de trafic solide pour alimenter le modèle AI.



#Ajout d'un csv contenant les données météorologie
#Lecture du 

#CHARGEMENT DE LA MÉTÉO
print("1/4 - Chargement du fichier météo...")
df_meteo = pd.read_csv('H_75_latest-2025-2026.csv.gz', sep=';', compression='gzip')

# NETTOYAGE MÉTÉO ET BOUCLIER ANTI-CRASH
print("2/4 - Préparation de la météo...")
colonnes_meteo = ['AAAAMMJJHH', 'NOM_USUEL', 'T', 'RR1']
df_meteo_propre = df_meteo[colonnes_meteo].copy()

df_meteo_propre = df_meteo_propre.rename(columns={
    'AAAAMMJJHH': 'Date_Heure', 'NOM_USUEL': 'Station',
    'T': 'Temperature', 'RR1': 'Pluie_1h'
})

df_meteo_propre['Date_Heure'] = pd.to_datetime(df_meteo_propre['Date_Heure'], format='%Y%m%d%H')
df_meteo_propre['Heure'] = df_meteo_propre['Date_Heure'].dt.hour
df_meteo_propre['Jour_Semaine'] = df_meteo_propre['Date_Heure'].dt.dayofweek

def traduire_jour(jour):
    if jour < 5: return 'JOHV'
    elif jour == 5: return 'SAHV'
    else: return 'DIJFP'

df_meteo_propre['CAT_JOUR'] = df_meteo_propre['Jour_Semaine'].apply(traduire_jour)

#ne garde qu'une seule station météo de référence pour ne pas tout multiplier
df_meteo_propre = df_meteo_propre[df_meteo_propre['Station'] == 'LUXEMBOURG']


# PRÉPARATION TRAFIC ET BOUCLIER ANTI-CRASH 🛡️
print("3/4 - Préparation du trafic...")
df_2025_complet = df_2025_complet[df_2025_complet['TRNC_HORR_60'] != 'ND'].copy()
df_2025_complet['Heure'] = df_2025_complet['TRNC_HORR_60'].str.split('H').str[0].astype(int)

# supprime les doublons exacts causés par la fusion des 4 trimestres
df_2025_complet = df_2025_complet.drop_duplicates(subset=['LIBELLE_ARRET', 'CAT_JOUR', 'Heure'])


# LA GRANDE FUSION SÉCURISÉE
print("4/4 - Fusion des données en cours (sans crash !)...")
df_final = pd.merge(
    left=df_meteo_propre,
    right=df_2025_complet,
    on=['CAT_JOUR', 'Heure'],
    how='inner'
)

print(f"Merge ok, le tableau final contient {len(df_final)} lignes.")
display(df_final.head())



#Exportation du fichier pour IA

# ÉCHANTILLONNAGE
print("Réduction de la taille du jeu de données pour le Membre 2...")

# tire au sort exactement 1 000 000 de lignes.
# le même million de lignes qui sera tiré.
df_final_echantillon = df_final.sample(n=1000000, random_state=42)

print(f"Taille réduite à {len(df_final_echantillon)} lignes.")


# EXPORTATION DU FICHIER POUR IA
print("Création du fichier CSV compressé en cours...")

# exporte tableau allégé
df_final_echantillon.to_csv('donnees_IA_1M.csv.gz', index=False, sep=';', compression='gzip')

print("Fichier 'donnees_IA_1M.csv.gz' prêt !")
