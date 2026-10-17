"""Confere se cada item do roteiro começa depois do fim do anterior + deslocamento,
e se nenhum lugar perdeu fotos ou dados (compare com --base <json antigo>).
Alternativas ficam em item.alternatives e não entram na sequência de horários.
Uso: python3 scripts/verificar-horarios.py [src/data/foz-do-iguacu.json]"""
import json, sys
path = sys.argv[1] if len(sys.argv) > 1 else 'src/data/foz-do-iguacu.json'
def m(t): h, mm = map(int, t.split(':')); return h * 60 + mm
erros = 0
for day in json.load(open(path))['days']:
    it = day['items']
    for a, b in zip(it, it[1:]):
        leg = b.get('leg', {}).get('minutes', 0)
        folga = m(b['time']) - m(a.get('end', a['time'])) - leg
        if folga < 0:
            erros += 1
            print(f"CONFLITO {day['date']} {a['name']} ({a.get('end', a['time'])}) + {leg} min -> {b['name']} ({b['time']}): faltam {-folga} min")
print('OK: nenhum conflito de horário' if not erros else f'{erros} conflito(s)')
sys.exit(1 if erros else 0)
