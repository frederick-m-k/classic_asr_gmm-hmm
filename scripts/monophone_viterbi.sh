
info_mess="This script runs everything necessary for preparing the viterbi
   this corresponds to the tasks 22...28 of the Graz kaldi tutorial
Furthermore, it starts the viterbi training
   this represents task 29 of the Graz kaldi tutorial
It is assumed that the train/ sub directory in the given data_main_dir holds
   the training material
"
usage_mess="
Usage:  $0 <data_main_dir> <mono_model_dir>
	<data_main_dir>: the path to the data directory,
		e.g. data/, 20phatts_data, ...
	<mono_model_dir>: the path to the directory, in
		which the models shall be placed,
		e.g. exp/mono/, exp/mono_testX
"

echo "$info_mess" # always echo this message

###### input parameters
if [ $# != 2 ]; then
	echo "$usage_mess"
	exit 1
fi

data_main_dir=${1%/}
mono_model_dir=${2%/}
######

# all echos are written in the two following scripts
# therefore, no echos are needed here

./scripts/prepare_mono.sh $data_main_dir $mono_model_dir

./scripts/train_mono.sh $data_main_dir $mono_model_dir

echo "You are done with viterbi training of your monophone model"
echo "Data is written to $mono_model_dir"
echo "The next step is generating the lattice graph"
echo "Furthermore your monophone model can be evaluated by measuring the WER"
echo "If you want to build a test set to evaluate the monophone model on, you can run the start.sh script yet again with different parameters."
echo "To evaluate the model, please run: "
echo "       scripts/monophone_evaluation.sh"
