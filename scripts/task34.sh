info_mess="This script computes the WER for your model and data
   It will show you the best results related to the language model weight
"

echo "$info_mess"
####### input parameters
if [ $# != 6 ]; then
	echo "Usage: $0 <model_dir> <data_dir> <test_or_train> <lmwt_start_value> <lmwt_end_value> <lmwt_steps>"
	echo "  e.g.: $0 exp/mono/ data/ train 1 100 2"
	echo "  e.g.: $0 exp/mono_cleaned phatts_cleaned_data test 5 20 5"
	exit 1
fi

model_dir=$1
dir=${model_dir%/}

data_dir=${2%/}
test_train=$3
lmwt=$4
lmwt_end=$5
lmwt_step=$6
#######

while [ $lmwt -le $lmwt_end ]; do
	lattice-scale --inv-acoustic-scale=$lmwt ark:$dir/decode_$test_train/lat ark:- | lattice-best-path --word-symbol-table=$dir/graph_$test_train/words.txt ark:- ark,t:$dir/decode_$test_train/scoring/$lmwt.tra
	kaldi/utils/int2sym.pl -f 2- $dir/graph_$test_train/words.txt < $dir/decode_$test_train/scoring/$lmwt.tra > $dir/decode_$test_train/scoring/$lmwt.txt
	python3 scripts/cut_SIL.py $dir/decode_$test_train/scoring/$lmwt.txt $data_dir/local/dict/silence_phones.txt $data_dir/local/dict/lexicon.txt $dir/decode_$test_train/scoring/$lmwt-updated.txt
	compute-wer --text --mode=present ark:$data_dir/$test_train/text ark,p:$dir/decode_$test_train/scoring/$lmwt-updated.txt > $dir/decode_$test_train/wer_$lmwt
	lmwt=$[lmwt + lmwt_step]
done

k_best=3
echo "Now showing the $k_best WERs"
python3 scripts/show_k_best_wer.py $dir/decode_$test_train $k_best
