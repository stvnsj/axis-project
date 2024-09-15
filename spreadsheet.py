
import numpy as np
import model as mdl
import utils


class Spreadsheet :
    
    def __init__ (self, model) :
        self.__model = model
    
    
    def writeWidth (self) :
        pass
    
    
    
    def writeSectionMOP (self,section,f) :
        
        # [i:] array from index i
        # [::-1] reverse numpy array
        
        ascendingIndex = np.argsort(section.distance[1:])
        section.distance[1:] = section.distance[1:][ascendingIndex]
        
        descendingIndex = np.argsort(np.where(section.distance[1:]<0)[0])[::-1]
        
        # Index of the last negative number 
        neg = len(descendingIndex)
        
        # reversed ordered on negative part of distance
        section.distance[1:neg+1] = section.distance[1:][descendingIndex]
        
        
        section.adjustedHeight[1:] = section.adjustedHeight[1:][ascendingIndex]
        section.adjustedHeight[1:neg+1] = section.adjustedHeight[1:][descendingIndex]
        
        section.labels[1:] = section.labels[1:][ascendingIndex]
        section.labels[1:neg+1] = section.labels[1:][descendingIndex]
        
        section.labels[0] = '0ep'
        
        section.side[1:] = section.side[1:][ascendingIndex]
        section.side[1:neg+1] = section.side[1:][descendingIndex]
        
        
        content = np.hstack((
            
            np.where(np.isnan(section.matrix[:,[0]]), '' , section.matrix[:,[0]].astype(str) ),
            utils.formatFloatArray (section.distance[:,None]),
            utils.formatFloatArray (section.adjustedHeight),
            section.labels[:,None],
            section.side))
        
        np.savetxt(f, content ,fmt='%s')
    
    
    
    
    def writeMOP (self,filename="testmop.csv") :
        sections = mdl.ModelIterator(self.__model,23,28)
        
        with open(filename, "w") as f:
            for section in sections :
                self.writeSectionMOP(section,f)
                print(section.getId())

