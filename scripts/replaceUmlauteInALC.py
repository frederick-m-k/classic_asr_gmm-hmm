
import sys

in_file = sys.argv[1]
out_file = sys.argv[2]

newtrdict = {'\"U':'Ü','\"A':'Ä','\"O':'Ö','\"S':'ß'}
punctuation = ['\.', '\:', '\,', '\;', '-']
textlist = []

with open(in_file, 'r', encoding="utf-8") as inf:
	for line in inf:
		tmp_line = line.strip("\n")
		for char in newtrdict.keys():
			if char in tmp_line:
				tmp_line = tmp_line.replace(char, newtrdict[char])
		textlist.append(tmp_line)

with open(out_file,'w', encoding="utf-8") as outf:
	for sent in textlist:
		outf.write(sent+"\n")
