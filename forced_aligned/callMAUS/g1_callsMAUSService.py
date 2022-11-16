import requests
import xml.etree.ElementTree as ET
import codecs
import argparse
import os, sys
"""
parser = argparse.ArgumentParser()
parser.add_argument("language", help="language of the MAUS acoustic model, e.g. 'deu-DE'")
parser.add_argument("skip", help="skip existing output files, e.g.'skip', 'overwrite'")
parser.add_argument("--format", help="format of the output file (default: csv)", dest="format", default="csv")
parser.add_argument("dir", help = "path you are in", nargs = '?', default = os.getcwd()) # current path
"""

url = "https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runMAUSBasic"
usage_mess= """
Usage: <corp_dir> <data_dir> <trans_dir>
e.g. ../../../corpora/phattsessionz ../../phatts_FK4forcedALign ./phattsFKforcedAlign
"""
###### input parameters
if len(sys.argv) != 4:
	print (usage_mess)
	exit(1)

corp_dir = sys.argv[1]
data_dir = sys.argv[2]
trans_dir = sys.argv [3]

language = "deu-DE"
#modus = "align"
#wav_dict = {}
wavfiles = []
ids = []
with open(data_dir + "/train/wav.scp", "r", encoding="utf-8") as input:
	for line in input:
		id = line.split(" ")[0]
		wav_name = line.strip("\n").split("/")[3:]
		wav_name = "/".join(wav_name)
#		wav_dict[id] = [wav]
		ids.append(id)
		wavfiles.append(wav_name)

for wavfile in wavfiles:
	wavi = wavfile.split("/")[1]
	textfile = wavfile.split("/")[1].replace(".wav", ".txt")
	outname = textfile.replace(".txt", ".TextGrid")
	print ("Processing")
	print (wavfile, textfile, outname)
#	textfilePath = path + "/" + textfile #path for all txt
#	outnamePath = path + '/' + outname #path for all csv

#	if os.path.exists(trans_dir + "ohne_align/") and os.path.isfile(trans_dir + "ohne_align/" + outname):
#		print("SKIPPING: " + outname)
#	else:
#		print(textfile)

	formdata = {
		"SIGNAL": (wavi, open(corp_dir + "/" + wavfile, "rb"), "audio/x-wav"),
		"TEXT": (textfile, open(trans_dir + "/" + textfile, "r"), "text/txt"),
		"LANGUAGE": (None, language),
		"OUTFORMAT": (None, "TextGrid"),
		"MODUS" : (None, "align"),
		}

	res = requests.post(url, files=formdata)
	if res.status_code == 200:
		try:
			tree = ET.fromstring(res.text)
			res2 = requests.get(tree.find('downloadLink').text)
			if res2.status_code == 200:
				outfile = codecs.open(trans_dir + "/forced_aligned_TGs" + "/" + outname, mode="w", encoding="utf-8")
				outfile.write(res2.text)
				outfile.close()

		except:
			print("ERROR: " + res.text)

