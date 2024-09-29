import sys
import numpy as np






class Point :
    
    def __init__ (
            self,
            num,
            start = False,
            point_uncorrected = 0.0,
            back_delta = 0.0,
            front_delta = 0.0,
            dm = [],
            intermediate = []):
        
        self.num                     = num
        self.start                   = start
        
        self.dm                      = dm
        self.intermediate            = intermediate
        
        self.back_delta              = back_delta
        self.front_delta             = front_delta
        
        self.point_uncorrected       = point_uncorrected
        self.instr_uncorrected       = 0.0
        
        self.point_corrected  = []
        self.instr_corrected  = 0.0
        
        
 
    def build (self, prev = None):
        """initializes point_uncorrected and instr_uncorrected
        interacting with previous control point."""
        if not self.start:
            self.__init_point_uncorrected (prev)
        self.__init_instr_uncorrected ()
        
    
    def __init_point_uncorrected (self, prev):
        
        instr = prev.instr_uncorrected
        self.point_uncorrected = instr - self.front_delta
        return
    
    def __init_instr_uncorrected (self) :
        self.instr_uncorrected = self.point_uncorrected + self.back_delta
        
 
    
    def correct_instr (self, correction):
        self.instr_corrected = self.instr_uncorrected + correction * self.num
 
 
    def correct_point (self):
        self.point_corrected =  self.instr_corrected - self.intermediate;
    
    
    
    
    
    
    
    ###########
    # GETTERS #
    ###########
    def get_point_uncorrected (self):
        return self.point_uncorrected
    def get_instr_uncorrected (self):
        return self.instr_uncorrected
    
    #########
    # PRINT #
    #########
    def __str__(self):
        return f'DM = {self.dm}\nuncorrected point = {self.point_uncorrected}'
      




class Segment :
    
    def __init__ (self, pr0, pr1, first_height, last_height, cplst=[]):
        
        self.pr0 = pr0 # string name of pr0
        self.pr1 = pr1 # string name of pr1
        
        self.control_point_list = cplst
        
        self.diff = 0
     
        self.first_height = 0
        self.last_height  = 0
        
        self.point_uncorrected = last_height
        
        self.ref_height = last_height
        
        self.size = 0
        
        self.__build()
 
    def __build (self):
        
        for i , cp in enumerate(self.control_point_list) :
            
            if i == 0:
                cp.build()
                continue
            
            cp.build(self.control_point_list[i-1])
        
        point_uncorrected = self.control_point_list[-1].get_point_uncorrected()
        
        self.diff = self.ref_height - point_uncorrected
        self.size = len(self.control_point_list) - 1
        
     
        for cp in self.control_point_list:
            cp.correct_instr(self.diff / self.size);
            cp.correct_point()
        
 

    def __str__ (self) :
        return f'pr0 = {self.pr0}\npr1 = {self.pr1}\npoint corrected = {self.control_point_list}'



class Circuit :
    def __init__ (self):
        pass
    


class Model :
    def __init__ (self):
        pass



def parse_circuit (circuit_matrix, height_matrix):
    start = 0
    end   = 1
    height_dict = dict(height_matrix)
    segment_list = []
    
    for i , row in enumerate(circuit_matrix):
        if row[0] != "" :
            
            start = i
           
        if row[2] != "":
            
            end = i
         
            pr0 = circuit_matrix[start][0]
            pr1 = circuit_matrix[end][2]
         
            h0  = float(height_dict[pr0])
            h1  = float(height_dict[pr1])
           
            seg = parse_segment(circuit_matrix[start:end+1], pr0, pr1, h0, h1)
            segment_list.append(seg)
            
    return segment_list


def parse_segment (string_matrix, pr0, pr1, h0, h1):
    
    POINT_NUM = 0
    START = 0
    END   = 0
    N     = len(string_matrix)
 
    point_list = []
    
    for i, row in enumerate(string_matrix[1:]):
      
        if row[1] == "" and  string_matrix[i][1] == "":
            END = i+1
            
            first = True if POINT_NUM == 0 else False
            point = parse_point(POINT_NUM, first, h0, string_matrix[START:END])
            point_list.append(point)
            POINT_NUM += 1
            
            START = i+1
            
            continue
        
        if row[1] == "":
            END = i+1
            
            first = True if POINT_NUM == 0 else False
            point = parse_point(POINT_NUM, first, h0, string_matrix[START:END])
            point_list.append(point)
            POINT_NUM += 1
            
            START = i+1
            continue
        
        if i == N-2:
            END = i+1
            first = True if POINT_NUM == 0 else False
            point = parse_point(POINT_NUM, first, h0, string_matrix[START:END])
            print("=================\n\n")
            print(point)
            print("=================\n\n")
            point_list.append(point)
            continue

    for point in point_list:
        print(point)
 
    return Segment(pr0, pr1, h0, h1, point_list)


def parse_point (num, start, h0, string_matrix):
 
    back_delta  = float(string_matrix[0][3]) if string_matrix[0][3] != "" else 0.0
    front_delta = float(string_matrix[0][5]) if string_matrix[0][5] != "" else 0.0
    point_uncorrected = float(h0) if start else 0.0
 
    dm = []
    im = []
 
    if len(string_matrix) > 0 :
        #dm = np.where(string_matrix[1:,1] == "", "0.0", string_matrix[1:,1]).astype(float)
        dm = string_matrix[1:,1]
        im = np.where(string_matrix[1:,4] == "", "0.0", string_matrix[1:,4]).astype(float)
    
    
    point = Point(
        num,
        start=start,
        point_uncorrected=point_uncorrected,
        back_delta = back_delta,
        front_delta = front_delta,
        dm = dm,
        intermediate = im
    )
    return point



if __name__ == "__main__":
 
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
 
    print(filename1)
 
    # string_matrix = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=0)[:,0]
    string_matrix = np.genfromtxt(filename1, delimiter=',', dtype=str, skip_header=0)
    height_matrix = np.genfromtxt(filename2, delimiter=',', dtype=str, skip_header=0)
 
    pro = parse_circuit(string_matrix, height_matrix)

    for seg in pro:
        for p in seg.control_point_list:
            print(p)
