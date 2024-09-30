import sys
import numpy as np
import utils





class Point :
    
    def __init__ (
            self,
            num,
            start = False,
            point_uncorrected = 0.0,
            back_delta = 0.0,
            front_delta = 0.0,
            dm = np.array([]),
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
        self.size = len(dm) + 1
        
        
 
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
        self.point_corrected = self.instr_corrected - self.intermediate;
 
    
    def get_table (self):
        X = np.column_stack((self.dm[:,None] , self.point_corrected[:,None]))
        return X
    
    
    
    
    
    ###########
    # GETTERS #
    ###########
    def get_point_uncorrected (self):
        return self.point_uncorrected
    def get_instr_uncorrected (self):
        return self.instr_uncorrected



class Segment :
    
    def __init__ (self, pr0, pr1, first_height, last_height, cplst=[]):
        
        self.pr0 = pr0 # string name of pr0
        self.pr1 = pr1 # string name of pr1
        
        self.positive = utils.pr_number(pr0) < utils.pr_number(pr1)
        
        self.pr = (utils.pr_number(pr0),self.positive)
        
        self.points = cplst
        
        self.diff = 0
        
        self.length = len(cplst)
     
        self.first_height = first_height
        self.last_height  = last_height
        
        self.point_uncorrected = last_height
        
        self.ref_height = last_height
        
        self.size = 0
        
        self.__build()
 
    def __build (self):
        
        for i , cp in enumerate(self.points) :
            
            if i == 0:
                cp.build()
                continue
            
            cp.build(self.points[i-1])
        
        point_uncorrected = self.points[-1].get_point_uncorrected()
        
        self.diff = self.ref_height - point_uncorrected
        self.size = len(self.points) - 1
        
        for cp in self.points:
            
            cp.correct_instr(self.diff / self.size);
            cp.correct_point()
            
 
 
    def  get_table (self):
        lst = [p.get_table() for p in self.points]
        if self.positive:
            return np.vstack(lst)
        else:
            return np.vstack(lst)[::-1]
            
        
 
    def __str__ (self) :
        return f'pr0 = {self.pr0}\npr1 = {self.pr1}\npoint corrected = {self.points}'



class Circuit :
    def __init__ (self, positive, negative):
        self.positive = positive
        self.negative = negative
 
    def get_positive_table(self):
        lst = [s.get_table() for s in self.positive]
        return np.vstack(lst)
    
    def get_negative_table(self):
        lst = [s.get_table() for s in self.negative]
        return np.vstack(lst)


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
    
    for i, row in enumerate(string_matrix):
        
        # NULL followed by NULL    or     final NULL
        if (row[1] == "" and i == N - 1)   or   (row[1] == "" and string_matrix[i+1][1] == ""):
            first = True if POINT_NUM == 0 else False
            point = parse_point(POINT_NUM,first,h0,string_matrix[i:i+1])
            POINT_NUM += 1
            point_list.append(point)
            continue
        
        # NULL followed by NON-NULL
        if (row[1] == "" and  string_matrix[i+1][1] != ""):
            START = i
            continue
        
        # NON-NULL followed by NULL
        if (row[1] != "" and string_matrix[i+1][1] == ""):
            first = True if POINT_NUM == 0 else False
            point = parse_point(POINT_NUM,first,h0,string_matrix[START:i+1])
            POINT_NUM += 1
            point_list.append(point)
            continue 
 
    
    return Segment(pr0, pr1, h0, h1, point_list)


def parse_point (num, start, h0, string_matrix):
 
    back_delta  = np.round(float(string_matrix[0][3]),3) if string_matrix[0][3] != "" else 0.0
    front_delta = np.round(float(string_matrix[0][5]),3) if string_matrix[0][5] != "" else 0.0
    point_uncorrected = np.round(float(h0),3) if start else 0.0
 
    dm = np.array([])
    im = np.array([])
 
    if len(string_matrix) > 1 :
        dm = np.array([utils.normalize_fstring(x) for x in string_matrix[1:,1]])
        im = np.round(np.where(string_matrix[1:,4] == "", "0.0", string_matrix[1:,4]).astype(float),3)
    
    
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
 
    string_matrix = np.genfromtxt(filename1, delimiter=',', dtype=str, skip_header=0)
    height_matrix = np.genfromtxt(filename2, delimiter=',', dtype=str, skip_header=0)
 
    pro = parse_circuit(string_matrix, height_matrix)
 
    positive_segments = []
    negative_segments = []
 
    for seg in pro:
        
        if seg.positive:
            positive_segments.append(seg)
        
        else: 
            negative_segments.append(seg)
 
    cir = Circuit(positive_segments, negative_segments)
    positive_table  = cir.get_positive_table()
    negative_table  = cir.get_negative_table()
    intersection = np.intersect1d(positive_table[:,0], negative_table[:,0])
    union        = np.union1d(positive_table[:,0], negative_table[:,0])
    complement   = np.setdiff1d(union,intersection)
    positive_dict = dict (positive_table)
    negative_dict = dict (negative_table)
    for dm in intersection:
        A = f'dm: {dm} '
        B = f'ida: {np.round(float(positive_dict[dm]),3)} '
        C = f'veulta: {np.round(float(negative_dict[dm]),3)} '
        D = f'diff : '
        print(A , B, C)


