
####### input parameters
if [ $# != 2 ]; then
	echo "Attention: This script has to be started in the ../kaldi/ - directory"
	echo "Usage: $0 <local_dir> <lang_dir>"
	echo "  e.g.: $0 phatts_wout_slash_data/local/ phatts_wout_slash_data/lang"
	exit 1
fi

local_dir=$1
local_dir=${local_dir%/}
lang_dir=$2
lang_dir=${lang_dir%/}
#######

utils/prepare_lang.sh --position-dependent-phones false $local_dir/dict "<UNK>" $local_dir/lang_tmp $lang_dir
