
# deregulated complexes
# enter the test type (pair or unpair) and mf percentage default 0.75

mainP="/media/sophie/ekokrek_HiC2/Yoshida22"
s="both"
m=5 # complex size is 5, max 5 protein members

## declare an array (-a) variable
declare -a comparison=("adult_disease" "child_disease" "age_healthy" "age_covid")

while read c;
do 
	for x in "${comparison[@]}"
	do
	case ${x} in

	  adult_disease)
	  java -jar $mainP/tools/CompleXChange/CompleXChange_1.01/CompleXChange.jar -hr -s=$mainP/tools/CompleXChange/hocomoco11_TF_769.txt -enr -sc "$mainP/analysis/${c}/adult_healthy_${s}/complexes_m${m}" "$mainP/analysis/${c}/adult_covid_${s}/complexes_m${m}" "$mainP/analysis/${c}/deregComp_${x}_${s}/"
	    ;;

	  child_disease)
	  java -jar $mainP/tools/CompleXChange/CompleXChange_1.01/CompleXChange.jar -hr -s=$mainP/tools/CompleXChange/hocomoco11_TF_769.txt -enr -sc "$mainP/analysis/${c}/child_healthy_${s}/complexes_m${m}" "$mainP/analysis/${c}/child_covid_${s}/complexes_m${m}" "$mainP/analysis/${c}/deregComp_${x}_${s}/"
	    ;;

	  age_healthy)
	  java -jar $mainP/tools/CompleXChange/CompleXChange_1.01/CompleXChange.jar -hr -s=$mainP/tools/CompleXChange/hocomoco11_TF_769.txt -enr -sc "$mainP/analysis/${c}/child_healthy_${s}/complexes_m${m}" "$mainP/analysis/${c}/adult_healthy_${s}/complexes_m${m}" "$mainP/analysis/${c}/deregComp_${x}_${s}/"
	    ;;

	  age_covid)
	  java -jar $mainP/tools/CompleXChange/CompleXChange_1.01/CompleXChange.jar -hr -s=$mainP/tools/CompleXChange/hocomoco11_TF_769.txt -enr -sc "$mainP/analysis/${c}/child_covid_${s}/complexes_m${m}" "$mainP/analysis/${c}/adult_covid_${s}/complexes_m${m}" "$mainP/analysis/${c}/deregComp_${x}_${s}/"
	    ;;

	  *)
	  # this part was prepared when the comparison was taken as an input
	    echo "something wrong"
	    ;;
	esac
	done
done < $mainP/docs/cellTypes.txt

