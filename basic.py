from nltk.tag import pos_tag_sents
import nltk
import os

file = open('sam2.txt', 'r') 
texts = file.readlines()
text_tokenized = []
for txt in texts:
	[date,text] = txt.strip().split('@')
	text = text.lower()
	text_tokenized.append(nltk.word_tokenize(text)) 
pos = pos_tag_sents(text_tokenized)

journal = open('journal.txt', 'w')

journal.write('------------------------------------------------------------------------------------------\n')
journal.write('Date \t\t\t\t\tParticulars\t\t\t\t\t\t\t\t\tAmount(Rs.)\n')
journal.write('%-10s 	%-20s%20s' %('', '  Dr.', 'Cr.\n'))
journal.write('==========================================================================================\n\n')

cash = open(os.path.join('ledgers', 'cash'), 'w')
cash.write('------------------------------------------------------------------------------------------\n')
cash.write('Date \t\t\t\t\tParticulars\t\t\t\t\t\t\t\t\tAmount(Rs.)\n')
cash.write('%-10s 	%-20s%20s' %('', '  Dr.', 'Cr.\n'))
cash.write('==========================================================================================\n\n')
cash.close()

for j in range(0,len(texts)):
	[date,text] = texts[j].strip().split('@')
	amount = 0
	noun = []
	verb = []
	for k,v in pos[j]:
		if k == 'rs' or k == 'rs.':
			continue
		if v == 'CD':
			amount = k
		if v == 'VB' or v == 'VBD' or v == 'VBG' or v == 'VBP' or v == 'VBN' or v == 'VBZ':
			verb.append(k)
		if v == 'NN' or v == 'NNS' or v == 'NNP' or v == 'NNPS' or v == 'JJ' or v == 'JJR' or v == 'JJS':
			noun.append(k)

	f1 = open('credit.txt', 'r')
	l = f1.readline()
	l = l.split(' ')
	state = 0 # for cash debit
	for v in verb:
		if v in l:
			state = 1 # for cash credit
	f1.close()

	acc_name = ''
	dirr = 'accnts'
	for d, sdir, flist in os.walk(dirr):
		for f in flist:
			ff = os.path.join(dirr,f)
			f1 = open(ff,'r')
			for l in f1:
				words = l.split(' ')
				for n in noun:
					if n in words:
						acc_name = f

	if acc_name == '':
		acc_name = noun[0]

	if(state == 0 and acc_name == 'goods.txt'):
		acc_name = 'sales.txt'
	if(state == 1 and acc_name == 'goods.txt'):
		acc_name = 'purchase.txt' 

	acc = acc_name.split('.')[0]

	for d, sdir, flist in os.walk('ledgers'):
		if acc not in flist:
			f2 = open(os.path.join('ledgers', acc), 'w')
			f2.write('------------------------------------------------------------------------------------------\n')
			f2.write('Date \t\t\t\t\tParticulars\t\t\t\t\t\t\t\t\tAmount(Rs.)\n')
			f2.write('%-10s 	%-20s%20s' %('', '  Dr.', 'Cr.\n'))
			f2.write('==========================================================================================\n\n')
			f2.close()

	f1 = open(os.path.join('ledgers', 'cash'), 'a')
	f2 = open(os.path.join('ledgers', acc), 'a')

	# f1.write('------------------------------------------------------------------------------------------\n')
	# f1.write('Date \t\t\t\t\tParticulars\t\t\t\t\t\t\t\t\tAmount(Rs.)\n')
	# f1.write('%-10s 	%-20s%20s' %('', '  Dr.', 'Cr.\n'))
	# f1.write('==========================================================================================\n\n')

	# f2.write('------------------------------------------------------------------------------------------\n')
	# f2.write('Date \t\t\t\t\tParticulars\t\t\t\t\t\t\t\t\tAmount(Rs.)\n')
	# f2.write('%-10s 	%-20s%20s' %('', '  Dr.', 'Cr.\n'))
	# f2.write('==========================================================================================\n\n')


	if state == 0:
		journal.write('%-10s	%-40s			%-20s' %(date, 'cash a/c', amount))
		journal.write('\n')
		journal.write('%-10s    %40s	    	%20s' %('', acc +' a/c', amount))
		journal.write('\n')
		f1.write('%-10s    %40s	    	%20s' %(date, acc +' a/c', amount))
		f1.write('\n')
		f2.write('%-10s 	%-40s			%-20s' %(date, 'cash a/c', amount))
		f2.write('\n')
	else:
		journal.write('%-10s	%-40s			%-20s' %(date, acc +' a/c', amount))
		journal.write('\n')
		journal.write('%-10s    %40s    		%20s' %('',  'cash a/c', amount))
		journal.write('\n')
		f1.write('%-10s    %-40s	    	%-20s' %(date, acc +' a/c', amount))
		f1.write('\n')
		f2.write('%-10s    %40s    		%20s' %(date,  'cash a/c', amount))
		f2.write('\n')

	f1.write('------------------------------------------------------------------------------------------')
	f1.write('\n')
	f2.write('------------------------------------------------------------------------------------------')
	f2.write('\n')
	f1.close()
	f2.close()
	journal.write('------------------------------------------------------------------------------------------')
	journal.write('\n')
print("Journal updated!!!")
journal.close()
