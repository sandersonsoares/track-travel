import json, copy
P='src/data/foz-do-iguacu.json'
d=json.load(open(P))
days={x['date']:x for x in d['days']}

# 1) Itaipu Circuito Especial -> meia
for it in days['2026-11-06']['items']:
    if it['name'].startswith('Itaipu · Circuito Especial'):
        it['cost']=92.5
        it['costDetails']={"unit":"pessoa","fullPerPerson":185,"halfPerPerson":92.5,"halfApplies":True,"payPerPerson":92.5,"people":1,"totalGroup":92.5,
          "status":"oficial (inteira) · meia a confirmar","checkedAt":"2026-10-21",
          "source":"https://www.h2foz.com.br/turismo/passeios/turismo-itaipu-tarifario-precos-dezembro-2025/",
          "note":"Tarifário desde 01/12/2025: inteira R$ 185, meia R$ 92,50. Levar a carteirinha de estudante e documento com foto. O site oficial não mostra a meia: confirmar em (45) 3198-1800 ou atendimento@turismoitaipu.com.br."}

# 2) Cafés: Trigo & Cia -> Airbnb (Trigo vira alternativa)
CAFE_IMG={"src":"/img/foz-do-iguacu/cafe-da-manha.jpg","page":"/img/foz-do-iguacu/cafe-da-manha.jpg","author":"Arquivo do roteiro"}
notes={
 '2026-11-04':("Café rápido no apartamento para cruzar cedo: a meta é estar no Paraguai às 6h. Almoço só sai por volta das 13h. Compras feitas no dia 3, na chegada.",
               "Levar: passaportes (Hortência e Sanderson), RG da Gracinha, dólares em notas novas e azuis, cartões, carregador e sacolas dobráveis. Pegar o carro na garagem e ir direto ao estacionamento perto da ponte."),
 '2026-11-05':("Café das meninas antes do congresso, no apartamento. Sanderson só toma um café aqui; o café da manhã dele é depois de deixá-las.",
               "Pegar o carro na garagem e levar as meninas ao congresso."),
 '2026-11-08':("Café no apartamento antes das Cataratas.","Pegar o carro na garagem e ir às Cataratas."),
 '2026-11-09':("Café da manhã sem pressa no apartamento.","Manhã leve. Pegar o carro na garagem e ir ao Cataratas JL Shopping."),
 '2026-11-10':("Último café no apartamento: aproveitar para terminar o que sobrou das compras.","Pegar o carro na garagem e começar o city tour de Foz."),
}
for date,(cnote,snote) in notes.items():
    items=days[date]['items']
    si=next(i for i,x in enumerate(items) if x['name']=='Saída do Airbnb')
    ci=next(i for i,x in enumerate(items) if x['name']=='Café da manhã · Trigo & Cia')
    saida=items[si]; trigo=items[ci]
    alt={"name":"Café da manhã · Trigo & Cia","type":"food",
         "note":"Padaria 24h a 200 m do Airbnb, se preferir não preparar o café em casa.",
         "place":copy.deepcopy(trigo['place']),"lat":trigo['lat'],"lng":trigo['lng'],
         "cost":trigo['cost'],"costDetails":copy.deepcopy(trigo['costDetails'])}
    people=trigo['costDetails'].get('people',3)
    cafe={"time":trigo['time'],"end":trigo['end'],"type":"food","name":"Café da manhã no Airbnb",
          "note":cnote,"lat":saida['lat'],"lng":saida['lng'],"place":copy.deepcopy(saida['place']),
          "cost":20,"costDetails":{"unit":"pessoa","fullPerPerson":20,"halfPerPerson":None,"halfApplies":False,"payPerPerson":20,
             "people":people,"totalGroup":20*people,"status":"estimativa","checkedAt":"2026-10-21","rangePerPerson":[10,30],
             "note":"Café no apartamento com as compras do supermercado no dia 3. Estimativa por pessoa."},
          "image":CAFE_IMG,"alternatives":[alt]}
    saida['time']=trigo['end']; saida['note']=snote
    rest=[x for i,x in enumerate(items) if i not in (si,ci)]
    pos=min(si,ci)
    if date=='2026-11-10':
        # ordem: café 07:00–07:30 → check-out 07:30–07:45 → saída 07:45
        cafe['time'],cafe['end']='07:00','07:30'
        co=next(x for x in rest if x['name'].startswith('Check-out antecipado'))
        co['time'],co['end']='07:30','07:45'; saida['time']='07:45'
        rest.remove(co)
        days[date]['items']=[cafe,co,saida]+rest
    else:
        days[date]['items']=rest[:pos]+[cafe,saida]+rest[pos:]

