import urllib.request
import xml.etree.ElementTree as ET
import json
import sys
import urllib.parse

def obtine_curs_bnr():
    # Listă de adrese (direct + proxy) în caz că BNR blochează unele IP-uri
    adrese = [
        'https://www.bnr.ro/nbrfxrates.xml',
        'https://curs.bnr.ro/nbrfxrates.xml',
        'https://api.allorigins.win/raw?url=' + urllib.parse.quote('https://www.bnr.ro/nbrfxrates.xml', safe='')
    ]

    for url in adrese:
        try:
            print(f"Încerc: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=15) as r:
                continut = r.read()

            radacina = ET.fromstring(continut)
            ns = {'b': 'http://www.bnr.ro/xsd'}
            cube = radacina.find('.//b:Cube', ns)
            
            if cube is None:
                print("Eroare: Nu am gasit Cube in XML")
                continue

            data = cube.get('date')
            
            for rata in radacina.iter('{http://www.bnr.ro/xsd}Rate'):
                if rata.get('currency') == 'EUR':
                    return {'eur': float(rata.text), 'date': data}
                    
            print("Eroare: Nu am gasit EUR in XML")
            
        except Exception as e:
            print(f"Eroare la {url}: {e}")
            continue
            
    return None

curs = obtine_curs_bnr()

if not curs:
    print("Eroare fatală: Nu am putut prelua cursul de la nicio sursă.")
    sys.exit(1)

with open('curs.json', 'w') as f:
    json.dump(curs, f)
    
print("Succes! curs.json a fost creat.")
