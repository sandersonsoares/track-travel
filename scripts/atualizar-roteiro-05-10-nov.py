# Reescreve os dias 05 a 10/11/2026 de src/data/foz-do-iguacu.json com o roteiro fechado em 18/10/2026.
# Reaproveita endereço, foto e custo dos itens que já existiam. Rodar na raiz do projeto: python3 scripts/atualizar-roteiro-05-10-nov.py
import json, copy

P = 'src/data/foz-do-iguacu.json'
d = json.load(open(P))
idx = {}
for day in d['days']:
    for i in day['items']:
        idx.setdefault(i['name'], i)
        for a in i.get('alternatives') or []:
            idx.setdefault('ALT:' + a['name'], a)

CHK = '2026-10-18'
ORDER = ['time', 'end', 'type', 'name', 'note', 'lat', 'lng', 'image', 'leg', 'place', 'cost', 'costDetails', 'alternatives']


def gm(pid):
    return f'https://www.google.com/maps/place/?q=place_id:{pid}'


def cd(full, half=None, applies=False, people=3, status='estimativa', note=None, source=None):
    pay = half if applies and half is not None else full
    c = {'unit': 'pessoa', 'fullPerPerson': full, 'halfPerPerson': half, 'halfApplies': applies, 'payPerPerson': pay,
         'people': people, 'totalGroup': round(pay * people, 2) if pay is not None else None, 'status': status, 'checkedAt': CHK}
    if source:
        c['source'] = source
    if note:
        c['note'] = note
    return c


def leg(m, label, mode='car'):
    return {'mode': mode, 'minutes': m, 'label': label}


def place(address, hours=None, phone=None, rating=None, url=None):
    p = {'address': address}
    if hours:
        p['hours'] = hours
    if phone:
        p['phone'] = phone
    if rating:
        p['rating'] = rating
    if url:
        p['googleMapsUrl'] = url
    p['photos'] = []
    return p


def it(src=None, alts=False, **kw):
    x = copy.deepcopy(idx[src]) if src else {}
    if not alts:
        x.pop('alternatives', None)
    for k in ('leg', 'cost', 'costDetails', 'end'):
        if k in kw and kw[k] is None:
            x.pop(k, None)
            kw.pop(k)
    x.update(kw)
    out = {k: x[k] for k in ORDER if k in x}
    out.update({k: v for k, v in x.items() if k not in ORDER})
    return out


def airbnb(time, name, note, end=None, legm=None, label=None, mode='car'):
    x = it('Airbnb Solar das Violetas', time=time, name=name, note=note, cost=None, costDetails=None, leg=None, end=end)
    if legm is not None:
        x['leg'] = leg(legm, label, mode)
        x = it_order(x)
    return x


def it_order(x):
    out = {k: x[k] for k in ORDER if k in x}
    out.update({k: v for k, v in x.items() if k not in ORDER})
    return out


def trigo(time, end, note, people=3, legm=None, label=None):
    return it('Café da manhã · Trigo & Cia', time=time, end=end, name='Café da manhã · Trigo & Cia', note=note,
              leg=leg(legm, label, 'walk') if legm else None,
              costDetails=cd(40, people=people, note='Valor médio por pessoa, sem bebida alcoólica.'))


def drop(t, e, m, label):
    return it('Deixar as meninas no Congresso Espectro', time=t, end=e, leg=leg(m, label))


def pick(t, e, m, label, name=None, note=None):
    kw = {'time': t, 'end': e, 'leg': leg(m, label)}
    if name:
        kw['name'] = name
    if note:
        kw['note'] = note
    return it('Buscar as meninas no congresso', **kw)


