import math
def log2(x,y):
	x= float(x)
	if 0 in [x,y]:
		return None
	return math.log(y/x,2)

def combine(x,y,File = 'mean.fpkm_tracking.csv'):
	f = open(File,'r')
	table = f.read().split('\n')
	f.close()
	head = table[0].split('\t')
	toKeep = [0,1,2,3]
	for i in [x,y]:
		toKeep.append(head.index(i))
	toKeep = sorted(toKeep)
	toKeep.reverse()
	newTable =[]
	for i in table:
		line = i.split('\t')
		for n in range(len(line)-1,-1,-1):
			if not(n in toKeep):
				line.pop(n)
		try:
			X = float(line[-2])
			Y = float(line[-1])
			line.append(str(log2(X,Y)))
		except:
			line.append('log2_fold_change')
		newTable.append('\t'.join(line))
	
	name=x+'_'+y+'.csv'
	f = open(name,'w')
	f.write('\n'.join(newTable))
	f.close()


		
		
		


f = open('mean.fpkm_tracking.csv','r') 
titles = f.read().split('\n')[0].split('\t')[4:]
f.close
combinations = []
for x in titles:
	for y in titles:
		if not(x == y):
			option = [x,y]
			if not(option in combinations):
				combinations.append(option)


for i in combinations:
	print i
	combine(i[0],i[1])

