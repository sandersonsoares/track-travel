# 04/11: uma parada por loja, com o produto e o comprador no nome (lista fechada em 01/11).
import json, copy, math
P = 'src/data/foz-do-iguacu.json'
d = json.load(open(P)); day = d['days'][1]; assert day['date'] == '2026-11-04'
cur = day['items']
OLD = {i['name']: i for i in json.load(open('scripts/foz-do-iguacu.backup-2026-11-01-antes-compras-quarta.json'))['days'][1]['items']}
def f(p, src=None):
    src = src or cur
    return copy.deepcopy(next(i for i in (src if isinstance(src, list) else src.values()) if i['name'].startswith(p)))
def dist(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 6371000 * math.hypot((lo2 - lo1) * math.cos((la1 + la2) / 2), la2 - la1)
ORDER = ['time', 'end', 'type', 'name', 'note', 'lat', 'lng', 'image', 'leg', 'place', 'cost', 'costDetails', 'alternatives']
ZERO = {'unit': 'pessoa', 'fullPerPerson': 0, 'halfPerPerson': 0, 'halfApplies': True, 'payPerPerson': 0, 'people': 3,
        'totalGroup': 0, 'status': 'oficial', 'checkedAt': '2026-11-01', 'note': 'Compras fora do orçamento turístico.'}
def gm(q): return 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '%20')
def novo(name, note, lat, lng, place):
    place.setdefault('photos', []); place.setdefault('googleMapsUrl', gm(name.split(' · ')[0] + ' Ciudad del Este'))
    return {'type': 'activity', 'name': name, 'note': note, 'lat': lat, 'lng': lng, 'place': place, 'cost': 0, 'costDetails': copy.deepcopy(ZERO)}
def rename(x, name, note=None):
    x['name'] = name
    if note is not None: x['note'] = note
    x.pop('alternatives', None); return x

head = cur[:3]  # café, saída, estacionamento
ac1 = rename(f('Atacado Connect (Jebai)'), 'Atacado Connect (Jebai 3º/4º) · ver e negociar: iPhone 18 Pro Max Bordô (Gracinha) e 18 Pro Bordô (Sanderson)')
cam = rename(f('Câmbio'), 'La Moneda (dentro do Jebai) · câmbio: dólar dos três (Gracinha, Sanderson e Hortência)')
ac2 = rename(f('Atacado Connect · COMPRA'), 'Atacado Connect (Jebai) · COMPRA iPhone 18 Pro Max Bordô (Gracinha) + Fino condicionador 550ml (Hortência)',
    'Pagar com o dólar recém-trocado. iPhone: testar, conferir caixa lacrada, IMEI da caixa = do aparelho, modelo LL e nota fiscal. '
    'Plano B no mesmo prédio: Mestre Atacado (4º piso, nº 3353), 18 Pro Max Bordô US$ 1.485, aceita Pix (não aceita cartão). '
    'Se o Sanderson fechar o 18 Pro por ≤ US$ 1.249 aqui, comprar o dele também e pular o Prime Shop. '
    'Hortência: Fino condicionador 550ml (se não tiver, comprar na Nissei, mais tarde).')
J = (ac1['lat'], ac1['lng'])
star = novo('Star Company (Jebai 1º, loja 2017) · Medicube, Fino, Victoria\'s Secret e Numbuzin (Hortência)',
    'Medicube: Exosome Shot 2000, Zero Pore Pad 2.0, TXA Niacinamide 15% e Collagen Night Wrapping Mask. '
    'Fino: máscara, óleo, sérum Airy Smooth e shampoo. Victoria\'s Secret Body Splash Pure Seduction 250ml. Numbuzin No.9 creme de olhos. '
    'Pagar em dólar. Avaliações citam demora na retirada e suspeita de falsificados: conferir lacre e lote. '
    'Se a retirada demorar, há outra Star Company no Shopping Paris (térreo, lojas 30–31), na parada do almoço.',
    -25.5108, -54.6100, {'address': 'Galería Jebai Center, 1º andar, loja 2017 · Av. Carlos Antonio López, Ciudad del Este',
    'hours': 'Seg–sex 7h–16h · sáb 6h30–15h', 'phone': '+595 991 959017', 'whatsapp': 'https://wa.me/595993085626',
    'instagram': 'https://instagram.com/starcompanypy.oficial'})
