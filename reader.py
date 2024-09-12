import numpy as np
import sys


class Reader :
    
    def __init__(self,path1,path2):
        self.matrix = np.genfromtxt(path1, delimiter=',', skip_header=0)
        self.labels = np.genfromtxt(path1, delimiter=',', dtype=str, skip_header=0)[:,4]
        self.heights = np.genfromtxt(path2, delimiter=',', skip_header=0, dtype=str)
        
    # Obtain  
    def getData (self) :
        return self.matrix,self.labels,self.heights



