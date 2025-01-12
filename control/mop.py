"""
Los campos del control de línea de tierra transversal son:
- dm               DONE
- lado             DONE
- distancia        DONE
- cota control     DONE
- cota estudio     DONE
- tipo terreno     DONE 
- tolerancia       DONE 
- diferencia       DONE
- cumple           DONE
"""

import numpy as np
import utils
import bisect
import re
import sys
from control.range import ControlRangeList

# 42  ---> demás ejes
# 108 ---> 70.0% # Eje 27

tolerance = {
    0  : 0.00,
    1  : 0.02,
    2  : 0.05,
    3  : 0.10,
    4  : 0.25,
}

class Line :
    
    def __init__(self,point1,point2):
        # PUNTOS DE PROYECTO
        self.x0 = point1.distance
        self.y0 = point1.height
        
        self.x1 = point2.distance
        self.y1 = point2.height
        # PENDIENTE DE LA RECTA
        self.slope = (self.y1-self.y0) / (self.x1-self.x0)
    
    def get_y (self,x) :
        y = np.round(self.slope * (x - self.x0) + self.y0, 3) # Redondeado
        #y = self.slope * (x - self.x0) + self.y0 # Sin redondear
        return y
    
    def contains_x (self,x) :
        return (self.x0 <= x and x <= self.x1)
    
    def __str__ (self):
        return f'x0={self.x0}  \t x1={self.x1}\ny0={self.y0}  \ty1={self.y1}'



class ControlMatrixIterator :
    def __init__(self,matrix):
        pass


class RandomMatrixIterator :
    
    def __init__ (self,matrix):
        self.matrix    = matrix
        self.index     = 0
        self.length    = len(matrix)
    
    def __iter__ (self):
        return self
    
    def __next__ (self):
        
        if self.index >= self.length :
            raise StopIteration
        
        START = 0
        END   = 0
        
        for i in range(self.index, self.length):
            
            if i == self.length-1:
                START = self.index
                END = i
                return self.matrix[START:END]
            
            if self.matrix[i][0] != self.matrix[i+1][0]:
                START = self.index
                END   = i
                self.index = i + 1
                return self.matrix[START : END]


class MopMatrixIterator :
    def __init__ (self, matrix) :
        self.matrix = matrix
        self.index  = 1
        self.length = len(matrix)
        
    
    def __iter__ (self) :
        return self
    
    def __next__ (self) :
        
        if self.index >= self.length :
            raise StopIteration
        
        START = 0
        END   = 0
        
        for i in range(self.index, self.length):
            # This is the first index of the following section
            if self.matrix[i][0] != '' or i == self.length - 1:
                START      = self.index - 1
                END        = i
                self.index = i + 1
                break
        
        return self.matrix[START:END]   

class MOPPoint :
    
    def __init__ (self, distance, height, descr):
        self.distance   = utils.str_to_flt (distance)
        self.height     = utils.str_to_flt (height)
        self.descriptor = descr
    
    def get_ground_type(self):
        match = re.search(r'\d+', self.descriptor)
        if match:
            return int(match.group())
        return 0
    
    def in_tolerance (self, delta):
        tol = tolerance.get(self.get_ground_type(), 0.000)
        if np.abs(delta) > tol :
            return False
        return True
    
    def __lt__ (self,point):
        return self.distance <  point.distance
    def __le__ (self,point):
        return self.distance <= point.distance
    def __str__(self):
        return f'd={self.distance}; h={self.height}, dscr={self.descriptor}'
        

class MOPSection:
    
    def __init__ (self, matrix):
        
        self.dm = matrix[0][0]
        self.point_list = []
        for row in matrix :
            point = MOPPoint(row[1],row[2],row[3])
            self.point_list.append(point)
        self.size = len(matrix)
        self.point_list.sort()
        
        self.__min_dist__   = min(self.point_list)
        self.__max_dist__   = max(self.point_list)
        self.__min_height__ = min(self.point_list, key=lambda point: point.height)
        self.__max_height__ = max(self.point_list, key=lambda point: point.height)
        
    def get_size(self):
        return self.size
    
    def get_min_dist (self):
        return self.__min_dist__

    def get_max_dist (self):
        return self.__max_dist__
    
    def get_min_height (self):
        return self.__min_height__
    
    def get_max_height (self):
        return self.__max_height__
    
    def get_bisection_index (self, point):
        return bisect.bisect_left(self.point_list, point)
    
    def get_neighbor_indices(self, point):
        i0 = self.get_bisection_index(point)
        if i0 == 0 or i0 == self.size:
            return None
        return (i0-1,i0)

    def get_point(self, index):
        return self.point_list[index]
    
    def __str__(self):
        print(f'SECTION: {self.dm}')
        #for p in self.point_list:
        #    print(p)
        return ''



