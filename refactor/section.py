
import numpy as np
import utils

class Section :
    def __init__ (
            self,
            km,
            matrix,
            labels,
            height,
            axis=np.array([0,0]),
            vector=np.array([0,0]),
            oriented=True   
    ):
    
        self.oriented = oriented 
        self.labels = matrix[:,4]
        self.vector = None
        self.axis = axis
        self.km = km
        self.matrix = matrix
        self.height = height
        self.distance = self.compute_distance()
        self.adjustedHeight = self.adjustHeight(self.height)
        self.id = km
        self.side = utils.parseLabelLetterArray(self.labels)
        self.coor_x = self.matrix[:,[1]]
        self.coor_y = self.matrix[:,[2]]
 
 
    def merge (self, section):
        """Merges this section with the argument section."""
        self.matrix         = np.vstack((self.matrix, section.matrix[1:]))
        self.distance       = np.concatenate((self.distance , section.distance[1:]))
        self.adjustedHeight = np.concatenate((self.adjustedHeight, section.adjustedHeight[1:]))
        self.labels         = np.concatenate((self.labels, section.labels[1:]))
        self.side           = np.concatenate((self.side, section.side[1:]))
        self.coor_x         = np.concatenate((self.coor_x, section.coor_x[1:]))
        self.coor_y         = np.concatenate((self.coor_y, section.coor_y[1:]))
        return
    
    
    
    def compute_distance (self):
        """Returns array with distances to point Zero."""
        XY   = utils.str_to_flt_arr(self.matrix[:,[1,2]])
        axis = utils.str_to_flt_arr(self.matrix[:,[1,2]][0])
        return  utils.round_float(np.sqrt( np.sum((XY - axis) ** 2, axis=1)))
    
    
    
    def adjustHeight (self, realHeight) :
        """Returns array with precise heights of the section."""
        trans_height = utils.str_to_flt(self.matrix[0][3])
        delta        = utils.str_to_flt(realHeight) - trans_height
        heights      = utils.str_to_flt_arr(self.matrix[:,3]) + delta
        return heights
    
    
    def compute_sign (self):
        if self.oriented:
            self.compute_oriented_sign()
        else:
            self.compute_descriptor_sign()

    def compute_descriptor_sign (self):
        signs  = utils.parseLabelArray(self.labels);
        self.distance = self.distance * signs
    
 
    def compute_oriented_sign (self):
        V1 = utils.str_to_flt_arr(self.matrix[:,1:3]) - utils.str_to_flt_arr(self.axis)
        V2 = utils.str_to_flt_arr(self.vector)
        
        signs = utils.compute_sign_array(V1,V2)
        self.distance = self.distance * signs
 
 
    
    ###################
    # PRIVATE METHODS #
    ###################
    def __lt__ (self,section):
        return np.float64(self.km) < np.float64(section.km)
    def __le__ (self,section):
        return np.float64(self.km) <= np.float64(section.km)
    def __eq__ (self,section):
        return self.km == section.km
    def __str__(self):
        return self.km


if __name__ == "__main__":
    print(__name__)



# class Section :
    
    
#     def __init__(self, km, matrix, labels, height, axis=np.array([0,0]), vector=np.array([0,0]), oriented=True):
        
#         self.oriented = oriented
#         self.labels = labels
#         self.axis = axis;
#         self.vector = vector;
#         self.km = km;
#         self.matrix = matrix;
#         #self.labels = labels;
#         self.height = height;
#         self.distance = self.compute_distance()
#         self.adjustedHeight = self.adjustHeight(self.height);
#         self.side = utils.parseLabelLetterArray(self.labels)[:,None];
#         self.id = km;
#         self.new = True
#         self.coor_x = self.matrix[:,[1]]
#         self.coor_y = self.matrix[:,[2]]
    
 
#     def compute_descriptor_sign (self):
#         signs  = utils.parseLabelArray(self.labels);
#         self.distance = self.distance * signs
    
 
#     def compute_oriented_sign (self):
#         signs = utils.compute_sign_array((self.matrix[:,1:3] - self.axis),  (self.vector))
#         self.distance = self.distance * signs
    
    
#     def compute_sign (self):
#         if self.oriented:
#             self.compute_oriented_sign()
#         else:
#             self.compute_descriptor_sign()
    
    
#     def getId(self) :
#         """Returns section id."""
#         return self.id
    
#     def compute_distance (self):
#         """Returns array with distances to point Zero."""
#         return  utils.round_float (
#             np.sqrt( np.sum(
#                 (self.matrix[:,[1,2]] - self.matrix[:,[1,2]][0]) ** 2, axis=1)))
    
#     def adjustHeight (self, realHeight) :
#         """Returns array with precise heights of the section."""
#         delta = realHeight - self.matrix[0][3];
#         return utils.round_float (self.matrix[:,[3]] + delta)
    
#     def merge (self, section):
#         """Merges this section with the argument section."""
#         self.matrix         = np.vstack((self.matrix, section.matrix[1:]))
#         self.distance       = np.concatenate((self.distance , section.distance[1:]))
#         self.adjustedHeight = np.concatenate((self.adjustedHeight, section.adjustedHeight[1:]))
#         self.labels         = np.concatenate((self.labels, section.labels[1:]))
#         self.side           = np.concatenate((self.side, section.side[1:]))
#         self.coor_x         = np.concatenate((self.coor_x, section.coor_x[1:]))
#         self.coor_y         = np.concatenate((self.coor_y, section.coor_y[1:]))
#         return
    
    
#     def __lt__ (self,section):
#         return np.float64(self.km) < np.float64(section.km)
#     def __le__ (self,section):
#         return np.float64(self.km) <= np.float64(section.km)
#     def __eq__ (self,section):
#         return self.km == section.km
#     def __str__(self):
#         return self.km



