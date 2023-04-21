import re
count = 0
pattern = re.compile('ab')
match = pattern.finditer('abaababa')
for m in match:
    count += 1
    print('Start : {}, End : {}, Group : {}'.format(m.start(), m.end(), m.group()))
print(f'The number of occurrences : {count}')