# ---------- 05/11 quinta ----------
d05 = [
    trigo('06:15', '06:40', 'Café das meninas antes do congresso. Sanderson só toma um café aqui; o café da manhã dele é depois de deixá-las.', people=2),
    airbnb('06:45', 'Saída do Airbnb', 'Pegar o carro na garagem.'),
    drop('06:55', '07:05', 10, 'Airbnb → Recanto Cataratas · cerca de 10 min'),
    it(time='07:20', end='08:00', type='food', name='Café da manhã do Sanderson · Engenho Doce',
       note='Padaria e confeitaria tradicional do Centro, abre às 6h30. Valor não estimado.',
       lat=-25.5404702, lng=-54.5763553, leg=leg(15, 'Recanto Cataratas → Av. Paraná · cerca de 15 min'),
       place=place('Av. Paraná, 909 · Centro, Foz do Iguaçu - PR', 'Seg–sáb 6h30–21h30 · dom 7h–19h', '+55 45 3028-7010', 4.4, gm('ChIJn_LSgFKQ9pQRdyDI_HHEG00'))),
    it('Ailabiu Iguassu · Centro', time='08:05', end='08:55', name='Ailabiu Souvenirs · lembranças',
       note='Loja de souvenirs de Foz. O Google indica abertura às 8h todos os dias; o Instagram indica 9h. Confirmar pelo WhatsApp na véspera; se abrir às 9h, inverter com a Feira Iguaçu.',
       lat=-25.53475, lng=-54.585892, leg=leg(5, 'Av. Paraná → Av. Brasil · 5 min')),
    it(time='09:00', end='10:10', type='shopping', name='Feira Iguaçu e Bela Artesanato · lembranças',
       note='Duas quadras de lojinhas no estilo feira: ímãs, canecas, camisetas, bandeiras e artesanato do Brasil, Paraguai e Argentina, com preços abaixo dos atrativos. A Bela Artesanato fica no nº 742, ao lado. Entrada livre; compras à parte.',
       lat=-25.5358073, lng=-54.5856072, leg=leg(4, 'A pé, cerca de 300 m', 'walk'),
       place=place('R. Eng. Rebouças, 770 · Centro, Foz do Iguaçu - PR', 'Feira Iguaçu: seg–sex 9h–19h · sáb 9h–16h · dom fechado. Bela Artesanato: todos os dias 9h–19h', '+55 45 99108-8565', 4.3, gm('ChIJcaiwiUiQ9pQRbAYPzRrztNk')),
       cost=0, costDetails=cd(0, 0, True, status='oficial', note='Entrada livre. Compras à parte.')),
    it('Pedacinho de Foz · Falls Galli Hotel', time='10:30', end='11:00', leg=leg(20, 'Centro → Falls Galli Hotel · cerca de 20 min')),
    it('AquaFoz', time='11:35', end='13:50', leg=leg(35, 'Falls Galli → AquaFoz, Av. das Cataratas · cerca de 35 min')),
    it('Divino Fogão (Sanderson)', alts=True, time='14:15', end='15:05', name='Almoço · Divino Fogão (Sanderson)', leg=leg(25, 'AquaFoz → Shopping Catuaí · cerca de 25 min')),
    it('Shopping Catuaí Palladium (Sanderson)', time='15:05', end='19:20', note='Compras no shopping até a hora de buscar as meninas.', leg=leg(0, 'Mesmo shopping')),
    pick('19:50', '20:10', 25, 'Catuaí → Recanto Cataratas · cerca de 25 min'),
    it('Rafain Churrascaria Show', alts=True, time='20:30', end='22:15', leg=leg(20, 'Recanto Cataratas → Rafain · 13 min + margem')),
    airbnb('22:30', 'Airbnb Solar das Violetas', 'Fim do dia.', legm=15, label='Rafain → Airbnb · 12 min + margem'),
]

# ---------- 06/11 sexta ----------
patio = copy.deepcopy(idx['Pátio Pomare'])
for k in ('alternatives', 'time', 'end', 'leg', 'image'):
    patio.pop(k, None)
