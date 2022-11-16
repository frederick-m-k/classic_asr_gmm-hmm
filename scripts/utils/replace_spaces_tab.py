
import os, sys
import shutil

error_mess = "This script replaces all \"    \" with a \'\\t\' symbol. The amount of spaces to replace can be chosen."
usage_mess = """
Usage: python3 """ + __file__ + """ <file2update> <amountOfSpaces>
	<file2update>: the file to change all spaces * <amountOfSpaces> with a tab symbol
"""
####### input parameters
if len(sys.argv) != 3:
	print(error_mess)
	print(usage_mess)
	exit(1)

file2change = sys.argv[1]
amount_spaces = int(sys.argv[2])

#######

with open(file2change, 'r', encoding="utf-8") as change_fd:
	lines = change_fd.readlines()

prefix, suffix = file2change.split('.')
tmp_file = prefix + "-tmp." + suffix
with open(tmp_file, 'w', encoding="utf-8") as write_fd:
	for line in lines:
		new_line = line.replace(" " * amount_spaces, '\t')
		write_fd.write(new_line)

shutil.move(tmp_file, file2change)
