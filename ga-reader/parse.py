import os

cnt = 0
content = ''
query = ''
cand = []
with open('test.txt') as f:
	for line in f:
			if(cnt%22 + 1 <= 20):
				prefix = line.split(' ')[0]
				line = line.replace(prefix, '', 1).rstrip()
				content += line
			elif(cnt%22 + 1 == 21):
				with open ('test_txt/'+str(cnt/22+1)+'.question' ,'w') as g:
					g.write(content)
				prefix = line.split(' ')[0]
				query = line.replace(prefix, '', 1).strip().split('\t')[0]
				query = query.replace('XXXXX', '@placeholder', 1)
				cand = line.split('\t')[-1].strip().split('|')
			else:
				with open ('test_new/'+str(cnt/22+1)+'.question' ,'w') as g:
					g.write('http://some_url')
					g.write('\n')
					g.write('\n')
					g.write(content.lower())
					g.write('\n')
					g.write('\n')
					g.write(query.lower())
					g.write('\n')
					g.write('\n')
					g.write(cand[0].lower())
					g.write('\n')
					g.write('\n')
					for one in cand:
						g.write(one.lower())
						g.write('\n')
				content = ''
			cnt += 1

with open ('test_new/'+str(cnt/22+1)+'.question' ,'w') as g:
					g.write('http://some_url')
					g.write('\n')
					g.write('\n')
					g.write(content.lower())
					g.write('\n')
					g.write('\n')
					g.write(query.lower())
					g.write('\n')
					g.write('\n')
					g.write(cand[0].lower())
					g.write('\n')
					g.write('\n')
					for one in cand:
						g.write(one.lower())
						g.write('\n')

