from pprint import pprint
import re

CONFIG = {}

with open('config/bot.config', 'r', encoding='utf-8') as f:
    file = f.read().split('\n')

klevel = []

for line in file:
    if line.strip() == '' and len(klevel) > 0:
        klevel.pop(-1)

    if re.match(r'\b[a-z]*:', line):
        CONFIG[line[:-1]] = {}
        klevel = []
        klevel.append(line[:-1])
        continue

    if re.match(r'\b.*', line) and len(klevel) == 3:
        CONFIG[klevel[0]][klevel[1]][klevel[2]] += f'\n{line}'
        continue

    if re.match(r'\s{4}\b[a-z]*:', line):
        # if 'intents' not in CONFIG:
        #     CONFIG['intents'] = None
        if len(klevel) > 1:
            klevel.pop(-1)

        CONFIG[klevel[0]][line.strip(' :')] = {}
        klevel.append(line.strip(' :'))
        continue
    
    if re.match(r'\s{8}\b[a-z]*:', line):
        # if 'intents' not in CONFIG:
        #     CONFIG['intents'] = None
        CONFIG[klevel[0]][klevel[1]][line.strip(' :')] = []
        klevel.append(line.strip(' :'))
        continue

    if re.match(r'\s{12}\b.*', line) and len(klevel) == 3:
        CONFIG[klevel[0]][klevel[1]][klevel[2]].append(line.strip())
        continue

    if re.match(r'\s{12}\b.*', line) and len(klevel) == 1:
        if CONFIG[klevel[0]] == {}:
            CONFIG[klevel[0]] = []
        CONFIG[klevel[0]].append(line.strip())
        continue

pprint(CONFIG)
