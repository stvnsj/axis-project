import numpy as np
import section as sec
import difflib


class ModelIterator :

    def __init__ (self, model, start=0 , end=0):
        self._model = model
        self._index = start
        self._end   = model.size if end==0 else end
        
    def __iter__ (self) :
        return self
    
    def __next__ (self) :
        if self._index >= self._model.size or self._index > self._end:
            raise StopIteration
        section = self._model.sections[self._model.sectionIndex[self._index]]
        self._index += 1
        return section


"""
Model represents a full set of cross sections, i.e. the full path.
"""
class Model :
    
    def __init__ (self, heights, matrix = None, labels= None):
        
        self.heights = dict(heights)
        self.kms = []
        self.sections = []
        self.sectionIndex = [] # Index of non-duplicate sections in self.sections
        self.__kmIdDict = {}
        self.errNum = 0
        self.build(matrix,labels)
        self.sections.sort()
        self.deduplicate()
        self.currSection = 0;
        self.size = len(self.sectionIndex)
    
    
    def getSection(self,index):
        i = self.sectionIndex[index]
        return self.sections[i]
    
    
    
    
    
    def getKmRange(self,km0,km1):
        
        i0 = 0
        i1 = self.size - 1
        
        i = 0
        

        
        
        itr = ModelIterator(self)
        
        for section in itr:
            
            if np.float64(section.km) >= np.float64(km0):
                
                i0 = i
                break
            
            else:
                
                i += 1
                
        
        if np.float64(km0) >= np.float64(km1) :
            return (i0, i1)
        
        itr2 = ModelIterator(self, i0)
        
        for section in itr2:
            
            if np.float64(section.km) <= np.float64(km1):
                
                i += 1
            
            else:
                
                i1 = i-1
                break
        
        return (i0,i1)
    
    
    
    def printMop (self):
        for i in self.sectionIndex:
            print(self.sections[i].mopFormat())
    
    
    def writeWidth (self,filename) :
        self.sections.sort()
        self.deduplicate()
        with open(filename, "w") as f:
            for i in self.sectionIndex:
                np.savetxt(f, self.sections[i].widthFormat(), delimiter=',' ,fmt='%s')  
    
    
    
    # Given the sorted section list `sections`, this functions merges
    # in one section all the duplicate sections.  It places in list
    # `section index` the indices of non-duplicate `sections`
    def deduplicate (self) :
        i = 0
        j = 1
        length = len(self.sections)
        self.sectionIndex.append(i)
        while j < length :
            if self.sections[i] == self.sections[j]:
                self.sections[i].merge(self.sections[j])
                j = j + 1
            else:
                i = j
                j = j + 1
                self.sectionIndex.append(i)
    
    
    
    
    def findHeight (self,km):
        
        try:
            
            height = self.heights[km]
            try:
                floatHeight = np.float64(height)
                return floatHeight
            except ValueError:
                print(f'> Error {self.errNum}: Altura erronea para el km {km}')
                self.errNum = self.errNum + 1 
                return np.float64(0)
        
        except KeyError:
            
            try:
                floatKm = np.float64(km)
                for i in range(0,10):
                    newKm = "{:.2f}".format(np.trunc(floatKm * 100) / 100) + str(i)
                    if newKm in self.heights:
                        print(f'> Advertencia {self.errNum}: Cota de {newKm} usada para {km}')
                        self.errNum += 1
                        return  np.float64(self.heights[newKm])
                raise ValueError("Not in dict")
                
            except:
                print(f'> Error {self.errNum}: Altura de {km} no encontrada')
                self.errNum = self.errNum + 1
                return np.float64(0)
    
    
    def build (self,matrix,labels):
        
        start = 0 # start index of matrix chunk copied
        end = 0 # end index of matrix chunk copied
        i = 1 # pointer to traverse the matrix 
        length = matrix.shape[0] # vertical size of matrix
        
        while i < length :
            
            # If the value of km is nan, then keep stacking more
            # points to the current section
            if np.isnan(matrix[i][0]):
                end = end + 1;
                i   = i + 1
                
                if(i == length):
                    
                    height = self.findHeight(labels[start])
                    
                    section = sec.Section(
                        labels[start],
                        matrix[start:end],
                        labels[start:end],
                        height)
                    
                    self.sections.append(section)
                    self.kms.append(matrix[start][0])
            
            
            elif (not np.isnan(matrix[i][0])):
                end = end + 1;
                
                height = self.findHeight(labels[start])
                               
                section = sec.Section(
                    labels[start],
                    matrix[start:end],
                    labels[start:end],
                    height)
                
                self.sections.append(section)
                self.kms.append(matrix[start][0])
                start = i
                end = i
                i = i + 1
    
    def __iter__ (self):
        return self
    
    def __next__ (self):
        if self.currSection >= self.size:
            raise StopIteration
        else:
            i = self.currSection
            self.currSection += 1
            return self.sections[self.sectionIndex[i]]




