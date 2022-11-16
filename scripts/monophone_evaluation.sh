
info_mess="This script ($0) runs an evaluation for a monophone model"
usage_mess="
Usage: 	$0 <model_dir> <data_dir> <which_test_set> <lm_dir>
		<lmwt_range_start> <lmwt_range_end>
		<lmwt_range_step>
	<model_dir>: the path to the directory in which the
		model files are located, e.g. exp/mono, ...
	<data_dir>: the path to the directory, in which the
		data ,like the text file, is located,
		e.g. data, 20phatts_data, ...
	<which_test_set>: the name of the sub directory of
		<data_dir> where the test set is located,
		e.g. test, test2, train, ...
	<lm_dir>: the path to the directory, in which the
		language model is located,
		e.g. data/lang, lang_all/, ...
	<lmwt_range_xx>: the model is evaluated multiple
		times, each time changing the weight of the
		language model. <lmwt_range_start> defines
		the starting weigth, <lmwt_range_end> the end 
		of the weights, and <lmwt_range_step> how
                the lmwt shall vary in each step,
		e.g. 5 20 5
"

echo "$info_mess" # always echo the info message

###### input parameters
if [ $# != 7 ]; then
	echo "$usage_mess"
	exit 1
fi

model_dir=${1%/}
data_dir=${2%/}
which_test=${3%/}
lm_dir=${4%/}
lmwt_start=$5
lmwt_end=$6
lmwt_step=$7
debug_mode=0
######

./scripts/task31-32.sh $model_dir $data_dir $which_test $lm_dir

./scripts/task34.sh $model_dir $data_dir $which_test $lmwt_start $lmwt_end $lmwt_step

echo "On top of the monophone model you can build a triphone model"
echo "To do so, please run: scripts/triphone_viterbi.sh"
