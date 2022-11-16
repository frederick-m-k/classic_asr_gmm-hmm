info_mess="Attention: The training of a triphone model requires a trained monophone model
This script runs everything necessary for preparing the viterbi of a triphone model
   this corresponds to the steps of task 37 in the Graz kaldi tutorial
A phonetic decision tree is generated. You can plot it by using the script plotSubtree.sh
Furthermore, this script starts the viterbi training for a triphone model
"

usage_mess="
Usage: $0 <mono_dir> <tri_dir> <data_dir> <test_train>
    <mono_dir> the path to the monophone models,
	  e.g. exp/mono, exp/mono_ASR1_phatts, ...
    <tri_dir> the path to the directory, in
	  which the triphone models shall be placed,
	  e.g exp/tri, exp/tri_ASR1_phatts
    <data_dir> the path to the data directory,
	  e.g data/ ASR1_phatts/
    <test_train> the name of the subdirectory of
	  <data_dir> which should be used for viterbi-training,
	  e.g. train/ test/ test_alc/
    <lm_dir> the name of the subdirectory in <data_dir> where
	  the language model is located,
	  e.g lang/ lang_test/
"

echo "$info_mess" # always echo this message

###### input parameters
if [ $# != 5 ]; then
	echo "$usage_mess"
	exit 1
fi

mono_dir=${1%/}
tri_dir=${2%/}
data_dir=${3%/}
test_train=$4
lang_dir=${5%/}
######

#all echos are written in the following scripts
#therefore, no echos are needed here

./scripts/prepare_tri.sh $mono_dir $tri_dir $data_dir $test_train $lang_dir

./scripts/train_tri.sh $tri_dir $data_dir $test_train

echo "You are done with viterbi training of your triphone model"
echo "Data is written to $tri_dir"
echo "The next step is generating the lattice graph"
echo "Furthermore, your triphone model will be evaluated by measuring the WER"
echo "  To tackle these tasks, please run: "
echo "       scripts/triphone_evaluation.sh"
