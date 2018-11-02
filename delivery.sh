dir=$1
for file in `ls $1`
do
	extend=${file##*.}
	foo=${file#*_}
	dirname=${foo%_*}
	[ ${extend} != 'jpg' ] && continue
	if [ ! -d ${dir}/${dirname} ]; then
		mkdir ${dir}/${dirname}
		echo 'create dir' ${dirname}
	fi
	# echo ${dirname}
	mv ${dir}/${file} ${dir}/${dirname}/
done
