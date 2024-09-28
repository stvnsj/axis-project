import numpy as np

formatFloat = lambda x : f'{np.round(x,3)}'
formatFloatArray = lambda array : np.vectorize(formatFloat)(array)


def compute_sign (v1, v2):
    
    x1 = v1[0]
    y1 = v1[1]
    
    x2 = v2[0]
    y2 = v2[1]
 
    prod = x1 * y2 - y1 * x2
    
    if prod >= 0:
        return -1
    else:
        return 1

compute_sign_array = np.vectorize(compute_sign,signature='(n),(n)->()')



def parseLabel(label):
    if label.endswith("i") or label.endswith("I"):
        return -1
    else:
        return 1


def parseLabelLetter(label):
    if label.endswith("i") or label.endswith("I"):
        return "l"
    elif label.endswith("d") or label.endswith("D"):
        return "r"
    else:
        return "e"  

parseLabelArray = np.vectorize(parseLabel)
parseLabelLetterArray = np.vectorize(parseLabelLetter)




round_float        = lambda x : np.round(x,3)
format_float       = lambda x : "{:.3f}".format(x)
format_float_array = lambda arr : np.vectorize(format_float)(arr)



