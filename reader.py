import numpy as np
import sys


class Reader :
    
    def __init__(self,path1,path2,path3):

        if path1:
            self.matrix = np.genfromtxt(path1, delimiter=',', skip_header=0)
            self.labels = np.genfromtxt(path1, delimiter=',', dtype=str, skip_header=0)[:,4]
        else:
            self.matrix = None
            self.labels = None

        if path2:
            self.oriented_matrix = np.genfromtxt(path2, delimiter=',', skip_header=0)
            self.oriented_labels = np.genfromtxt(path2, delimiter=',', dtype=str, skip_header=0)[:,4]

        else:
            self.oriented_matrix = None
            self.oriented_labels = None
            
            
        if path3 : 
            self.heights = np.genfromtxt(path3, delimiter=',', skip_header=0, dtype=str)
        else :
            self.heights = None
        
    
    # Obtain  
    def getData (self) :
        
        return self.matrix, self.labels, self.oriented_matrix, self.oriented_labels, self.heights
     




