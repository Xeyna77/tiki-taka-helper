import pandas as pd
import os

DATA_DIR = "data"

def charger_base():
    print("⏳ Chargement des fichiers CSV...")
    df_p = pd.read_csv(os.path.join(DATA_DIR, 'players.csv'))
    # On change 'player_club_name' par 'player_club_id'
    df_a = pd.read_csv(os.path.join(DATA_DIR, 'appearances.csv'), 
                       usecols=['player_id', 'player_club_id'])
    # On a besoin des noms de clubs
    df_c = pd.read_csv(os.path.join(DATA_DIR, 'clubs.csv'),
                       usecols=['club_id', 'name'])
    print("✅ Données prêtes !")
    return df_p, df_a, df_c

def filtrer_par_critere(df_p, df_a, df_c, type_c, valeur):
    valeur = str(valeur).lower().strip()
    
    if type_c == "club":
        # 1. Trouver l'ID du club à partir du nom
        club_match = df_c[df_c['name'].str.contains(valeur, case=False, na=False)]
        if club_match.empty:
            return set()
        c_id = club_match.iloc[0]['club_id']
        
        # 2. Trouver les joueurs ayant cet ID dans appearances
        return set(df_a[df_a['player_club_id'] == c_id]['player_id'])
    
    elif type_c == "pays":
        mask = df_p['country_of_citizenship'].str.contains(valeur, case=False, na=False)
        return set(df_p[mask]['player_id'])
    
    
    
    # ... reste du code (position, etc.)
    return set()