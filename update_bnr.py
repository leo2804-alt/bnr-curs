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

def aduna_stiri_direct(url, sursa, lista):
    # Conexiune directă, fără proxy
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=10) as r:
            radacina = ET.fromstring(r.read())
        for item in radacina.iter('item'):
            titlu = item.findtext('title')
            if titlu:
                lista.append(f"*({sursa})* {titlu.strip()}")
    except Exception as e:
        print(f"Eșuat {sursa}: {e}")

def obtine_stiri(n=3):
    toate_stirile = []
    
    # Surse directe, care funcționează pe GitHub fără proxy
    aduna_stiri_direct('https://www.digi24.ro/rss', 'Digi24', toate_stirile)
    aduna_stiri_direct('https://rss.romaniatv.net/rss.xml', 'RomaniaTV', toate_stirile)
    aduna_stiri_direct('https://rss.antena3.ro/rss.xml', 'Antena3', toate_stirile)
    aduna_stiri_direct('https://rss.b1tv.ro/rss', 'B1TV', toate_stirile)
    
    random.shuffle(toate_stirile)
    return toate_stirile[:n]

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
