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
    	ppixTool = "{0}/tools/CompleXChange/PPIXpress_1.23/PPIXpress.jar".format(arg_p)
    	ppinRef = "{0}/tools/CompleXChange/preppi_final600.sif".format(arg_p)
	# predict protein complexes based on the condition-specific ppin and ddin using JDACO
    	compTool = "{0}/tools/CompleXChange/JDACO_1.03/JDACO.jar".format(arg_p)
    	seedRef = "{0}/tools/CompleXChange/hocomoco11_TF_769.txt".format(arg_p)
 
	
	
