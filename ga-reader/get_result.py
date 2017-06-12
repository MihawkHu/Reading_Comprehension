import os

id_list = []
ans_list = []
with open('raw.txt') as f:
	id_list = f.readlines()
cnt = 0
content = ''
query = ''
cand = []
with open('test.txt') as f:
	for line in f:
			if(cnt%22 + 1 == 21):
				prefix = line.split(' ')[0]
				query = line.replace(prefix, '', 1).strip().split('\t')[0]
				query = query.replace('XXXXX', '@placeholder', 1)
				cand = line.split('\t')[-1].strip().split('|')
				ans_list.append(cand[eval(id_list[cnt/22].strip())].strip())
			cnt += 1

with open('result.txt', 'w') as f:
	for i in range(0, 2500):
		f.write(ans_list[i] + '\n')
		
		
		
