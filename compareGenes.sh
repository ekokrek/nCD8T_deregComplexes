
# differentially expressed gene analysis

mainP="/media/sophie/ekokrek_HiC2/Yoshida22"

# declare an array (-a) variable
# 1:"adult_disease" 2:"child_disease" 3:"age_healthy" 4:"age_covid"
declare -a comparison=(1 2 3 4)

while read c;
do 
	for x in "${comparison[@]}"
	do
	
	Rscript $mainP/scripts/DEG.R $mainP ${x} ${c} 
	
	done
done < $mainP/docs/cellTypes.txt

