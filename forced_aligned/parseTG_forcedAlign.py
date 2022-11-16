
import subprocess, sys, os
import id2phone, ctm2tg
from praatio import textgrid as tg

from datetime import datetime

error_message = """
Usage: python3 """ + __file__ + ''' <path2aliFile> <path2phones_txt> <path2corpus>
 e.g.: python3 ''' + __file__ + """ data/models/ali_forcedAlign_1 data/lang/phones.txt ../corpora/phattsessionz
	<path2aliFile>: the exact path to the alignments file
	<path2phones_txt>: the exact path to the phones.txt file
	<path2corpus>: the path to the dir in which existing TextGrid files are
"""

def create_ctm_file(path2aliFile, path2FinalMdl, dir2Save=""):
	tmp = path2FinalMdl.split('/')
	ctm_file = dir2Save + tmp[len(tmp)-1] + ".ctm"
	subprocess.run(['ali-to-phones', '--ctm-output', path2FinalMdl + "/final.mdl", 'ark:'+path2aliFile, ctm_file])
	return ctm_file
	

def check_kaldi():
	''' Check if kaldi commands are available '''
	command = ["ali-to-phones"]
	try:
		result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except FileNotFoundError:
		return False
	return True

def check_args(all_args):
	''' Check all arguments for correctness
	Check if path_to_ali-dir is a dir and contains a ali file
	Check if phones_txt is a file

	Check if textgrid_path is a path

	Return true or false for each argument in the same order
	 '''

	if len(all_args) != 4:
		print(error_message)
		exit(1)
	kaldi = check_kaldi()

	path_to_ali_dir = all_args[1]
	phones_txt = all_args[2]
	utterance_id = all_args[3]

	ali_dir =  os.path.isfile(path_to_ali_dir) #and "ali" in os.listdir(path_to_ali_dir)
	phones = os.path.isfile(phones_txt)
	utt_id = True

	if not kaldi or not ali_dir or not phones or not utt_id:
		print(error_message)
		if not kaldi:
			print("There are no kaldi commands available in your current path. You should run a source kaldi/path.sh\n")
		if not ali_dir:
			print("ERROR in your parameter " + path_to_ali_dir + ". It should be the path to the dir in which the ali files are\n")
		if not phones:
			print("ERROR in " + phones_txt + ". It should be the path to your phones.txt file\n")
		if not utt_id:
			print("ERROR in " + utterance_id + ". It should be a valid utterance ID\n")
		exit(1)


def run(argv):
	start_time = datetime.now()

	check_args(argv)

	path_to_ali = argv[1]
	path_to_ali = path_to_ali.rstrip('/')

	phones_txt = argv[2]
	dir2forcAlignedTG = "TextGrids_realMAUS"
	print("The merged TextGrids are going to get placed in the " + dir2ForcAligned + " directory")
	path2corpus = argv[3]
	path2corpus = path2corpus.rstrip('/')
	
# first, parse the ctm file
	ctm_file = create_ctm_file(path_to_ali, '/'.join(path_to_ali.split('/')[:-1]))
	upd_ctm_file = id2phone.id2phone(phones_txt, ctm_file)
	all_utts = ctm2tg.get_utterances(upd_ctm_file)
	
	for subdir in os.listdir(path2corpus):
		if os.path.isdir(path2corpus + '/' + subdir):
			for sub_file in os.listdir(path2corpus + '/' + subdir):
				if ".TextGrid" in sub_file:
					file_path = path2corpus + '/' + subdir + '/' + sub_file
					utt_id = sub_file.split(".TextGrid")[0]
					if utt_id in all_utts.keys():
						subprocess.run(["cp", file_path, dir2forcAlignedTG + '/' + sub_file])
						old_tg = tg.openTextgrid(dir2forcAlignedTG + '/' + sub_file, False)
						new_tg = tg.Textgrid()
						for tier_name in old_tg.tierDict.keys():
							new_tg.addTier(tg.IntervalTier(tier_name, old_tg.tierDict[tier_name].entryList))
						new_tg.addTier(tg.IntervalTier("g1Mdl_forcAli", all_utts[utt_id]))
						new_tg.save(dir2forcAlignedTG + '/' + sub_file, format="short_textgrid", includeBlankSpaces=False)
		elif subdir.endswith(".TextGrid"):
			file_path = path2corpus + '/' + subdir
			utt_id = subdir.split(".TextGrid")[0]
			if utt_id in all_utts.keys():
				subprocess.run(["cp", file_path, dir2forcAlignedTG + '/' + subdir])
				old_tg = tg.openTextgrid(dir2forcAlignedTG + '/' + subdir, False)
				new_tg = tg.Textgrid()
				for tier_name in old_tg.tierDict.keys():
					new_tg.addTier(tg.IntervalTier(tier_name, old_tg.tierDict[tier_name].entryList))
				new_tg.addTier(tg.IntervalTier("g1Mdl_forcAli", all_utts[utt_id]))
				new_tg.save(dir2forcAlignedTG + '/' + subdir, format="short_textgrid", includeBlankSpaces=False)

	end_time = datetime.now()
	print("The program started at", start_time.strftime("%H:%M:%S"))
	print("  and ended at", end_time.strftime("%H:%M:%S"))


if __name__ == "__main__":
	print("This program runs best, when run from the forced_aligned/ directory")
	run(sys.argv)
