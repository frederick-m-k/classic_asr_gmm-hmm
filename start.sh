
#########
# this script shall be used to start the process of ASR
# author: group I (FK)
#########


error_mess="This script does all the basic file preparations regarding the utterances from the corpus
This represents the tasks 0..3 in the Graz kaldi tutorial"
usage_mess="
Usage:	$0 <path2corp> <dataDir> <howManyUtts> <furtherSpecification>
	<path2corp>: provide the path to the corpus directory.
		The corpus should have a specific structure. In the main
		director of the corpus, e.g. \'phattsessionz/\',
		there should be sub folders, e.g. for speakers or rec session,
		in there, \'.wav\' and \'.par\' files should be.
		If there is a \'content_table.tab\' file in the corpus main dir,
		it well be used to get the transcriptions, otherwise the \'.par\'
		files will be used
	<dataDir>: specify the data-directory with the sub dir in which the files
		should be placed, e.g. data/test or 20phatts_data/train, ...
		if the directory is not created yet, it will get created
	<howManyUtts>: how many of all utterances provided in the corpus should be
		selected. They get selected randomly, if you want all utterances,
		please type 'all'
	<furtherSpecification>: digits, None
		digits will only include utterances consisting of digits from
		  \"null\" to \"zwanzig\"
		None will result in no further specification
"

######### input parameters
if [ $# != 5 ]; then
	echo "$error_mess"
	echo "$usage_mess"
	exit 1
fi

corp_path=${1%/}
dataDir=${2%/}
utts=$3
furtherSpec=$4
#########


## welcome text
echo "Welcome in the ASR project of group I"
echo "With this script, you have started the process of this ASR project"
echo "After running a script, all scripts will have a detailed description and information on the next script which should be run"
sleep 1


echo "The provided corpus will be loaded into the needed files, being 'wav.scp' and 'text'"
## execute task 0 and 1
mkdir -p $dataDir
python3 scripts/task0_1.py $corp_path $corp_path/content_table.tab $dataDir $utts $furtherSpec || exit $?
echo "Done with creating 'wav.scp' and 'text'"
echo "Now, normalizing the text file"
python3 scripts/replaceUmlauteInALC.py $dataDir/text $dataDir/text_tmp
mv $dataDir/text $dataDir/text_before_norm # save the old text file
python3 scripts/normalize_words_in_text_FK.py $dataDir/text_tmp $dataDir/text
rm $dataDir/text_tmp

sleep 1

echo "Now, the utterances with their corresponding speakers will be written into 'spk2utt' and 'utt2spk'"
## execute task 2
python3 scripts/task2.py $dataDir || exit $?

## execute task 3
kaldi/utils/spk2utt_to_utt2spk.pl < $dataDir/spk2utt > $dataDir/utt2spk || exit $?

echo "Done with writing 'spk2utt' and 'utt2spk'"

sleep 1

echo "You're done with the basic file preparation regarding the utterances"
echo "To proceed, the lexicon should get created"
echo "You can run the following script for this:"
echo "	scripts/lexicon_FK.sh"
