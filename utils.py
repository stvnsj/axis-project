import numpy as np

formatFloat = lambda x : f'{np.round(x,3)}'
formatFloatArray = lambda array : np.vectorize(formatFloat)(array)


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
