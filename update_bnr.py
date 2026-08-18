import urllib.request
import xml.etree.ElementTree as ET
import json
import sys

url = 'https://www.bnr.ro/nbrfxrates.xml'

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as r:
        continut = r.read()

    radacina = ET.fromstring(continut)
    ns = {'b': 'http://www.bnr.ro/xsd'}
    cube = radacina.find('.//b:Cube', ns)
    
    if cube is None:
        print("Eroare: Nu am gasit Cube in XML")
        sys.exit(1)

    data = cube.get('date')
    curs = {}

    for rata in radacina.iter('{http://www.bnr.ro/xsd}Rate'):
        if rata.get('currency') == 'EUR':
            curs = {'eur': float(rata.text), 'date': data}
            break

    if not curs:
        print("Eroare: Nu am gasit EUR in XML")
        sys.exit(1)

    with open('curs.json', 'w') as f:
        json.dump(curs, f)
        
    print("Succes! curs.json a fost creat.")

except Exception as e:
    print(f"Eroare la preluarea BNR: {e}")
    sys.exit(1)
