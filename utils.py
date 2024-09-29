import numpy as np
import re

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

def round_float (x):
    """round float to three decimal places"""
    return np.round(x,3)

def format_float (x):
    """float to string with three decimal places"""
    return "{:.3f}".format(x)


def format_float_array (arr):
    """floats of array to string with three decimal places"""
    return np.vectorize(format_float)(arr)



# Function to extract the numeric part of PR points
def pr_number(s):
    # Use regular expression to find the number in the string
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    return None


def normalize_fstring(s):
    """Converts a string decimal"""
    
    try:
        f = float(s)
        r = np.round(f,3)
        s0 = "{:.3f}".format(r)
        return s0
    
    except:
        return s

def normalize_fstring_array(arr):
    np.vectorize(normalize_fstring)(arr)
