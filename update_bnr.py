import urllib.request
import xml.etree.ElementTree as ET
import json
import sys
import urllib.parse

def obtine_curs():
    # Folosim un proxy invers (allorigins) ca să oprim BNR să ne mai dea eroarea 522
    url_direct = 'https://www.bnr.ro/nbrfxrates.xml'
    url_proxy = 'https://api.allorigins.win/raw?url=' + urllib.parse.quote(url_direct, safe='')
    
    adrese = [url_proxy, url_direct]

    for url in adrese:
        try:
            print(f"Încerc: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=20) as r:
                continut = r.read()

            radacina = ET.fromstring(continut)
            ns = {'b': 'http://www.bnr.ro/xsd'}
            cube = radacina.find('.//b:Cube', ns)
            
            if cube is None:
                continue

            data = cube.get('date')
            for rata in radacina.iter('{http://www.bnr.ro/xsd}Rate'):
                if rata.get('currency') == 'EUR':
                    return {'eur': float(rata.text), 'date': data}
        except Exception as e:
            print(f"Eșuat: {e}")
            continue
            
    return None

curs = obtine_curs()

if not curs:
    print("Eroare: Nu am putut prelua cursul de la nicio sursă.")
    sys.exit(1)

with open('curs.json', 'w') as f:
    json.dump(curs, f)
    
print("Succes! curs.json a fost creat.")
