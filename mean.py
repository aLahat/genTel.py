def mean(n):
	return sum(n)/len(n)

f = open('output.fpkm_tracking.csv')
table = f.read().split('\n')
f.close
header = table[0].split('\t')
table = table[1:]

data =[]
for line in table:
	line = line.split('\t')
	d={}
	for i in range(len(line)):
		d.update({header[i]:line[i]})
	data.append(d)


jointNames = ['3Y','10AL','10DR','15AL','15DR','30AL','30DR']
headerClean = header[2:-2]
headDirt = header[:2]+header[-2:]
HEAD = headDirt + jointNames
rule = dict.fromkeys(headerClean)

n=0
for h in jointNames:
	for i in range(3):
		rule[headerClean[n]]=h
		n+=1
output = ['\t'.join(HEAD)]	
for line in data:

	lineOut={}
	for k in line:
		if k in rule:
			if not(rule[k] in lineOut): lineOut.update({rule[k]:[]})
				
			lineOut[rule[k]].append(float(line[k]))
	out=[]
	for i in lineOut:
		lineOut[i] = str(mean(lineOut[i]))
	for i in headDirt:
		out.append(line[i])
	for i in jointNames:
		out.append(lineOut[i])
	output.append('\t'.join(out))

output = '\n'.join(output)
f = open('mean.fpkm_tracking.csv','w')
f.write(output)
f.close()
