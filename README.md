# nCD8T_deregComplexes
deregulated protein complex analysis in naive CD8+ T cells to test age and disease factor


prepareComplexes.sh takes cellTypes.txt file and calls three python scripts:
	1. analysis_1.py 
	generating condition-specific h5ad files; 
	2. analysis_2.py 
	generating condition-specific individual expression files
	3. analysis_3.py
	generating condition-specific ppins, ddins and predicting protein complexes
	
	
