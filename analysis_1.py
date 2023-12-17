import sys
import getopt
import pandas as pd
import scanpy as sc


def myfunc(argv):
    global mdata
    arg_p = ""
    arg_c = ""
    arg_a = ""
    arg_d = ""
    arg_s = ""
    arg_help = "{0} \n\n -p <mainPath> \n -c <cellType> out of 9: \n\t naturalKiller,\n\t classical,\n\t nonclassical," \
               "\n\t cd4posHelperT,\n\t cd8posCytotoxic,\n\t naiveThymusCD8T,\n\t centralMemoryCD8T,\n\t naiveT," \
               "\n\t naiveB\n -a <age> out of 2: child or adult \n " \
               "-d <disease> out of 2: healthy or covid \n -s <sex> out of 3: both, male or female \n".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hp:c:a:d:s:",
                                   ["help", "mainPath=", "cellType=", "age=", "disease=","sex="])
    except:
        print(arg_help)
        sys.exit(2)
    arg: str
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-p", "--mainPath"):
            arg_p = arg
        elif opt in ("-c", "--cellType"):
            arg_c = arg
        elif opt in ("-a", "--age"):
            arg_a = arg.lower()
        elif opt in ("-d", "--disease"):
            arg_d = arg.lower()
        elif opt in ("-s", "--sex"):
            arg_s = arg.lower()

    print('mainPath:', arg_p)
    print('cellType:', arg_c)
    print('age:', arg_a)
    print('disease:', arg_d)
    print('sex:', arg_s)

    # It will accept
    # the path to the main directory which includes following folders: rawD, data, analysis, scripts, docs, tools
    # main directory of the Yoshida study 	"/media/sophie/ekokrek_HiC2/Yoshida22"
    # cell type included in the dataset; renamed for the coding purposes
    # age group, disease state, sex

    # get the data; backed option helps the memory
    adata = sc.read_h5ad("{0}/rawD/local.h5ad".format(arg_p), backed=True)

    # a table of columns cellTypeName and cell_type name
    cellLabels = pd.read_csv('{0}/docs/cellTypeNamesLabels.csv'.format(arg_p))
    ct_name = cellLabels['cellTypeName'][cellLabels['cellTypeLabel'] == arg_c].item()

    if arg_a == 'child':
        if arg_d == 'healthy':
            # CHILD & HEALTHY
            mdata = adata[(adata.obs['cell_type'] == ct_name) & (adata.obs['COVID_severity'] == 'Healthy') & (adata.obs['Group'] == 'Paediatric')]
        elif arg_d == 'covid':
            # CHILD & COVID
            mdata = adata[(adata.obs['cell_type'] == ct_name) & (adata.obs['COVID_severity'] != 'Healthy') & (adata.obs['Group'] == 'Paediatric')]
    elif arg_a == 'adult':
        if arg_d == 'healthy':
            # ADULT & HEALTHY
            mdata = adata[(adata.obs['cell_type'] == ct_name) & (adata.obs['COVID_severity'] == 'Healthy') & (adata.obs['Group'] == 'Adult')]
        elif arg_d == 'covid':
            # ADULT & COVID
            mdata = adata[(adata.obs['cell_type'] == ct_name) & (adata.obs['COVID_severity'] != 'Healthy') & (adata.obs['Group'] == 'Adult')]
    else:
        print("There is a problem here!")
    mdata.write_h5ad('{0}/rawD/{1}_{2}_{3}_{4}.h5ad'.format(arg_p, arg_c, arg_a, arg_d, arg_s))


if __name__ == "__main__":
    myfunc(sys.argv)
