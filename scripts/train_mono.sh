
# input arguments
if [ $# != 2 ]; then
	echo "Usage: $0 <data_dir> <model_dir>"
	echo "  e.g.: $0 data/ exp/mono"
	echo "  e.g.: $0 phatts_cleaned_data exp/mono_cleaned/"
	exit 1
fi

data_dir=$1
data_dir=${data_dir%/} # strip of trailing / if present

model_dir=$2
dir=${model_dir%/}

scale_opts="--transition-scale=1.0 --acoustic-scale=0.1 --self-loop-scale=0.1"

cp $dir/ali-equal $dir/ali

totgauss=1000
i=1
numgauss=$(gmm-info --print-args=false $dir/0.mdl | awk '/gaussians/ {print $NF}')

while [ $i -le 30 ]; do
	if (( $i % 5 == 0 ))
	then
		gmm-boost-silence --boost=1.75 3 $dir/$i.mdl $dir/$i.mdl
		gmm-align-compiled $scale_opts --beam=10 --retry-beam=40 $dir/$i.mdl ark:$dir/fsts scp:$data_dir/train/feats-deltas.scp ark:$dir/ali
		cp $dir/ali $dir/ali-$i
	fi
	gmm-acc-stats-ali $dir/$i.mdl scp:$data_dir/train/feats-deltas.scp ark:$dir/ali $dir/$i.acc
	gmm-est --write-occs=$dir/$[i + 1].occs --mix-up=$numgauss $dir/$i.mdl $dir/$i.acc $dir/$[i + 1].mdl

	if [ $numgauss -lt $totgauss ];
	then
		numgauss=$[numgauss + 12]
	fi
	echo "Starting iteration $[i++]"
done
