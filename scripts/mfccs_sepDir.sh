
info_mess="This script ($0) calculates mfccs for the utterances in the given path
It saves the mfccs into the sub directory $data_dir/feats/
Therefore, the mfccs are specific to one project
A check for exisiting feats is not implemented
"
usage_mess="
Usage: 	$0 <data_main_dir> <which_set>
	<data_main_dir>: the path to the data main directory,
		e.g. data, 20phatts_data, ...
	<which_set>: the name of the sub directory under the
		<data_main_dir>, which holds the utterances,
		e.g. test, train, 20phatts_test, ...
"

echo "$info_mess" # always echo the info_mess"
sleep 1

####### input parameters
if [ $# != 2 ]; then
	echo "$usage_mess"
	exit 1
fi

data_dir=${1%/}
test_train=${2%/}
#######


echo "Checking $data_dir/conf/mfcc.conf"
sleep 1
mfcc_conf="$data_dir/conf/mfcc.conf"
if [ ! -f "$data_dir/conf/mfcc.conf" ]; then
	echo "$data_dir/conf/mfcc.conf does not exist"
	echo "Now, checking for conf/mfcc.conf"
	sleep 1
	mfcc_conf="conf/mfcc.conf"
	if [ ! -f "conf/mfcc.conf" ]; then
		echo "conf/mfcc.conf does not exist"
		echo "You should create a mfcc.conf file in one of the above checked places"
		echo "Then, run this script ($0) again"
		exit 1
	fi
fi
# check sample-freq in mfcc.conf
sleep 3

mkdir -p $data_dir/feats

echo Starting with computing the MFCCs
compute-mfcc-feats --config=$mfcc_conf scp:$data_dir/$test_train/wav.scp ark:- | copy-feats --compress=true ark:- ark,scp:$data_dir/feats/mfcc-$test_train.ark,$data_dir/$test_train/feats.scp || exit $?
echo Done with computing the MFCCs

#read -p "Press a key to continue" var
sleep 1

echo Doing the CMVN normalization on the MFCCs
compute-cmvn-stats --spk2utt=ark:$data_dir/$test_train/spk2utt scp:$data_dir/$test_train/feats.scp ark,scp:$data_dir/feats/cmvn-$test_train.ark,$data_dir/$test_train/cmvn.scp || exit $?
echo Done with CMVN normalization

#read -p "Press a key to continue" var
sleep 1

echo Starting with computing the deltas
apply-cmvn --utt2spk=ark:$data_dir/$test_train/utt2spk scp:$data_dir/$test_train/cmvn.scp scp:$data_dir/$test_train/feats.scp ark:- | add-deltas ark:- ark,scp:$data_dir/feats/mfcc-deltas-$test_train.ark,$data_dir/$test_train/feats-deltas.scp || exit $?
echo Done with computing the deltas

echo Done with calculating the mfccs
echo "As the next step, the Viterbi training should get prepared and executed"
echo "For a monophone model, use this script: scripts/monophone_viterbi.sh"
echo "Or, if you run for a test set, you can evaluate your monophone or triphone model"
echo "	scripts/monophone_evaluation.sh"
echo "	scripts/triphone_evaluation.sh"
