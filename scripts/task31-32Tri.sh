###### input parameters
if [ $# != 4 ]; then
        echo "Usage: $0 <model_dir_triphone> <data_dir> <test_or_train> <lm>"
        echo "  e.g.: $0 exp/tri/ data test data/lang"
        echo "  e.g.: $0 exp/tri phatts_cleaned_data/ train data/lang_bigram"
        exit 1
fi

model_dir=${1%/}
data_dir=${2%/}
test_train=$3
lm=${4%/}
debug_mode=0
#######

# task 31
ln -s $(pwd)/$model_dir/21.mdl $model_dir/final.mdl
kaldi/utils/mkgraph.sh $lm $model_dir $model_dir/graph_$test_train

if [ $debug_mode == 1 ]; then
        read -p "Press a key to continue" var
fi

# task 32
mkdir -p $model_dir/decode_$test_train/scoring
gmm-latgen-faster-parallel --num-threads=2 --beam=32 --allow-partial=true --word-symbol-table=$model_dir/graph_$test_train/words.txt $model_dir/final.mdl $model_dir/graph_$test_train/HCLG.fst scp:$data_dir/$test_train/feats-deltas.scp ark:$model_dir/decode_$test_train/lat
