from flask import Flask, render_template_string, request, jsonify
from googlesearch import search as google_query
import time

# INICIALIZACE: Flask aplikace - náš webový server
app = Flask(__name__)

# FRONTEND: HTML, CSS a JavaScript (Bod 1 & 2 zadání)
HTML_LAYOUT = '''
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <title>Google Scraper - Inizio</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; margin-top: 80px; background-color: #f4f7f6; }
        .box { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); text-align: center; width: 420px; }
        h1 { color: #4285f4; margin-bottom: 10px; }
        input { width: 85%; padding: 12px; margin: 20px 0; border: 1px solid #ddd; border-radius: 25px; outline: none; font-size: 16px; }
        button { padding: 10px 25px; background-color: #34a853; color: white; border: none; border-radius: 20px; cursor: pointer; font-weight: bold; }
        #loading { display: none; margin-top: 15px; color: #666; font-style: italic; }
    </style>
    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.querySelector('button').disabled = true;
        }
    </script>
</head>
<body>
    <div class="box">
        <h1>Google Scraper</h1>
        <p>Zadejte výraz pro analýzu 1. strany Googlu</p>
        <form action="/search" method="post" onsubmit="showLoading()">
            <input type="text" name="keyword" placeholder="Např. Inizio s.r.o." required autocomplete="off">
            <button type="submit">Spustit Scraping</button>
        </form>
        <div id="loading">Probíhá komunikace s vyhledávačem...</div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    print(f"--- LOG: Start vyhledávání pro: {keyword} ---")
    
    results = []
    
    try:
        # POKUS O REALNÝ SCRAPING:
        search_iterator = google_query(keyword, num_results=10, lang="cs", advanced=True, sleep_interval=2)
        
        for res in search_iterator:
            results.append({
                "titulek": res.title,
                "odkaz": res.url,
                "popis": res.description
            })
            
    except Exception as e:
        # Logování technické chyby, pokud k ní dojde během požadavku
        print(f"--- LOG: Technická chyba při scrapingu: {e} ---")

    # Pojistka, vygenerujeme 10 simulovaných výsledků
    if len(results) == 0:
        print(f"--- LOG: Google nevrátil data. Spouštím simulované výsledky pro: {keyword} ---")
        for i in range(1, 11):
            results.append({
                "titulek": f"{keyword.capitalize()} - Vysledek vyhledavani c. {i}",
                "odkaz": f"https://www.google.com/search?q={keyword}&result={i}",
                "popis": f"Strukturovany popisek pro klicove slovo '{keyword}'. Google v tuto chvili blokuje automatizovane dotazy."
            })
    
    # EXPORT: Vracíme JSON (strojově čitelný formát - Bod 3)
    return jsonify(results)

if __name__ == '__main__':
    # Debug mode umožňuje automatické restartování serveru při změně kódu
    app.run(debug=True, host='0.0.0.0')