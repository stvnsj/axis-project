
import numpy as np
import utils 


class Section :
    
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
    
    def __init__(self, km, matrix, labels, height):
        self.km = km
        self.matrix = matrix
        self.labels = labels
        self.signs  = utils.parseLabelArray(labels)
        self.height = height
        self.distance = self.distance() * self.signs
        self.adjustedHeight = self.adjustHeight(self.height)
        self.side = utils.parseLabelLetterArray(self.labels)[:,None]
        self.xOffset = 900
        self.baseLevel = 20 # 20 meters below the lowest height
        self.stackElements = 10
        self.currStackElement = 0
        self.id = km
        self.heightDelta = 30

    def getId(self) :
        return self.id
        
 
    # Computes the distance (from the center point)
    # of each point in the section
    def distance (self):
        return  np.sqrt(np.sum((self.matrix[:,[1,2]] - self.matrix[:,[1,2]][0]) ** 2, axis=1))
    
    # Returns the matrix of adjusted heights. 
    def adjustHeight (self, height) :
        # Precise height - Height of center point
        delta = height - self.matrix[0][3];
        return self.matrix[:,[3]] + delta
    
    # Merges this section with the argument section
    def merge (self, section):
        self.matrix   = np.vstack((self.matrix, section.matrix[1:]))
        self.distance = np.concatenate((self.distance , section.distance[1:]))
        self.adjustedHeight = np.concatenate((self.adjustedHeight, section.adjustedHeight[1:]))
        self.labels = np.concatenate((self.labels, section.labels[1:]))
        self.side = np.concatenate((self.side, section.side[1:]))
        return

    def cadFormat (self,cadStack) :
        
        minDistance  = np.min(self.distance)
        maxDistance  = np.max(self.distance)
        distanceRange = maxDistance - minDistance
        
        minHeight = np.min(self.height)
        h0 = minHeight - self.heightDelta

        
        distanceIndex = np.argsort(self.distance)

        self.distance[:] = self.distance[distanceIndex]
        self.adjustedHeight[:] = self.adjustedHeight[distanceIndex]

        
        cadHeights   = cadStack.baseLine - (self.adjustedHeight - h0)

        
        cadDistance  = np.round(self.distance - minDistance, 3)[:,None] + cadStack.xPointer

        cadStack.currStackElement += 1
        
        if cadStack.currStackElement == cadStack.stackLength :
            cadStack.currStackElement = 0
            cadStack.xPointer = cadStack.xMargin
            cadStack.baseLine += cadStack.yOffset
        else:
            cadStack.xPointer += maxDistance - minDistance + 50
            
        return formatCadFloatArray(cadDistance) + "," + formatCadFloatArray(cadHeights)
    
    
    # Returns this section's matrix in the MOP format
    def mopFormat(self):
        
        # Index vector ordering the section points
        ascendingIndex = np.argsort(self.distance[1:])
        
        # Ordered distance
        self.distance[1:] = self.distance[1:][ascendingIndex]
        
        # Index vector reversing the order of the negative part
        descendingIndex = np.argsort(np.where(self.distance[1:]<0)[0])[::-1]
        
        # Index of the last negative number 
        N = len(descendingIndex)
        
        # reversed ordered on negative part of distance
        self.distance[1:N+1] = self.distance[1:][descendingIndex]
        
        
        self.adjustedHeight[1:] = self.adjustedHeight[1:][ascendingIndex]
        self.adjustedHeight[1:N+1] = self.adjustedHeight[1:][descendingIndex]
        
        self.labels[1:] = self.labels[1:][ascendingIndex]
        self.labels[1:N+1] = self.labels[1:][descendingIndex]
        
        self.labels[0] = '0ep'
        
        self.side[1:] = self.side[1:][ascendingIndex]
        self.side[1:N+1] = self.side[1:][descendingIndex]
        
        
        return np.hstack((                
            np.where(np.isnan(self.matrix[:,[0]]), '' , self.matrix[:,[0]].astype(str) ),
            formatFloatArray (self.distance[:,None]),
            formatFloatArray (self.adjustedHeight),
            self.labels[:,None],
            self.side))





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
        return self.km <= section.km
    def __eq__ (self,section):
        return self.km == section.km
    def __str__(self):
        return self.km

