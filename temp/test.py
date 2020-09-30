import json

f1 = open('../data/Dataset1.json', 'r')
f2 = open('../data/Dataset2.json', 'r')
f3 = open('../data/Dataset3.json', 'r')
f_o = open('output.txt', 'w')
count = 0

for f in [f1, f2, f3]:
    for line in f:
        gt = json.loads(line)['ground_truth']

        for item in gt:
            for token in item['consensus']['tokens']:
                f_o.write(token['word'] + ' ' + token['lang'] + '\n')
            f_o.write('\n')
            count += 1

print(count)
