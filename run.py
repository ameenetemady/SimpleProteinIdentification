""" To predict protein identification probabilities given peptide identification probabilities. """
import sys
import os
import csv
from Bio import SeqIO

def getDefaultSetting(strDatabaseDir):
    dicSetting = {
        "strDatasetDir": strDatabaseDir,
        "strFastaDB": '{:s}/db.fasta'.format(strDatabaseDir),
        "strFilePathIdentification": '{:s}/identification.tsv'.format(strDatabaseDir),
        "strFilePathPredOutput": '{:s}/pred.csv'.format(strDatabaseDir),
        "strFilePathProtRefList": '{:s}/ref.txt'.format(strDatabaseDir)
    }

    return dicSetting

def loadProtPeptideDic(strFilePath, delimiter = "\t", protColId = 1, pepColId = 0, probColId = 2):
    """ Description: Load protein, peptide, and probablity info into single dictionary
    Return: 
      1) Dictionary of proteins pointed to the corresponding peptides and probabilities
      2) Dictionary of peptides with associated probababilities """

    protDic = {}
    pepDic = {}

    with open(strFilePath, "r") as bfCsv:
        csvReader = csv.reader(bfCsv, delimiter = delimiter, skipinitialspace=True)
        for row in csvReader:
            strPep = row[pepColId]
            strProt = row[protColId]
            dProb = float(row[probColId])

            # update peptide info
            pepInfo = pepDic.get(strPep)
            if pepInfo is None:
                pepInfo = [dProb, 0] # [probability, matchingCount(to be filled)]
                pepDic[strPep] = pepInfo
            else:
                pepInfo[0] = max(dProb, pepInfo[0]) # Note: allways using 'max', if mean need a little more work
            
            # update protInfo
            protInfo = protDic.get(strProt)
            if protInfo is None:
                protInfo = {}
                protDic[strProt] = protInfo

            protInfo[strPep] = True
        
        return protDic, pepDic

def updatePepProtMatchingCounts(protDic, pepDic):
    for strProt, protInfo in protDic.items():
        for strPep, __ in protInfo.items():
            pepDic[strPep][1] += 1

def getProtScores(protDic, pepDic):
    listProtScores = []
    for strProt, protInfo in protDic.items():
        dProtScore = 0
        for strPep, __ in protInfo.items():
            pepScoreScaled = pepDic[strPep][0]/pepDic[strPep][1]
            dProtScore += pepScoreScaled
        listProtScores.append([strProt, dProtScore])

    return listProtScores

def getPretyProteinName(strProtName):
    if strProtName[2] == '|':
        return strProtName.split('|')[1]
    else:
        return strProtName

def saveProtScores(listProtScores, strFilename):
    with open(strFilename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(listProtScores)

def trimPeps(protInfo, seq):
    pepsToDel = []
    for strPep, __ in protInfo.items():
        if seq.find(strPep) < 0:
            pepsToDel.append(strPep)

    for strPep in pepsToDel:
        del protInfo[strPep]
    
    return len(pepsToDel)

def removeNonMatchingPairs(protDic, strFastaFilename):
    for currRecord in SeqIO.parse(strFastaFilename, "fasta"):
        if currRecord.name in  protDic:
            trimPeps(protDic[currRecord.name], currRecord.seq)

def runOne(dicSetting):
    print("running for: {!s}".format(dicSetting['strDatasetDir']))
    protDic, pepDic = loadProtPeptideDic(dicSetting['strFilePathIdentification'])
    removeNonMatchingPairs(protDic, dicSetting['strFastaDB'])
    updatePepProtMatchingCounts(protDic, pepDic)
    listProtScores = getProtScores(protDic, pepDic)

    for item in listProtScores:
        item[0] = getPretyProteinName(item[0])

    saveProtScores(listProtScores, dicSetting['strFilePathPredOutput'])


# 18mix:
# Input: db.fasta, identification.tsv, ref.txt
# Output: pred.csv
# Note: Ensure Input files (with exact names) are copied under strDataDir directory apriori
#strDataDir = sys.argv[1]
#runOne(getDefaultSetting(strDataDir))
runOne(getDefaultSetting("data/18mix"))
runOne(getDefaultSetting("data/Sigma49"))
runOne(getDefaultSetting("data/UPS2"))
runOne(getDefaultSetting("data/DME"))
runOne(getDefaultSetting("data/HumanEKC"))
runOne(getDefaultSetting("data/HumanMD"))
runOne(getDefaultSetting("data/Yeast"))