class MOPControlPoint :
    
    def __init__ (
            self,
            dist,
            proj_height,
            ctrl_height,
            descr,
            delta_y,
            dm = "",
    ):
        
        self.distance         = dist
        self.proj_height      = proj_height 
        self.ctrl_height      = ctrl_height
        self.descriptor       = descr
        self.delta            = delta_y
        self.tolerance_weight = 10 if self.is_within_tolerance() else 0
        
        if delta_y is None:
            self.weight = 0
        elif np.abs(dist) < 0.001:
            self.weight = 0
        elif np.abs(dist) < 6.000:
            self.weight = 10 + self.tolerance_weight
        elif np.abs(dist) < 9.000:
            self.weight = 7  + self.tolerance_weight
        elif np.abs(dist) < 12.000:
            self.weight = 4  + self.tolerance_weight
        else:
            self.weight = 2  + self.tolerance_weight
    
    def __lt__ (self, point):
        return self.distance <  point.distance
    def __le__ (self, point):
        return self.distance <= point.distance
    def __str__ (self) :
        return f'Point: dist={self.distance} ; cota = {self.ctrl_height}'
    
    def get_ground_type(self):
        # Use regular expression to find the number in the string
        match = re.search(r'\d+', self.descriptor)
        if match:
            return int(match.group())
        return 0
    
    def get_tolerance (self) :
        return tolerance.get(self.get_ground_type(), 0.000)
    
    def is_within_tolerance (self) :
        ground_type = self.get_ground_type()
        tol = tolerance[ground_type]
        try:
            if np.abs(self.delta) > tol:
                return False
            return True
        except:
            return False
    
    def get_side (self) :
        if self.distance < 0 :
            return "i"
        elif self.distance > 0 :
            return "d"
        else :
            return "c"



class MOPControlSection :
    
    def __init__ (self, dm, point_list):
        self.dm         = dm
        self.point_list = point_list
    
    def select_random_points (self):
        zero_point = MOPControlPoint(0,0,0,'',0)
        index = bisect.bisect_left (self.point_list, zero_point)
        
        neg_distr = np.array([p.weight for p in self.point_list[0:index]])
        pos_distr = np.array([p.weight for p in self.point_list[index+1:]])
        
        pointsA = np.array([])
        pointsB = np.array([])
        
        for i in range(0,4):
            SAMPLE_SIZE = 3 - i
            try:
                pointsA = np.random.choice(self.point_list[0:index], size=SAMPLE_SIZE, replace=False, p=neg_distr/sum(neg_distr))
                break
            except:
                if SAMPLE_SIZE > 1:
                    continue
                else:
                    print(f'No se seleccionaron puntos negativos para dm = {self.dm}')
                    pointsA = np.array([])
        
        for i in range(0,4):
            SAMPLE_SIZE = 3-i
            try:
                pointsB = np.random.choice(self.point_list[index+1:], size=SAMPLE_SIZE, replace=False, p=pos_distr/sum(pos_distr))
                break
            except:
                if SAMPLE_SIZE > 1:
                    continue
                else:
                    print(f'No se seleccionaron puntos positivos para dm = {self.dm}')
                    pointsB = np.array([])
        
        random_points = np.sort(np.concatenate(( pointsA , pointsB )))
        #for p in random_points:
        #    print(p)
        #print(random_points)
        
        return random_points

class MOP :
    
    def __init__ (self, filename) :
        
        self.filename = filename
        self.matrix = utils.read_csv(filename)
        self.section_list = []
        self.dm_list = []
        self.dm_section = {}
        
        
        i = 0
        for sec in MopMatrixIterator(self.matrix):
            section = MOPSection(sec)
            self.dm_section[section.dm] = i
            self.dm_list.append(section.dm)
            self.section_list.append(section)
            i += 1
        self.size = len(self.section_list)
    
    
    def get_dm_list (self) :
        return self.dm_list
    
    def get_section (self,dm) :
        idx = self.dm_section.get(dm, None)
        if idx is None:
            return None
        return self.section_list[self.dm_section[dm]]
    

