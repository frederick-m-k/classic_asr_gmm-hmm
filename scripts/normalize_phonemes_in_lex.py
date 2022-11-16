
import sys
import json

####### input parameters
if len(sys.argv) != 3:
	print("This script iterates over all words in a lexicon and replaces some phones for others.")
	print("Currently, the following phones get replaced: T, D, Z, a~, y:6, 2:6, E:6")
	print()
	print("Usage: " + __file__ + " <lexicon_file> <output_file>")
	print("   e.g.: " + __file__ + " data/grass-read.dict data/updated_grass.dict")
	exit()

lexicon_file = sys.argv[1]
output_file = sys.argv[2]
#######

replacements = dict()
with open("scripts/normalize_config.json", 'r', encoding="utf-8") as normConf_fd:
	replacements = json.load(normConf_fd)["phonemes"]

new_lines = []
with open(lexicon_file, 'r', encoding="utf-8") as lex_fd:
	for line in lex_fd.readlines():
		word, transcript = line.strip('\n').split('\t')
		new_transcript = []
		for phoneme in transcript.split(' '):
			if phoneme in replacements.keys():
				new_transcript.append(replacements[phoneme])
			else:
				new_transcript.append(phoneme)
		new_lines.append(word + '\t' + ' '.join(new_transcript))

with open(output_file, 'w', encoding="utf-8") as out_fd:
	for line in new_lines:
		out_fd.write(line + '\n')
