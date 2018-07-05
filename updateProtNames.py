import csv
import sys

def getPretyProteinName(strProtName):
    parts = strProtName.split('|')
    if len(parts) > 1:
        return parts[1]
    return strProtName

strFilename = sys.argv[1]

listAll = []
with open(strFilename, "r") as bfCsv:
        csvReader = csv.reader(bfCsv, delimiter = '\t', skipinitialspace=True)
        for row in csvReader:
            newRow = row
            newRow[1] = getPretyProteinName(newRow[1])
            listAll.append(newRow)

strFilenameUpdated = strFilename
with open(strFilenameUpdated, "w") as bfCsv:
    csvWriter = csv.writer(bfCsv, delimiter = '\t')
    csvWriter.writerows(listAll)
    print("updated in {!s}".format(strFilenameUpdated))
