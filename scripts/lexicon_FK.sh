
error_mess="This script creates a lexicon based on the tasks 4...13 of the Graz kaldi tutorial"

usage_mess="
Usage:  $0 <data_main_dir> <test_or_train>
	<data_main_dir>: provide the path to the data main directory, e.g. data/, 20phatts_data, ...
	<test_or_train>: name of the subfolder of the <data_main_dir>, e.g. test, train, test2, ...
"
####### input parameters
if [ $# != 2 ]; then
	echo "$error_mess"
	echo "$usage_mess"
	exit 1
fi
data_dir=${1%/}
test_train=${2%/}
#######

## welcome text
echo "This script writes everything related to the lexicon in the $data_dir/local/dict directory"
echo "  A change to this is not implemented in this script"
echo "Furthermore, this script is used to build a grammar (LM) for your ASR"

#### FK: ich hab das ins start.sh Skript gepackt, damit die Normalisierung auch für ein test set gemacht wird
# first: normalize the words in the text file
#echo "normalizing words in the text file"
#python3 scripts/normalize_words_in_text_FK.py $data_dir/$test_train/text $data_dir/$test_train/text_tmp
#mv $data_dir/$test_train/text $data_dir/$test_train/text_before_norm # save the old text file
#python3 scripts/replaceUmlauteInALC.py $data_dir/$test_train/text_tmp $data_dir/$test_train/text_tmp
#mv $data_dir/$test_train/text_tmp $data_dir/$test_train/text # and work only with the new one
echo "Preparing the g2p"
cut -d ' ' -f 2- $data_dir/$test_train/text > $data_dir/$test_train/text_cut
sort --unique $data_dir/$test_train/text_cut > $data_dir/$test_train/text_sorted
# output of this part is text

# second: run g2p.pl
echo "running g2p.pl"
g2p.pl -task apply -lng deu -i $data_dir/$test_train/text_sorted -iform txt -o $data_dir/grass-read.dict -oform tab
sed 's/;/\t/g' $data_dir/grass-read.dict > $data_dir/updated_grass-read.dict
mv $data_dir/updated_grass-read.dict $data_dir/grass-read.dict

# third: normalize the phonemes
echo "normalizing the phonemes"
python3 scripts/normalize_phonemes_in_lex.py $data_dir/grass-read.dict $data_dir/updated_grass-read.dict
sort --unique $data_dir/updated_grass-read.dict > $data_dir/sorted_grass-read.dict

mkdir -p $data_dir/local/dict

# fourth & task 6: create nonsilence_phones.txt
echo "creating nonsilence_phones.txt"
python3 scripts/task6.py $data_dir/sorted_grass-read.dict $data_dir/local/dict/nonsilence_phones.txt

# task 7: create silence_phones.txt
echo "creating silence_phones.txt"
echo SIL > $data_dir/local/dict/silence_phones.txt
echo UNK >> $data_dir/local/dict/silence_phones.txt

# task 9: create lexicon.txt
echo "creating lexicon.txt"
cp $data_dir/sorted_grass-read.dict $data_dir/local/dict/lexicon.txt
echo -e "!SIL\tSIL" >> $data_dir/local/dict/lexicon.txt
echo -e "<UNK>\tUNK" >> $data_dir/local/dict/lexicon.txt
sort --unique $data_dir/local/dict/lexicon.txt > tmp
mv tmp $data_dir/local/dict/lexicon.txt

# task 10: create optional_silence.txt
echo "creating optional_silence.txt"
echo SIL > $data_dir/local/dict/optional_silence.txt

# task 11: create empty extra_questions.txt
echo "creating empty extra_questions.txt"
touch $data_dir/local/extra_questions.txt

# task 12: build kaldi lexicon from it
echo "building kaldi lexicon in task 12"
sleep 2
cd kaldi
utils/prepare_lang.sh --position-dependent-phones false ../$data_dir/local/dict "<UNK>" ../$data_dir/local/lang_tmp ../$data_dir/lang
cd ..

################################################################################
##### Calling a script to generate a trigram LM or select a existing LM ########
##### If you want to build a bigram LM, you have to adapt the script below #####
################################################################################

./scripts/lang_model.sh $data_dir

# task 13: run oov
echo "running oov check over text file"
oov_sym=$(cat $data_dir/lang/oov.int)
kaldi/utils/sym2int.pl --map-oov $oov_sym -f 2- $data_dir/lang/words.txt < $data_dir/$test_train/text > $data_dir/$test_train/text.int

echo "You're done with creating the lexicon files"
echo "To proceed, the MFCCs should get calculated"
echo "For this, you can run the following script:"
echo 	"scripts/mfccs_sepDir.sh"
