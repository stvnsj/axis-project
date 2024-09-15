import numpy as np
import utils
import model as mdl


#############################################################
# I must have a box structure to enclose a stack element.   #
# What are the elements of a box ??                         #
#                                                           #
# y0 : bottom line                                          #
# x0 : top line                                             #
#                                                           #
# elements of a stack element are introduced in a bottom-   #
# top direction, subtrracting subtracting certain offset.   #
#                                                           #
#############################################################
class StackElement:
    
    def __init__(self,section,f,x=900,y=900):
        
        self.f = f
        
        # Left border of the box
        self.x0 = x;
        
        # Bottom border of the box
        self.y0 = y;
        
        # Cross section to be drawn
        self.section = section
        
        # Lowest and greastet relative distances.
        self.minDist = np.min(section.distance);
        self.maxDist = np.max(section.distance);
        
        # Distance between left and right extremes of the
        # cross section.
        self.distRange = self.maxDist - self.minDist;
        
        # horizontal excess
        self.excess = 2.0
        
        # Length of horizontal structural lines.
        self.structLineLength = self.distRange + 2 * self.excess;
        
        # Minimum height of section
        self.minHeight = np.min(section.adjustedHeight);
        self.heightDelta = 10;
        self.h0 = self.minHeight - self.heightDelta;
        
        
        # This list indexes the distance array, so that
        # the order goes from negative to positive, e.g.:
        # -17.1, ... , 0 , +15.24
        self.indexList = np.argsort(section.distance);
        
        
        
        ##############
        # BOX LAYOUT #
        ##############
        
        # Y Coordinates
        self.y_km = 0.5 + self.y0;
        self.y_distUnderline = 2.0 + self.y_km;
        self.y_distNum = 0.5 + self.y_distUnderline; 
        self.y_heightUnderline = 3.6 + self.y_distNum;
        self.y_heightNum = 0.5 + self.y_heightUnderline;
        self.y_figure = 3.6 + self.y_heightNum;
        self.y_refline = 0.2 * self.heightDelta + self.y_figure;
        
        # X Coordinates
        self.x_refline    = 0.5 + self.x0;
        self.x_structLine = 8.0 + self.x_refline;
        self.x_figure     = self.excess + self.x_structLine;
        self.x_num        = self.x_figure
        self.x_km         = 0.5 * self.structLineLength + self.x_structLine;
        self.x_labelText  = 7.0 + self.x0;
        
        self.x1 = self.x_structLine + self.structLineLength + 10
    
    
    def groundLine (self, f):
        distance = utils.formatFloatArray(self.section.distance[self.indexList] - self.minDist + self.x_figure);
        height   = utils.formatFloatArray(self.y_figure + (self.section.adjustedHeight[self.indexList] - self.h0));
        content = (distance + "," +height[:,0])[:,None]
        f.write("\n")
        f.write("PLINE")
        f.write("\n")
        np.savetxt(f, content ,fmt='%s')
        self.f.write("\n\n")
    
    def heightLine (self, f):
        distance = utils.formatFloatArray(self.section.distance[self.indexList] - self.minDist + self.x_figure);
        height   = utils.formatFloatArray(self.y_figure + (self.section.adjustedHeight[self.indexList] - self.h0));        
        content = ("LINE " + distance + "," + f'{self.y_figure} ' + distance + "," + height[:,0] + "\n")[:,None]
        np.savetxt(self.f, content ,fmt='%s')
    
    def structLine (self,f):
        
        x1 = utils.formatFloatArray( np.array([
            self.x_structLine,
            self.x_structLine,
            self.x_structLine,
            self.x_figure + np.absolute(self.minDist),
        ]))
        
        x2 = utils.formatFloatArray(np.array([
            self.x_structLine + self.structLineLength,
            self.x_structLine + self.structLineLength,
            self.x_structLine + self.structLineLength,
            self.x_figure + np.absolute(self.minDist),
        ]))
        
        y1 = utils.formatFloatArray(np.array([
            self.y_distUnderline,
            self.y_heightUnderline,
            self.y_refline,
            self.y_refline,
        ]))
        
        y2 = utils.formatFloatArray(np.array([
            self.y_distUnderline,
            self.y_heightUnderline,
            self.y_refline,
            self.y_refline + 20,
        ]))
        
        content = ("LINE " + x1 + "," +  y1 + " " + x2 + "," + y2 + "\n")[:,None]
        np.savetxt(self.f, content ,fmt='%s')
    
    
    def distNum (self,f):
        distance = utils.formatFloatArray(self.section.distance[self.indexList] - self.minDist + self.x_figure);
        labels   = utils.formatFloatArray(self.section.distance[self.indexList])
        content = "-TEXT M " + distance + "," + utils.formatFloat(self.y_distNum) + " 0.50 90 " + "\"" + labels + "\""
        np.savetxt(self.f, content ,fmt='%s')
        
    
    def heightNum (self,f):
        distance = utils.formatFloatArray(self.section.distance[self.indexList] - self.minDist + self.x_figure);
        labels   = utils.formatFloatArray(self.section.adjustedHeight[self.indexList])[:,0]
        content  = ("-TEXT M " + distance + "," + utils.formatFloat(self.y_heightNum) + " 0.50 90 " + "\"" + labels + "\"")
        np.savetxt(self.f, content ,fmt='%s')
    
    def heightRef (self,f):
        x = utils.formatFloat(self.x_refline)
        y = utils.formatFloat(self.y_refline)
        d = utils.formatFloat(self.h0)
        self.f.write(f'-TEXT M {x},{y} 0.45 0 \"Ref: {d}\"')
    
    def kmLabel (self,f):
        x = utils.formatFloat(self.x_km)
        y = utils.formatFloat(self.y_km)
        self.f.write(f'-TEXT M {x},{y} 0.85 0 \"DM: {self.section.id}\"')
        
    def distLabel (self,f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_distNum)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 \"DIST.\"')
        
    def heightLabel (self, f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_heightNum)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 \"COTA\"')
        
        
    def write (self):
        
        self.groundLine(self.f)
        self.f.write("\n\n")
        
        self.heightLine(self.f)
        self.f.write("\n\n")
        
        self.structLine(self.f)
        self.f.write("\n\n")
        
        self.distNum(self.f)
        self.f.write("\n\n")
        
        self.heightNum(self.f)
        self.f.write("\n\n")
        
        self.heightRef(self.f)
        self.f.write("\n")
        self.kmLabel(self.f)
        self.f.write("\n")
        self.distLabel(self.f)
        self.f.write("\n")
        self.heightLabel(self.f)
        self.f.write("\n\n")
        
        return self.x1



