import subprocess
import sys
import getopt
import os


def myfunc(argv):
    arg_p = ""
    arg_c = ""
    arg_a = ""
    arg_d = ""
    arg_s = ""
    arg_m = ""
    arg_help = "{0} \n\n -p <mainPath> \n -c <cellType> out of 9: \n\t naturalKiller,\n\t classical,\n\t nonclassical," \
               "\n\t cd4posHelperT,\n\t cd8posCytotoxic,\n\t naiveThymusCD8T,\n\t centralMemoryCD8T,\n\t naiveT," \
               "\n\t naiveB\n -a <age> out of 2: child or adult \n " \
               "-d <disease> out of 2: healthy or covid \n -s <sex> out of 3: both, male or female \n -m <complexSize>".format(argv[0])
    try:
        opts, args = getopt.getopt(argv[1:], "hp:c:a:d:s:m:",
                                   ["help", "mainPath=", "cellType=", "age=", "disease=","sex=","complexSize="])
    except:
        print(arg_help)
        sys.exit(2)
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
        elif opt in ("-m", "--complexSize"):
            arg_m = int(arg)

    print('mainPath:', arg_p)
    print('cellType:', arg_c)
    print('age:', arg_a)
    print('disease:', arg_d)
    print('sex:', arg_s)
    print('complexSize:', arg_m)


# count the number of individual expression files per condition

    pToExpFiles = "{0}/data/{1}/{2}/{3}/ProtComp".format(arg_p, arg_c, arg_a, arg_d)
    sampleSize = int(subprocess.run(["ls -l {0}| wc -l ".format(pToExpFiles)], shell=True, capture_output=True).stdout.decode('utf-8'))-1

    exFiles = []
    for n in range(sampleSize):
        if n<9:
            exFiles.append("{0}/{1}_{2}_{3}_{4}_0{5}.tsv".format(pToExpFiles, arg_c, arg_a, arg_d, arg_s,n + 1))
        else:
            exFiles.append("{0}/{1}_{2}_{3}_{4}_{5}.tsv".format(pToExpFiles, arg_c, arg_a, arg_d, arg_s,n + 1))

    exFilesToCommand = " ".join(exFiles)

# pathToPredictedComplexes
    os.makedirs("{0}/analysis/{1}/{2}_{3}_{4}/complexes_m{5}/".format(arg_p, arg_c, arg_a, arg_d, arg_s, arg_m))
    pToPredComp = "{0}/analysis/{1}/{2}_{3}_{4}/complexes_m{5}".format(arg_p, arg_c, arg_a, arg_d, arg_s, arg_m)

# generating sample specific ppins and ddins using PPIXpress
    ppixTool = "{0}/tools/CompleXChange/PPIXpress_1.23/PPIXpress.jar".format(arg_p)
    ppinRef = "{0}/tools/CompleXChange/preppi_final600.sif".format(arg_p)

    subprocess.run("java -jar {0} -d -mg -t=0 -r=108 {1} {2}/ {3}".format(ppixTool, ppinRef, pToPredComp, exFilesToCommand), shell=True, capture_output=True)

# predict protein complexes based on the condition-specific ppin and ddin using JDACO
    compTool = "{0}/tools/CompleXChange/JDACO_1.03/JDACO.jar".format(arg_p)
    seedRef = "{0}/tools/CompleXChange/hocomoco11_TF_769.txt".format(arg_p)

    for k in range(1,sampleSize+1):
        subprocess.run('java -jar {0} -pb=0.95 {1}/{2}_ppin.txt {1}/{2}_ddin.txt {3} {4} {1}/{2}_complexes.txt > {1}/{2}_log.txt'.format(compTool,pToPredComp,k,seedRef,arg_m), shell=True, capture_output=True)


if __name__ == "__main__":
    myfunc(sys.argv)

