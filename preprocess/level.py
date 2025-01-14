import numpy as np
import utils


def guessHeight (dm,dm_array,line=None):
    dm2 = dm[:-1]
    for i in range(0,10):
        dm3 = dm2 + f'{i}'
        if dm3 in dm_array:
            print(f"Cambio de DM sugerido en línea {line}: {dm} --> {dm3}\n")
            return
    print(f"No hay cambio de DM sugerido para {dm} en línea {line}\n")

class Interval :
    def __init__ (self, matrix):
        self.pr1 = matrix[0][1]
        self.pr2 = matrix[-1][3]
        self.matrix = matrix
        self.positive = True if utils.pr_number(self.pr1) < utils.pr_number(self.pr2) else False
    
    def test_order (self) :
        indices = np.where(self.matrix[:,2] != "")[0]
        for i in range(len(self.matrix[:,2][indices]) - 1):
            
            try:
                dm0 = float(self.matrix[:,2][indices][i])
            except:
                dm0 = -1
                
                
            try:
                dm1 = float(self.matrix[:,2][indices][i+1])
            except:
                dm1 = -1
                
                
            negative = not self.positive
            if self.positive and float(dm0) < float(dm1):
                continue
            if self.positive and float(dm0) >= float(dm1):
                print()
                print(f'ERROR DE ORDEN en {self.pr1} ; {self.pr2}')
                print(f'dm0={dm0} ; dm1={dm1}')
                continue
            if negative and float(dm0) > float(dm1):
                continue
            if negative and float(dm0) <= float(dm1):
                print()
                print(f'ERROR DE ORDEN en {self.pr1} ; {self.pr2}')
                print(f'dm0={dm0} ; dm1={dm1}')
                continue
    
    def test_dm (self,dm_array) :
        indices = np.where(self.matrix[:,2] != "")[0]
        for i in range(len(self.matrix[:,2][indices])):
            dm = self.matrix[:,2][indices][i]
            line = self.matrix[:,0][indices][i]
            if dm not in dm_array:
                guessHeight(dm,dm_array,line)


class MatrixLevelIterator:
    
    def __init__ (self, matrix) :
        self.matrix = matrix
        self.index  = 0
        self.length = len(matrix)
    
    def __iter__ (self) :
        return self
    
    def __next__(self) :
        
        if self.index >= self.length:
            raise StopIteration
        
        for i in range(self.index, self.length):
            
            if self.matrix[i][3] == "":
                continue
            
            else:
                START = self.index
                END   = i + 1
                self.index = i + 1
                return self.matrix[START:END]



def main () :
    
    
    
    data = utils.read_csv('/home/jstvns/EQC-files/NIVELACION_SOCAIRE_P3.csv')
    dm   = utils.read_csv('/home/jstvns/EQC-files/dm.csv')
    
    
    # Generate an enumeration column
    row_numbers = np.arange(1, data.shape[0] + 1).reshape(-1, 1)
    
    # Add the enumeration column as the first column
    data_num = np.hstack((row_numbers, data))
    
    for mat in  MatrixLevelIterator(data_num):
        Interval(mat).test_order()
        #Interval(mat).test_dm(dm)

if __name__ == "__main__" :
    main()
