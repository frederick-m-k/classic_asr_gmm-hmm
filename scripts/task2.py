
import os, sys

####### input parameters
if len(sys.argv) != 2:
	print("Usage: " + __file__ + " <data_path>")
	print("  e.g.: " + __file__ + " data/test")
	print("  e.g.: " + __file__ + " phatts_cleaned_data/test_phatts")
	exit()

data_path = sys.argv[1]
if data_path.endswith('/'):
	data_path = data_path.rstrip('/')
#######

spk2utt = dict()
with open(data_path + "/wav.scp", 'r', encoding="utf-8") as wav_scp:
	for wav_line in wav_scp.readlines():
		rec_name = wav_line.split(' ')[0]
		spk_name = rec_name[3:7]
		if not spk_name in spk2utt.keys():
			spk2utt[spk_name] = []
		spk2utt[spk_name].append(rec_name)

with open(data_path + "/spk2utt", 'w', encoding = "utf-8") as spk2utt_file:
	for spk, utts in spk2utt.items():
		spk2utt_file.write(spk + ' ' + ' '.join(utts) + '\n')
