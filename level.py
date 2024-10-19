import sys
import numpy as np
import utils
import levelCad


class Point :
    
    def __init__ (
            self,
            num,
            start = False,
            point_uncorrected = 0.0,
            back_delta = 0.0,
            front_delta = 0.0,
            dm = np.array([]),
            intermediate = [],
            str_dm = np.array([])
    ):
        
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
        self.str_dm = str_dm
        
        
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
        # X = np.column_stack((
        #     np.round(self.dm[:,None],3),
        #     np.round(self.point_corrected[:,None],3),
            
        # ))
        return (self.str_dm, np.round(self.point_corrected,3))
    
    
    
    
 
    ###########
    # GETTERS #
    ###########
    def get_point_uncorrected (self):
        return self.point_uncorrected
    def get_instr_uncorrected (self):
        return self.instr_uncorrected



class Segment :
    
    def __init__ (self, pr0, pr1, first_height, last_height, cplst=[], start_points = [], end_points=[]):
        self.pr0 = pr0 # string name of pr0
        self.pr1 = pr1 # string name of pr1
        self.pr_dict = {}
        
        if pr1 in start_points and pr0 in end_points:
            self.positive = False
            start_points.append(pr0)
            end_points.append(pr1)
            
        elif pr0 in start_points and pr1 in end_points:
            self.positive = False
            end_points.append(pr0)
            start_points.append(pr1)
            
        else:
            self.positive = True
            start_points.append(pr0)
            end_points.append(pr1)
            
        
        
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
        
        for cp in self.points:
            
            cp.correct_instr(self.diff / self.size);
            cp.correct_point()
        
        if utils.pr_number(self.pr0) < utils.pr_number(self.pr1):
            for p in self.points:
                self.pr_dict.update({dm:(self.pr0,self.pr1) for dm in p.str_dm})
        else :
            for p in self.points:
                self.pr_dict.update({dm:(self.pr1,self.pr0) for dm in p.str_dm})
                
                
                
    def get_pr_dict(self):
        return self.pr_dict
 
    def  get_table (self):
        
        lst = [p.get_table() for p in self.points]
        
        dm_list, pnt_list = list(zip(*lst))
        
        return (np.concatenate(dm_list),np.concatenate(pnt_list))


