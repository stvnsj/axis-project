



class PR :
    
    def __init__ (self, name, back_delta, front_delta):
     
        self.name = name;
        self.back_delta = back_delta;
        self.front_delta = front_delta;
   
  
    def get_back_delta (self):
        return self.back_delta;
 
    
    def get_front_delta (self):
        return self.front_delta;
    
    


class ControlPoint :
    
    def __init__ (self,
                  num,
                  dm_list,
                  inter_list,
                  first):
     
        self.first       = True
        self.num         = num
        self.dm_list     = []
        
        self.back_delta  = 0.0
        self.front_delta = 0.0
    
    def get_instr_uncorrected (self, prev_control_point):
        point = self.get_point_uncorrected(prev_control_point);
        return point + self.back_delta
 
    def get_point_uncorrected (self, prev_control_point):
        instr = prev_control_point.get_instr_uncorrected()
        return instr - self.front_delta
    




class Segment :
    def __init__ (self):
        
        pass
        



class Circuit :
    def __init__ (self):
        pass
    
