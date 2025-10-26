import csv, random, datetime, os, json
heroes = [h['name'] for h in json.load(open(os.path.join(os.path.dirname(__file__),'..','data','mlbb','meta.json')))['heroes']]
out = []
for i in range(1000):
    t0 = random.sample(heroes, 3)
    t1 = random.sample([h for h in heroes if h not in t0], 3)
    winner = 'A' if random.random() > 0.5 else 'B'
    out.append({'match_id': f'ml-{i}', 'teamA':'|'.join(t0), 'teamB':'|'.join(t1), 'winner':winner, 'timestamp': datetime.datetime.utcnow().isoformat()})
path = os.path.join(os.path.dirname(__file__),'..','data','mlbb_dataset.csv')
with open(path,'w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['match_id','teamA','teamB','winner','timestamp'])
    w.writeheader(); w.writerows(out)
print('Wrote', path)
