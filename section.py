
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
    def __init__(self, km, matrix, labels, height):
        
        self.km = km
        
        self.matrix = matrix
        
        self.labels = labels
        
        self.signs  = utils.parseLabelArray(labels)
        
        self.height = height
        
        self.distance = self.distance() * self.signs
        
        self.adjustedHeight = self.adjustHeight(self.height)
        
        self.side = utils.parseLabelLetterArray(self.labels)[:,None]
        
        self.id = km

    def getId(self) :
        """Returns section id."""
        return self.id
    
    def distance (self):
        """Returns array with distances to point Zero."""
        return  np.sqrt(
            np.sum((self.matrix[:,[1,2]] - self.matrix[:,[1,2]][0]) ** 2, axis=1))
    
    def adjustHeight (self, realHeight) :
        """Returns array with precise heights of the section."""
        delta = realHeight - self.matrix[0][3];
        return self.matrix[:,[3]] + delta
    
    def merge (self, section):
        """Merges this section with the argument section."""
        self.matrix         = np.vstack((self.matrix, section.matrix[1:]))
        self.distance       = np.concatenate((self.distance , section.distance[1:]))
        self.adjustedHeight = np.concatenate((self.adjustedHeight, section.adjustedHeight[1:]))
        self.labels         = np.concatenate((self.labels, section.labels[1:]))
        self.side           = np.concatenate((self.side, section.side[1:]))
        return
    
 
    
    # Returns this section's matrix in the MOP format
    def widthFormat(self):
        
        minIndex = np.argmin(self.distance)
        maxIndex = np.argmax(self.distance)
        
        minDistance = self.distance[minIndex]
        maxDistance = self.distance[maxIndex]        
        
        leftLabel = 'T' if minDistance < -20.0 else ''
        rightLabel = 'T' if maxDistance > 20.0 else ''
        
        return np.array([[
            self.km,
            formatFloatArray(minDistance),
            formatFloatArray(maxDistance),
            leftLabel,
            rightLabel
        ]])
    
    
    
    def __lt__ (self,section):
        return np.float64(self.km) < np.float64(section.km)
    def __le__ (self,section):
        return np.float64(self.km) <= np.float64(section.km)
    def __eq__ (self,section):
        return self.km == section.km
    def __str__(self):
        return self.km
