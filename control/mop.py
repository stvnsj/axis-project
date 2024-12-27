
import numpy as np
import utils

class MopMatrixIterator :
    def __init__ (self, matrix) :
        self.matrix = matrix
        self.index  = 1
        self.length = len(matrix)
    
    def __iter__ (self) :
        return self
    
    def __next__ (self) :
        
        if self.index == self.length :
            raise StopIteration
        
        START = 0
        END   = 0
        
        for i in range(self.index, self.length):
            # This is the first index of the following section
            if self.matrix[i][0] == '' or i == self.length - 1:
                START      = self.index - 1
                END        = i - 1
                self.index = i
                break
        
        return self.matrix
    
    

class MOPPoint :
    
    def __init__ (self, distance, height):
        self.distance = distance
        self.height   = height

class MOPSection:
    
    def __init__ (self, ):
        
        

class MOP :
    def __init__ (self, filename) :
        self.matrix = utils.read_csv(filename)
        for row in

