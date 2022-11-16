
import os, sys

print("This script runs best, when run from the groupI/ directory")
print("This script checks, if given utterances, e.g. a test set, is in a provided set, e.g. a training set.")
####### input parameters
if len(sys.argv) != 3:
	exit()

path2checkedSet = sys.argv[1]
path2examine = sys.argv[2]
#######

allUtts2Check = set()
with open(path2examine, 'r', encoding="utf-8") as examined_fd:
	for line in examined_fd.readlines():
		allUtts2Check.add(line.split(' ')[0])
	allUtts2Check = sorted(list(allUtts2Check))

not_inside = list()
with open(path2checkedSet, 'r', encoding="utf-8") as checked_fd:
	for line in checked_fd.readlines():
		utt_id, *_ = line.split(' ')
		if not utt_id in allUtts2Check:
			not_inside.append(utt_id)

print("These " + str(len(not_inside)) +  " utterances are not inside the checked set " + str(path2examine) + ':')
print(not_inside)
