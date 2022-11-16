
import os, sys
import time

inp_file = sys.argv[1]
out_file = sys.argv[2]

new_lines = []
with open(inp_file, 'r', encoding="utf-8") as inpF_fd:
	for line in inpF_fd.readlines():
		words = line.strip('\n').split(' ')[1:]
		new_words = []
		for word in words:
			if not word == "!SIL" and not len(word) == 0:
				new_words.append(word)
		if len(new_words) > 0:
			new_lines.append(' '.join(new_words) + '\n')

with open(out_file, 'w', encoding="utf-8") as out_fd:
	for line in sorted(list(set(new_lines))):
		line = line.rstrip(' ').lstrip(' ')
		last_char = ''
		new_line = ""
		for char in line:
			if char == ' ' and last_char == ' ':
				continue
			new_line += char
			last_char = char
		out_fd.write(line)
