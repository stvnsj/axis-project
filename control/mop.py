
import numpy as np
import utils
import bisect

from control.range import ControlRangeList

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


class MopMatrixIterator :
    def __init__ (self, matrix) :
        self.matrix = matrix
        self.index  = 1
        self.length = len(matrix)
        
    
    def __iter__ (self) :
        return self
    
    def __next__ (self) :
        
        if self.index == self.length :
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
    
    def __init__ (self, dist, height, descr, delta_y):
        
        self.distance   = dist
        self.height     = height
        self.descriptor = descr
        self.delta      = delta_y
        
        if delta_y is None:
            self.weight = 0
        elif np.abs(dist) < 0.001:
            self.weight = 0
        elif np.abs(dist) < 6.000:
            self.weight = 10
        elif np.abs(dist) < 9.000:
            self.weight = 7
        elif np.abs(dist) < 12.000:
            self.weight = 4
        else:
            self.weight = 2
            
    def __lt__ (self, point):
        return self.distance <  point.distance
    def __le__ (self, point):
        return self.distance <= point.distance
    def __str__ (self) :
        return f'POINT d={self.distance} {type(self.distance)}'



class MOPControlSection :
    
    def __init__ (self, dm, point_list):
        self.dm         = dm
        self.point_list = point_list
    
    def select_random_points (self):
        zero_point = MOPControlPoint(0,0,'',0)
        index = bisect.bisect_left (self.point_list, zero_point)
        
        neg_distr = np.array([p.weight for p in self.point_list[0:index]])
        pos_distr = np.array([p.weight for p in self.point_list[index+1:]])
        
        try:
            pointsA = np.random.choice(self.point_list[0:index],  size=3, replace=False, p=neg_distr/sum(neg_distr))
        except:
            pointsA = np.array([])
            print(f"No se pueden seleccionar 3 puntos negativos de DM {self.dm} !")
        
        try:
            pointsB = np.random.choice(self.point_list[index+1:], size=3, replace=False, p=pos_distr/sum(pos_distr))
        except:
            pointsB = np.array([])
            print(f"No se pueden seleccionar 3 puntos positivos de DM {self.dm} !")
        
        random_points = np.sort(np.concatenate(( pointsA , pointsB )))
        for p in random_points:
            print(p)
        input("NEXT SAMPLE\n")
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
    
    def __init__ (self, filename_proj, filename_ctrl, filename_range):
        
        self.mop_proj = MOP(filename_proj)
        self.mop_ctrl = MOP(filename_ctrl)
        
        self.control_range_list = ControlRangeList(filename_range)
        
        self.project_dm_list = self.control_range_list.filter_dm_list(self.mop_proj.get_dm_list())
        self.control_dm_list = self.mop_ctrl.get_dm_list()
        
        self.is_complete = True
        self.__check_completeness__()
        
        self.control_section_list = []
        
        self.control_matrix = np.empty((0,4))
        #self.__control__()
    
    def __check_completeness__ (self) :
        for dm in self.project_dm_list:
            if not dm in self.control_dm_list:
                print(f'{dm} en proyecto no está en el control')
                self.is_complete = False
    
    def __control__ (self) :
        # iterate over project dm's 
        for dm in self.project_dm_list:
            if dm not in self.control_dm_list:
                continue
            
            proj_section = self.mop_proj.get_section(dm)
            ctrl_section = self.mop_ctrl.get_section(dm)
            mop_control_point_list = []            
            
            for point_ctrl in ctrl_section.point_list:
                
                pair = proj_section.get_neighbor_indices(point_ctrl)
                
                if pair is not None:
                    
                    point_proj_1 = proj_section.get_point(pair[0])
                    point_proj_2 = proj_section.get_point(pair[1])
                    line = Line(point_proj_1,point_proj_2)
                    y = line.get_y(point_ctrl.distance)
                    DELTA = np.round(y-point_ctrl.height,3)
                    
                    new_row = np.array([
                        dm,
                        utils.format_float(point_ctrl.distance),
                        utils.format_float(point_ctrl.height),
                        utils.format_float(point_ctrl.height - y)
                    ])
                    
                    self.control_matrix = np.vstack((self.control_matrix,new_row))
                else:
                    DELTA = None
                    new_row = np.array([
                        dm,
                        utils.format_float(point_ctrl.distance),
                        utils.format_float(point_ctrl.height),
                        "null"
                    ])
                    self.control_matrix = np.vstack((self.control_matrix,new_row))
                
                mop_control_point = MOPControlPoint(
                    point_ctrl.distance,
                    point_ctrl.height,
                    point_ctrl.descriptor,
                    DELTA
                )
                
                mop_control_point_list.append(mop_control_point)
                
            self.control_section_list.append(MOPControlSection(dm,mop_control_point_list))
 
 
    def write(self):
        self.__control__()
        utils.write_csv('/home/jstvns/axis/eqc-input/control-mop/control.csv', self.control_matrix)
        
        
    def select_random_points(self):
        self.__control__()
        for sec in self.control_section_list:
            sec.select_random_points()
        

def main () :
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
    
    mop_control = MOPControl(
        '/home/jstvns/axis/eqc-input/control-mop/mop-proj.csv',
        '/home/jstvns/axis/eqc-input/control-mop/mop-ctrl.csv',
        '/home/jstvns/axis/eqc-input/control-mop/tramos.csv'
    )
 
    #mop_control.write()
    mop_control.select_random_points()

if __name__ == '__main__':
    main()
