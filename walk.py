import os
dirr = 'accnts'
for d, sdir, flist in os.walk(dirr):
	for f in flist:
		ff = os.path.join(dirr,f)
		f1 = open(ff,'r')
		# l = f1.readLine()
		# l = l.split(' ')
		for l in f1:
			print(l)