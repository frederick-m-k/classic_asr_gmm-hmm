
import subprocess, sys, os
import id2phone, ctm2tg


error_message = "Usage:  python3 " + __file__ + ''' <path2ali_dir> <path2phones_txt> <path2corpus> <forcedAlignment? True/False>
	e.g. python3 ''' + __file__ + " data/models data/lang/phones.txt ../corpora/phattsessionz False"

def create_ctm_files(path_to_dir, delimiter = "-"):
	ctm_files = list()
	for filename in os.listdir(path_to_dir):
		if filename.startswith('ali') and delimiter in filename:
			_, extension  = filename.split(delimiter)
			if extension == 'equal':
				extension = '0'
			print(path_to_dir, filename, extension)
			subprocess.run(['ali-to-phones', '--ctm-output', path_to_dir + '/final.mdl', 'ark:'+path_to_dir+'/'+filename, path_to_dir+'/'+extension+'.ctm'])
			ctm_files.append(extension+'.ctm')
	return ctm_files

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

	if len(all_args) < 5:
		print(error_message)
		exit(1)
	kaldi = check_kaldi()

	path_to_ali_dir = all_args[1]
	phones_txt = all_args[2]
	utterance_id = all_args[3]
	forced_align_value = all_args[4]

	ali_dir =  os.path.isdir(path_to_ali_dir) #and "ali" in os.listdir(path_to_ali_dir)
	phones = os.path.isfile(phones_txt)
	utt_id = True

	forced_align = forced_align_value == "False" or forced_align_value == "True"

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
		if not forced_align:
			print("ERROR in " + forced_align_value + ". It should be either True or False\n")
		exit(1)


def run(argv):
	check_args(argv)

	path_to_ali_dir = argv[1]
	if path_to_ali_dir.endswith('/'):
		path_to_ali_dir.rstrip('/')

	phones_txt = argv[2]
	dir2forcAlignedTG = "forced_aligned"
	path2corpus = argv[3]
	if path2corpus.endswith('/'):
		path2corpus.rstrip('/')
	forcedAlign_TF = argv[4]
	for subdir in os.listdir(path2corpus):
		if os.path.isdir(path2corpus + '/' + subdir):
			for sub_file in os.listdir(path2corpus + '/' + subdir):
				if ".TextGrid" in sub_file:
					file_path = path2corpus + '/' + subdir + '/' + sub_file
					tgdict_list = dict()
					for ctm_file in create_ctm_files(path_to_ali_dir):
						id2phone.id2phone(phones_txt, path_to_ali_dir+'/'+ctm_file)
						ctm_file = ctm_file.split('.')[0]+'-updated.ctm'
						tgdict = ctm2tg.get_utterance(file_path, path_to_ali_dir+'/'+ctm_file)
						tiername,_ = ctm_file.split('.c')
						tgdict_list[tiername] = tgdict
					ctm2tg.create_textgrid(tgdict_list, dir2forcAlignedTG + '/' + sub_file, forcedAlign_TF)

if __name__ == "__main__":
	print("Did you run the wrong script?")
	print("Yes, you did!")
	print("You should run run.py")
