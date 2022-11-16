
import os, sys
import json

import utils
from enum import Enum

class PhoneType(Enum):
	VOWELS = "VOW"
	CONSONANTS = "CON"
	FRICATIVES = "FRI"
	NASAL = "NAS"
	PLOSIVES = "PLO"
	AFFRICATES = "AFF"
	SINGLE_VOWELS = "S_VOW"
	SINGLE_CONSONANTS = "S_CON"
	DIPHTONGS = "DIP"
	LEFTOVER_CONS = "LEFTOV"
	
phon_types = dict()
phon_types[PhoneType.SINGLE_CONSONANTS.value] = ["C", "N", "S", "b", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v", "x", "z"]
phon_types[PhoneType.LEFTOVER_CONS.value] = ["l", "r"]
phon_types[PhoneType.FRICATIVES.value] = ["C", "S", "f", "h", "j", "s", "v", "x", "z"]
phon_types[PhoneType.NASAL.value] = ["N", "m", "n"]
phon_types[PhoneType.PLOSIVES.value] = ["?", "b", "d", "g", "k", "p", "t"]
phon_types[PhoneType.AFFRICATES.value] = ["dZ", "dz", "tS", "ts"]
phon_types[PhoneType.SINGLE_VOWELS.value] = ["2:", "6", "9", "@", "E", "E:", "I", "O", "U", "Y", "a", "a:", "e", "e:", "i", "i:", "o", "o:", "u", "u:", "y", "y:"]
phon_types[PhoneType.DIPHTONGS.value] = ["96", "E6", "I6", "O6", "OY", "U6", "Y6", "a6", "a:6", "aI", "aU", "e:6", "i:6", "o:6", "u:6"]

phon_types[PhoneType.VOWELS.value] = phon_types[PhoneType.SINGLE_VOWELS.value] + phon_types[PhoneType.DIPHTONGS.value]
phon_types[PhoneType.CONSONANTS.value] = phon_types[PhoneType.SINGLE_CONSONANTS.value] + phon_types[PhoneType.AFFRICATES.value]


path="data_analysis/saved_data/"
sfx = ""
with open(path + sfx + "all_results.json", 'r', encoding="utf-8") as res_js:
	all_results = json.load(res_js)
with open(path + sfx + "label2deviation.json", 'r', encoding="utf-8") as l2d_js:
	label2deviation = json.load(l2d_js)
with open(path + sfx + "all_deviations.json", 'r', encoding="utf-8") as devs_js:
	all_deviations = json.load(devs_js)
with open(path + sfx + "overall_average.json", 'r', encoding="utf-8") as avg_js:
	overall_average = json.load(avg_js)

utils.print_DelInsSub(all_results, len(all_deviations))
utils.print_overallTransAccuracy(all_results)
utils.print_dataPointAmount(all_deviations)

print("Overall average is " + str(sum(overall_average)/len(overall_average)))

answ1 = input("Do you want to plot the histogram? Y/N ")
if answ1 == "Y":
	utils.plotHistogram(all_deviations)

answ2 = input("Do you want to plot the boxplot? Y/N ")
if answ2 == "Y":
	sorted_lab2dev = dict()
	for phon in phon_types[PhoneType.VOWELS.value] + phon_types[PhoneType.FRICATIVES.value] + phon_types[PhoneType.NASAL.value] + phon_types[PhoneType.PLOSIVES.value] + phon_types[PhoneType.AFFRICATES.value] + phon_types[PhoneType.LEFTOVER_CONS.value]:
		if phon in label2deviation.keys():
			sorted_lab2dev[phon] = label2deviation[phon]
	utils.drawBoxPlot(list(sorted_lab2dev.values()), list(sorted_lab2dev.keys()))

answ3 = input("Do you want to plot the ECDF? Y/N ")
if answ3 == "Y":
	x,y = utils.ecdf_function(all_deviations)
	utils.plotECDF(x,y)

ans = input("Do you want to plot the classes? Y/N")
if ans == "Y":
	new_phon = dict()
	for k, v in phon_types.items():
		if k != PhoneType.LEFTOVER_CONS.value:
			new_phon[k] = v
	class2devs = utils.prepare_phonemClasses(label2deviation, new_phon)
	utils.plotPhonemClasses(class2devs)
