document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('btnChercher');
    const resultBox = document.getElementById('resultat-box');

    // Autocomplete
    const setupAuto = (inputId, listId, typeId) => {
        const input = document.getElementById(inputId);
        input.addEventListener('input', async () => {
            const query = input.value;
            const type = document.getElementById(typeId).value;
            if (query.length < 2) return;

            try {
                const res = await fetch(`http://127.0.0.1:5000/suggestions?type=${type}&query=${encodeURIComponent(query)}`);
                const data = await res.json();
                document.getElementById(listId).innerHTML = data.map(s => `<option value="${s}">`).join('');
            } catch (e) { console.error(e); }
        });
    };

    setupAuto('valeur1', 'liste-suggestions1', 'type1');
    setupAuto('valeur2', 'liste-suggestions2', 'type2');

    // Recherche
    btn.addEventListener('click', async () => {
        const t1 = document.getElementById('type1').value;
        const v1 = document.getElementById('valeur1').value;
        const t2 = document.getElementById('type2').value;
        const v2 = document.getElementById('valeur2').value;

        resultBox.innerHTML = "⏳ Recherche...";

        try {
            const url = `http://127.0.0.1:5000/recherche_avancee?type1=${t1}&valeur1=${encodeURIComponent(v1)}&type2=${t2}&valeur2=${encodeURIComponent(v2)}`;
            const res = await fetch(url);
            const data = await res.json();

            if (data.joueurs.length > 0) {
                resultBox.innerHTML = data.joueurs.map(j => `
                    <div style="background:#222; padding:8px; margin-bottom:5px; border-left:3px solid #4CAF50; border-radius:4px;">
                        <b style="color:white;">${j.name}</b><br>
                        <small style="color:#aaa;">📍 ${j.current_club_name}</small>
                    </div>
                `).join('');
            } else {
                resultBox.innerHTML = "❌ Aucun joueur trouvé.";
            }
        } catch (e) {
            resultBox.innerHTML = "🚫 Serveur Python non détecté.";
        }
    });
});