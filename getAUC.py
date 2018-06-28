# arg1: identification.tsv, arg2: pred.csv, arg3: positives.csv
import sys, os
import csv
import numpy as np
from numpy import genfromtxt
from sklearn import metrics

def getPretyProteinName(strProtName):
    if strProtName[2] == '|':
        return strProtName.split('|')[1]
    else:
        return strProtName

def initList(strPepIdentificationFilename):
    listData = []
    allProts = set()
    with open(strPepIdentificationFilename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader, None)
        for row in reader:
            if not row[1] in allProts:
                allProts.add(row[1])
                listData.append([row[1], 0, 0])
    
    return listData

def updateScores(listData, strProtScoresFilename):
    # load all scores
    dicScores = {}
    with open(strProtScoresFilename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            dicScores[row[0]] = float(row[1])

    scoreNotFound = set()
    for row in listData:
        strName = row[0]
        if not strName in dicScores:
            strName = getPretyProteinName(strName)

        if strName in dicScores:
            row[1] = dicScores[strName]
        else:
            scoreNotFound.add(strName)
    
    if len(scoreNotFound) > 0:
        print("Warning: {} out of {} scores not predicted (assume zero score).".format(len(scoreNotFound), len(listData)))
        #print(scoreNotFound)

def updateLabelsGoldStandard(listData, strPositivesFilename):
    # load positives
    positives = set()
    with open(strPositivesFilename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            positives.add(row[0])
    
    updatedSet = set()
    # assign labels
    for row in listData:
        strName = row[0]
        if strName in positives:
            row[2] = 1
            updatedSet.add(strName)
        elif getPretyProteinName(strName) in positives:
            row[2] = 1
            updatedSet.add(getPretyProteinName(strName))
    
    diff = positives-updatedSet
    if len(diff) != 0:
        print("Warning: {} out of {} positive[s], don't exist in peptide identification file".format(len(diff), len(positives)))
        #print(diff)
        #for strName in diff: # If to be assumed as wrong predictions instead. This is not needed if we limit all comparisons to only what comes out of peptideProphet.
        #    listData.append([strName, 0, 1])

def updateLabelsDecoy(listData):
    for row in listData:
        if row[0].startswith("DECOY"):
            row[2] = 0
        else:
            row[2] = 1

def updateLabels(listData, strPositivesFilename):
    if os.path.isfile(strPositivesFilename):
        updateLabelsGoldStandard(listData, strPositivesFilename)
    elif strPositivesFilename == "DECOY":
        updateLabelsDecoy(listData)
    else:
        raise Exception("Third argument should either be strPositivesFilename or 'DECOY'")


strPepIdentificationFilename = sys.argv[1]
strProtScoresFilename = sys.argv[2]
strPositivesFilename = sys.argv[3]

'''
strPepIdentificationFilename = "../DeepPep/data/18mix/identification.tsv"
strProtScoresFilename = "../DeepPep/data/18mix/pred.csv"
strPositivesFilename = "./ref/18mix_reference.csv"
'''


# load data
listData = initList(strPepIdentificationFilename)
updateScores(listData, strProtScoresFilename)
updateLabels(listData, strPositivesFilename)

# extract columns
y = np.array([ x[2] for x in listData ], dtype=np.int)
pred = np.array([ x[1] for x in listData], dtype=np.float)

# calc AUC(roc)
fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
print("{:f}".format( metrics.auc(fpr, tpr)), end=";")

# save ROC data
roc_data = np.stack((fpr, tpr), axis=1)
np.savetxt("{}.roc".format(strProtScoresFilename), roc_data)

# calc AUC(pr)
precision, recall, thresholds = metrics.precision_recall_curve(y, pred, pos_label=1)
print("{:f}".format( metrics.auc(recall, precision)), end=";")

#save PR data
pr_data = np.stack((precision, recall), axis=1)
np.savetxt("{}.pr".format(strProtScoresFilename), pr_data)

'''
def getDicRef(strFilename):
    dicRes = {}
    with open(strFilename) as f:
        for line in f:
            dicRes[line.strip()]= True
    return dicRes

# read file into my_data
my_data = []
strProtProbsFilename=sys.argv[2]
with open(strProtProbsFilename, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader, None)
    for row in reader:
#        print(row[0])
#        print("##")
#        print(dicRef)
        isInRef= row[0] in dicRef
        my_data.append((row[0], float(row[1]) ,int(isInRef)))

# extract columns
y = np.array([ x[2] for x in my_data ], dtype=np.int)
pred = np.array([ x[1] for x in my_data], dtype=np.float)

# calc AUC(roc)
fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
print("{:f}".format( metrics.auc(fpr, tpr)), end=";")

# save ROC data
roc_data = np.stack((fpr, tpr), axis=1)
np.savetxt("{}.roc".format(strProtProbsFilename), roc_data)

# calc AUC(pr)
precision, recall, thresholds = metrics.precision_recall_curve(y, pred, pos_label=1)
print("{:f}".format( metrics.auc(recall, precision)), end=";")

#save PR data
pr_data = np.stack((precision, recall), axis=1)
np.savetxt("{}.pr".format(strProtProbsFilename), pr_data)

my_data = [list(elem) for elem in my_data]#[:,1:2]
for row in my_data:
    row[0] = None
my_data = np.asarray(my_data, dtype=np.float32)


# calculate f1 score
if len(sys.argv) > 3:
    my_data = my_data[np.argsort(my_data[:, 1])][::-1]
    nTop = int(sys.argv[3])
    nRows = my_data.shape[0]
    labels = np.zeros([nRows, 1])
    labels[0:nTop,:].fill(1)
    my_data = np.append(my_data, labels, 1)

    # positive:
    f1Score = metrics.f1_score(my_data[:, 2], my_data[:, 3], pos_label=1)
    print("{:f}".format( f1Score), end=";")

    # negative:
    f1Score = metrics.f1_score(my_data[:, 2], my_data[:, 3], pos_label=0)
    print("{:f}".format( f1Score), end=";")

print()

'''