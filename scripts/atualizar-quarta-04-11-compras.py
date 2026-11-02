# Reorganiza 04/11 (Paraguai): compras dos iPhones logo cedo no Jebai/Hijazi, câmbio, capinhas TechWoven,
# saída do Paraguai antes do pico e pausa no Airbnb antes do Yup Star.
# Rodar na raiz: python3 scripts/atualizar-quarta-04-11-compras.py
import json, copy, math
P = 'src/data/foz-do-iguacu.json'
d = json.load(open(P))
day = d['days'][1]
assert day['date'] == '2026-11-04'
old = {i['name']: i for i in day['items']}
def g(prefix):
    return copy.deepcopy(next(v for k, v in old.items() if k.startswith(prefix)))
CHK = '2026-11-01'
def dist(a, b):
    R = 6371000
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    x = (lo2 - lo1) * math.cos((la1 + la2) / 2); y = la2 - la1
    return R * math.hypot(x, y)
def zero(note='Compras fora do orçamento turístico.'):
    return {'unit': 'pessoa', 'fullPerPerson': 0, 'halfPerPerson': 0, 'halfApplies': True, 'payPerPerson': 0,
            'people': 3, 'totalGroup': 0, 'status': 'oficial', 'checkedAt': CHK, 'note': note}
ORDER = ['time', 'end', 'type', 'name', 'note', 'lat', 'lng', 'image', 'leg', 'place', 'cost', 'costDetails', 'alternatives']
def fmt(x): return {k: x[k] for k in ORDER if k in x}

cafe, saida, estac = g('Café da manhã no Airbnb'), g('Saída do Airbnb'), g('Estacionar')
cell = g('CellShop'); jebai = g('Galeria Jebai'); nissei = g('Nissei'); laila = g('Lai Lai')
eleg, mona, terra, digi = g('Elegancia'), g('Monalisa'), g('Terra Nova'), g('Digital Center')
alm, paris, china, newz, cela = g('Almoço'), g('Shopping Paris'), g('Shopping China'), g('New Zone'), g('Café da tarde')
carro, yup, marco, jantar, airbnb = g('Pegar o carro'), g('Yup Star'), g('Marco'), g('Jantar'), g('Airbnb Solar')
moto_leg = copy.deepcopy(cell['leg']); moto_leg['minutes'] = 30
moto_leg['label'] = 'Mototáxi pela Ponte da Amizade (1 por pessoa, combinar o preço antes, capacete) + aduana + 5 min a pé até o Jebai'

JEB = (-25.5105, -54.6099); HIJ = (-25.5111, -54.6096)
jplace = copy.deepcopy(jebai['place']); jplace.pop('phone', None)
jplace['address'] = 'Galería Jebai Center · Av. Monseñor Rodríguez c/ Av. Carlos Antonio López, Ciudad del Este'
jplace['hours'] = 'Galeria seg–sáb ~7h–16h · Atacado Connect seg–sex 6h–16h'
for k in ('lookupKey', 'checkedAt'): jplace.pop(k, None)

def item(base, **kw):
    x = copy.deepcopy(base); x.pop('alternatives', None); x.update(kw); return x

items = [cafe, saida, estac]
items.append(item(jebai, time='06:00', end='07:00', name='Atacado Connect (Jebai) · ver, testar e negociar os iPhones',
    note='1ª parada, logo na abertura (6h). Atacado Connect fica no Jebai, 3º/4º andar (vendedor Kellynton; não faz reserva). '
         'GRACINHA: pedir o 18 Pro Max 256GB Bordô LL por US$ 1.450 — exigir LACRADO (evitar o anúncio "Deslacrado"), conferir modelo LL e nota. '
         'SANDERSON: negociar o 18 Pro Bordô por ≤ US$ 1.249 (pedir US$ 1.230; débito ≈ +6%). Se não baixar, a compra dele é no Prime Shop (Hijazi, ao lado). '
         'Se o Jebai ainda estiver fechado, esperar na entrada da Av. Monseñor Rodríguez (abre 7h).',
    lat=JEB[0], lng=JEB[1], leg=moto_leg, place=copy.deepcopy(jplace), cost=0, costDetails=zero()))
