
import csv, sys

def id2phone(phonestxt, ctmfilename):
	'''Replace phone-IDs in CTM file, with actual phones'''
	with open(phonestxt, 'r') as phonefile:
		phones = list(csv.reader(phonefile, delimiter=' '))

	with open(ctmfilename, 'r') as ctmfile:
		ctm = list(csv.reader(ctmfile, delimiter=' '))

	id2phone = {}
	for row in phones: # build own dict for mapping phones to integer
		id2phone[row[1]] = row[0]

	for phone in ctm:
		phone_id = phone[-1]
		phone_name = id2phone[phone_id]
		phone[-1] = phone_name

	with open(ctmfilename.split('.c')[0] + "-updated.ctm", 'w') as ctmfile:
		ctmout = csv.writer(ctmfile, delimiter=' ')
		for phone in ctm:
			ctmout.writerow(phone)
	return ctmfilename.split('.c')[0] + "-updated.ctm"

def main():
	if (len(sys.argv) < 2):
		print("Usage: python3 id2phone.py <phonelvl.ctm> <phones.txt>")
		print("phones.txt should be the mapping of each phone to its corresponding integer value")
		exit(1)
	ctmfilename = sys.argv[1]
    	#phonestxt = 'exp/tdnn_7b_chain_online/phones.txt'
	phonestxt = sys.argv[2]
	id2phone(phonestxt, ctmfilename)

if __name__ == '__main__':
	#main()
	print("Did you run the wrong script?")
	print("Yes, you did")
	print("You should run run.py")
