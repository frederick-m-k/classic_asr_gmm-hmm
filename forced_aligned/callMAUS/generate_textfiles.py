import os, sys

text_path = sys.argv[1]
output_path = sys.argv[2]

with open(text_path, "r", encoding="utf-8") as input:
	for line in input:
		id = line.split(" ")[0]
		utt = line.split(" ")[1:]
		utt = [u.lower() for u in utt if u != "!sil"]
		utt = " ".join(utt)
		with open(output_path + "/" + id + ".txt", "w", encoding = "utf-8") as output:
			output.write(utt)