items.append(item(jebai, time='07:00', end='07:20', type='activity', name='Câmbio · La Moneda (dentro do Jebai)',
    note='Trocar reais por dólar logo que abrir: ≈ US$ 1.450 da Gracinha + ≈ US$ 193 do Sanderson (separar R$ 1.170). Cotação ≈ 5,43. '
         'Confirmar antes se aceita Pix (+595 985 600049). Se não aceitar: Ita Cambios Matriz (Calle Curupayty 300, Globo Center; 5,45; aceita Pix; 7h–15h30). '
         'Notas novas, conferir na hora.',
    lat=JEB[0], lng=JEB[1], leg={'mode': 'walk', 'minutes': 0, 'label': 'Mesmo prédio'}, place=dict(copy.deepcopy(jplace), address='La Moneda · Galería Jebai Center, Ciudad del Este', hours='Confirmar horário (Ita Matriz: seg–sex 7h–15h30)', phone='+595 985 600049'),
    cost=0, costDetails=zero('Câmbio: só a troca de moeda.')))
items.append(item(jebai, time='07:20', end='07:50', name='Atacado Connect · COMPRA do iPhone da Gracinha (plano B: Mestre)',
    note='Pagar com o dólar recém-trocado. Testar o aparelho, conferir caixa lacrada, IMEI na caixa = no aparelho, modelo LL e nota fiscal. '
         'Plano B no mesmo prédio: Mestre Atacado (4º piso, nº 3353), 18 Pro Max Bordô US$ 1.485, aceita Pix direto. '
         'Mestre NÃO aceita cartão. Se o Sanderson fechar ≤ US$ 1.249 aqui, comprar o dele também e pular o Prime Shop.',
    lat=JEB[0], lng=JEB[1], leg={'mode': 'walk', 'minutes': 0, 'label': 'Mesmo prédio'}, place=copy.deepcopy(jplace), cost=0, costDetails=zero()))
items.append(item(jebai, time='07:50', end='08:10', name='Star Games (Jebai 3º, 3264) · capinhas TechWoven',
    note='Capas "Apple TechWoven MagSafe" por ~US$ 25 (17 Pro e 17 Pro Max: preto, marrom, azul, verde, roxo), bem abaixo da original (US$ 74–85). '
         'Capa de 17 Pro serve no 18 Pro na prática (câmera só 0,1 mm maior), mas a Apple não garante: TESTAR NO APARELHO recém-comprado (botões, câmera, MagSafe). '
         'Original lacrada: Nissei, no Hijazi (próxima parada), US$ 79–85. Plano B barato: Madrid Center (Galeria San Blás), US$ 20–25, e New Zone (C-Covers, US$ 17).',
    lat=JEB[0], lng=JEB[1], leg={'mode': 'walk', 'minutes': 0, 'label': 'Mesmo prédio'},
    place=dict(copy.deepcopy(jplace), address='Galería Jebai Center, 3º piso, loja 3264 · Ciudad del Este', website='https://stargamesparaguay.com/', hours='Confirmar (Jebai seg–sáb ~7h–16h)'),
    cost=0, costDetails=zero()))
hp = copy.deepcopy(nissei['place'])
items.append(item(nissei, time='08:15', end='09:00', name='Prime Shop (Hijazi, 4º, sala 417) · COMPRA do iPhone do Sanderson',
    note='18 Pro 256GB Bordô por US$ 1.259 (promo). Pagar: débito em dólar (Nomad US$ 330 + BTG US$ 100 + Avenue US$ 709; +5%) e o resto (~US$ 193) no dólar da La Moneda. '
         'Contato: Amanda +595 986 420 415. Na maquininha, pedir o valor em guaranis e recusar conversão para reais. Conferir lacre, modelo LL e nota. '
         'Nissei fica no mesmo prédio: capa TechWoven original (US$ 79–85) se preferir a da Apple.',
    lat=HIJ[0], lng=HIJ[1], leg={'mode': 'walk', 'minutes': 3, 'label': f'{round(dist(JEB, HIJ), -1):.0f} m'},
    place=dict(hp, address='Shopping Hijazi Center, 4º andar, sala 417 · Av. Adrián Jara esq., Ciudad del Este', phone='+595 986 420 415'),
    cost=0, costDetails=zero()))
