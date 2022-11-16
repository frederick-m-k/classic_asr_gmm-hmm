#This script plots a subtree of the phonetic decision tree
#It is assumed that plot output dir already exists with tree.dump file in it 

if [ $# != 4 ]; then
	echo " "
	echo "Usage: <chose_SAMPA_phone> <triphone_model> <data_directory> <plot_output_dir>"
	echo "e.g.:  2: exp/tri/ data/ plot_subtree/"
	echo "Make sure that the plot_subtree/ directory exists with tree.dump file in it before you run this script"
	echo " "
	exit 1
fi

phone=$1
tri_mod=$2
data_dir=$3
plot_dir=$4


#draw-tree $data_dir/lang/phones.txt $tri_mod/tree |\
#sed 's/label=\([[:alnum:]][:~][[:alnum:]]*\),/label="\1",/g' |\
#sed 's/label=\([?@]\)/label="\1"/g' > $plot_dir/tree.dump

input=$plot_dir/tree.dump
root="0"
#label='label="2:"'
label="label=\"${phone}\""
phoneChecked="false"

head -n 2 $input >> $plot_dir/phone_$phone.dump 

while read -r line;do
	if [[ $phoneChecked == "true" ]]; then
		if [[ "$line" != "$root"* ]]; then
			#echo "$line"
			echo "$line" >> $plot_dir/phone_$phone.dump 
		else
			phoneChecked="false"
		fi
	fi
	if [[ "$line" == "$root"* ]] && [[ "$line" == *"$label"* ]]; then
		#echo "$line"
		echo "$line" >> $plot_dir/phone_$phone.dump 
		phoneChecked="true"
	fi
done < "$input"

cat << EOF >> $plot_dir/phone_$phone.dump 
}
EOF

cat $plot_dir/phone_$phone.dump   |  dot -Tps -Gsize=6,8 | ps2pdf - $plot_dir/phone_$phone.pdf
