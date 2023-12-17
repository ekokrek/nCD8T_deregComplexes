import sys
import getopt
import scanpy as sc
import pandas as pd
from adpbulk import ADPBulk
import os


def myfunc(argv):
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
                                   ["help", "mainPath=", "cellType=", "age=", "disease=", "sex="])
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

    # main directory of the Yoshida study "/media/sophie/ekokrek_HiC2/Yoshida22"

    adata = sc.read_h5ad('{0}/rawD/{1}_{2}_{3}_{4}.h5ad'.format(arg_p, arg_c, arg_a, arg_d, arg_s), backed=True)

    # initialize the object
    adpb = ADPBulk(adata, ["sample_id"])

    # perform the pseudobulking
    pseudobulk_matrix = adpb.fit_transform()

    # retrieve the sample meta data
    sample_meta = adpb.get_meta()
    sample_meta.to_csv("{0}/rawD/metadata_{1}_{2}_{3}_{4}.txt".format(arg_p, arg_c, arg_a, arg_d, arg_s))

    cellLabels = pd.read_csv('{0}/docs/cellTypeNamesLabels.csv'.format(arg_p))
    ct_name = cellLabels['cellTypeName'][cellLabels['cellTypeLabel'] == arg_c].item()

    # check out the cell counts
    sampleCellCounts = pd.DataFrame(adata.obs['sample_id'][(adata.obs['cell_type'] == ct_name)].value_counts())
    sampleCellCounts.to_csv("{0}/rawD/sampleCellCounts_{1}_{2}_{3}_{4}.tsv".format(arg_p, arg_c, arg_a, arg_d, arg_s),
                            sep="\t", index=True)

    idz = list(sampleCellCounts.index)
    expressionMat = pseudobulk_matrix.transpose()

    # cellCountThreshold is important; min 60
    cct = 60

    os.makedirs("{0}/data/{1}/{2}/{3}/ProtComp/".format(arg_p, arg_c, arg_a, arg_d, arg_s))

    for n in range(0, len(sample_meta)):
        print(n, sample_meta['sample_id'][n])
        nn = idz.index(sample_meta['sample_id'][n])
        cell_count = sampleCellCounts.iloc[nn, 0]
        if cell_count < cct:
            print("The sample {0} does not have enough cells".format(sample_meta['sample_id'][n]))
            continue
        if nn < 9:
            expM = expressionMat.iloc[:, n]
            expM.to_csv(
                "{0}/data/{1}/{2}/{3}/ProtComp/{1}_{2}_{3}_{4}_0{5}.tsv".format(arg_p, arg_c, arg_a, arg_d, arg_s,
                                                                               nn + 1),
                sep='\t', index_label='target_id')
        else:
            expM = expressionMat.iloc[:, n]
            expM.to_csv(
                "{0}/data/{1}/{2}/{3}/ProtComp/{1}_{2}_{3}_{4}_{5}.tsv".format(arg_p, arg_c, arg_a, arg_d, arg_s,
                                                                              nn + 1),
                sep='\t', index_label='target_id')


if __name__ == "__main__":
    myfunc(sys.argv)
