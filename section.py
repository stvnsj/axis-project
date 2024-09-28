
import numpy as np
import utils 



    ##########################################################################
    # The following matrices should be attributes of                         #
    # a section out of the constructor. No method should                     #
    # have to be called to set them up, because these tables                 #
    # must be stacked together when sections are merged                      #
    #                                                                        #
    # - MATRIX : This matrix contains (KM; X; Y)  ==DONE==                   #
    #                                                                        #
    # - SIGNED DISTANCE : this contains the distances from each              #
    #   point to the center of the section.  ==DONE==                        #
    #                                                                        #
    # - ADJUSTED HEIGHTS : This contains the corrected height of each point. #
    #   ==DONE==                                                             #
    #                                                                        #
    # - LABELS : This field contains a ground descriptor with                #
    #   a letter indicating the orientation. ==DONE==                        #
    #                                                                        #
    # - SIDE : Can be 'l' or 'r' depending on the side of the axis           #
    #   the point is on  ==DONE==                                            #
    ##########################################################################
 
class Section :
    # km: This is a string representation of the km of the cross section.
    # matrix: numpy array with rows `km, x, y, z, label`
    # labels: These are the labels from row 4 of matrix
    # height: this is the precise measurement of the profile height.
    def __init__(self, km, matrix, labels, height, axis=np.array([0,0]), vector=np.array([0,0]), oriented=True):
        
        self.oriented = oriented
        self.labels = labels
        self.axis = axis;
        self.vector = vector;
        self.km = km;
        self.matrix = matrix;
        self.labels = labels;
        self.height = height;
        self.distance = self.compute_distance()
        self.adjustedHeight = self.adjustHeight(self.height);
        self.side = utils.parseLabelLetterArray(self.labels)[:,None];
        self.id = km;
 
    def compute_descriptor_sign (self):
        signs  = utils.parseLabelArray(self.labels);
        self.distance = self.distance * signs
 
    def compute_oriented_sign (self):
        signs = utils.compute_sign_array((self.matrix[:,1:3] - self.axis),  (self.vector))
        self.distance = self.distance * signs

    
    def compute_sign (self):
        if self.oriented:
            self.compute_oriented_sign()
        else:
            self.compute_descriptor_sign()
        
    
    def getId(self) :
        """Returns section id."""
        return self.id
    
    def compute_distance (self):
        """Returns array with distances to point Zero."""
        return  utils.round_float (
            np.sqrt( np.sum(
                (self.matrix[:,[1,2]] - self.matrix[:,[1,2]][0]) ** 2, axis=1)))
    
    def adjustHeight (self, realHeight) :
        """Returns array with precise heights of the section."""
        delta = realHeight - self.matrix[0][3];
        return utils.round_float (self.matrix[:,[3]] + delta)
    
    def merge (self, section):
        """Merges this section with the argument section."""
        self.matrix         = np.vstack((self.matrix, section.matrix[1:]))
        self.distance       = np.concatenate((self.distance , section.distance[1:]))
        self.adjustedHeight = np.concatenate((self.adjustedHeight, section.adjustedHeight[1:]))
        self.labels         = np.concatenate((self.labels, section.labels[1:]))
        self.side           = np.concatenate((self.side, section.side[1:]))
        return
    
    
    def __lt__ (self,section):
        return np.float64(self.km) < np.float64(section.km)
    def __le__ (self,section):
        return np.float64(self.km) <= np.float64(section.km)
    def __eq__ (self,section):
        return self.km == section.km
    def __str__(self):
        return self.km
