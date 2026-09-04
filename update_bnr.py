import urllib.request
import xml.etree.ElementTree as ET
import json
import sys
import random

def obtine_bnr():
    url = 'https://curs.bnr.ro/nbrfxrates.xml'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
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

def obtine_stiri(n=10):
    # Surse cu numele complete
    surse = [
        ('https://www.libertatea.ro/rss', 'Libertatea'),
        ('https://rss.hotnews.ro/', 'HotNews'),
        ('https://www.digi24.ro/rss', 'Digi24')
    ]
    random.shuffle(surse) # Amestecăm lista ca să vină aleatoriu!
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    for url, sursa in surse:
        try:
            print(f"Încerc știri de la: {sursa}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                radacina = ET.fromstring(r.read())
            # Punem sursa completă între paranteze și bold
            titluri = [f"*({sursa})* {item.findtext('title').strip()}" for item in radacina.iter('item') if item.findtext('title')][:n]
            if titluri:
                print(f"Succes știri de la {sursa}!")
                return titluri
        except Exception as e:
            print(f"Eșuat {sursa}: {e}")
            
    return []

# Main
date_finale = {}
date_finale.update(obtine_bnr())
date_finale['stiri'] = obtine_stiri()

if 'eur' in date_finale:
    with open('curs.json', 'w', encoding='utf-8') as f:
        json.dump(date_finale, f, ensure_ascii=False)
    print(f"Succes! Salvat BNR si {len(date_finale['stiri'])} stiri.")
    sys.exit(0)
else:
    print("Eroare fatala la BNR.")
    sys.exit(1)
