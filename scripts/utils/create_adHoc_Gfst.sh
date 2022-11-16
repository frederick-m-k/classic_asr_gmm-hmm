#!/usr/bin/env bash

# Copyright 2012 Johns Hopkins University (Author: Daniel Povey)
# Apache 2.0.
### Change by FK

usage_mess="
Usage: $0 <lang_dir> <lexicon_file>
	<lang_dir>: the /lang/ directory in,
		e.g. data/lang/, digits/lang, ...
	<lexicon_file>: path to the lexicon file,
		e.g. data/local/dict/lexicon.txt
"
if [ $# != 2 ]; then
	echo "$usage_mess"
	exit 1
fi

lang=${1%/}
file=$2
###################

penalty1=`perl -e '$prob = 1.0/22; print -log($prob);'` # negated log-prob,22 numbers
penalty0=`perl -e '$prob = 1.0; print -log($prob);'` #only one silence
  # which becomes the cost on the FST.
uniqued=$(awk -F "\t" 'NR>=8 {print $1}' $file | sort --unique)
( for y in `awk -F "\t" 'NR<=1 {print $1}' $file`;do
   echo 0 1 $y $y $penalty0
 done
 for x in $uniqued; do
   echo 1 1 $x $x $penalty1   # format is: from-state to-state input-symbol output-symbol cost
 done
 for z in `awk -F "\t" 'NR<=1 {print $1}' $file`;do
   echo 1 0 $z $z $penalty1
 done
 echo 0 $penalty0 # format is: state final-cost
) | fstcompile --isymbols=$lang/words.txt --osymbols=$lang/words.txt \
   --keep_isymbols=true --keep_osymbols=true |\
   fstarcsort --sort_type=ilabel > "${lang}_test/G.fst"

exit 0;
