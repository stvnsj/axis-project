"""
Fields to be included in the control table:
- dm
- Norte (Proyecto)
- Este  (Proyecto)
- Norte (Control)
- Este  (Control)
- Diferencia
- Cumple
"""




import numpy as np
import utils
import sys
from control.range import ControlRangeList

TOLERANCE = 0.10

class Axis :
    """represents the 'eje-estaca' file"""
    def __init__ (self, filename) :
        self.filename  = filename
        self.matrix    = utils.read_csv(filename, cols=(0,1,2))
        # self.dm_coor   = {row[0]: (utils.str_to_flt(row[1]),utils.str_to_flt(row[2])) for row in self.matrix}
        self.dm_coor   = {row[0]: (row[1],row[2]) for row in self.matrix}
 
    def get_dm_list (self):
        return self.matrix[:,0]
    
    def get_coor (self, dm) :
        return self.dm_coor.get(dm)




class AxisControl :
    
    def __init__ (self, filename_proj, filename_ctrl) :
        # Axis file models for project and control
        self.axis_proj = Axis(filename_proj)
        self.axis_ctrl = Axis(filename_ctrl)
        
        
        
        # Project and Control dm lists
        self.project_dm_list = self.axis_proj.get_dm_list()
        self.control_dm_list = self.axis_ctrl.get_dm_list()
        self.dm_list         = np.intersect1d(self.project_dm_list,self.control_dm_list)
        self.tolerance       = 0.10
 
    def control (self,output_filename) :
        output = np.empty((0,7))
        for dm in self.dm_list:
            
            xp , yp  = self.axis_proj.get_coor(dm)
            xc , yc  = self.axis_ctrl.get_coor(dm)
            delta    = utils.euc_dist(
                utils.str_to_flt (xp),
                utils.str_to_flt (yp),
                utils.str_to_flt (xc),
                utils.str_to_flt (yc),
            )
            
            row = np.array([
                dm,
                xp,
                yp,
                xc,
                yc,
                utils.format_float(delta),
                "Cumple" if delta <= TOLERANCE else "No Cumple"
            ])
            
            output = np.vstack((output, row))
        
        utils.write_csv(output_filename, output)




def main (input1, input2, output) :
    
    file_proj = input1
    file_ctrl = input2
    
    level_control = AxisControl(file_proj,file_ctrl)
    level_control.control(output)

if __name__ == '__main__':
    
    main(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
    )
