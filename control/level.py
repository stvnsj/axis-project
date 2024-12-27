import numpy as np
import utils
from control.range import ControlRangeList


class Longitudinal:
    """Represents the longitudinal file || dm | cota || """
    def __init__ (self, filename):
        self.filename = filename
        self.matrix = utils.read_csv(filename)
        self.dm_height = dict(self.matrix)
        
    def get_height(self, dm):
        """Returns the height associated with some dm"""
        try:
            return self.dm_height[dm]
        except:
            print(f'No se encuentra el dm {dm} en el archivo {filename}')
    
    def get_dm_list (self) :
        return self.matrix[:,0]
    
    def get_height_list (self) :
        return self.matrix[:,1]


class LevelControl:
    """It compares the project and control longitudinal files"""
    
    def __init__ (self,filename_proj, filename_ctrl, filename_range):
        
        #longitudinal file models for project and control
        self.longitudinal_proj = Longitudinal(filename_proj)
        self.longitudinal_ctrl = Longitudinal(filename_ctrl)
        
        # Control scheme
        self.control_range_list = ControlRangeList(filename_range)
        
        # Project and Control dm lists
        self.project_dm_list = self.control_range_list.filter_dm_list(self.longitudinal_proj.get_dm_list())
        self.control_dm_list = self.longitudinal_ctrl.get_dm_list()
        
        self.is_complete = True
        self.__check_completeness__()
        
    
    def __check_completeness__ (self) :
        for dm in self.project_dm_list:
            if not dm in self.control_dm_list:
                print(f'{dm} en proyecto no está en el control')
                self.is_complete = False
    
    def control (self) :
        for dm in self.project_dm_list:
            dm_proj = utils.str_to_flt( self.longitudinal_proj.get_height(dm))
            dm_ctrl = utils.str_to_flt( self.longitudinal_ctrl.get_height(dm))
            
            delta = dm_proj - dm_ctrl
            print("dm project : " , dm_proj)
            print("dm control : " , dm_ctrl)
            print("difference : " , delta)
            print(f'controlando el dm {dm} de proyecto del tramo {self.control_range_list.get_range_name(dm)}')


def main () :
    
    file_proj = '/home/jstvns/axis/eqc-input/control-level/longi-proj.csv'
    file_ctrl = '/home/jstvns/axis/eqc-input/control-level/longi-ctrl-complete.csv'
    file_rang = '/home/jstvns/axis/eqc-input/control-level/tramos.csv'
    
    level_control = LevelControl(file_proj,file_ctrl,file_rang)
    level_control.control()
    


if __name__ == '__main__' :
    main()
