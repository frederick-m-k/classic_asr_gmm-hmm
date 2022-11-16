
import sys, os

####### input parameters
if len(sys.argv) != 3:
	print("Usage: " + __file__ + " <wer_dir> <k_best>")
	print("  e.g.: " + __file__ + " exp/mono_cleaned/decode_test/ 4")
	exit(1)

wer_dir = sys.argv[1]
if wer_dir.endswith('/'):
	wer_dir.rstrip('/')
k_best = sys.argv[2]

all_wers = dict()
for one_file in os.listdir(wer_dir):
	if os.path.isfile(wer_dir + '/' + one_file) and "wer" in one_file:
		with open(wer_dir + '/' + one_file, 'r', encoding="utf-8") as wer_file_fd:
			for line in wer_file_fd.readlines():
				if "WER" in line:
					current_wer = line.split('/')[1]
					all_wers[wer_dir+'/'+one_file] = current_wer

best_wers = sorted([(fi, w) for fi, w in all_wers.items() if w in sorted(list(all_wers.values())[-int(k_best):])], reverse=True)

for best_wer in best_wers:
	print("-------------------")
	with open(best_wer[0], 'r', encoding="utf-8") as best_wer_fd:
		print("lmwt of", best_wer[0].split("wer_")[1])
		for line in best_wer_fd.readlines():
			print(line.strip('\n'))
	print()