class Stack:
    
    def __init__(self, model, y):
        
        self.x0 = 0;
        self.y0 = y;
        self.currX = self.x0
        self.km0 = ""
        self.km1 = ""
        self.model = model
        
    def write (self, f, i , j):
        
        if i >= self.model.size:
            return ""
        
        self.km0 = self.model.getSection(i).id;
        
        iterator = mdl.ModelIterator(self.model,i,j)
            
        self.currX += 10;
        
        for section in iterator:
            stackElement = StackElement(section, f, x=self.currX, y=self.y0)
            print(section.id)
            self.km1 = section.id
            self.currX = stackElement.write()
        
        f.write(f'-TEXT ML {self.x0},{self.y0+4} 2.50 0 \"PT Desde M: {self.km0}\"\n')
        f.write(f'-TEXT ML {self.x0},{self.y0} 2.50 0 \"   Hasta M: {self.km1}\"\n\n')
        
        self.y0 -= 120;
        
        return self.y0




class CadScript:
    
    def __init__ (self, model):
        self.model = model;
        self.stackSize = 2;
        
    
    def write (self, i , j , filename="test.txt"):
        
        y0 = 0.0
        
        with open(filename, "w") as f:
            
            while True:
                
                if  i + self.stackSize - 1 < j :
                    stack = Stack(self.model, y0)
                    y0 = stack.write(f, i, i + self.stackSize - 1)
                    i += self.stackSize;
                else:
                    stack = Stack(self.model, y0)
                    stack.write(f, i, j)
                    break

