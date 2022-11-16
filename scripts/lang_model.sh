info_mess="This script $0 either generates a trigram model of training data by using kenlm, or selects an existing language model for the specific ASR-task.
It will create a new folder lang_test/. In there, the newly generated language model will be stored.
"
#It is integrated in the scripts/lexicon_FK.sh

usage_mess="
Usage: $0 <data_main_dir>
	e.g. ../ASR1_phatts/, ../ASR3_ALC/
"
### input paramaters
if [ $# != 1 ]; then
	echo "$info_mess"
	echo "$usage_mess"
	exit 1
fi
data_dir=${1%/}

######

#generating or selecting a language model
mkdir $data_dir/lang_test/
cp -r $data_dir/lang/* $data_dir/lang_test/
echo "Which language model should be used for this ASR project?"
sleep 1
echo "If a lm based on your training data should be used, please type 'corpus'"
sleep 1
echo "If a specific language model from any other source should be used, please type 'other'"

#generating 3-gram model with kenlm
read lminput
if [ $lminput == "corpus" ]; then
	echo "creating a trigram model"
	cut -d ' ' -f 2- $data_dir/train/text > tmp
	/usr/local/kenlm/bin/lmplz -o 3 < tmp > $data_dir/train/text.arpa
	sleep 1
	arpa2fst --read-symbol-table=$data_dir/lang/words.txt --disambig-symbol=#0 $data_dir/train/text.arpa $data_dir/train/G.fst
	rm tmp
	mv $data_dir/train/G.fst $data_dir/lang_test/
	echo "The trigram model of your training data is stored in"
	echo "\t $data_dir/lang_test called G.fst"
fi

#selecting one from existing arpa-files, storing as G.fst in data_dir/lang_test
if [ $lminput == "other" ]; then
	echo "There are a few language models in ./lang_mod/"
	cd lang_mod
 	ls *.arpa
	cd ..
	echo "Which LM should be used? If none, type 'none'"
	read dirinput
	if [ $dirinput == "none" ];then
		echo "You can create a new LM or get one from the WWW"
		echo "Make sure the LM is stored in $data_dir/lang_test and named G.fst"
 		sleep 2
	else
		arpa2fst --read-symbol-table=$data_dir/lang_test/words.txt --disambig-symbol=#0 lang_mod/$dirinput $data_dir/lang_test/G.fst
		#cp lang_mod/$dirinput $data_dir/lang_test/
		#mv $data_dir/lang_test/$dirinput $data_dir/lang_test/G.fst
		echo "The chosen LM has been compiled, based on the present words.txt file and moved to $data_dir/lang_test"
		echo "It is named G.fst"
	fi
fi

exit 1
