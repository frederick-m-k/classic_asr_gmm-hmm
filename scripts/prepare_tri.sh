#this script is based on task37 of the Graz tutorial
#used to build a phonetic decision tree

######## input parameters
if [ $# != 5 ]; then
	echo "Usage: $0 <mono_dir> <tri_dir> <data_dir> <test_train> <lang_dir>"
	echo "  e.g.: $0 exp/mono exp/tri phatts_wout_slash_data train lang_test"
	exit 1
fi

mono_dir=${1%/}
data_dir=${3%/}
dir=${2%/}
test_train=$4
lang_dir=${5%/}

########

scale_opts="--transition-scale=1.0 --acoustic-scale=0.1 --self-loop-scale=0.1"
gmm-align-compiled $scale_opts --beam=10 --retry-beam=40 $mono_dir/final.mdl ark:$mono_dir/fsts scp:$data_dir/train/feats-deltas.scp ark:$mono_dir/ali
echo "Done with aligned the mfcc features"
read -p "Press a key to continue" var

ciphones=$(cat $data_dir/$lang_dir/phones/context_indep.csl)
mkdir -p $dir
acc-tree-stats --ci-phones=$ciphones $mono_dir/final.mdl scp:$data_dir/$test_train/feats-deltas.scp ark:$mono_dir/ali $dir/treeacc
echo "Done with accumulating the tree statistics"
read -p "Press a key to continue" var

cluster-phones $dir/treeacc $data_dir/$lang_dir/phones/sets.int $dir/questions.int
compile-questions $data_dir/$lang_dir/topo $dir/questions.int $dir/questions.qst
echo "Done with compiling the questions"
read -p "Press a key to continue" var

numgauss=2000
totgauss=10000
build-tree --max-leaves=$numgauss $dir/treeacc $data_dir/$lang_dir/phones/roots.int $dir/questions.qst $data_dir/$lang_dir/topo $dir/tree
echo "Done with building the tree"
read -p "Press a key to continue" var

#../kaldi/utils/tree-plot.sh data/lang/phones.txt $dir/tree $dir/tree.png
#read -p "Press a key" war

gmm-init-model --write-occs=$dir/1.occs $dir/tree $dir/treeacc $data_dir/$lang_dir/topo $dir/1.mdl
echo "Initializing the model"
read -p "Press a key to continue" var

gmm-mixup --mix-up=$numgauss $dir/1.mdl $dir/1.occs $dir/1.mdl
echo "mixing up the gaussians"
read -p "Press a key to continue" var

convert-ali $mono_dir/final.mdl $dir/1.mdl $dir/tree ark:$mono_dir/ali ark:$dir/ali
echo "Converting the alignment"
read -p "Press a key to continue" var

compile-train-graphs $dir/tree $dir/1.mdl $data_dir/$lang_dir/L.fst ark:$data_dir/$test_train/text.int ark:$dir/fsts
echo "Compiling the train graphs"
read -p "Press a key to continue" var