# 3) Supermercado no dia 3, entre o aeroporto e o Airbnb
d3=days['2026-11-03']['items']
ai=next(i for i,x in enumerate(d3) if x['name']=='Airbnb Solar das Violetas')
air=d3[ai]
def gm(q,pid): 
    from urllib.parse import quote
    return f"https://www.google.com/maps/search/?api=1&query={quote(q)}&query_place_id={pid}"
mercado={"time":"21:00","end":"21:35","type":"shopping","name":"Super Muffato · compras do café da manhã",
 "note":"Supermercado dentro do Cataratas JL Shopping, no caminho do aeroporto para o Airbnb. Fecha às 22h: chegar até 21h. Lista para 5 cafés dos três (dias 4, 5, 8, 9 e 10, além dos de 6 e 7): pão de forma ou bisnaguinha, frios, queijo, manteiga, ovos, frutas, iogurte, café, leite sem lactose para a Hortência, suco e água. Comprar só o que cabe em 7 dias; o pão fresco dá para repor no Trigo & Cia (24h, a 200 m).",
 "lat":-25.5329826,"lng":-54.5751925,
 "leg":{"mode":"car","minutes":30,"label":"Aeroporto → Av. Costa e Silva, 185 · cerca de 25 min + estacionar · noite"},
 "cost":0,"costDetails":{"unit":"pessoa","fullPerPerson":0,"halfPerPerson":None,"halfApplies":False,"payPerPerson":0,"people":3,"totalGroup":0,
    "status":"estimativa","checkedAt":"2026-10-21","note":"As compras já estão contadas nos cafés no Airbnb (cerca de R$ 20 por pessoa por dia)."},
 "place":{"address":"Av. Costa e Silva, 185 · Cataratas JL Shopping · Polo Centro, Foz do Iguaçu - PR, 85863-000",
    "hours":"Seg–sáb 9h–22h · dom 9h–21h","phone":"(45) 2102-6300","rating":4.5,
    "googlePlaceId":"ChIJGbeB5urw3JQREz_ERVy4wWU","googleMapsUrl":gm("Super Muffato Foz do Iguaçu Shopping Cataratas","ChIJGbeB5urw3JQREz_ERVy4wWU"),
    "photos":[],"lookupKey":"Super Muffato · compras do café da manhã@-25.5329826,-54.5751925"},
 "alternatives":[
  {"name":"Maxxi Atacado","type":"shopping","note":"Atacarejo do grupo Carrefour, em geral mais barato, a cerca de 1 km do Airbnb. Também fecha às 22h. Bom se quiserem comprar em maior quantidade.",
   "place":{"address":"Av. Juscelino Kubitscheck, 2404 · Monjolo, Foz do Iguaçu - PR, 85864-000","hours":"Seg–sáb 7h–22h · dom 8h–18h","phone":"0800 705 5050","rating":4.2,
     "googlePlaceId":"ChIJQdIJEmuQ9pQR01sLvHlueAQ","googleMapsUrl":gm("Maxxi Atacado Foz do Iguaçu","ChIJQdIJEmuQ9pQR01sLvHlueAQ"),"photos":[],
     "lookupKey":"Maxxi Atacado@-25.5219697,-54.5839107"},"lat":-25.5219697,"lng":-54.5839107},
  {"name":"Plano B: comprar no Trigo & Cia","type":"shopping","note":"Se o voo atrasar e o mercado fechar: o Trigo & Cia é 24h e fica a 200 m. Comprar pão, frios, leite e frutas na hora do jantar e fazer um mercado maior depois.",
   "place":copy.deepcopy(next(x for x in d3 if x['name']=='Trigo & Cia')['place']),"lat":-25.5177,"lng":-54.5742}]}
air['time'],air['end']='21:45','22:00'
air['leg']={"mode":"car","minutes":10,"label":"Super Muffato → Airbnb · cerca de 2 km · noite"}
d3.insert(ai,mercado)

json.dump(d,open(P,'w'),ensure_ascii=False,indent=2); open(P,'a').write('\n')
