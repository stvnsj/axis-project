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
        
        self.num                     = num  # Ordinal number of this point in the segment
        self.start                   = start # Boolean. True if it is the first point in the segment
        
        self.dm                      = dm # List of kilometers
        self.intermediate            = intermediate # list of deltas for each dm
        
        self.back_delta              = back_delta
        self.front_delta             = front_delta
        
        self.point_uncorrected       = point_uncorrected # Uncorrected height for each dm
        self.instr_uncorrected       = 0.0 # Uncorreted instr 
        
        self.point_corrected  = []
        self.instr_corrected  = 0.0
        self.size = len(dm) + 1
        
        
    def __str__ (self):
        A = f'{self.instr_corrected}'
        B = f'{self.point_corrected}'
        return A + " " + B
 
    def build (self, prev = None):
        """initializes point_uncorrected and instr_uncorrected
        interacting with previous control point."""
        if not self.start:
            self.__init_point_uncorrected (prev)
        self.__init_instr_uncorrected ()
        
    
    def __init_point_uncorrected (self, prev):
        instr = prev.instr_uncorrected
        self.point_uncorrected = utils.round(instr - self.front_delta)
    
    def __init_instr_uncorrected (self) :
        self.instr_uncorrected = utils.round(self.point_uncorrected + self.back_delta)
        
 
    def correct_instr (self, correction):
        self.instr_corrected = utils.round(self.instr_uncorrected + correction * self.num)
 
    def correct_point (self):
        self.point_corrected = utils.round(self.instr_corrected - self.intermediate)
 
    def get_table (self):
        X = np.column_stack((
            np.round(self.dm[:,None],3),
            np.round(self.point_corrected[:,None],3),
            
        ))
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
        
        self.diff = 0.0
        
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
     
        self.diff = np.round (self.ref_height - point_uncorrected , 3)
        self.size = len(self.points) - 2
        # print("REF : " , self.ref_height)
        # print("UNCOR : " , self.point_uncorrected)
        # print("DIFF  : " , self.diff)
        # print("")
        for cp in self.points:
            
            cp.correct_instr(self.diff / self.size);
            cp.correct_point()
            
 
 
    def  get_table (self):
        lst = [p.get_table() for p in self.points]
        if self.positive:
            return np.vstack(lst)
        else:
            return np.vstack(lst)[::-1]
            
        

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
    
    def write_circuit_table(self, filename):
        
        positive_table  = self.get_positive_table()
        negative_table  = self.get_negative_table()
        intersection    = np.intersect1d(positive_table[:,0], negative_table[:,0])
        union           = np.union1d(positive_table[:,0], negative_table[:,0])
        complement      = np.setdiff1d(union,intersection)
        positive_dict   = dict (positive_table)
        negative_dict   = dict (negative_table)
        full_table = np.array([["DM", "IDA","VUELTA","DIF","MEDIA"]])
        
        for dm in intersection:
            
            positive_h = positive_dict[dm]
            negative_h = negative_dict[dm]
            dif = np.absolute(float(positive_h) - float(negative_h))
            mean = np.mean([float(positive_h),float(negative_h)])
            #print(dm , " " , positive_h , " " , negative_h)
            
            new_row = np.array([[
                dm,
                utils.normalize_fstring(positive_h),
                utils.normalize_fstring(negative_h),
                utils.format_float(dif),
                utils.format_float(mean)
            ]])
            full_table = np.append(full_table, new_row, axis=0)
            
        with open(filename, "w") as f:
            np.savetxt(f,full_table,delimiter=',',fmt='%s')



class Model :
    def __init__ (self):
        pass




def parse_circuit (circuit_matrix, height_matrix, circuit_num_matrix = None, pr_num_matrix = None):
    start = 0
    end   = 1
    
    height_dict = dict(zip (height_matrix[:,0], pr_num_matrix[:,1]))
    
    
    segment_list = []
    
    for i , row in enumerate(circuit_matrix):
        
        if row[0] != "" :
            start = i
        
        if row[2] != "":
            
            end = i
         
            pr0 = circuit_matrix[start][0]
            pr1 = circuit_matrix[end][2]
         
            h0  = height_dict[pr0]
            h1  = height_dict[pr1]
           
            seg = parse_segment(circuit_matrix[start:end+1], pr0, pr1, h0, h1, num_matrix=circuit_num_matrix[start:end+1])
            segment_list.append(seg)
    
    return segment_list


def parse_segment (string_matrix, pr0, pr1, h0, h1, num_matrix=None):
    POINT_NUM = 0
    START = 0
    END   = 0
    N     = len(string_matrix)
 
    point_list = []
    
    for i, row in enumerate(string_matrix):
        
        # NULL followed by NULL    or     final NULL
        if (row[1] == "" and i == N - 1)   or   (row[1] == "" and string_matrix[i+1][1] == ""):
            first = True if POINT_NUM == 0 else False
            point = parse_point(POINT_NUM,first,h0,string_matrix[i:i+1],num_matrix[i:i+1])
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
            point = parse_point(POINT_NUM,first,h0,string_matrix[START:i+1],num_matrix[START:i+1])
            POINT_NUM += 1
            point_list.append(point)
            continue 
 
    
    return Segment(pr0, pr1, h0, h1, point_list)


def parse_point (num, start, h0, string_matrix, num_matrix = None):
    
    back_delta   = 0.0 if np.isnan(num_matrix[0][3]) else num_matrix[0][3]
    front_delta  = 0.0 if np.isnan(num_matrix[0][5]) else num_matrix[0][5]
 
    point_uncorrected = h0 if start else 0.0
 
    dm = np.array([])
    im = np.array([])
 
    if len(string_matrix) > 1 :
        dm = num_matrix[1:,1]
        im = num_matrix[1:,4]
    
    
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


def parser (filename1, filename2, filename3):
 
    libreta_string_matrix = np.genfromtxt(filename1, delimiter=',', dtype=str, skip_header=0)
    height_string_matrix = np.genfromtxt(filename2, delimiter=',', dtype=str, skip_header=0)
    
    libreta_num_matrix = np.round(np.genfromtxt(filename1, delimiter=',', skip_header=0),3)
    height_num_matrix =  np.round(np.genfromtxt(filename2, delimiter=',', skip_header=0),3)
    
    pro = parse_circuit(libreta_string_matrix, height_string_matrix,
                  circuit_num_matrix=libreta_num_matrix,
                  pr_num_matrix=height_num_matrix)
 
    positive_segments = []
    negative_segments = []
 
    for seg in pro:
        if seg.positive:
            positive_segments.append(seg)
        else: 
            negative_segments.append(seg)
 
    cir = Circuit(positive_segments, negative_segments,)
    cir.write_circuit_table(filename3)