extra = novo('Extra Shop (Jebai térreo, loja 2016) · SKIN1004 Centella Ampoule 55ml (Hortência)',
    'SKIN1004 Madagascar Centella Ampoule 55ml. Loja vizinha da Star Company. Pagar em dólar.',
    -25.5102, -54.6096, {'address': 'Galería Jebai Center, térreo, loja 2016 · Av. Carlos Antonio López, Ciudad del Este',
    'hours': 'Confirmar (Jebai seg–sáb ~7h–16h)', 'whatsapp': 'https://wa.me/595983222219'})
sg = rename(f('Star Games'), 'Star Games (Jebai 3º, loja 3264) · capinhas TechWoven para os iPhones (Sanderson e Gracinha)')
prime = rename(f('Prime Shop'), 'Prime Shop (Hijazi 4º, sala 417) · COMPRA iPhone 18 Pro Bordô (Sanderson)')
prime['note'] = prime['note'].split(' Nissei fica no mesmo prédio')[0].split(' 👩')[0]
nis = rename(f('Nissei', OLD), 'Nissei (Hijazi) · Fino condicionador 550ml (Hortência, se faltou) e capa TechWoven original (opcional)',
    'Fino condicionador 550ml, se não achou na Atacado Connect. Capa TechWoven original lacrada: US$ 79–85 (a da Star Games sai ~US$ 25). '
    'A fila no caixa cresce depois das 11h, então comprar agora. Seg–sáb 6h30–15h45.')
nis['leg'] = {'mode': 'walk', 'minutes': 0, 'label': 'Mesmo prédio'}
lai = f('Lai Lai')
point = rename(lai, 'Point Informática (Lai Lai 4º, loja 408) · microfone Hollyland Lark M2 Combo (Hortência)',
    'Microfone Hollyland Lark M2 Combo. Seg–sáb 7h30–16h30; WhatsApp +595 973 519759. Alternativa: Intershop (Shopping DFS). '
    'No mesmo andar: Matrix e Visão Vip (notebooks/MacBook) para dar uma olhada. Se a Gracinha mudar para o 17 Pro Max, perguntar se esta Matrix é a "Matrix Importados" (Laranja US$ 1.170).')
point['place'] = dict(point['place'], address='Lai Lai Center, 4º andar, loja 408 · Av. Adrián Jara, Ciudad del Este', whatsapp='https://wa.me/595973519759', hours='Seg–sáb 7h30–16h30')
cell = rename(f('CellShop'), 'CellShop (Shopping Ibiza) · rímel Maybelline Sky High (Hortência, backup) e comparar Eros Parfum (US$ 85)',
    'Rímel Maybelline Sky High: comprar aqui se a Paris Store não confirmar estoque até terça (a Paris Store só vem às 12h40). '
    'Eros Parfum aqui está US$ 85, mais caro que na Ponto Com e na Mega: só comparar. Seg–sex 6h30–17h.')
eleg = f('Elegancia')
brands = novo('Brands Shop · Celimax Vita-A Retinal Shot (Hortência)',
    'Celimax Vita-A Retinal Shot (substituto do IOPE Retinol Shot). Seg–sáb 7h–16h30; WhatsApp +595 992 979 800. Tem outlet no último andar.',
    -25.5098, -54.6109, {'address': 'Av. Monseñor Rodríguez · Ciudad del Este, Paraguai', 'hours': 'Seg–sáb 7h–16h30 · dom 7h–15h',
    'phone': '+595 61 50603', 'whatsapp': 'https://wa.me/595992979800'})
mona = f('Monalisa'); mona.pop('alternatives', None)
opc = []
for k in ('Terra Nova', 'Digital Center'):
    t = f(k); opc.append({'name': t['name'] + ' (se sobrar tempo)', 'lat': t['lat'], 'lng': t['lng'], 'note': t['note'].split(' Capinhas, plano B')[0], 'place': t['place']})