patio['note'] = 'Alternativa para a noite do grupo: food park ao ar livre. Sex 15h–23h; os portões fecham 30 min antes.'
d06 = [
    it('Café da manhã no Airbnb (os três)', time='06:00', end='06:30', note='Café rápido no apartamento antes do congresso. O café da manhã do Sanderson é no Bella Foz, depois de deixar as meninas.'),
    airbnb('06:35', 'Saída do Airbnb', 'Pegar o carro na garagem.'),
    drop('06:50', '07:00', 15, 'Airbnb → Recanto Cataratas, Av. Costa e Silva, 3500'),
    it(time='07:15', end='08:00', type='food', name='Café da manhã do Sanderson · Bella Foz Café',
       note='Padaria e cafeteria do Centro (nota 4,8), abre às 7h. Tapioca, omelete, sucos naturais. Valor não estimado.',
       lat=-25.5408574, lng=-54.5801342, leg=leg(15, 'Recanto Cataratas → Centro · cerca de 15 min'),
       place=place('R. Jorge Sanwais, 1239 · Centro, Foz do Iguaçu - PR', 'Seg–sex 7h–22h · sáb e dom 7h–21h', '+55 45 99825-0727', 4.8, gm('ChIJkSs53hyR9pQRxzQ-ARS1S5E'))),
    it('Itaipu Panorâmica', time='08:30', end='11:00', name='Itaipu · Circuito Especial (Sanderson)',
       note='Visita por dentro da usina: galeria de quase 1 km, descida ao nível das turbinas e sala de controle, além dos mirantes. Cerca de 2h30. Relatos indicam idade mínima de 14 anos. Confirmar no site oficial de ingressos o horário da saída, o calçado exigido e o documento.',
       leg=leg(25, 'Centro → Centro de Recepção de Visitantes da Itaipu · cerca de 25 min'),
       cost=182, costDetails=cd(182, people=1, status='a confirmar', note='Valor inteiro da lista de passeios. Verificar se há meia para estudante.')),
    it('Ecomuseu de Itaipu', time='11:10', end='12:10', leg=leg(10, 'Centro de Recepção → Ecomuseu · 1 km')),
    it('Itaipu Bistrot', time='12:20', end='13:15', name='Almoço · Itaipu Bistrot (Sanderson)', leg=leg(10, 'Ecomuseu → Itaipu Bistrot')),
    it('Almoço · Cataratas JL Shopping (Sanderson)', time='13:40', end='19:30', type='shopping', name='Cataratas JL Shopping · compras (Sanderson)',
       note='Compras no shopping. Lojas seg–sáb 10h–22h. Fica na mesma avenida do congresso.', costDetails=None,
       leg=leg(20, 'Itaipu → Av. Costa e Silva · cerca de 20 min'), cost=0),
    pick('19:45', '20:10', 10, 'JL → Recanto Cataratas · mesma avenida'),
    it(time='20:30', end='22:00', type='food', name='Fondue no Óga Restaurante',
       note='Restaurante do roteiro do city tour de Foz, com cozinha regional da fronteira (nota 4,7). De segunda a sexta abre às 17h. Reservar. Alternativa para a noite: Pátio Pomare.',
       lat=-25.534113, lng=-54.5882284, leg=leg(15, 'Recanto Cataratas → Centro · cerca de 15 min'),
       place=place('Av. República Argentina, 632 · Centro, Foz do Iguaçu - PR', 'Seg–sex 17h–23h30 · sáb e dom 11h30–23h30', '+55 45 3026-5035', 4.7, gm('ChIJbUBax6aR9pQRTF8JLx9NT1k')),
       cost=249.9, costDetails=cd(249.9, status='a confirmar', note='Valor da lista de passeios (Fondue no Óga). Confirmar se é por pessoa ou por casal.'),
       alternatives=[patio]),
    airbnb('22:15', 'Airbnb Solar das Violetas', 'Fim do dia.', legm=15, label='Centro → Airbnb · cerca de 15 min'),
]

