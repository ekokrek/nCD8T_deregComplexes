

# cell type, age, disease amd sex should be entered as arguments

mainP="/media/sophie/ekokrek_HiC2/Yoshida22"
s="both"

## declare an array (-a) variable 
declare -a age=("adult" "child")
declare -a disease=("healthy" "covid")

while read c;
do 
	for a in "${age[@]}"
	do
		for d in "${disease[@]}"
		do
		
# call analysis_1.py for generating condition-specific h5ad files; args: p,c,a,d,s
		python $mainP/scripts/analysis_1.py -p $mainP -c ${c} -a "${a}" -d "${d}" -s ${s}
		
# call analysis_2.py for generating condition-specific individual expression files; args: p,c,a,d,s
		python $mainP/scripts/analysis_2.py -p $mainP -c ${c} -a "${a}" -d "${d}" -s ${s}

# call analysis_3.py for generating condition-specific ppins, ddins and predicting protein complexes; args: p,c,a,d,s,m
# m is the complex size; since it is constant throughout the analysis, assigned directly
		python $mainP/scripts/analysis_3.py -p $mainP -c ${c} -a "${a}" -d "${d}" -s ${s} -m 5

		done
	done
done < $mainP/docs/cellTypes.txt


