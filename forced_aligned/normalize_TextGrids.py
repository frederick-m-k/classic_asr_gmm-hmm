
import os, sys

error_mess = "This script runs over all TextGrids and replaces symbols with other symbols, e.g. all pause symbols with SIL"
usage_mess = """
Usage: python3 """ + __file__ + """ <directory2TextGrids>
	<directory2TextGrids>: define the directory with the TextGrids to normalize
"""

###### input parameters
if len(sys.argv) != 2:
	print(error_mess)
	print(usage_mess)
	exit(1)

tg_dir = sys.argv[1].rstrip('/')
#######

replacements = {
	"<p:>":"SIL",
	"<nib>":"SIL",
	"<usb>":"SIL"
}

if os.path.isdir(tg_dir):
	for tg_file in os.listdir(tg_dir):
		if tg_file.endswith("_0.TextGrid"):
			with open(tg_dir + '/' + tg_file, 'r', encoding="utf-8") as oldTG_fd:
				norm_tg_file = tg_file.split(".TextGrid")[0] + "-normed.TextGrid"
				with open(tg_dir + '/' + norm_tg_file, 'w', encoding="utf-8") as normTG_fd:
					for line in oldTG_fd.readlines():
						for key, repl in replacements.items():
							if key in line:
								line = line.replace(key, repl)
						normTG_fd.write(line)
