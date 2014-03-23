#script that adds telomere and centromere distances to fpkm_tracking files
#needs the fpkm file and a hg gap table

import os
os.system('clear')

def readHG():
	f = open('mm10.hg','r')
	hg = f.read().split('\n')[2:-2]
	f.close()	
	chromosomes = {}
	for line in hg:
		parts =  line.split('\t')
		CHR = parts[1][3:]
		start = int(parts[2])
		end = int(parts[3])
		type = parts[-2]
		#print(CHR + '\t' + str(start) + '\t' + str(end) + '\t' + type)
		if not(CHR in chromosomes): 
			chromosomes.update({CHR:{'telomere':[],'centromere':[]}})
		chromosomes[CHR][type].append(start)
		chromosomes[CHR][type].append(end)
	for CHR in chromosomes:
		chromosomes[CHR]['telomere']=sorted(chromosomes[CHR]['telomere'])[1:-1]
	return chromosomes
def findClosest(what,CHR,where,hg):
	locations = hg[CHR][what]
	distances = []
	if locations == []:
		return 'none'
	for d in locations:
		distances.append(abs(d-where))
	dist=str(sorted(distances)[0])
	return dist

hg = readHG()

f = open('genes.fpkm_tracking','r')
fpkm = f.read()
f.close()
header = fpkm.split('\n')[0].split('\t')[4:]+['telomere','centromere']


output=[]

fpkm = fpkm.split('\n')[1:-1]
for gene in range(len(fpkm)): 
	fpkm[gene] = fpkm[gene].split('\t')

	locus = fpkm[gene][6].split(':')
	CHR = locus[0]

	#calculates mid of gene
	startEnd = locus[1].split('-')
	mid = sum([int(startEnd[0]),int(startEnd[1])])/2

	#adds telomere and centromere distances
	try: fpkm[gene].append(findClosest('telomere',CHR,mid,hg ))
	except: fpkm[gene].append('none')
	try: fpkm[gene].append(findClosest('centromere',CHR,mid,hg ))
	except: fpkm[gene].append('none')
	#removes columns 
	fpkm[gene]=fpkm[gene][4:]
	acceptedHeader = ['name','ocus','FPKM','mere']
	line =[]
	for i in header:
		if i[-4:] in acceptedHeader:
			locus = header.index(i)
			line.append(fpkm[gene][locus])
	output.append('\t'.join(line))



head = []
for i in header:
	if i[-4:] in acceptedHeader:
		locus = header.index(i)
		head.append(header[locus])
head = '\t'.join(head)
output = head + '\n'+'\n'.join(output)


f = open('output.fpkm_tracking.csv','w')
f.write(output)
f.close()
