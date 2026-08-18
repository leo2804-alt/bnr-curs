import urllib.request
import xml.etree.ElementTree as ET
import json

url = 'https://www.bnr.ro/nbrfxrates.xml'
with urllib.request.urlopen(url, timeout=10) as r:
    radacina = ET.fromstring(r.read())

ns = {'b': 'http://www.bnr.ro/xsd'}
data = radacina.find('.//b:Cube', ns).get('date')
curs = {}

for rata in radacina.iter('{http://www.bnr.ro/xsd}Rate'):
    if rata.get('currency') == 'EUR':
        curs = {'eur': float(rata.text), 'date': data}

with open('curs.json', 'w') as f:
    json.dump(curs, f)
