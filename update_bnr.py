import urllib.request
import xml.etree.ElementTree as ET
import json
import sys

def obtine_bnr():
    url = 'https://curs.bnr.ro/nbrfxrates.xml'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            radacina = ET.fromstring(r.read().decode('utf-8'))
        
        data_curs = None
        for elem in radacina.iter():
            if elem.tag.endswith('Cube') and elem.get('date'):
                data_curs = elem.get('date')
                break
                
        curs = {'date': data_curs}
        for elem in radacina.iter():
            if elem.tag.endswith('Rate'):
                moneda = elem.get('currency')
                if moneda in ['EUR', 'USD']:
                    curs[moneda.lower()] = float(elem.text)
        return curs
    except Exception as e:
        print(f"Eroare BNR: {e}")
        return {}

def obtine_stiri_direct(url_rss, sursa, n=3):
    # GitHub are acces liber direct la RSS, nu trebuie ocolit ca pe PythonAnywhere
    try:
        req = urllib.request.Request(url_rss, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            radacina = ET.fromstring(r.read())
        titluri = [item.findtext('title').strip() for item in radacina.iter('item') if item.findtext('title')][:n]
        return titluri
    except Exception as e:
        print(f"Eroare {sursa}: {e}")
    return []

# Main
date_finale = {}
date_finale.update(obtine_bnr())

stiri_hotnews = obtine_stiri_direct('https://rss.hotnews.ro/', 'HotNews')
stiri_libertatea = obtine_stiri_direct('https://www.libertatea.ro/rss', 'Libertatea')

date_finale['stiri'] = stiri_hotnews + stiri_libertatea

if 'eur' in date_finale:
    with open('curs.json', 'w', encoding='utf-8') as f:
        json.dump(date_finale, f, ensure_ascii=False)
    print(f"Succes! Salvat BNR si {len(date_finale['stiri'])} stiri.")
    sys.exit(0)
else:
    print("Eroare fatala la BNR.")
    sys.exit(1)
