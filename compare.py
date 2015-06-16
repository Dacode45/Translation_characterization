import glob, os
import csv
import math

filenames = []
raws = {}

def openCSV(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(row)
    return rows

def checkIfValid(rawCSV, filename):
    #print(rawCSV)
    file = filename[:-4]
    #print(file)
    if file in raws and raws[file] is not None:
        raise ValueError('Trying to process two of the same file')
    if rawCSV[0][1] != file: #Row should have title in 2nd column
        raise ValueError('Filename does not match file title')
    organism = file[-2:]
    #print(organism)
    #Check if is the right organism
    if organism == 'cy':
        if rawCSV[3][1] != "Cyanothece sp. ATCC 51142 (ACCTCCTTA)**":
            print(file+'\n')
            raise ValueError("File should be for Cyanothece sp. ATCC 51142 (ACCTCCTTA)** instead %s"%( rawCSV[3][1]))
    elif organism == 'ec':
        if rawCSV[3][1] != "Escherichia coli 536 (ACCTCCTTA)":
            raise ValueError("File should be for Escherichia coli 536 (ACCTCCTTA)")
    elif organism == 'sy':
        if rawCSV[3][1] != "Synechocystis sp. PCC 6803 (ACCTCCTTT)**":
            raise ValueError("File should be for Synechocystis sp. PCC 6803 (ACCTCCTTT)**")
    else:
        raise("No organism for this file")

#initializes filenames array
def getFiles():
    os.chdir("./new_data")
    for file in glob.glob("*.csv"):
        filenames.append(file)
    raws = dict.fromkeys(filenames)
    os.chdir("../")

def checkUniqueDNA():
    seqs = dict()
    for  file, csv in raws.items():
        seq = csv[4][1]
        if seq in seqs:
            seqs[seq].append(file)
        else:
            seqs[seq]=[file]
    for seq, files in seqs.items():
        if len(files) > 3:
            raise ValueError("Similar Sequences %s\n %s"%(files, seq))

if __name__ == "__main__":
    try:

        #initialization
        getFiles()
        #print(filenames)
        for filename in filenames:
            rawCSV = openCSV("new_data/"+filename)
            checkIfValid(rawCSV, filename)
            file = filename[:-4]
            raws[file] = rawCSV

        #check that all DNA sequences are unique
        checkUniqueDNA()


        #get comparisons
        files = list(raws.keys())
        files.sort()
        for i in range(0, math.floor(len(files)/3)):
            cy = raws[files[3*i]]
            ec = raws[files[3*i+1]]
            sy = raws[files[3*i+2]]
            print("Comparing " + cy[0][1] + " and " + ec[0][1] + " and " + sy[0][1] + "\n") #filenames
            mRNA = cy[4][1]
            print("mRNA seq:\t%s\n"% mRNA)

            #get all okay dNA sequences
            seq_cy = [row for row in cy[7:] if row[8]=="OK"]
            seq_ec = [row for row in ec[7:] if row[8]=="OK"]
            seq_sy = [row for row in sy[7:] if row[8]=="OK"]
            #get intersection where dna have same start site
            #print('Start Position,Translation Initiation Rate (au),dG_total (kcal/mol),dG_mRNA_rRNA (kcal/mol),dG_spacing (kcal/mol),dG_standby (kcal/mol),dG_start (kcal/mol),dG_mRNA (kcal/mol),Accuracy (warnings)')
            column_keys = 'Start Position,Translation Initiation Rate (au),dG_total (kcal/mol),dG_mRNA_rRNA (kcal/mol),dG_spacing (kcal/mol),dG_standby (kcal/mol),dG_start (kcal/mol),dG_mRNA (kcal/mol),Accuracy (warnings)'.split(',')
            if(len(seq_cy) != len(seq_ec)):
                #TODO intersect list, perform comparisons
                #will this ever happen?
                print("Sizes differ\n");
            else:
                for i in range(0, len(seq_cy)):
                    #originally tried to compare rates, but it turns out all rates are
                    #the same, now trying to compare everything
                    # if float(seq_cy[i][1]) != float(seq_ec[i][1]):
                    #     print("Cyanothece:\tStart Site: pos:%d, seq:%s \tRate: %d\n"%(int(seq_cy[i][0]), cy[4][1][int(seq_cy[i][0]):int(seq_cy[i][0])+5], float(seq_cy[i][1])) )
                    #     print("Escherichia:\tStart Site: pos:%d, seq:%s \tRate: %d\n"%(int(seq_ec[i][0]), ec[4][1][int(seq_ec[i][0]):int(seq_ec[i][0])+5], float(seq_ec[i][1])) )
                    # else:
                    #     print("Same rate for Start Site:%d\n"%int(seq_cy[i][0]))
                    all_same = True
                    for j in range(1, len(column_keys)):
                        if seq_cy[i][j] != seq_ec[i][j] and seq_ec[i][j] != seq_sy[i][j]:
                            all_same = False
                            print("Start Site: %s,%s\t%s differs.\n Cyanothece:%s\t Escherichia:%s\t Synechocystis:%s\n"%(seq_cy[i][0], mRNA[int(seq_cy[i][0])-1:int(seq_cy[i][0])+4], column_keys[j], seq_cy[i][j], seq_ec[i][j], seq_sy[i][j]))
                    if all_same:
                        print("Start Site: %s, %s have the same values in Cyanothece, Escherichia, and Synechocystis."%(seq_cy[i][0], mRNA[int(seq_cy[i][0])-1:int(seq_cy[i][0])+4]))


    except ValueError as err:
        print(err)
