#this script performs forced alignment

echo "This script runs best, when run from the main directory groupI/"

if [ $# != 3 ]; then
	echo ""
	echo "Usage: $0 <path2data> <path2lang> <path2model>"
	echo " e.g.: $0 data/train data/lang exp/mono/"
	echo "      <path2data>: the path in which both the text file as well as the feats-deltas.scp file reside, e.g. data/train"
	echo "      <path2lang>: the path in which the compiled lexicon from task 12 is. L.fst, words.txt and the phones/ dir should be in there. E.g. data/lang/"
	echo "      <path2model>: the path in which the final.mdl is. The generated ali file will be in there"
	exit 1
fi

scale_opts="--transition-scale=1.0 --acoustic-scale=0.1 --self-loop-scale=0.1"

#args
data_dir=${1%/}
lang_dir=${2%/}
model_dir=${3%/}
feats=$data_dir/feats-deltas.scp

output_ali=$model_dir/ali_forcAlign-1

echo "Currently running for $data_dir"

echo First, creating a text.int file
oov=`cat $lang_dir/oov.int`
kaldi/utils/sym2int.pl --map-oov $oov -f 2- $lang_dir/words.txt < $data_dir/text > $data_dir/text.int
echo Done with text.int

read -p "Press a key to continue" var
sleep 1

echo Compiling the training graphs
compile-train-graphs --read-disambig-syms=$lang_dir/phones/disambig.int $model_dir/tree $model_dir/final.mdl $lang_dir/L.fst ark:$data_dir/text.int ark:$data_dir/trained_graphes.fst
echo Done with the training graphs

read -p "Press a key to continue" var
sleep 1

echo Aligning the data/$test_train/text with the corresponding features
gmm-align-compiled $scale_opts --beam=10 --retry-beam=40 $model_dir/final.mdl ark:$data_dir/trained_graphes.fst scp:$feats "ark,t:|gzip -c >$output_ali.gz"
echo Done with aligning

echo Lastly, unzipping the created file $output_ali.gz
gzip -d $output_ali.gz
echo Done with the whole script

echo Now, you can run a script to convert this alignment file to a TextGrid file, e.g. by running groupI/parseAli2TG/run.py
echo Just run the script once, it will display an example on how to run it
