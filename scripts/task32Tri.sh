# Execute Task32

if [ $# != 3 ]; then
        echo " "
        echo "Usage: <triphone_model> <data_dir> <test_or_train>"
        echo "e.g.: exp/tri/ data/ test"
        echo " "
        exit 1
fi      


tri_dir=$1
data_dir=$2
test_train=$3

##rm -r exp/mono/decode_dev
mkdir -p $tri_dir/decode_dev/scoring
gmm-latgen-faster-parallel --num-threads=2 --allow-partial=false \
--word-symbol-table=$tri_dir/graph/words.txt $tri_dir/final.mdl $tri_dir/graph/HCLG.fst \
scp,p:$data_dir/$test_train/feats-deltas.scp ark:$tri_dir/decode_dev/lat_$test_train
