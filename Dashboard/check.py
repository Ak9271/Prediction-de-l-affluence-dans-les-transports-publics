import os
import pandas as pd

base = os.getcwd()
parent = os.path.join(base, '..', 'Resultats-Machine Learning')
dirs = os.listdir(parent)
donnees_dir = [d for d in dirs if d.startswith('Don')][0]
csv_path = os.path.join(parent, donnees_dir, 'donnees_IA_finales.csv.gz')
df = pd.read_csv(csv_path, sep=';', usecols=['Station'])
stations = df['Station'].unique()
print(f"Total stations: {len(stations)}")
for s in stations:
    print(s)
