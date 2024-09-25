



class PR :
    
    def __init__ (self, name, back_delta, front_delta, height=0):
     
        self.name = name;
        self.back_delta = back_delta;
        self.front_delta = front_delta;
        self.height = height
 
    def get_point_uncorrected (self) :
        return self.height
    
    def get_instr_uncorrected (self) :
        return self.height + self.back_delta;
  
    def get_back_delta (self):
        return self.back_delta;
 
    def get_front_delta (self):
        return self.front_delta;
 
    
    


class ControlPoint :
    
    def __init__ (self,
                  
                  num,
                  prev_control_point,
                  back_delta = 0.0,
                  front_delta = 0.0,
                  
                  dm_list = [],
                  inter_list = []):
        
        self.num         = num;
        
        self.dm_list     = dm_list;
        self.inter_list  = inter_list;
        
        self.back_delta  = back_delta;
        self.front_delta = front_delta;
        
        self.point_uncorrected = 0.0;
        self.instr_uncorrected = 0.0;
        
        
 
    def build (self, prev):
        """initializes point_uncorrected and instr_uncorrected
        interacting with previous control point."""
        self.point_uncorrected = prev_control_point.get_point_uncorrected()
        self.instr_uncorrected = self.point_uncorrected + self.back_delta
        
    
    def get_point_uncorrected (self):
        return self.point_uncorrected
    
    def get_instr_uncorrected (self):
        return self.instr_uncorrected
    
    def __init_point_uncorrected (self, prev_control_point):
        instr = prev_control_point.instr_uncorrected
        self.point_uncorrected = instr - self.front_delta
    




class Segment :
    
    def __init__ (self, pr0, pr1, ref_height, cplst=[]):
        
        self.pr0 = pr0;
        self.pr1 = pr1;
        
        self.control_point_list = cplst;
        
        self.diff = 0;
        
        self.point_uncorrected = pr0.get_point_uncorrected() # Last uncorrected point.
        self.ref_height = 0
 
    def __build (self):
        
        instr_uncorrected = pr0.get_instr_uncorrected()
        
        for i , cp in enumerate(self.control_point_list) :
            
            if i == 0:
                cp.build(pr0)
                instr_uncorrected = cp.get_point_uncorrected()
                continue
            
            cp.build(self.control_point_list[i-1])
            instr_uncorrected = cp.get_instr_uncorrected()
         
        
        point_uncorrected = instr_uncorrected - pr1.front_delta
        
        self.diff = ref_height - point
 
    def __correct (self):
        for cp in self.control_point_list:
            print(cp.num * self.diff)



class Circuit :
    def __init__ (self):
        pass
    


class Model :
    def __init__ (self):
        pass