# ---------- 07/11 sábado ----------
d07 = [
    it('Café da manhã no Airbnb (os três)', time='06:45', end='07:15', note='Café no apartamento, os três.'),
    airbnb('07:25', 'Saída do Airbnb', 'Pegar o carro na garagem.'),
    drop('07:40', '07:50', 15, 'Airbnb → Recanto Cataratas'),
    airbnb('08:15', 'Agência busca o Sanderson no Airbnb', 'Deixar o carro na garagem. Levar documento com foto (RG ou passaporte) para a fronteira. Horário da busca a confirmar com a agência.', legm=15, label='Recanto Cataratas → Airbnb'),
    it(time='08:30', end='17:00', type='activity', name='City Tour Paraguai com parada para compras (Sanderson)',
       note='Roteiro típico: Catedral de San Blas, Casino Acaray, Mesquita del Este, Chipería Mi Abuela, Museu El Mensú, Lago de la República, passagem pela Prefeitura de Ciudad del Este e Saltos del Monday (cerca de 1h), com parada para compras no fim. Almoço: lanche na Chipería Mi Abuela, parada do próprio tour (o tour não inclui refeição). Horários de saída e volta a confirmar com a agência.',
       lat=-25.55928, lng=-54.6315432, leg=leg(40, 'Transporte da agência · ponte e aduana'),
       place=place('Ciudad del Este e Saltos del Monday · Presidente Franco, Paraguai', url=gm('ChIJbWMMrEqO9pQRPc49_XBaN8I')),
       cost=150, costDetails=cd(150, people=1, status='a confirmar', note='Valor da lista (City Tour Paraguai com parada para compras). A versão só city tour sai R$ 130 e termina por volta das 15h30.')),
    airbnb('17:15', 'Volta ao Airbnb', 'A agência deixa no Airbnb. Banho e troca de roupa. Sair às 19h20 para o Capitão Bar.', end='19:20', legm=40, label='Transporte da agência · aduana e ponte'),
    it('Recanto Cataratas · festa do congresso (a confirmar)', time='19:45', name='Festa do congresso (Hortência e Gracinha)', leg=None,
       note='As meninas seguem do congresso direto para a festa no Recanto Cataratas. Confirmar se acontece e a que horas termina, para combinar a busca.'),
    it('ALT:Capitão Bar', time='19:45', end='21:30', type='food', name='Jantar do Sanderson · Capitão Bar',
       note='Restaurante e bar com música ao vivo na Av. Jorge Schimmelpfeng, 288. Pode ter couvert artístico. Depois, buscar as meninas no fim da festa.',
       lat=-25.547145, lng=-54.585441, leg=leg(25, 'Airbnb → Capitão Bar · cerca de 25 min')),
    pick('22:00', '22:20', 15, 'Capitão Bar → Recanto Cataratas', name='Buscar as meninas na festa (horário a confirmar)',
         note='O horário depende do fim da festa do congresso.'),
    airbnb('22:35', 'Airbnb Solar das Violetas', 'Fim do dia.', legm=15, label='Recanto Cataratas → Airbnb'),
]

