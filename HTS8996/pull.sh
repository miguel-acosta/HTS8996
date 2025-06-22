## no basic 1990 
mkdir pdf 
for yy in 89 91 92 93 94 95 96 97
do
    mkdir pdf/19${yy}
    for ch in $(seq -f "%02g" 1 99)
    do
	if [ $yy == 92 ] || [ $yy == 91 ]
	then
	    wget --user-agent="Mozilla/4.0" https://www.usitc.gov/tata/hts/archive/${yy}00/${yy}0c${ch}0.pdf
	    mv ${yy}0c${ch}0.pdf pdf/19${yy}/${yy}0c${ch}.pdf
	else
	    wget --user-agent="Mozilla/4.0" https://www.usitc.gov/tata/hts/archive/${yy}00/${yy}0c${ch}.pdf
	    mv ${yy}0c${ch}.pdf pdf/19${yy}/
	fi
	
    done
done


wget --user-agent="Mozilla/4.0" https://www.usitc.gov/tata/hts/archive/8910/891c62.pdf
wget --user-agent="Mozilla/4.0" https://www.usitc.gov/tariff_affairs/documents/890c622.pdf
pdftk 891c62.pdf 890c622.pdf cat output pdf/1989/89c62.pdf
rm 891c62.pdf 890c622.pdf

wget --user-agent="Mozilla/4.0" https://www.usitc.gov/tata/hts/archive/9200/920c621.pdf
wget --user-agent="Mozilla/4.0" https://www.usitc.gov/tata/hts/archive/9200/920c622.pdf
pdftk 920c621.pdf 920c622.pdf cat output pdf/1992/920c62.pdf
rm 920c621.pdf 920c622.pdf

wget --user-agent="Mozilla/4.0" https://www.usitc.gov/tata/hts/archive/9200/920c841.pdf
wget --user-agent="Mozilla/4.0" https://www.usitc.gov/tata/hts/archive/9200/920c842.pdf
pdftk 920c841.pdf 920c842.pdf cat output pdf/1992/920c84.pdf
rm 920c841.pdf 920c842.pdf


# 1995 supplement
mkdir pdf/1995supp
for ch in $(seq -f "%02g" 1 99)
do
    wget --user-agent="Mozilla/4.0" https://www.usitc.gov/tata/hts/archive/9510/951c${ch}.pdf
    mv 951c${ch}.pdf pdf/1995supp/
done
