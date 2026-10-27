import json
p='src/data/foz-do-iguacu.json'; d=json.load(open(p))
B=lambda how,url,cta='Comprar ingresso',deadline=None,title='Comprar antes':dict(title=title,how=how,url=url,cta=cta,booking=True,**({'deadline':deadline} if deadline else {}))
T={
'Yup Star':B('Comprar online a tarifa estudante (R$ 39,90) para os 3; levar DNE + RG.','https://foz.yupstar.com.br/'),
'Marco das Três':B('Comprar online a meia (R$ 35,25) para os 3; testar cupom de 15% de sites parceiros sobre a meia (pode cair para ~R$ 30). Levar carteirinha.','https://marcodastresfronteiras.com.br/'),
'AquaFoz':B('Comprar no site oficial até 04/11 (1 dia antes): a meia cai de R$ 75 para R$ 67,50. Levar comprovante de meia.','https://aquafoz.com.br/',deadline='Comprar até qua 04/11'),
'Itaipu · Circuito':B('Comprar no site oficial a saída das 9h (vagas limitadas). Confirmar se há meia para estudante (economia ~R$ 90) e o calçado exigido.','https://www.turismoitaipu.com.br/pt',deadline='Comprar já (vagas limitadas)'),
'City Tour Paraguai':B('Pedir orçamento a 2–3 agências da versão só city tour, pagar no Pix e pedir desconto fechando junto com o By Night. Combinar busca às 8h15 no Airbnb.',None,cta=None,title='Fechar com agência'),
'Cataratas do Iguaçu':B('Comprar online no site oficial (sem meia para estudante). Não compensa o combo com AquaFoz.','https://tickets.cataratasdoiguacu.com.br/'),
'Parque das Aves':B('Comprar online a meia (R$ 55) para os 3; levar carteirinha + RG. Preço válido até 30/11.','https://www.parquedasaves.com.br/'),
'Kattamaram II':B('Comprar a tarifa estudante sem buffet (R$ 120) no site oficial. Perguntar no WhatsApp se há promoção para domingo antes de pagar.','https://kattamaram.com.br/por-do-sol-com-jantar-a-bordo/'),
'Wonder Park':B('Comprar o passaporte 5 atrações reduzido (R$ 170) e reservar a sessão das 20h do Wonder Games. Antes, ver se algum cupom (Laçador de Ofertas) vale para o passaporte.','https://ingresso.wonderparkfoz.com.br/produto/vitrine/passaporte'),
'MMC Turismo':B('Reservar com 2 dias de antecedência, para os 3. Pedir Hito Tres Fronteras e Cassino, confirmar se R$ 110 é por pessoa e pedir desconto no Pix.','https://mmcturismo.com.br/passeios/puerto-iguazu-arg/transporte/by-night-argentina/9',cta='Reservar transporte',deadline='Reservar até sáb 07/11'),
}
R={ # restaurantes: só adiciona url
'Pátio Pomare':'https://wa.me/5545910152 53'.replace(' ',''),
'Bona Trattoria':'https://wa.me/5545999247162',
'Di Paolo':'tel:08007252025',
}
n=0
for day in d['days']:
  for it in day['items']:
    for k,v in T.items():
      if k in it['name']:
        if not v['url']: v={x:y for x,y in v.items() if x not in('url','cta')}
        it['promo']=v; n+=1
    if 'Pátio Pomare' in it['name'] or 'Bona Trattoria' in it['name']:
      it['promo']=dict(title='Precisa de reserva',booking=True,how=('Assinar Prime Gourmet (R$ 200) e reservar com sinal pelo WhatsApp.' if 'Pomare' in it['name'] else 'Reservar mesa para 3 na sexta à noite pelo WhatsApp.'),url=R['Pátio Pomare' if 'Pomare' in it['name'] else 'Bona Trattoria'],cta='Reservar no WhatsApp'); n+=1
    if 'Di Paolo' in it['name']:
      it['promo']['url']=R['Di Paolo']; it['promo']['cta']='Ligar para o Concierge'; n+=1
    if 'AquaFoz' in it['name']:
      it['cost']=67.5; c=it['costDetails']; c.update(payPerPerson=67.5,halfPerPerson=67.5,totalGroup=67.5,status='oficial (compra antecipada)',checkedAt='2026-10-20')
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2); print('itens atualizados',n)