class MOPControl :
    
    def __init__ (self, filename_proj, filename_ctrl):
        
        self.mop_proj = MOP(filename_proj)
        self.mop_ctrl = MOP(filename_ctrl)
        
        self.project_dm_list = self.mop_proj.get_dm_list()
        self.control_dm_list = self.mop_ctrl.get_dm_list()
        self.dm_list         = np.intersect1d(self.project_dm_list,self.control_dm_list)
        
        # min_ctrl_point   = np.min(self.dm_list.astype(float))
        # max_ctrl_point   = np.max(self.dm_list.astype(float))
        # self.ctrl_length = max_ctrl_point - min_ctrl_point
        
        # min_proj_point   = np.min(self.project_dm_list.astype(float))
        # max_proj_point   = np.max(self.project_dm_list.astype(float))
        # self.proj_length = max_proj_point - min_proj_point
        
        # self.ctrl_dm_number = len(self.dm_list)
        
        self.control_section_list = []
        self.TOTAL                = 0
        self.control_matrix       = np.empty((0,9))
        #self.print_control_stats()
    
    # def print_control_stats (self):
    #     print(f"Longitud de Proyecto: {self.proj_length} m")
    #     print(f"Longitud de tramo de Control: {self.ctrl_length} m")
    #     print(f"Perfiles controlados por KM: {1000 * self.ctrl_dm_number / self.ctrl_length} perfil/km")
    
    def __control__ (self) :
        # iterate over project dm's 
        for dm in self.dm_list:
            
            proj_section = self.mop_proj.get_section(dm)
            ctrl_section = self.mop_ctrl.get_section(dm)
            proj_height  = 0
            mop_control_point_list = []            
            
            for point_ctrl in ctrl_section.point_list:
                
                pair = proj_section.get_neighbor_indices(point_ctrl)
                
                if pair is not None:
                    
                    point_proj_1 = proj_section.get_point(pair[0])
                    point_proj_2 = proj_section.get_point(pair[1])
                    line = Line(point_proj_1,point_proj_2)
                    y = line.get_y(point_ctrl.distance)
                    DELTA = np.round(y-point_ctrl.height,3)
                    proj_height = y
                    
                    new_row = np.array([
                        dm,
                        "i" if point_ctrl.distance < 0 else "d",
                        utils.format_float(point_ctrl.distance),
                        utils.format_float(point_ctrl.height),
                        utils.format_float(y),
                        str(point_ctrl.get_ground_type()),
                        utils.format_float(tolerance.get(point_ctrl.get_ground_type(),0.000)),
                        utils.format_float(DELTA),
                        "Cumple" if point_ctrl.in_tolerance(DELTA) else "No cumple"
                    ])
                    
                    self.control_matrix = np.vstack((self.control_matrix,new_row))
                else:
                    DELTA = None
                    new_row = np.array([
                        dm,
                        "i" if point_ctrl.distance < 0 else "d",                        
                        utils.format_float(point_ctrl.distance),
                        utils.format_float(point_ctrl.height),
                        "0.000",
                        str(point_ctrl.get_ground_type()),
                        str(tolerance.get(point_ctrl.get_ground_type(),0.000)),
                        "null",
                        "null",
                    ])
                    self.control_matrix = np.vstack((self.control_matrix,new_row))
                
                mop_control_point = MOPControlPoint(
                    point_ctrl.distance,
                    proj_height,
                    point_ctrl.height,
                    point_ctrl.descriptor,
                    DELTA
                )
                
                mop_control_point_list.append(mop_control_point)
           
            self.control_section_list.append(MOPControlSection(dm,mop_control_point_list))
 
 
    def write(self, outputfile=""):
        print("write full table")
        self.__control__()
        utils.write_csv(outputfile, self.control_matrix)
    
    def select_random_points(self, seed=42, outputfile=""):
        
        np.random.seed(seed)
        
        self.__control__()
        random_table = np.empty((0,9))
        TOTAL_POINTS = 0
        OK_POINTS    = 0
        for sec in self.control_section_list:
            
            rand_points = sec.select_random_points()
            
            for p in rand_points:
                
                row = np.array([
                    sec.dm,
                    p.get_side(),
                    p.distance,
                    p.ctrl_height,
                    p.proj_height,
                    p.get_ground_type(),
                    p.get_tolerance(),
                    p.delta,
                    p.is_within_tolerance()
                ])
                
                TOTAL_POINTS += 1
                OK_POINTS    = OK_POINTS + (1 if p.is_within_tolerance() else 0)
                random_table = np.vstack((random_table,row))
        
        PERCENT = np.round(100 * OK_POINTS / TOTAL_POINTS, 1)
        print(f"Porcentaje de Puntos dentro de Tolerancia: {PERCENT}%")
        utils.write_csv(outputfile, random_table)


"""
This class models the random selection of
points from the control of mop.
"""
class RandomMop :
    
    def __init__(self, matrix) :
        self.section_list = []
        for mat in RandomMatrixIterator(matrix):
            
        

class RandomMopSection :
    
    def __init__ (self) :
        self.dm = dm
        self.pos_points = []
        self.neg_points = []
        

class RandomMopPoint :
    
    def __init__ (self, distance, ctrl_height, proj_height, tipo, tol, dif) :
        self.distance     = distance
        self.ctrl_height  = ctrl_height
        self.proj_height  = proj_height
        self.tipo         = tipo
        self.tol          = tol
        self.dif          = dif


def main (input1,input2,output,option=0) :
    #mop = MOP('/home/jstvns/axis/eqc-input/control-mop/mop-proj.csv')
    # for s in mop.section_list:
    #     point = MOPPoint("2.000","238.239","x")
    #     pair = s.get_neighbor_indices(point)
    #    
    #     print("search point" , point)
    #     print("indices : " , pair)
    #     if pair is not None:
    #         print(s.get_point(pair[0]))
    #         print(s.get_point(pair[1]))
    #    
    #     input("CONTINUE")

    mop_control = MOPControl( input1, input2 )
    if option == "0" :
        mop_control.write(output)
        return 
    if option == "1" :
        mop_control.select_random_points(output)
        return

if __name__ == '__main__':
    main(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        sys.argv[4])
