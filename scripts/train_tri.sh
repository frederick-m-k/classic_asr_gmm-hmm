######## input parameters
if [ $# != 3 ]; then
	echo "Usage: $0 <tri_dir> <data_dir> <test_train>"
	echo "  e.g.: $0 exp/tri phatts_wout_slash_data/ train"
	exit 1
fi

data_dir=${2%/}
test_train=$3
dir=${1%/}
########

scale_opts="--transition-scale=1.0 --acoustic-scale=0.1 --self-loop-scale=0.1"

totgauss=10000
numgauss=2000

i=1
while [ $i -le 20 ];do
        if (( $i % 5 == 0 ))
	then
		#gmm-boost-silence --boost=1.75 4 $dir/$i.mdl $dir/$i.mdl
		gmm-align-compiled $scale_opts --beam=10 --retry-beam=40 $dir/$i.mdl ark:$dir/fsts scp:$data_dir/$test_train/feats-deltas.scp ark:$dir/ali
		cp $dir/ali $dir/ali-$i
        fi
	#gmm-boost-silence --boost=1.75 4 $dir/$i.mdl $dir/$i.mdl
	gmm-acc-stats-ali $dir/$i.mdl scp:$data_dir/$test_train/feats-deltas.scp ark:$dir/ali $dir/$i.acc
	gmm-est --write-occs=$dir/$[i + 1].occs --mix-up=$numgauss $dir/$i.mdl $dir/$i.acc $dir/$[i + 1].mdl
	if [ $numgauss -lt $totgauss ];then
                numgauss=$[numgauss + 320]
	fi
        echo "Starting iteration $[i++]"
done
