####### input paramters
if [ $# != 2 ]; then
	echo "Usage: $0 <data/lang> </text-file>"
	echo "e.g.: $0 phatts_wout_slash_data/lang/words.txt phatts_wout_slash_data/train/text"
	exit 1
fi

lang_dir=$1
lang_dir=${lang_dir%/}
text_file=$2


oov_sym=$(cat $lang_dir/oov.int)
echo $oov_sym
kaldi/utils/sym2int.pl --map-oov $oov_sym -f 2- $lang_dir/words.txt < $text_file > $text_file.int

