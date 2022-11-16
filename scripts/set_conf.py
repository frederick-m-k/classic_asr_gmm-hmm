import sys, os
#This script checks the sample-frequency settings in conf/mfcc.conf

##### input parameters
if len(sys.argv) != 2:
	print("Usage: "+ __file__ +" <file2MfccConf>")
	print("e.g. " + __file__ + " conf/mfcc.conf")

mfcc_conf = sys.argv[1]
phatts_freq = "22050"
alc_freq = "44100"

with open (mfcc_conf, "r", encoding = "utf-8") as conf:
	for line in conf.readlines():
		i = line.split("=")[1]
		sample_freq = i.strip("false").split(" ")[0]
		print("sample-frequency is set to:", sample_freq)

		if sample_freq == alc_freq:
			print("If the acoustic data is ALC-corpus")
			print("sample-frequency in conf/mfcc.conf is correct")

		if sample_freq == phatts_freq:
			print("If the acoustic data is phattsessionz corpus")
			print("sample-frequency in conf/mfcc.conf is correct")