# ---------- 08/11 domingo ----------
d08 = [
    trigo('06:45', '07:15', 'Café da manhã ao lado do Airbnb (24 horas).'),
    airbnb('07:20', 'Saída do Airbnb', 'Levar dinheiro em espécie para a feirinha.', legm=2, label='Trigo → Airbnb · a pé', mode='walk'),
    it(time='07:30', end='08:30', type='shopping', name='Feirinha da JK · artesanato e lembranças',
       note='A feira de artesanato mais conhecida de Foz, só aos domingos: cerca de 40 barracas de artesanato, produtos regionais e doces. Ir cedo. Muitas barracas não aceitam cartão.',
       lat=-25.5444069, lng=-54.5881291, leg=leg(10, 'Airbnb → Av. JK, Centro · cerca de 10 min'),
       place=place('Av. Juscelino Kubitschek, 256 · Centro (ao lado da Praça da Paz), Foz do Iguaçu - PR', 'Domingos 7h–12h', rating=4.3, url=gm('ChIJrzPsCkqQ9pQRSHC7FSXfVew')),
       cost=0, costDetails=cd(0, 0, True, status='oficial', note='Entrada livre. Compras à parte.')),
    it('Cataratas do Iguaçu · lado brasileiro', time='09:10', end='11:50', leg=leg(40, 'Centro → Centro de Visitantes · 29 min + estacionar e fila')),
    it('ALT:Sabores da Floresta', time='12:15', end='13:00', type='food', name='Almoço · Sabores da Floresta (Parque das Aves)',
       note='Restaurante dentro do Parque das Aves, em frente ao Centro de Visitantes das Cataratas. Escolhido no lugar do Porto Canoas, que segundo relato de agosto de 2026 está com o buffet fechado por obra.',
       leg=leg(25, 'Ônibus interno até o Centro de Visitantes + atravessar a rua')),
    it('Parque das Aves', time='13:00', end='15:30', leg=leg(0, 'Já dentro do parque')),
    it(time='15:45', end='16:20', type='shopping', name='Artesanato e Chocolate Caseiro Três Fronteiras',
       note='Loja grande de souvenirs, pedras, artesanato, café e chocolate caseiro, com degustação. Entrada livre; compras à parte.',
       lat=-25.5789007, lng=-54.5364949, leg=leg(10, 'Parque das Aves → Av. das Cataratas, km 11 · cerca de 10 min'),
       place=place('Av. das Cataratas, km 11 · Carimã, Foz do Iguaçu - PR', 'Todos os dias 8h–18h30', '+55 45 3529-6565', 3.9, gm('ChIJ2XmGbuST9pQRzEiLUx2kkAA')),
       cost=0, costDetails=cd(0, 0, True, status='oficial', note='Entrada livre. Compras à parte.')),
    it('Kattamaram II no pôr do sol', alts=True, time='16:50', end='19:00', leg=leg(20, 'Av. das Cataratas → Porto Meira · cerca de 20 min')),
    it('Wonder Park: Movie Cars e Big Land (Sanderson)', time='19:25', end='22:00', name='Wonder Park · passaporte 5 atrações (grupo)',
       note='19h30 Lumina Park (percurso iluminado de 700 m, plano) · 20h Wonder Games (reservar a sessão das 20h na compra) · 20h30 Show das Águas (sessão única) · 20h55 Movie Cars · 21h30 Big Land. O parque fecha às 22h. Estacionamento gratuito. Ingresso com QR code por e-mail, válido por 180 dias.',
       leg=leg(25, 'Porto Meira → Av. das Cataratas, 11547 · cerca de 25 min'),
       cost=170, costDetails=cd(199, 170, True, status='oficial', source='https://ingresso.wonderparkfoz.com.br/produto/vitrine/passaporte',
                                note='Passaporte 5 atrações: inteira R$ 199, reduzida R$ 170 (estudante, professor, 60+, com comprovante).')),
    it('Trigo & Cia', time='22:40', end='23:30', name='Jantar · Trigo & Cia',
       note="Jantar ao lado do Airbnb, aberto 24 horas. O Bonnie's Burger, no Wonder Park, fecha às 22h.",
       leg=leg(40, 'Wonder Park → Airbnb · 25 min + margem')),
    airbnb('23:35', 'Airbnb Solar das Violetas', 'Fim do dia.', legm=2, label='A pé', mode='walk'),
]

