
info_mess="This script ($0) prepares the viterbi training"
error_mess="
Usage:  $0 <data_dir> <model_dir>
	<data_dir>: the path to the data directory,
		e.g. data, 20phatts_data, ...
	<model_dir>: the path to the directory, in
		which the model shall be placed,
		e.g. exp/mono, exp/mono_testX, ...
"

echo "$info_mess" # always echo the info

##### input parameters
if [ $# != 2 ]; then
	echo "$error_mess"
	exit 1
fi

data_dir=${1%/} # remove a trailing slash if present
dir=${2%/}
######

## info message

feat_dim=39
mkdir -p $dir

echo Initialize acoustic model
gmm-init-mono --train-feats=scp:$data_dir/train/feats-deltas.scp $data_dir/lang/topo $feat_dim $dir/0.mdl $dir/tree

echo number of Gaussians
numgauss=$(gmm-info --print-args=false $dir/0.mdl | awk '/gaussians/ {print $NF}')
echo $numgauss

echo Compile training graphs
compile-train-graphs $dir/tree $dir/0.mdl $data_dir/lang/L.fst ark:$data_dir/train/text.int ark:$dir/fsts

echo Align training graphs
align-equal-compiled ark:$dir/fsts scp:$data_dir/train/feats-deltas.scp ark,t:$dir/ali-equal

echo Collect occupation statistics
gmm-acc-stats-ali --binary=true $dir/0.mdl scp:$data_dir/train/feats-deltas.scp ark:$dir/ali-equal $dir/0.acc

echo Estimate model parameters
gmm-est --min-gaussian-occupancy=3 --mix-up=$numgauss $dir/0.mdl $dir/0.acc $dir/1.mdl

echo Done with preparing the viterbi algorithm
