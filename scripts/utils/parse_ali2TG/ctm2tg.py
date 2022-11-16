

'''
ConvertKaldi'sCTMalignment	outputtoPraat'sTextGrid	format.
'''

import csv,sys,os
from praatio import textgrid
import praatio as tg
import time

def get_utterances(ctmfile):
	all_utts = dict()
	with open(ctmfile, 'r') as rf:
		for line in rf:
			utterance_id, _, begin, dur, phone = line.strip('\n').split(' ')
			if str(utterance_id) not in all_utts.keys():
				all_utts[str(utterance_id)] = []
			all_utts[str(utterance_id)].append((str(begin), str(float(begin) + float(dur)), str(phone)))
	return all_utts

def create_textgrid(tgdict, textgrid_path, forced_align):
	tg = textgrid.Textgrid()
	tmp_dict = dict()
	for tiername in tgdict.keys():
		tmp = tgdict[tiername]
		tiername = tiername.split('-')[0]
		if len(tiername) == 1:
			tiername = '0'+tiername
		tmp_dict[tiername] = tmp
	if forced_align:
		for tiername, values in tmp_dict.items():
			if len(values) != 0:
				tg.addTier(textgrid.IntervalTier(tiername, values))
	else:
		for tiername in sorted(tmp_dict.keys()):
			tg.addTier(textgrid.IntervalTier(tiername, tmp_dict[tiername]))
	tg.save(textgrid_path)

def main():
	if(len(sys.argv)<4):
		print("Usage: python3 ctm2tg.py <ctmfile> <utteranceid> <textGrid-path>")
		exit(1)
	ctmfile=sys.argv[1]
	utterance_id=sys.argv[2]
	textgrid_path = sys.argv[3]
	tgdict = get_utterance(utterance_id, ctmfile)
	create_textgrid(tgdict, textgrid_path)
	#ctm2tg(wavdir,outdir)

if __name__ =='__main__':
	#main()
	print("Did you run the wrong script?")
	print("Yes, you did")
	print("You should run run.py")
