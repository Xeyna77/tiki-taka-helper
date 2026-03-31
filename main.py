from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

DATA_DIR = "data"

print("⏳ Chargement des fichiers CSV...")
df_p = pd.read_csv(os.path.join(DATA_DIR, 'players.csv'))
df_c = pd.read_csv(os.path.join(DATA_DIR, 'clubs.csv'), usecols=['club_id', 'name'])
# Appearances est lourd, on ne prend que l'essentiel
df_a = pd.read_csv(os.path.join(DATA_DIR, 'appearances.csv'), usecols=['player_id', 'player_club_id'])

# Listes pour l'autocomplétion
LISTE_PAYS = sorted(df_p['country_of_citizenship'].dropna().unique().tolist())
LISTE_CLUBS = sorted(df_c['name'].dropna().unique().tolist())

print("✅ Serveur prêt sur le port 5000 !")

def obtenir_ids(t, v):
    if not v: return set()
    v = v.lower().strip()
    
    if t == "club":
        # Recherche flexible pour ignorer "FC", "CF", etc.
        v_clean = v.replace("fc", "").replace("cf", "").replace("football club", "").strip()
        match = df_c[df_c['name'].str.contains(v_clean, case=False, na=False, regex=False)]
        if match.empty: return set()
        c_id = match.iloc[0]['club_id']
        return set(df_a[df_a['player_club_id'] == c_id]['player_id'])
    
    elif t == "pays":
        # Dans players.csv, le pays est souvent en anglais (ex: Spain)
        mask = df_p['country_of_citizenship'].str.contains(v, case=False, na=False)
        return set(df_p[mask]['player_id'])
    
    return set()

@app.route('/recherche_avancee')
def api_recherche():
    t1, v1 = request.args.get('type1'), request.args.get('valeur1')
    t2, v2 = request.args.get('type2'), request.args.get('valeur2')
    
    # Intersection des deux ensembles d'IDs
    ids_communs = obtenir_ids(t1, v1).intersection(obtenir_ids(t2, v2))
    
    # Récupération des noms et nettoyage des NaN
    res = df_p[df_p['player_id'].isin(ids_communs)].head(25)
    joueurs = res[['name', 'current_club_name']].fillna("Libre / Retraité").to_dict('records')
    
    return jsonify({"joueurs": joueurs})

@app.route('/suggestions')
def get_suggestions():
    t, q = request.args.get('type'), request.args.get('query', '').lower()
    if t == "club":
        res = [c for c in LISTE_CLUBS if q in c.lower()][:10]
    elif t == "pays":
        res = [p for p in LISTE_PAYS if q in p.lower()][:10]
    else: res = []
    return jsonify(res)

if __name__ == "__main__":
    app.run(port=5000)