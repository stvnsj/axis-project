import numpy as np



class CadScript:
    
    def __init__ (self, model):
        
        self.stackLength = 8
        self.heightDelta = 30
        self.baseLine = 900
        self.currStackElement = 0
        
        self.y0 = 900
        self.x0 = 900
        
        self.currX = self.x0
        self.currY = self.y0


    def printScript (self, i=0, j=0):
        pass
    
    
    def formatSection (self, section):
        # distance of left-most point
        minDist = np.min(section.distance)
        # distance of right-most point
        maxDist = np.max(section.distance)
        # Total width of the cross section
        distRange = maxDist - minDist
        # Lowest height of the section
        minHeight = np.min(section.adjustedHeight)
        # height to be subtracted from every height
        h0 = minHeight - self.heightDelta
        # index list of sorted distances
        distanceIndex = np.argsort(section.distance)
        
        section.distance[:] = section.distance[distanceIndex]
        section.adjustedHeight[:] = section.adjustedHeight[distanceIndex]
        
        yArray = self.baseLine - (section.adjustedHeight - h0)
        xArray = np.round(self.distance - minDistance, 3)[:,None] + cadStack.xPointer
        
        self.currStackElement += 1
        
        if self.currStackElement == self.stackLength :
            self.currStackElement = 0
            self.currX = self.x0
        else:
            self.currX += distRange + 50
            
        return xArray + "," + yArray
