import numpy as np


def formatFloatArray (array) :
    def formatFloat(x):
        return f'{x:.3f}'
    return np.vectorize(formatFloat)(array)

def formatCadFloatArray (array) :
    def formatFloat(x):
        return f'{x:.3f}'.replace('.',',')
    return np.vectorize(formatFloat)(array)

def parseLabel(label):
    if label.endswith("i"):
        return -1
    else:
        return 1

def parseLabelLetter(label):
    if label.endswith("i"):
        return "l"
    elif label.endswith("d"):
        return "r"
    else:
        return "e"  

parseLabelArray = np.vectorize(parseLabel)
parseLabelLetterArray = np.vectorize(parseLabelLetter)
