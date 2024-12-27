import numpy as np
import utils
from control.range import ControlRangeList


class Axis :
    """represents the 'eje-estaca' file"""
    def __init__ (self, filename) :
        self.filename  = filename
        self.matrix    = utils.read_csv(filename, cols=(0,1,2))
        self.dm_x      = dict(self.matrix[:,[0,1]])
        self.dm_y      = dict(self.matrix[:,[0,2]])
    
    
    def get_x(self, dm):
        """Returns the x-coordinate associated with some dm"""
        try:
            return self.dm_x[dm]
        except:
            print(f'No se encuentra el dm {dm} en el archivo {filename}')
 
 
 
    def get_y(self, dm):
            """Returns the x-coordinate associated with some dm"""
            try:
                return self.dm_y[dm]
            except:
                print(f'No se encuentra el dm {dm} en el archivo {filename}')
 
 
    def get_dm_list (self):
        return self.matrix[:,0]




class AxisControl :
    def __init__ (self, filename_proj, filename_ctrl, filename_range) :
        # Axis file models for project and control
        self.axis_proj = Axis(filename_proj)
        self.axis_ctrl = Axis(filename_ctrl)
        
        self.control_range_list = ControlRangeList(filename_range)
        
        # Project and Control dm lists
        self.project_dm_list = self.control_range_list.filter_dm_list(self.axis_proj.get_dm_list())
        self.control_dm_list = self.axis_ctrl.get_dm_list()
        
        self.tolerance = 0.05
        
        self.is_complete = True
        self.__check_completeness__()
 
 
    def __check_completeness__ (self) :
        for dm in self.project_dm_list:
            if not dm in self.control_dm_list:
                print(f'{dm} en proyecto no está en el control')
                self.is_complete = False
                

    
    def control (self) :
        output = np.empty((0,6))
        print('control')
        for dm in self.project_dm_list:
            
            x_proj = utils.str_to_flt( self.axis_proj.get_x(dm))
            y_proj = utils.str_to_flt( self.axis_proj.get_y(dm))
            
            x_ctrl = utils.str_to_flt( self.axis_ctrl.get_x(dm))
            y_ctrl = utils.str_to_flt( self.axis_ctrl.get_y(dm))
            
            delta_x = np.round (x_proj - x_ctrl , 3)
            delta_y = np.round (y_proj - y_ctrl , 3)
            
            output = np.vstack((output, np.array([x_proj, x_ctrl, y_proj, y_ctrl,delta_x,delta_y])))
            
            print(f'delta x = {delta_x}')
            print(f'delta y = {delta_y}')
            print(f'tramo   = {self.control_range_list.get_range_name(dm)}')
            
            
            
            print(f'controlando el dm {dm} de proyecto del tramo {self.control_range_list.get_range_name(dm)}')
        
        utils.write_csv('AXIS_CONTROL.CSV', output)




def main () :
    file_proj = '/home/jstvns/axis/eqc-input/control-eje-estaca/eje-estaca-proj.csv'
    file_ctrl = '/home/jstvns/axis/eqc-input/control-eje-estaca/eje-estaca-ctrl.csv'
    file_rang = '/home/jstvns/axis/eqc-input/control-eje-estaca/tramos.csv'
    
    level_control = AxisControl(file_proj,file_ctrl,file_rang)
    level_control.control()
    

if __name__ == '__main__':
    print('2')
    main()
