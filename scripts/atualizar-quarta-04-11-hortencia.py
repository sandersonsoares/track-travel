# 04/11: encaixa a lista de compras da Hortência nas paradas existentes (endereços levantados em 01/11).
import json
P = 'src/data/foz-do-iguacu.json'
d = json.load(open(P)); day = d['days'][1]; assert day['date'] == '2026-11-04'
def f(p): return next(i for i in day['items'] if i['name'].startswith(p))
H = '👩 HORTÊNCIA: '
f('Câmbio · La Moneda')['note'] = f('Câmbio · La Moneda')['note'].replace(
    '≈ US$ 1.450 da Gracinha + ≈ US$ 193 do Sanderson (separar R$ 1.170).',
    '≈ US$ 1.450 da Gracinha + ≈ US$ 193 do Sanderson (separar R$ 1.170) + o dólar da Hortência para as compras dela (paga tudo em espécie).')
g = f('Atacado Connect · COMPRA')
g['note'] += (' ' + H + 'em paralelo (7h20–7h50), no mesmo prédio: STAR COMPANY (1º andar, loja 2017; abre 7h; WhatsApp +595 993 085626) — '
    'Medicube (Exosome Shot 2000, Zero Pore Pad 2.0, TXA Niacinamide 15%, Collagen Night Wrapping Mask), Fino (máscara, óleo, sérum Airy Smooth, shampoo), '
    'Victoria\'s Secret Body Splash Pure Seduction 250ml e Numbuzin No.9 creme de olhos. Avaliações citam demora na retirada e suspeita de falsificados: conferir lacre e lote. '
    'Se a retirada demorar, há outra Star Company no Shopping Paris (térreo, lojas 30–31), na parada do almoço. '
    'Ao lado, EXTRA SHOP (térreo, loja 2016; WhatsApp +595 983 222219): SKIN1004 Madagascar Centella Ampoule 55ml. '
    'Fino condicionador 550ml: tentar aqui na Atacado Connect; se não tiver, na Nissei (próxima parada).')
p = f('Prime Shop'); p['note'] += ' ' + H + 'Nissei (mesmo prédio): Fino condicionador 550ml, se não achou na Atacado Connect. Fila no caixa cresce depois das 11h: comprar agora.'
l = f('Lai Lai'); l['time'], l['end'] = '09:05', '09:20'
l['note'] += (' ' + H + 'POINT INFORMÁTICA (4º andar, loja 408; seg–sáb 7h30–16h30; WhatsApp +595 973 519759): microfone Hollyland Lark M2 Combo. '
    'Alternativa: Intershop (Shopping DFS).')
c = f('CellShop'); c['note'] += (' ' + H + 'CellShop fica no Shopping Ibiza (térreo). Rímel Maybelline Sky High: se a Paris Store não confirmar estoque até terça, comprar aqui (a Paris Store só vem às 13h). '
    'BRANDS SHOP (Av. Monseñor Rodríguez, ~70 m, a caminho da Monalisa; 7h–16h30; WhatsApp +595 992 979 800): Celimax Vita-A Retinal Shot (substituto do IOPE Retinol Shot).')
f('Ponto Com')['note'] += ' ' + H + 'Dr. Althea 345 Relief Cream 50ml.'
sp = f('Shopping Paris'); sp['time'], sp['end'] = '13:00', '13:40'
sp['note'] += (' ' + H + 'PARIS STORE (2º andar; WhatsApp +595 993 005 000): rímel Maybelline Sky High, MAC blush Sheertone e MAC base Studio Radiance; '
    'perguntar por MAC paleta e Studio Fix. Também tem Star Company no térreo (lojas 30–31), se faltou algo no Jebai.')
sc = f('Shopping China'); sc['time'], sc['end'] = '13:50', '14:15'
f('New Zone')['note'] += ' ' + H + 'MAC batom (3º andar); perguntar por MAC paleta e Studio Fix, se não achou na Paris Store.'
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); open(P, 'a').write('\n')
def mm(t): h, m = map(int, t.split(':')); return h * 60 + m
it = day['items']; bad = 0
for a, b in zip(it, it[1:]):
    fol = mm(b['time']) - mm(a.get('end', a['time'])) - (b.get('leg') or {}).get('minutes', 0)
    if fol < 0: bad += 1; print('CONFLITO', b['name'], fol)
print('ok, conflitos:', bad)
