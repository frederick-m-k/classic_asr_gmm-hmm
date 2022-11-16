
import os, sys
import shutil


print("This script runs best, when run from the groupI/ directory")
print("This script goes through all feats- .ark files and places the correct path in the corresponding .scp files")
####### input parameters
if len(sys.argv) != 2:
	print("Usage: " + __file__ + " <path2arkFeats>")
	print(" e.g.: " + __file__ + " data/feats/")
	print("        <path2arkFeats>: the path to the folder in which the ark-files with the features are located")
	exit(1)

path2feats = sys.argv[1].rstrip('/')
#######

if os.path.isdir(path2feats):
	for ark_file in os.listdir(path2feats):
		tmp = ark_file.replace(".ark", '')
		if tmp.startswith("mfcc-deltas"):
			sub_dir = tmp.replace("mfcc-deltas-", '')
			scp_name = "feats-deltas"
		elif tmp.startswith("cmvn"):
			scp_name, sub_dir = tmp.split('-')
		elif tmp.startswith("mfcc"):
			scp_name = "feats"
			sub_dir = tmp.split('-')[1]
		main_dir = path2feats.split('/')[0]
		scp_file = main_dir + '/' + sub_dir + '/' + scp_name + ".scp"
		scp_tmp = main_dir + '/' + sub_dir + '/' + scp_name + "-tmp.scp"
		with open(scp_file, 'r', encoding="utf-8") as scp_fd:
			with open(scp_tmp, 'w', encoding="utf-8") as tmp_fd:
				for line in scp_fd.readlines():
					utt_id, t_path = line.strip('\n').split(' ')
					act_path, line_id = t_path.split(':')
					tmp_fd.write(utt_id + ' ' + path2feats + '/' + ark_file + ':' + line_id + '\n')
		shutil.move(scp_tmp, scp_file)

print("Done with replacing the files")
