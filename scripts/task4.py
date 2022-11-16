
import os, sys

corp_lex_file = sys.argv[1]
data_dir = sys.argv[2]

all_phones = set()

with open(corp_lex_file, 'r', encoding="utf-8") as lex_file:
	all_trans = dict()
	for lex_line in lex_file.readlines():
		trans, _, phones = lex_line.strip('\n').split('\t')
		if '*' in trans or '~' in trans:
			continue
		trans = trans.replace('\"', '').upper()
		all_trans[trans] = phones

	with open(data_dir + "/train/text", 'r', encoding="utf-8") as text_file:
		grass_dict = dict()
		for text_line in text_file.readlines():
			rec_trans = text_line.strip('\n').split(' ')[1:]
			for word in rec_trans:
				if word == '':
					continue
				grass_dict[word] = all_trans[word]
				for phone in all_trans[word].split(' '):
					all_phones.add(phone)

# task 5
with open(data_dir + "/grass-read.dict", 'w', encoding="utf-8") as grass_file:
	for trans, phones in grass_dict.items():
		grass_file.write(trans + '\t' + phones + '\n')