mona['alternatives'] = opc
pc = rename(f('Ponto Com'), 'Ponto Com · Eros Parfum 100ml US$ 70 (perfume) + Dr. Althea 345 Relief Cream 50ml (Hortência)',
    'Eros Parfum 100ml US$ 70, o mais barato (estoque a confirmar: WhatsApp +595 994 510 072 na terça). Se não tiver, comprar na Mega (próxima parada). '
    'Hortência: Dr. Althea 345 Relief Cream 50ml. Conferir o valor antes de pagar no cartão (há relato de cobrança duplicada); Pix às vezes indisponível.')
mega = rename(f('Mega Eletrônicos'), 'Mega Eletrônicos · Eros Energy 100ml US$ 67 (+ Eros Parfum US$ 77 se faltou na Ponto Com)')
alm = f('Almoço'); alm.pop('alternatives', None); alm = f('Almoço')
paris = rename(f('Shopping Paris'), 'Paris Store (Shopping Paris 2º) · rímel Sky High, MAC blush Sheertone e base Studio Radiance (Hortência)',
    'Rímel Maybelline Sky High, MAC blush Sheertone e MAC base Studio Radiance; perguntar por MAC paleta e Studio Fix. WhatsApp +595 993 005 000. '
    'No térreo: Star Company (lojas 30–31), se faltou algo no Jebai. O Shopping Paris tem perfumaria grande e loja da Matrix. Aberto até 19h.')
china = f('Shopping China')
nz = rename(f('New Zone'), 'New Zone (Shopping del Este 3º) · MAC batom (Hortência) + plano C do iPhone do Sanderson',
    'Hortência: MAC batom; perguntar por MAC paleta e Studio Fix, se não achou na Paris Store. '
    'Plano C do iPhone do Sanderson: 18 Pro Bordô US$ 1.295 (Pix Especial 9h30–16h via Call Center). Capinha C-Covers TechWoven US$ 17. '
    'Pagar em dólar: no cartão o câmbio para guarani sai ~3,5% pior. Aberto até 22h.')
cela = f('Café da tarde'); cela['note'] = cela['note'].replace('Sair às 15h25', 'Sair às 15h15')
tail = cur[cur.index(next(i for i in cur if i['name'].startswith('Pegar o carro'))):]
plan = [(ac1, '06:00', '07:00'), (cam, '07:00', '07:15'), (ac2, '07:15', '07:45'), (star, '07:45', '08:10'), (extra, '08:10', '08:20'),
        (sg, '08:20', '08:35'), (prime, '08:40', '09:20'), (nis, '09:20', '09:30'), (point, '09:35', '09:55'), (cell, '10:00', '10:15'),
        (eleg, '10:17', '10:30'), (brands, '10:33', '10:43'), (mona, '10:45', '11:10'), (pc, '11:15', '11:30'), (mega, '11:33', '11:50'),
        (alm, '12:00', '12:40'), (paris, '12:40', '13:15'), (china, '13:25', '13:55'), (nz, '14:05', '14:30'), (cela, '14:35', '15:15')]
out = list(head); prev = None
for x, t, e in plan:
    x['time'], x['end'] = t, e
    p = (x['lat'], x['lng'])
    if prev is not None:
        m = dist(prev, p)
        if (x.get('leg') or {}).get('label') == 'Mesmo prédio' or m <= 40:
            x['leg'] = {'mode': 'walk', 'minutes': 0, 'label': 'Mesmo prédio' if m <= 40 else x['leg']['label']}
        else:
            x['leg'] = {'mode': 'walk', 'minutes': max(2, math.ceil(m / 60)), 'label': f'{round(m, -1):.0f} m'}
    prev = p
    out.append({k: x[k] for k in ORDER if k in x})
out += tail
day['items'] = out
day['note'] = day['note'].replace('Saída do Paraguai às 15h25', 'Saída do Paraguai às 15h15')
day['note'] = day['note'].replace('Ordem otimizada (tudo a pé, sem vai e volta): ', 'Cada parada traz no nome o que comprar e quem compra. Ordem otimizada (tudo a pé, sem vai e volta): ')
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); open(P, 'a').write('\n')
def mm(t): h, m = map(int, t.split(':')); return h * 60 + m
for a, b in zip(out, out[1:]):
    lg = (b.get('leg') or {}).get('minutes', 0); fol = mm(b['time']) - mm(a.get('end', a['time'])) - lg
    print(f"{'⚠️' if fol<0 else '  '} {b['time']}-{b.get('end',''):5} | {b['name'][:110]}")
