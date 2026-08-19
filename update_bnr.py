import urllib.request
import xml.etree.ElementTree as ET
import json
import sys

url = 'https://curs.bnr.ro/nbrfxrates.xml'

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as r:
        continut = r.read().decode('utf-8')

    radacina = ET.fromstring(continut)
    
    # Căutăm orice etichetă care se termină cu "Cube" și are atribut "date"
    data_curs = None
    for elem in radacina.iter():
        if elem.tag.endswith('Cube') and elem.get('date'):
            data_curs = elem.get('date')
            break
            
    if not data_curs:
        print("Eroare: Nu am gasit data in XML")
        sys.exit(1)

    # Căutăm orice etichetă care se termină cu "Rate" și are currency="EUR"
    for elem in radacina.iter():
        if elem.tag.endswith('Rate') and elem.get('currency') == 'EUR':
            curs_valoare = float(elem.text)
            curs = {'eur': curs_valoare, 'date': data_curs}
            with open('curs.json', 'w') as f:
                json.dump(curs, f)
            print(f"Succes! curs.json a fost creat cu valoarea: {curs_valoare} (data: {data_curs})")
            sys.exit(0)
            
    print("Eroare: Nu am gasit EUR in XML")
    sys.exit(1)
            
except Exception as e:
    print(f"Eroare: {e}")
    sys.exit(1)
