import sys
import csv
import numpy as np
from numpy import genfromtxt
from sklearn import metrics

def getDicRef(strFilename):
    dicRes = {}
    with open(strFilename) as f:
        for line in f:
            dicRes[line.strip()]= True
    return dicRes

strRefFilename=sys.argv[1]
dicRef=getDicRef(strRefFilename)

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

#'''
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

#'''
