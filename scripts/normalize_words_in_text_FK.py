import sys
import json

####### input parameters
if len(sys.argv) != 3:
	print("Error, please fill in some information")
	exit()

text_file = sys.argv[1]
output_file = sys.argv[2]
#######

corp= dict()
to_replace = dict()
with open("scripts/normalize_config.json", 'r', encoding="utf-8") as normConf_fd:
	to_replace = json.load(normConf_fd)["words"]

with open (text_file, 'r', encoding='utf-8') as in_f:
	for line in in_f:
		file, text = line.split(' ',1)
		text = text.strip('\n').replace('-', ' ').replace('_', ' ').replace(":","")
		text_tmp = [] 
		for word in text.split(' '):
			if word in to_replace.keys():
				word = to_replace[word]
			text_tmp.append(word)
		corp[file] = ' '.join(text_tmp)

with open (output_file,'w', encoding='utf-8') as out_f:
	for f, t in corp.items():
		out_f.write(f+' '+t + '\n')