# ---------- 09/11 segunda ----------
d09 = [
    trigo('06:30', '07:00', 'Café da manhã ao lado do Airbnb.'),
    airbnb('07:15', 'Agência busca no Airbnb', 'Dia inteiro na Argentina com transporte da agência: o carro alugado não pode entrar no país. O ideal é um transfer de dia inteiro, para não voltar ao Brasil entre o parque e o By Night. Horários a confirmar com a agência.', legm=2, label='A pé', mode='walk'),
    it('ALT:Cataratas argentinas (Parque Nacional Iguazú)', time='08:30', end='12:00', type='place', name='Cataratas argentinas · Parque Nacional Iguazú',
       note='Desde 15/10/2026 só o Circuito Inferior está aberto; o Circuito Superior e a Garganta del Diablo seguem fechados pela cheia, sem data de reabertura. Confirmar com a agência a regra de reembolso ou troca. Levar documento com foto (RG ou passaporte).',
       leg=leg(75, 'Transporte da agência · ponte Tancredo Neves e aduana'),
       cost=510, costDetails=cd(510, status='a confirmar', note='Combo Cataratas Argentinas com transporte e ingresso (valor da lista). Confirmar se é por pessoa.')),
    it(time='12:00', end='13:00', type='food', name='Almoço · Restaurante La Selva (dentro do parque)',
       note='Buffet com churrasco e saladas, dentro do Parque Nacional Iguazú. Alternativa: Fortín Cataratas (buffet e parrilla, 8h–16h30). Valor não estimado.',
       lat=-25.6810706, lng=-54.4543811, leg=leg(10, 'Dentro do parque'),
       place=place('Área Cataratas · Parque Nacional Iguazú, Misiones, Argentina', 'Todos os dias 8h–17h', rating=4.5, url=gm('ChIJBTpOZwDr9pQRmuua2QYw4FE'))),
    it('Duty Free Shop Puerto Iguazú', time='13:45', end='15:30', leg=leg(40, 'Parque → Duty Free, logo depois da aduana argentina')),
    it('Feirinha de Puerto Iguazú', time='15:45', end='16:45', leg=leg(10, 'Duty Free → Feirinha · cerca de 10 min'),
       note='Paseo gastronómico: alfajores, azeitonas, queijos, salames, doce de leite e vinhos. Muitas barracas não aceitam cartão; aceitam pesos ou reais.'),
    it(time='17:00', end='17:45', type='activity', name='Icebar Iguazú',
       note='Bar de gelo a -10 °C: casaco e luvas fornecidos, drinques servidos em copos de gelo. Visita de cerca de 20 a 30 min. Valor a confirmar.',
       lat=-25.6195139, lng=-54.5548889, leg=leg(10, 'Feirinha → Ruta 12, km 4,5 · cerca de 10 min'),
       place=place('Ruta 12, km 4,5 · Puerto Iguazú, Misiones, Argentina', 'Todos os dias 14h–0h', rating=4.4, url=gm('ChIJO0LuPAmT9pQRxt6l9EZBJTk'))),
    it('Hito Tres Fronteras (opcional)', time='18:15', end='19:10', name='Hito Tres Fronteras · pôr do sol', leg=leg(15, 'Icebar → Hito Tres Fronteras · cerca de 15 min'),
       note='Marco argentino da tríplice fronteira, com vista para Brasil e Paraguai. Pôr do sol por volta das 19h. Gratuito.'),
    it(time='19:20', end='21:00', type='food', name='Jantar com show de tango · El Quincho del Tío Querido',
       note='Jantar do By Night: parrilla argentina com show de tango ao vivo. Na segunda abre só para o jantar, às 18h30.',
       lat=-25.6060772, lng=-54.5657043, leg=leg(10, 'Hito → Av. Perón · cerca de 10 min'),
       place=place('Av. Pres. Juan Domingo Perón, 159 · Puerto Iguazú, Misiones, Argentina', 'Seg 18h30–22h30 · ter–dom 11h30–14h30 e 18h30–22h30', '+54 3757 42-0151', 4.3, gm('ChIJafD1JTGS9pQRTb23YN3CBwc')),
       cost=390, costDetails=cd(390, status='a confirmar', note='By Night com jantar no Tío Querido (R$ 260) + transporte saindo de Foz (R$ 130), valores da lista. Confirmar o que está incluído.')),
    airbnb('22:15', 'Airbnb Solar das Violetas', 'Volta com a agência, passando pela aduana.', legm=75, label='Transporte da agência · aduana e ponte'),
]

