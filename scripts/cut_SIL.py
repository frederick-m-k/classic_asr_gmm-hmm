import os
import sys

model_txt = sys.argv[1]
silencephones = sys.argv[2]
lexicon = sys.argv[3]
output_txt = sys.argv[4]

silence_words = []
silence_phones = []

with open (silencephones, "r", encoding="utf-8") as silence_phones_file:
	for line in silence_phones_file:
		silence_phones.append(line.strip("\n"))

with open (lexicon, "r", encoding="utf-8") as silence_words_file:
	for line in silence_words_file:
		line = line.strip("\n")
		word, phonem = line.split('\t')
		word = word.strip(' ')
		phonem = phonem.strip(' ')
		if phonem in silence_phones:
			silence_words.append(word)

silence_words = list(set(silence_words))

new_lines= []
with open (model_txt, "r", encoding = "utf-8") as input:
	for line in input:
		line = line.strip("\n")
		new_list = []
		for word in line.split(" "):
			if not word in silence_words:
				if "!SIL" == word:
					print("Gefunden")
				new_list.append(word)
		new_lines.append(new_list)

with open (output_txt, "w", encoding = "utf-8") as outfile:
	for line in new_lines:
		outfile.write(" ".join(line) + "\n")