class Circuit :
    
    def __init__ (self, positive, negative):
        
        # self.positive and self.negative are lists
        # of Segment instances.
        self.positive = positive
        self.negative = negative
        
        self.pr_dict  = {}
        
        for s in positive:
            self.pr_dict.update(s.get_pr_dict())
            
        for s in negative:
            self.pr_dict.update(s.get_pr_dict())
 
    def get_positive_table(self):
        lst = [s.get_table() for s in self.positive]
        
        dm_list, pnt_list = list(zip(*lst))
        return (np.concatenate(dm_list),np.concatenate(pnt_list))
    
    def get_negative_table(self):
        lst = [s.get_table() for s in self.negative]
        dm_list, pnt_list = list(zip(*lst))
        return (np.concatenate(dm_list),np.concatenate(pnt_list))
    
    def write_circuit_table(self, filename):
        
        pos_dm, pos_pnt = self.get_positive_table()
        neg_dm, neg_pnt = self.get_negative_table()
        
        intersection    = np.intersect1d(pos_dm, neg_dm)
        union           = np.union1d(pos_dm, neg_dm)
        
        # complement      = np.setdiff1d(union,intersection)
        positive_dict   = dict (zip(pos_dm,pos_pnt))
        negative_dict   = dict (zip(neg_dm,neg_pnt))
        
        full_table = np.empty((0, 8))
        
        for dm in union:
            
            if dm == "":
                continue
            
            if dm in intersection:
                
                positive_h = positive_dict.get(dm)
                negative_h = negative_dict.get(dm)
                dif = np.round(np.absolute(float(positive_h) - float(negative_h)),3)
                mean = np.mean([float(positive_h),float(negative_h)])
                
                new_row = np.array([[
                    dm,
                    utils.format_float(positive_h),
                    utils.format_float(negative_h),
                    utils.format_float(dif),
                    utils.format_float(mean),
                    self.pr_dict.get(dm)[0],
                    self.pr_dict.get(dm)[1],
                    "FT" if dif >= 0.01 else ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            if dm in positive_dict:
                positive_h = positive_dict.get(dm)
                negative_h = "SIN COTA"
                dif        = 0.0
                mean       = positive_h
                new_row = np.array([[
                    dm,
                    utils.format_float(positive_h) if not np.isnan(positive_h) else "VACIO",
                    negative_h,
                    utils.format_float(dif),
                    utils.format_float(mean),
                    self.pr_dict.get(dm)[0],
                    self.pr_dict.get(dm)[1],
                    ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
                
            if dm in negative_dict:
                positive_h = "SIN COTA"
                negative_h = negative_dict.get(dm)
                dif        = 0.0
                mean       = negative_h
                new_row = np.array([[
                    dm,
                    positive_h,
                    utils.format_float(negative_h) if not np.isnan(negative_h) else "VACIO",
                    utils.format_float(dif),
                    utils.format_float(mean),
                    self.pr_dict.get(dm)[0],
                    self.pr_dict.get(dm)[1],
                    ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            
            
        
        num_index = np.where([utils.is_float(x) for x in full_table[:,0]])
        str_index = np.where([not utils.is_float(x) for x in full_table[:,0]])
        ordered_num_index = np.argsort(full_table[num_index][:,0].astype(float))
        
        output = np.vstack((
            np.array([["DM", "IDA","VUELTA","DIF","MEDIA","PR-A","PR-B","TOLERANCIA"]]),
            full_table[ordered_num_index] ,
            full_table[str_index]
        ))
        
        
        with open(filename, "w") as f:
            np.savetxt(f,output,delimiter=',',fmt='%s')
 
 
    def get_report_long (self):
        
        pos_dm, pos_pnt = self.get_positive_table()
        neg_dm, neg_pnt = self.get_negative_table()
        
        intersection    = np.intersect1d(pos_dm, neg_dm)
        union           = np.union1d(pos_dm, neg_dm)
        
        # complement      = np.setdiff1d(union,intersection)
        positive_dict   = dict (zip(pos_dm,pos_pnt))
        negative_dict   = dict (zip(neg_dm,neg_pnt))
        
        full_table = np.empty((0, 8))
        
        for dm in union:
            
            if dm == "":
                continue
            
            if dm in intersection:
                
                positive_h = positive_dict.get(dm)
                negative_h = negative_dict.get(dm)
                dif = np.round(np.absolute(float(positive_h) - float(negative_h)),3)
                mean = np.mean([float(positive_h),float(negative_h)])
                
                new_row = np.array([[
                    dm,
                    utils.format_float(positive_h),
                    utils.format_float(negative_h),
                    utils.format_float(dif),
                    utils.format_float(mean),
                    self.pr_dict.get(dm)[0],
                    self.pr_dict.get(dm)[1],
                    "FT" if dif >= 0.01 else ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            if dm in positive_dict:
                positive_h = positive_dict.get(dm)
                negative_h = "SIN COTA"
                dif        = 0.0
                mean       = positive_h
                new_row = np.array([[
                    dm,
                    utils.format_float(positive_h) if not np.isnan(positive_h) else "VACIO",
                    negative_h,
                    utils.format_float(dif),
                    utils.format_float(mean),
                    self.pr_dict.get(dm)[0],
                    self.pr_dict.get(dm)[1],
                    ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
                
            if dm in negative_dict:
                positive_h = "SIN COTA"
                negative_h = negative_dict.get(dm)
                dif        = 0.0
                mean       = negative_h
                new_row = np.array([[
                    dm,
                    positive_h,
                    utils.format_float(negative_h) if not np.isnan(negative_h) else "VACIO",
                    utils.format_float(dif),
                    utils.format_float(mean),
                    self.pr_dict.get(dm)[0],
                    self.pr_dict.get(dm)[1],
                    ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            
            
        
        num_index = np.where([utils.is_float(x) for x in full_table[:,0]])
        str_index = np.where([not utils.is_float(x) for x in full_table[:,0]])
        ordered_num_index = np.argsort(full_table[num_index][:,0].astype(float))
        
        output = np.vstack((
            np.array([["DM", "IDA","VUELTA","DIF","MEDIA","PR-A","PR-B","TOLERANCIA"]]),
            full_table[ordered_num_index] ,
            full_table[str_index]
        ))
        
        
        return output
 
    def write_longitudinal(self, filename):
        
        pos_dm, pos_pnt = self.get_positive_table()
        neg_dm, neg_pnt = self.get_negative_table()
        intersection    = np.intersect1d(pos_dm, neg_dm)
        union           = np.union1d(pos_dm, neg_dm)
        # complement      = np.setdiff1d(union,intersection)
        positive_dict   = dict (zip(pos_dm,pos_pnt))
        negative_dict   = dict (zip(neg_dm,neg_pnt))
        full_table = np.empty((0, 3))
        
        for dm in union:
            
            if dm == "" or not utils.is_float(dm):
                continue
            
            if dm in intersection:
                
                positive_h = positive_dict.get(dm)
                negative_h = negative_dict.get(dm)
                dif = np.round(np.absolute(float(positive_h) - float(negative_h)),3)
                mean = np.mean([float(positive_h),float(negative_h)])
                
                if np.isnan(positive_h) or np.isnan(negative_h):
                    continue
                
                new_row = np.array([[
                    dm,
                    utils.format_float(mean),
                    "FT" if dif >= 0.01 else ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            if dm in positive_dict:
                positive_h = positive_dict.get(dm)
                mean       = positive_h
                
                if np.isnan(positive_h):
                    continue
                
                new_row = np.array([[
                    dm,
                    utils.format_float(mean),
                    "COTA UNICA"
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
                
            if dm in negative_dict:
                negative_h = negative_dict.get(dm)
                mean       = negative_h
                if np.isnan(negative_h):
                    continue
                new_row = np.array([[
                    dm,
                    utils.format_float(mean),
                    "COTA UNICA"
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
        
        num_index = np.where([utils.is_float(x) for x in full_table[:,0]])
        ordered_num_index = np.argsort(full_table[num_index][:,0].astype(float))
         
        with open(filename, "w") as f:
            np.savetxt(f,full_table[ordered_num_index],delimiter=',',fmt='%s')
    
 
    
    def plot(self, filename):
        
        pos_dm, pos_pnt = self.get_positive_table()
        neg_dm, neg_pnt = self.get_negative_table()
        
        intersection    = np.intersect1d(pos_dm, neg_dm)
        union           = np.union1d(pos_dm, neg_dm)
        
        positive_dict   = dict (zip(pos_dm,pos_pnt))
        negative_dict   = dict (zip(neg_dm,neg_pnt))
        
        full_table = np.empty((0, 2))
        
        for dm in union:
            
            if (dm == "") or (not utils.is_float(dm)):
                continue
            
            # DM's with two measurements 
            if dm in intersection:
                positive_h = positive_dict.get(dm)
                negative_h = negative_dict.get(dm)
                if np.isnan(positive_h) or np.isnan(negative_h):
                    continue
                mean = utils.round(np.mean([positive_h,negative_h]))
                new_row = np.array([[ np.round(float(dm),3), mean]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            # DM's with positive direction only
            if dm in positive_dict:
                positive_h = positive_dict.get(dm)
                if np.isnan(positive_h):
                    continue
                mean       = utils.round(positive_h)                
                new_row = np.array([[ np.round(float(dm),3), utils.round(mean) ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            # DM's with negative direction only
            if dm in negative_dict:
                negative_h = negative_dict.get(dm)
                if np.isnan(negative_h):
                    continue
                mean       = utils.round(negative_h)
                new_row = np.array([[  np.round(float(dm),3), utils.round(mean) ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
        
        num_index = np.where([utils.is_float(x) for x in full_table[:,0]])
        ordered_num_index = np.argsort(full_table[num_index][:,0].astype(float))
        
        with open(filename, "w") as f:
            cad = levelCad.LevelCad(full_table[ordered_num_index])
            cad.write(f)






def parse_circuit (circuit_matrix, height_matrix, circuit_num_matrix = None, pr_num_matrix = None):
    start = 0
    end   = 1
    
    start_points = []
    end_points   = []
    
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
           
            seg = parse_segment(circuit_matrix[start:end+1], pr0, pr1, h0, h1, num_matrix=circuit_num_matrix[start:end+1],
                                start_points = start_points, end_points=end_points)
            segment_list.append(seg)
    
    return segment_list


def parse_segment (string_matrix, pr0, pr1, h0, h1, num_matrix=None, start_points= [], end_points= [] ):
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
 
    
    return Segment(pr0, pr1, h0, h1, point_list, start_points=start_points, end_points=end_points)


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
        intermediate = im,
        str_dm = string_matrix[1:,1]
    )
    
    return point


def parser (filename1, filename2):
    
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
 
    return Circuit(positive_segments, negative_segments)
    

if __name__ == "__main__":
    f1 = sys.argv[0]
    f2 = sys.argv[1]
    cir = parser(f1,f2)
    cir.write_circuit_table("REPORT.csv")

