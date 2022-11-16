
echo "This script plots a language model named G.fst"
echo "You need a sourced kaldi for this script, since the command fstdraw is used"
echo "It may take a while if the language model is big"
echo "Be aware of Klaus!!"
if [ $# != 1 ]; then
	echo "Usage: $0 <path2GFst>"
	echo "       <path2GFst>: path to the directory, in which the G.fst file is located"
	exit 1
fi

path2GFst=${1%/}

fstdraw --portrait $path2GFst/G.fst $path2GFst/G.dot
dot -Tpdf $path2GFst/G.dot > $path2GFst/G.pdf
