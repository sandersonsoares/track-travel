# 04/11: encaixa as lojas da pesquisa de perfumes (Eros Energy / Eros Parfum, 01/11): CellShop, Ponto Com e Mega.
import json, copy, math
P = 'src/data/foz-do-iguacu.json'
B = 'scripts/foz-do-iguacu.backup-2026-11-01-antes-compras-quarta.json'
d = json.load(open(P)); day = d['days'][1]; assert day['date'] == '2026-11-04'
old = {i['name']: i for i in json.load(open(B))['days'][1]['items']}
def g(src, prefix): return copy.deepcopy(next(v for k, v in src.items() if k.startswith(prefix)))
cur = {i['name']: i for i in day['items']}
def dist(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 6371000 * math.hypot((lo2 - lo1) * math.cos((la1 + la2) / 2), la2 - la1)
ORDER = ['time', 'end', 'type', 'name', 'note', 'lat', 'lng', 'image', 'leg', 'place', 'cost', 'costDetails', 'alternatives']
zero = {'unit': 'pessoa', 'fullPerPerson': 0, 'halfPerPerson': 0, 'halfApplies': True, 'payPerPerson': 0, 'people': 3,
        'totalGroup': 0, 'status': 'oficial', 'checkedAt': '2026-11-01', 'note': 'Compras fora do orçamento turístico.'}
cell = g(old, 'CellShop'); cell.pop('alternatives', None)
cell['name'] = 'CellShop · perfumes (Eros Parfum US$ 85)'
cell['note'] = 'Ao lado da Elegancia. Só para comparar: Eros Parfum 100ml US$ 85 (mais caro que Ponto Com e Mega). Pagar em dólar.'
mega = g(old, 'Mega Eletrônicos'); mega.pop('alternatives', None)
mega['name'] = 'Mega Eletrônicos · COMPRA Eros Energy (US$ 67) e Eros Parfum (US$ 77)'
mega['note'] = ('🥇 Eros Energy 100ml US$ 67, em estoque (o mais barato). Eros Parfum 100ml US$ 77, em estoque: comprar aqui se a Ponto Com (parada anterior) não tiver. '
                'Avaliações citam fila no caixa. Fecha 16h30.')
pc = copy.deepcopy(mega)
pc.update(name='Ponto Com · Eros Parfum (US$ 70)', lat=-25.5111, lng=-54.6082, image=None,
    note='🥇 Eros Parfum 100ml US$ 70 (estoque a confirmar: WhatsApp +595 994 510 072 na terça). Se não tiver, comprar na Mega (próxima parada). '
         'Perfumes, maquiagem e cosméticos originais. Conferir valor antes de pagar no cartão (há relato de cobrança duplicada); Pix às vezes indisponível.',
    place={'address': 'Av. Adrián Jara esq. Itá Ybaté · Ciudad del Este, Paraguai', 'hours': 'Seg–sex 7h–16h · sáb 6h30–15h30',
           'phone': '+595 61 515 125', 'whatsapp': 'https://wa.me/595994510072', 'website': 'https://pontocom.com/', 'photos': [],
           'googleMapsUrl': 'https://www.google.com/maps/search/?api=1&query=Ponto%20Com%20Ciudad%20del%20Este'},
    cost=0, costDetails=zero)
pc.pop('image')
names = [i['name'] for i in day['items']]
def find(p): return next(i for i in day['items'] if i['name'].startswith(p))
head = day['items'][:names.index(find('Lai Lai')['name'])]
tail = day['items'][names.index(find('Almoço')['name']):]
seq = [(find('Lai Lai'), '09:05', '09:20'), (cell, '09:25', '09:45'), (find('Elegancia'), '09:47', '10:05'),
       (find('Monalisa'), '10:10', '10:35'), (find('Terra Nova'), '10:40', '11:00'), (find('Digital Center'), '11:05', '11:25'),
       (pc, '11:30', '11:45'), (mega, '11:48', '12:10')]
times = {'Almoço': ('12:20', '13:00'), 'Shopping Paris': ('13:00', '13:30'), 'Shopping China': ('13:40', '14:15'),
         'New Zone': ('14:25', '14:45'), 'Café da tarde': ('14:50', '15:25')}
prev = (find('Prime Shop')['lat'], find('Prime Shop')['lng']); mid = []
for x, t, e in seq + [(i, None, None) for i in tail]:
    x = copy.deepcopy(x)
    k = next((k for k in times if x['name'].startswith(k)), None)
    if t: x['time'], x['end'] = t, e
    elif k: x['time'], x['end'] = times[k]
    if (t or k) and 'lat' in x:
        p = (x['lat'], x['lng']); m = dist(prev, p)
        if (x.get('leg') or {}).get('label') != 'Mesmo prédio' and m > 20:
            x['leg'] = {'mode': 'walk', 'minutes': max(2, math.ceil(m / 60)), 'label': f'{round(m, -1):.0f} m'}
        prev = p
    mid.append({kk: x[kk] for kk in ORDER if kk in x})
day['items'] = head + mid
for i in day['items']:
    if i['name'].startswith('Shopping China'): i['note'] += ' Perfumes: Eros Energy US$ 92 e Eros Parfum US$ 87 aqui (mais caros que na Mega/Ponto Com).'
    if i['name'].startswith('New Zone'): i['note'] += ' Eros Parfum US$ 95 aqui (o mais caro).'
    if i['name'].startswith('Digital Center'): i['note'] = i['note'].replace('WhatsApp +595 974 314441.', 'WhatsApp +595 974 314441. Eros Parfum US$ 91 na Madrid Center.')
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); open(P, 'a').write('\n')
def mm(t): h, m = map(int, t.split(':')); return h * 60 + m
it = day['items']
for a, b in zip(it, it[1:]):
    leg = (b.get('leg') or {}).get('minutes', 0)
    print(f"{b['time']}-{b.get('end',''):5} folga {mm(b['time'])-mm(a.get('end',a['time']))-leg:>3} | {b['name'][:60]} | {(b.get('leg') or {}).get('label','')[:25]}")
