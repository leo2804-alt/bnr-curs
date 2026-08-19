import urllib.request
import xml.etree.ElementTree as ET
import json
import sys

# Adresa corectă indicată de tine
url = 'https://curs.bnr.ro/nbrfxrates.xml'

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        continut = r.read()

    radacina = ET.fromstring(continut)
    ns = {'b': 'http://www.bnr.ro/xsd'}
    cube = radacina.find('.//b:Cube', ns)
    
    data = cube.get('date')
    
    for rata in radacina.iter('{http://www.bnr.ro/xsd}Rate'):
        if rata.get('currency') == 'EUR':
            curs = {'eur': float(rata.text), 'date': data}
            with open('curs.json', 'w') as f:
                json.dump(curs, f)
            print("Succes! curs.json a fost creat cu valoarea:", curs['eur'])
            sys.exit(0)
            
    print("Eroare: Nu am gasit EUR in XML")
    sys.exit(1)
            
except Exception as e:
    print(f"Eroare: {e}")
    sys.exit(1)
