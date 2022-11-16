### This script counts the frequency of occurance of a phone in a speech corpus ###

import sys
from collections import Counter

error_mess = """
This script counts the frequencies of phones in an ASR project,
it returns the number of unique phones, all phones and words
"""

###### input parameters
if len(sys.argv) != 3:
	print(error_mess)
	print("""Usage: <path_to_text> <path_to_lexicon>
		   <path_to_text>, path to the text-file that belongs
		      to the corpus, e.g. ASR1_phatts/train/text,
	 	   <path_to_lexicon>, path to the lexicon that belongs
		      to the corpus, e.g. ASR1_phatts/local/dict/lexicon.txt""")
	exit(1)

text_path = sys.argv[1]
lexicon_path = sys.argv[2]
######

phones = []
words_in_text = []
words_in_lex = []

#Get all words appearing in text-corpus
with open(text_path, "r", encoding = "utf-8") as text_file:
	for line in text_file.readlines():
		text = line.strip("\n").split(" ", 1)[1]
		words_in_text.append(text)

#Get all phones appearing in words
with open (lexicon_path, "r", encoding= "utf-8") as lexicon_file:
	print (" +++ calculation has started! +++")
	for entry in lexicon_file.readlines():
		counter = dict()
		transcriptions = entry.split("\t")[0]
		phonem = entry.strip("\n").split("\t")[1]
		for word in words_in_text:
			if " " in word:
				for w in word.split(" "):
					if w in transcriptions:
						phones.append(phonem)

# Start Counter
w = " ".join(words_in_text).split(" ")
list_of_phones = " ".join(phones).split(" ")
results = Counter(list_of_phones)
t = set(list_of_phones)
print ("number of unique phones:", len(t))
print ("number of all phones:", len(list_of_phones))
print ("number of words:", len(w))
print (results)

