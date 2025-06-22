rm -f error.log
for yy in 1989 1991 1992 1993 1994 1995 1996
do
    for ch in {1..97}
    do
	python HTSPDF.py ${yy} $ch
	if [ $? -eq 1 ]
	then
	    echo $yy chapter $ch >> error.log
	fi
    done
done
