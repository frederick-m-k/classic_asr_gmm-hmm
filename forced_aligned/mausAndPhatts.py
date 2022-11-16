
import os, sys

from praatio import textgrid as tg

phatts_path = "../../corpora/phattsessionz"
maus_path = "callMAUS/phatts_FK4ForcAliAG/ohne_align"
out_path = "mausPhattsTGs"

all_phatts = dict()
for sub_dir in os.listdir(phatts_path):
	if os.path.isdir(phatts_path + '/' + sub_dir):
		for sub_file in os.listdir(phatts_path + '/' + sub_dir):
			if sub_file.endswith(".TextGrid"):
				file_path = phatts_path + '/' + sub_dir + '/' + sub_file
				textG = tg.openTextgrid(file_path, False)
				all_phatts[sub_file] = textG.tierDict["MAU"].entryList

for sub_dir in os.listdir(maus_path):
	if os.path.isfile(maus_path + '/' + sub_dir) and sub_dir.endswith(".TextGrid"):
		if sub_dir in all_phatts.keys():
			maus_tg = tg.openTextgrid(maus_path + '/' + sub_dir, False)
			new_tg = tg.Textgrid()
			new_tg.addTier(tg.IntervalTier("MAUS-MAU", maus_tg.tierDict["MAU"].entryList))
			new_tg.addTier(tg.IntervalTier("phatts-MAU", all_phatts[sub_dir]))
			new_tg.save(out_path + '/' + sub_dir, format="short_textgrid", includeBlankSpaces=False)
