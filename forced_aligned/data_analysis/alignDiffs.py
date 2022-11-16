
import sys, time, os
import utils
import json

from praatio import textgrid
from wagnerfischer import WagnerFischer
from enum import Enum
from scipy.stats import skew

print("This script runs only, when executed from the forced_aligned/ directory")

dir_name = sys.argv[1].rstrip('/')

wf = WagnerFischer()

ref_tier = "MAU"
check_tier = "g1Mdl_forcAli"

rounding_amount = 3

class PhoneType(Enum):
	VOWELS = 1
	CONSONANTS = 2
	FRICATIVES = 3
	PLOSIVES = 4
	AFFRICATES = 5
	GLOTTAL_STOP = 6
	DIPHTONGS = 7
	TEST = 8

phon_types = dict()

phon_types['PhoneType.VOWELS'] = ['e', 'eː', 'ɐ', 'u', 'uː', 'a', 'a:', 'i', 'i:', 'o', 'o:', 'ɛ', 'ɛ:', 'ɪ', 'ə']
phon_types['PhoneType.CONSONANTS'] = ['d', 't', 's', 'S', 'z', 'Z', 'v', 'f', 'l', 'r', 'n', 'm', 'ç', 'x', 'k']
phon_types['PhoneType.AFFRICATES'] = ['dz', 'ts', 'tS', 'dZ', 'pf', 'ks']
phon_types['PhoneType.GLOTTAL_STOP'] = 'ʔ'
phon_types['PhoneType.DIPHTONGS'] = ['aɪ', 'oɪ', 'uɪ', 'au']

result_list = []
overall_average = []
all_deviations = []
#List with all label differencies
label_occurencies_dict = dict()
label2deviation = dict()

for file in os.listdir(dir_name):
	if file.endswith('_0-normed.TextGrid'):
		tierDict = dict()
		#opens files
		tg = textgrid.openTextgrid(dir_name + '/' + file, False)

		tierDict[ref_tier] = tg.tierDict[ref_tier].entryList
		tierDict[check_tier] = tg.tierDict[check_tier].entryList

		#Contain intervals
		ref_tier_list = tierDict[ref_tier]
		second_tier_list = tierDict[check_tier]

		#Lists of reference and another string containing labels only
		ref_list = []
		second_list = []

		for interval in ref_tier_list:
			_, _, l = interval
			ref_list.append(l)

		for interval in second_tier_list:
			_, _, l = interval
			second_list.append(l)

		"""
		Mind that it should be a list of labels
		"""
		#Returns a string list containing symbols like ^v*=
		occs_list = wf.calculateWagnerFischer(ref_list, second_list, file.split(".TextGr")[0])

		#Deletions,substitutions, insertions are summed up
		wf.sumOccurencies(occs_list)

		#Save the number of dels, subs, ins per string
		dels = wf.getDeletions()
		ins = wf.getInsertions()
		subs = wf.getSubstitutions()

		#Computes accuracy value of two strings and puts it into the list
		result = utils.measureTransAccuracy(len(ref_tier_list), subs, dels, ins)
		result_list.append((len(ref_tier_list), subs, dels, ins))

		#List containing label and differences between start and end boundaries
		diff_list = []
		if result == 1:
			for n_ref, ref_int in enumerate(ref_tier_list):
				s_ref, e_ref, l_ref = ref_int  # Unpack start, end time and label of the segment
				for n_second, second_int in enumerate(second_tier_list):
					s, e, l = second_int  # Unpack start, end time and label of the segment
					if n_ref == n_second:
						diff_start = round(s_ref - s, rounding_amount)
						diff_end = round(e_ref - e, rounding_amount)
						if abs(diff_start) < 10 and abs(diff_end) < 10:
							diff_list.append((l_ref, diff_start, diff_end))
							all_deviations.append((l_ref, diff_start, diff_end))
						break
			overall_average.append(utils.getAverage(diff_list))
			for (l, s, e) in diff_list:
				if l not in label2deviation.keys():
					label2deviation[l] = []
				label2deviation[l].append(s)
				label2deviation[l].append(e)


		else:
			#Handle cases with unequal strings length or unequal labels
			del_idx = 0
			ins_idx = 0
			for n, sign in enumerate(occs_list):
				if sign == "=":
					#Check if index in the range
					if ((n + del_idx) <= len(ref_tier_list)-1) and (n + ins_idx) <= (len(second_tier_list)-1):
						#Label of ref list
						l = ref_tier_list[n + del_idx][2]
						#Label of second list
						l2 = second_tier_list[n + ins_idx][2]

						if sign == '=' and l == l2:
							#Unpack start & end of ref
							s = ref_tier_list[n + del_idx][0]
							e = ref_tier_list[n + del_idx][1]
							#Unpack start & end of second
							s2 = second_tier_list[n + ins_idx][0]
							e2 = second_tier_list[n + ins_idx][1]

							diff_start = round(s - s2, rounding_amount)
							diff_end = round(e - e2, rounding_amount)
							if abs(diff_start) < 10 and abs(diff_end) < 10:
								diff_list.append((l, diff_start, diff_end))
								all_deviations.append((l, diff_start, diff_end))

				if sign == "v":
					#diff_list.append((ref_tier_list[n][2], ref_tier_list[n][0], ref_tier_list[n][1]))
					if del_idx <= dels:
						del_idx += 1
				if sign == "^":
					#diff_list.append((second_tier_list[n][2], -second_tier_list[n][0], -second_tier_list[n][1]))
					if ins_idx <= ins:
						ins_idx += 1

			overall_average.append(utils.getAverage(diff_list))

			#List with all label occurencies
			for (l, s, e) in diff_list:
				if l.strip(">") not in label2deviation.keys():
					label2deviation[l] = []
				label2deviation[l].append(s)
				label2deviation[l].append(e)
				

###### the created results are
# - result_list <- a [(ref_len, subs, dels, ins)] list with all things to calculate the accuracies
# - all_deviations <- deviations of all utterances of all labels
# - label2deviation <- dictionary sorted by labels with their corresponding deviations
# - overall_average <- a list of all averages calculated per utterance

path = "data_analysis/saved_data/"
sfx = ""
with open(path + sfx + "all_results.json", 'w', encoding="utf-8") as res_js:
	json.dump(result_list, res_js)
with open(path + sfx + "label2deviation.json", 'w', encoding="utf-8") as l2d_js:
	json.dump(label2deviation, l2d_js)
with open(path + sfx + "all_deviations.json", 'w', encoding="utf-8") as devs_js:
	json.dump(all_deviations, devs_js)
with open(path + sfx + "overall_average.json", 'w', encoding="utf-8") as avg_js:
	json.dump(overall_average, avg_js)

# the analysis is seperated in file analyze.py
