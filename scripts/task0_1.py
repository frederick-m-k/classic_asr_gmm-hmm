
import os, sys
import random

info_mess="""
This script corresponds to the tasks 0 and 1 in the Graz tutorial.
The wav.scp and text files will get created in here.
Therefore, all utterances are first gatherered.
\tIf there is a content_table.tab file in the <corpus_path>, it will be used.
\tOtherwise, the existing .par files will be used.
"""

###### input parameters
if len(sys.argv) != 6:
	print("Usage: " + __file__ + " <corpus_path> <content_table> <data_dir> <how_many_utts> <further_specification>")
	print("  e.g.: " + __file__ + " ../corpora/phattsessionz ../corpora/phattsessionz/content_table.tab data/test 20 digits")
	print("  e.g.: " + __file__ + " ../corpora/phattsessionz ../corpora/phattsessionz/content_table.tab phatts_cleaned_data/train all None")
	print("  <how_many_utts>: either an integer value of how many utterances have to be included in the set")
	print("                    or \"all\" to include all utterances")
	print("  <further_specification>: digits, None")
	print("                           digits will only include utterances consisting of digits from \"null\" to \"zwanzig\"")
	print("                           None will result in no further specifications")
	exit()

# should be corpora/corp_name
path = sys.argv[1]
path = path.rstrip('/') + '/'

content_table = sys.argv[2]

which_data = sys.argv[3] # e.g. data or phatts_cleaned_data or ...
which_data = which_data.rstrip('/')

how_many = sys.argv[4]
further_specification = sys.argv[5]
#######

digits = ["null", "eins", "zwo", "zwei", "drei", "vier", "sechs", "sieben", "acht", "neun", "zehn", "elf", "dreizehn", "vierzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn", "zwanzig"]

wav_dict = dict()
with open(which_data + "/wav.scp", 'w', encoding="utf-8") as wav_scp:
	for dir in sorted(os.listdir(path)):
		if os.path.isdir(path + dir):
			for rec_file in sorted(os.listdir(path + dir)):
				if rec_file.endswith("_0.wav") or (rec_file.endswith("_00.wav") and not rec_file.endswith("_m_00.wav")): # the last thing is something for ALC. To exclude the files which have no .par partner
					rec_name = rec_file.split(".")[0]
					wav_dict[rec_name] = path + dir + '/' + rec_file + '\n'

	all_trans = dict()
	if os.path.isfile(content_table):
		with open(content_table, 'r', encoding="utf-8") as cont_tbl:
			first_line = False
			for cont_line in cont_tbl.readlines():
				if not first_line:
					first_line = True
					continue
				filename, _, _, trans = cont_line.strip('\n').split('\t')
				if '*' in trans or '~' in trans:
					continue
				if '\'' in trans or  "/" in trans:
					continue
				all_trans[filename + '_0'] = trans.replace('\"', '').upper()
	else: # there is no content_table.tab
		for sub_dir in sorted(os.listdir(path)):
			if os.path.isdir(path + sub_dir):
				for sub_file in os.listdir(path + sub_dir):
					whole_file = path + sub_dir + '/' + sub_file
					file_id = sub_file.split('.')[0] 
					if sub_file.endswith(".par"):
						sentence = []
						for line in open(whole_file, 'r', encoding="utf-8").readlines():
							# first check for ORT:, the split it up, because there are some lines in the .par files which have no two '\t'
							if line.split('\t')[0] == "ORT:":
								_, _, trans = line.strip('\n').split('\t')
								sentence.append(trans)
						all_trans[file_id] = ' '.join(sentence).upper()

	if further_specification != "None":
		if further_specification == "digits":
			new_trans = dict()
			for filename, trans in all_trans.items():
				found_non_digit = False
				for word in trans.split(' '):
					if not word in digits and not word in [d.upper() for d in digits]:
						found_non_digit = True
				if not found_non_digit:
					new_trans[filename] = trans
			all_trans = new_trans
		else:
			print("Did you give a correct argument for <further_specification> ?")
			print("Proceeding as like <further_specification> is None")

	if how_many == "all":
		print("all utterances will be included: " + str(len(all_trans.keys())))
	else:
		many = int(how_many)
		print(str(many) + " random utterances will be included")
		keys = random.sample(all_trans.keys(), many)
		values = [all_trans[k] for k in keys]
		all_trans = dict(zip(keys, values))

	with open(which_data + "/text", 'w', encoding = "utf-8") as text_file:
		for filename, trans in all_trans.items():
			if filename in wav_dict.keys():
				text_file.write(filename + ' ' + trans + '\n')
				wav_scp.write(filename + ' ' + wav_dict[filename])
