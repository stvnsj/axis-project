"""

Brief description:
This module has functions that take a file a return a smaller randomly altered
file for control comparison purposes.

Detailed Description:

"""
import numpy as np
import utils
from control.range import ControlRangeList
from control.mop   import MopMatrixIterator



def random_sign ():
    choice = np.random.choice([1,-1], size=1, p=[0.5,0.5])
    return choice[0]

def binary_choice ():
    choice = np.random.choice([True,False], size=1, p=[0.5,0.5])
    return choice[0]

def choose_random_atom (choices, weights) :
    choice  = np.random.choice(choices, size=1, replace=True, p=weights)
    return choice[0]

def choose_random_array (choices, weights=None, size=1) :
    if weights is None:
        weights = [x for x in []]
    choices  = np.random.choice(choices, size=size, replace=True, p=weights)
    return np.array(choices)



def mop_ctrl_file (mop_file, ranges_file, output_proj_file, output_ctrl_file) :
    """Returns a randomly modified version of the provided eje-estaca file."""
    
    matrix = utils.read_csv(mop_file)

    proj_matrix = np.empty((0,4))
    ctrl_matrix = np.empty((0,4))

    # List of dm indices
    mask   = matrix[:,0] != ''
    
    # List of dm's to be controlled
    control_dm_list = ControlRangeList(ranges_file).filter_dm_list(matrix[mask,0])
    
    for section in MopMatrixIterator(matrix):
        section_dm = section[0][0]
        
        if not (section_dm in control_dm_list):
            proj_matrix = np.vstack((proj_matrix, section))
            continue
        
        
        proj_matrix = np.vstack((proj_matrix, section[0]))
        ctrl_matrix = np.vstack((ctrl_matrix, section[0]))
        
        for row in section[1:]:
            if binary_choice() :
                proj_matrix = np.vstack((proj_matrix, row))
            else:
                ctrl_matrix = np.vstack((ctrl_matrix, row)) 
 
    utils.write_csv(output_proj_file, proj_matrix)
    utils.write_csv(output_ctrl_file, ctrl_matrix)



# filename is the name of a subset of eje-estaca filename.
def main (filename, output_filename) :
    """Returns a randomly modified version of the provided eje-estaca file."""
    
    # filename = '/home/jstvns/axis/eqc-input/control-eje-estaca/eje-estaca-proj-sub.csv'
    matrix   = utils.read_csv(filename)
    N = len(matrix)
    
    choices = [0.000 , 0.010, 0.020, 0.030, 0.040, 0.050, 0.060, ]
    weights = [0.100 , 0.200, 0.200, 0.200, 0.100, 0.100, 0.100, ]
    
    delta_x = choose_random_array(choices,weights,N)
    delta_y = choose_random_array(choices,weights,N)
    
    x = matrix[:,1].astype(float) + delta_x
    y = matrix[:,2].astype(float) + delta_y
    
    matrix[:,1] = utils.format_float_array (x)
    matrix[:,2] = utils.format_float_array (y)    
    
    utils.write_csv(output_filename, matrix)




def main1 (filename, output_filename) :
    """Returns a randomly modified version of the provided longitudinal file."""
    # filename = '/home/jstvns/axis/eqc-input/control-level/longi-proj-sub.csv'
    matrix   = utils.read_csv(filename)
    N = len(matrix)
    choices = [0.000 , 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, ]
    weights = [0.100 , 0.200, 0.200, 0.200, 0.100, 0.100, 0.100, ]
    arr = choose_random_array(choices,weights,N)
    matrix[:,1] = utils.format_float_array(matrix[:,1].astype(float) + arr)
    utils.write_csv(output_filename, matrix)


if __name__ == '__main__':
    mop_ctrl_file(
        "/home/jstvns/axis/eqc-input/control-mop/mop.csv",
        "/home/jstvns/axis/eqc-input/control-mop/tramos.csv",
        "/home/jstvns/axis/eqc-input/control-mop/mop-proj.csv",
        "/home/jstvns/axis/eqc-input/control-mop/mop-ctrl.csv"
    )
