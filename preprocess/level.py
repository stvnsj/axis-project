import numpy as np
import utils


def guessHeight (dm,dm_array,line=None):
    try:
        dm_float = np.round(float(dm),3)
    except:
        print (f'Linea {int(line)}: No hay cambio sugerido para {dm}')
    
    for dm0 in dm_array:
        try:
            dm0_float = np.round(float(dm0),3)
        except:
            continue
        
        if np.abs(dm_float - dm0_float) <= 0.01:
            print(f'Linea {int(line)}: {dm} --> {dm0}')
            return
    
    print (f'Linea {int(line)}: No hay cambio sugerido para {dm}')
    return

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
    
    
    
    data = utils.read_csv('/home/jstvns/NIVELACION/mariaelena.csv')
    dm   = utils.read_csv('/home/jstvns/NIVELACION/dm.csv')
    
    
    # Generate an enumeration column
    row_numbers = np.arange(1, data.shape[0] + 1).reshape(-1, 1)
    
    # Add the enumeration column as the first column
    data_num = np.hstack((row_numbers, data))
    
    for mat in  MatrixLevelIterator(data_num):
        #Interval(mat).test_order()
        Interval(mat).test_dm(dm)

if __name__ == "__main__" :
    main()
