# nCD8T_deregComplexes
deregulated protein complex analysis in naive CD8+ T cells to test age and disease factor

prepareComplexes.sh takes cellTypes.txt file and calls three python scripts:

	1. analysis_1.py
 
	generating condition-specific h5ad files
 
	2. analysis_2.py
 
	generating condition-specific individual expression files
 
	3. analysis_3.py
 
	generating condition-specific ppins, ddins and predicting protein complexes
 	# generating sample specific ppins and ddins using PPIXpress
    	ppixTool = "tools/CompleXChange/PPIXpress_1.23/PPIXpress.jar"
        to download: https://sourceforge.net/projects/ppixpress/
    	ppinRef = "/tools/CompleXChange/preppi_final600.sif"
     	to download: https://bhapp.c2b2.columbia.edu/PrePPI/
	# predict protein complexes based on the condition-specific ppin and ddin using JDACO
    	compTool = "/tools/CompleXChange/JDACO_1.03/JDACO.jar"
        to download: https://sourceforge.net/projects/dacoalgorithm/
    	seedRef = "/tools/CompleXChange/hocomoco11_TF_769.txt"
 	to download: https://hocomoco12.autosome.org/
	
compareComplexes.sh quantifies and compares predicted complexes by calling CompleXChange tool.
	
	tools/CompleXChange/CompleXChange_1.01/CompleXChange.jar 
	to download: https://sourceforge.net/projects/complexchange/


Yoshida etal 2022 Dataset: 
https://cellxgene.cziscience.com/collections/03f821b4-87be-4ff4-b65a-b5fc00061da7 