# ---------- 10/11 terça ----------
d10 = [
    trigo('06:45', '07:20', 'Café da manhã ao lado do Airbnb.'),
    it('Check-out antecipado · malas na SUV', time='07:20', end='07:50', leg=leg(2, 'A pé', 'walk'),
       note='Check-out e malas no carro. Mulheres: levar roupa que cubra as pernas para a mesquita (o véu é emprestado na entrada).'),
    it(time='08:00', end='08:15', type='place', name='Avenida Pedro Basso · túnel de árvores',
       note='Primeira parada do city tour de Foz, feito de carro próprio: avenida com o "túnel" de árvores, tombada como patrimônio de Foz. Passar devagar de carro.',
       lat=-25.5230689, lng=-54.5728452, leg=leg(3, 'Ao lado do Airbnb'),
       place=place('Av. Pedro Basso · Foz do Iguaçu - PR', url=gm('ChIJOwvoRFyQ9pQRodi_YjGq3FM')),
       cost=0, costDetails=cd(0, 0, True, status='oficial', note='Gratuito.')),
    it('Mesquita Omar Ibn Al-Khattab', time='08:40', end='09:20', leg=leg(5, 'Av. Pedro Basso → Mesquita · cerca de 5 min'),
       note='A maior mesquita do Brasil. Visita gratuita com vídeo sobre a cultura islâmica; mulheres recebem o véu na entrada. Roupa cobrindo as pernas. Abertura: o roteiro anterior indica 8h30 e um blog indica visitas a partir das 9h. Se for 9h, fazer a Kapadokya antes.'),
    it('Kapadokya · doces árabes', time='09:20', end='09:40', leg=leg(1, 'Em frente à mesquita, a pé', 'walk'), lat=-25.521068, lng=-54.578823,
       note='Loja de doces árabes e artesanato em frente à mesquita, com o letreiro "Eu ❤ Foz" para fotos. Ao lado fica a Albayan Doceria Arabic (8h30–20h), se a Kapadokya estiver fechada.',
       place=place('R. Meca, 642 · Monjolo, Foz do Iguaçu - PR', 'Seg–sex 9h–12h e 14h–17h30 · sáb 9h–12h e 14h–16h · dom 9h–14h', '+55 45 3526-2567', 4.6, gm('ChIJ4XdSmeWR9pQRN-h3hE2X7Tc'))),
    it('Templo Budista Chen Tien', time='09:55', end='10:45', leg=leg(15, 'Mesquita → Templo Budista · cerca de 15 min')),
    it('Catedral Nossa Senhora de Guadalupe', time='10:55', end='11:25', leg=leg(10, 'Templo → Catedral · 11 min'),
       note='Inaugurada em 2023, com arquitetura moderna e vitrais grandes. Na terça fecha às 11h30.'),
    it('Almoço · Mercado Público Barrageiro', time='11:35', end='12:50', name='Almoço · Mercado Público Barrageiro + Artes Sem Fronteiras',
       note='Mercado com lojinhas, comidinhas e produtos regionais. Dentro dele fica a Artes Sem Fronteiras, loja de artesanato regional com muita variedade (ter–sáb 10h–21h): bom lugar para as últimas lembranças. Sair às 12h50 para o aeroporto.',
       leg=leg(5, 'Catedral → Mercado · cerca de 5 min')),
    it('Posto + devolução da SUV', time='13:20', end='14:00', leg=leg(30, 'Mercado → posto perto do aeroporto · 29 min + margem')),
    it('Aeroporto: check-in e despacho', time='14:30', end='14:45'),
    it('Voo Foz → João Pessoa (LATAM)', time='17:30', end='23:20'),
]

titles = {
    '2026-11-05': 'Congresso + lembranças, AquaFoz e Catuaí (Sanderson) + Rafain',
    '2026-11-06': 'Congresso + Itaipu Circuito Especial e JL (Sanderson) + fondue no Óga',
    '2026-11-07': 'Congresso + city tour no Paraguai (Sanderson) + festa do congresso',
    '2026-11-08': 'Feirinha da JK, Cataratas, Parque das Aves, Kattamaram e Wonder Park',
    '2026-11-09': 'Dia inteiro na Argentina: Cataratas argentinas e By Night',
    '2026-11-10': 'City tour de Foz de carro e volta para casa',
}
new = {'2026-11-05': d05, '2026-11-06': d06, '2026-11-07': d07, '2026-11-08': d08, '2026-11-09': d09, '2026-11-10': d10}
for day in d['days']:
    if day['date'] in new:
        day['title'] = titles[day['date']]
        day['items'] = new[day['date']]

# Checagens: coordenadas, fotos e horários em ordem.
for day in d['days']:
    prev = ''
    for i in day['items']:
        assert isinstance(i.get('lat'), (int, float)) and isinstance(i.get('lng'), (int, float)), i['name']
        if 'place' in i:
            i['place'].setdefault('photos', [])
        assert i['time'] >= prev or day['date'] < '2026-11-05', (day['date'], i['name'])
        prev = i['time']

with open(P, 'w') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('ok')