seq = [
    (laila, '09:05', '09:25', None),
    (eleg, '09:30', '09:55', None),
    (mona, '10:00', '10:35', None),
    (terra, '10:40', '11:05', None),
    (digi, '11:10', '11:35', None),
    (alm, '11:45', '12:30', None),
    (paris, '12:30', '13:10', None),
    (china, '13:20', '14:05', None),
    (newz, '14:15', '14:40', None),
    (cela, '14:45', '15:25', None),
]
prev = HIJ
for b, t, e, _ in seq:
    x = copy.deepcopy(b); x['time'] = t; x['end'] = e
    p = (x['lat'], x['lng']); m = dist(prev, p)
    if x['leg'].get('label') != 'Mesmo prédio' and m > 20:
        x['leg'] = {'mode': 'walk', 'minutes': max(2, math.ceil(m / 60)), 'label': f'{round(m, -1):.0f} m'}
    prev = p; items.append(x)
L = {x['name']: x for x in items}
lai = next(x for x in items if x['name'].startswith('Lai Lai'))
lai['note'] += ' Se a Gracinha mudar para o 17 Pro Max: a Matrix daqui pode ser a "Matrix Importados" (Laranja US$ 1.170) — perguntar.'
dg = next(x for x in items if x['name'].startswith('Digital Center'))
dg['note'] += ' Capinhas, plano B: Madrid Center, na Galeria San Blás (mesma avenida), TechWoven ~US$ 20–25; seg–sex 6h–16h; WhatsApp +595 974 314441.'
alm2 = next(x for x in items if x['name'].startswith('Almoço'))
alm2['note'] = 'Almoço mais cedo (café foi às 4h45). ' + alm2['note']
nz = next(x for x in items if x['name'].startswith('New Zone'))
nz['note'] += ' Plano C do iPhone do Sanderson (Bordô US$ 1.295; Pix Especial 9h30–16h via Call Center). Capinha C-Covers TechWoven US$ 17.'
ce = next(x for x in items if x['name'].startswith('Café da tarde'))
ce['note'] = ce['note'].replace('Sair às 16h30 para a ponte, para garantir o pôr do sol no Yup Star.',
    'Sair às 15h25 para a ponte: atravessa antes do pico (16h–19h) e sobra tempo para guardar as compras no Airbnb.')
c = copy.deepcopy(carro); c['time'] = '16:35'; c['end'] = '16:40'
c['leg']['label'] = 'Táxi do Shopping del Este até o estacionamento · saindo 15h25, antes do pico (margem de 70 min para fila da ponte e da Receita)'
items.append(c)
items.append(item(airbnb, time='16:55', end='17:50', name='Airbnb · guardar as compras e descansar',
    note='Tirar iPhones e compras do carro, colocar a capinha, banho rápido e descanso para os joelhos. Sair às 17h50 para o Yup Star.',
    leg={'mode': 'car', 'minutes': 15, 'label': 'Estacionamento 277 → Airbnb, 3,9 km (recalcular no Maps)'}))
y = copy.deepcopy(yup)
y['leg'] = {'mode': 'car', 'minutes': 30, 'label': 'Airbnb → Yup Star, ~10 km · estimativa com margem de horário de pico (recalcular no Maps às 17h50)'}
y['note'] = y['note'].replace('Compras no porta-malas.', 'Compras já guardadas no Airbnb.')
items += [y, marco, jantar]
a2 = copy.deepcopy(airbnb); a2['note'] = 'Fim do dia.'; items.append(a2)
day['items'] = [fmt(x) for x in items]
day['title'] = 'Paraguai: iPhones logo cedo, capinhas e compras + Yup Star e Marco'
day['note'] = ('Madrugada: saída 5h10, carro no estacionamento 277 e mototáxi às 5h30 para chegar ao Paraguai às 6h. '
    'Ordem otimizada (tudo a pé, sem vai e volta): Jebai (Atacado Connect + La Moneda + Star Games) → Hijazi (Prime Shop e Nissei, a ~70 m) → '
    'perfumes/eletrônicos no microcentro → Shopping Paris e China → Shopping del Este, ao lado da ponte. '
    'Câmbio às 7h (Ita fecha 15h30). Saída do Paraguai às 15h25, antes do pico da ponte. '
    'Cota de US$ 500 por pessoa (não soma): cada iPhone passa da cota e o excedente paga 50%. Valores de 30/10–01/11: reconferir na terça (03/11).')
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); open(P, 'a').write('\n')
print('ok', len(items))
