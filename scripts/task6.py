
import sys

####### input parameters
if len(sys.argv) != 3:
	print("This script shall create the nonsilence_phones.txt file sorted")
	print()
	print("Usage: " + __file__ + " <lexicon_file> <nonsil_file>")
	print("   e.g.: " + __file__ + "data/grass-read.dict data/local/dict/nonsilence_phones.txt")
	exit()

lexicon_file = sys.argv[1]
nonsil_file = sys.argv[2]
#######

all_phonemes = set()
with open(lexicon_file, 'r', encoding="utf-8") as lex_fd:
	for line in lex_fd.readlines():
		_, phonemes = line.strip('\n').split('\t')
		for phoneme in phonemes.split(' '):
			all_phonemes.add(phoneme)

with open(nonsil_file, 'w', encoding="utf-8") as nonsil_fd:
	for phoneme in sorted(list(all_phonemes)):
		nonsil_fd.write(phoneme + '\n')
