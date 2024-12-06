import numpy as np
from .section import Section
import utils
import sys
import os




class Model :
    def __init__ (
            self,
            filename1 = "", # Descriptor File
            filename2 = "", # Coordinate File
            filename3 = "", # Longitudinal File
    ):
        
        
        
        
        matrix_descr  = utils.read_csv("/home/jstvns/eqc-input/dbase-input/dat-et-descr.csv")
        matrix_coor   = utils.read_csv("/home/jstvns/eqc-input/dbase-input/dat-et-coord.csv")
        matrix_height = utils.read_csv("/home/jstvns/eqc-input/dbase-input/longitudinal.csv")
        
        
        
        #######################
        # PRINT FILE MESSAGES #
        #######################
        if (filename1 == "") and (filename2 == "") :
            print(">> Error: Se ha cargado ningún archivo transversal")
            return
        if (filename3 == "") :
            print(">> Advertencia: No se ha cargado un archivo longitudinal")
        
        
        
        
        # This dictionary contains the precise height of the DM in the project.
        self.heights = dict(matrix_height) if filename3 else {}
        
        # list of cross sections of this model
        self.sections = []
        self.sectionIndex = []
        
        # oriented cross sections are build and oriented
        if matrix_coor is not None:
            self.build_oriented(matrix_coor)
            self.sections.sort()
            self.reference_vector()
        
        if matrix_descr is not None:
            self.build_descriptor(matrix_descr)
            
        self.distance_sign()
        self.sections.sort()
        self.deduplicate()
        self.currSection = 0
        self.size = len(self.sectionIndex)
    
    def deduplicate (self) :
        i = 0
        j = 1
        length = len(self.sections)
        self.sectionIndex.append(i)
        while j < length :
            if self.sections[i] == self.sections[j]:
                self.sections[i].merge(self.sections[j])
                j = j + 1
            else:
                i = j
                j = j + 1
                self.sectionIndex.append(i)
    
 
    def reference_vector(self):
        N = len(self.sections)
        for i in range(0,N):
            for d in range (1,N):
                if i + d < N :
                    if self.sections[i+d].km != self.sections[i].km:
                        axis1 = utils.str_to_flt_arr(self.sections[i].axis)
                        axis2 = utils.str_to_flt_arr(self.sections[i+d].axis)
                        self.sections[i].vector = axis2 - axis1
                        break
                if i - d >= 0:
                    if self.sections[i-d].km != self.sections[i].km:
                        axis1 = utils.str_to_flt_arr(self.sections[i].axis)
                        axis0 = utils.str_to_flt_arr(self.sections[i-d].axis)
                        self.sections[i].vector = axis1 - axis0
                        break
    
    def get_size(self):
        """Returns the number of non-duplicate cross sections in the model"""
        return len(self.sectionIndex)
    
    def distance_sign (self):
        "Compute the signs of the model's sections"
        for sec in self.sections:
            sec.compute_sign()
    
    def getSection(self,index):
        "Get a section by its index number"
        i = self.sectionIndex[index]
        return self.sections[i]
    
    
    
    def build_descriptor (self,matrix):
        
        start = 0 # start index of matrix chunk copied
        end = 0 # end index of matrix chunk copied
        i = 1 # pointer to traverse the matrix 
        length = matrix.shape[0] # vertical size of matrix
        
        while i < length :
            
            # If the value of km is nan, then keep stacking more
            # points to the current section
            if matrix[i][0] == "" :
                end = end + 1;
                i   = i + 1
                
                if(i == length):
                    
                    height = matrix[start][3]
                    
                    section = Section(
                        matrix[start][0],
                        matrix[start:end+1],
                        matrix[start:end+1,4],
                        height,
                        axis = matrix[start,1:3],
                        oriented = False
                    )
                    
                    self.sections.append(section)
            
            
            elif matrix[i][0] != "" :
                
                end = end + 1;
                height = matrix[start][3]
                section = Section(
                    matrix[start][0],
                    matrix[start:end],
                    matrix[start:end,4],
                    height,
                    axis = matrix[start, 1:3],
                    oriented = False
                )
                
                self.sections.append(section)
                start = i
                end = i
                i = i + 1

    
    
    
    def build_oriented (self,matrix):
        start = 0 # start index of matrix chunk copied
        end = 0 # end index of matrix chunk copied
        i = 1 # pointer to traverse the matrix 
        length = matrix.shape[0] # vertical size of matrix
        
        while i < length :
            # If the value of km is nan, then keep stacking more
            # points to the current section
            if matrix[i][0] == "":
                
                end = end + 1;
                i   = i + 1;
                
                if(i == length):
                    
                    #if self.heights:
                    #    height = self.findHeight(labels[start],default=matrix[start][3])
                    #else:
                    #    height = matrix[matrix][3]
                    
                    height = matrix[start][3]
                    
                    section = Section(
                        matrix[start][0],
                        matrix[start:end+1],
                        matrix[start:end+1,4],
                        height,
                        axis = matrix[start,1:3],
                        oriented = True
                    )
                    
                    self.sections.append(section)
            
            
            
            elif matrix[i][0] != "":
                end = end + 1;
                
                # if self.heights:
                #     height = self.findHeight(labels[start],default=matrix[start][3])
                # else:
                #     height = matrix[start][3]
                
                height = matrix[start][3]
                
                section = Section(
                    matrix[start][0],
                    matrix[start:end],
                    matrix[start:end,4],
                    height,
                    axis = matrix[start, 1:3],
                    oriented = True
                )
                
                self.sections.append(section)
                start = i
                end = i
                i = i + 1





def main ():
    
    filename1 = "/home/jstvns/eqc-input/dbase-input/dat-et-descr.csv"
    filename2 = "/home/jstvns/eqc-input/dbase-input/dat-et-coord.csv"
    filename3 = "/home/jstvns/eqc-input/dbase-input/longitudinal.csv"
    
    model = Model(
        filename1 = filename1,
        filename2 = filename2,
        filename3 = filename3,
    )

if __name__ == "__main__":
    main()



# class ModelIterator :

#     def __init__ (self, model, start=0 , end=0):
#         self._model = model
#         self._index = start
#         self._end   = model.size if end==0 else end
        
#     def __iter__ (self) :
#         return self
    
#     def __next__ (self) :
#         if self._index >= self._model.size or self._index > self._end:
#             raise StopIteration
#         section = self._model.sections[self._model.sectionIndex[self._index]]
#         self._index += 1
#         return section




# class Model :
#     """Represents an ordered sequence of cross sections."""
    
#     def __init__ (self,
#                   heights, # String Matrix (dm,h) file "longitudinal"
#                   matrix = None, # Data with descriptors
#                   labels= None,  # Label with descriptors
#                   orientedMatrix = None,  # Data with Coordinates
#                   orientedLabels = None): # Labels with coordinates
        
################ DONE
#         self.heights = dict(heights) if heights is not None else {}
################ DONE
#         self.sections = []
#         self.sectionIndex = []
################ DONE
#         if orientedMatrix is not None:
#             self.build_oriented(orientedMatrix,orientedLabels)
#             self.sections.sort()
#             self.reference_vector()
################ DONE
#         if matrix is not None :
#             self.build_descriptor(matrix,labels)
#
################ DONE
#         self.distance_sign()
#         self.sections.sort()
#
################ DONE
#         self.deduplicate()
#         self.currSection = 0;
#         self.size = len(self.sectionIndex)
    
    
    
#     def get_size(self):
#         """Returns the number of non-duplicate cross sections in the model"""
#         return len(self.sectionIndex)
 
 
#     def distance_sign (self):
#         for sec in self.sections:
#             sec.compute_sign()
 
 
#     def getSection(self,index):
#         i = self.sectionIndex[index]
#         return self.sections[i]
 
 
 
#     def reference_vector(self):
        
#         N = len(self.sections)
        
#         for i in range(0,N):
#             for d in range (1,N):
#                 if i + d < N :
#                     if self.sections[i+d].km != self.sections[i].km:
#                         self.sections[i].vector = self.sections[i+d].axis - self.sections[i].axis
#                         break
#                 if i - d >= 0:
#                     if self.sections[i-d].km != self.sections[i].km:
#                         self.sections[i].vector = self.sections[i].axis -  self.sections[i-d].axis
#                         break
    
#     def getKmRange(self,km0,km1):
        
#         i0 = 0
#         i1 = self.size - 1
#         i = 0
#         itr = ModelIterator(self)
        
#         for section in itr:
            
#             if np.float64(section.km) >= np.float64(km0):
                
#                 i0 = i
#                 break
            
#             else:
                
#                 i += 1
                
        
#         if np.float64(km0) >= np.float64(km1) :
#             return (i0, i1)
        
#         itr2 = ModelIterator(self, i0)
        
#         for section in itr2:
            
#             if np.float64(section.km) <= np.float64(km1):
                
#                 i += 1
            
#             else:
                
#                 i1 = i-1
#                 break
        
#         return (i0,i1)
    
    

#     # Given the sorted section list `sections`, this functions merges
#     # in one section all the duplicate sections.  It places in list
#     # `section index` the indices of non-duplicate `sections`
#     def deduplicate (self) :
#         i = 0
#         j = 1
#         length = len(self.sections)
#         self.sectionIndex.append(i)
#         while j < length :
#             if self.sections[i] == self.sections[j]:
#                 self.sections[i].merge(self.sections[j])
#                 j = j + 1
#             else:
#                 i = j
#                 j = j + 1
#                 self.sectionIndex.append(i)
    
    
#     def get_km_index_dict (self):
#         d = {self.getSection(i).km : i for i in range(len(self.sectionIndex))}
#         return d 
            
    
    
#     def guessHeight (self,km):
#         dm2 = km[:-1]
#         for i in range(0,10):
#             dm3 = dm2 + f'{i}'
#             if dm3 in self.heights:
#                 print(f"Cambio de dm's sugerido:\n{km} --> {dm3}\n")
    
    
#     def findHeight (self,km,default=0):
        
#         normalized_dm = utils.normalize_fstring(km)
#         # Check if the Dict contains the normalized dm.
#         try:
#             height = self.heights[normalized_dm]
#         except KeyError:
#             print(f'>> Advertencia: DM {normalized_dm} no se encuentra en el archivo Longitudinal')
#             self.guessHeight(normalized_dm)
#             return default
        
#         try:
#             return np.float64(height)
#         except:
#             print(f'>> Advertencia: DM {normalized_dm} presenta un error en el archivo longitudinal')
#             return default
    
    
#     def build_descriptor (self,matrix,labels):
        
#         start = 0 # start index of matrix chunk copied
#         end = 0 # end index of matrix chunk copied
#         i = 1 # pointer to traverse the matrix 
#         length = matrix.shape[0] # vertical size of matrix
        
#         while i < length :
            
#             # If the value of km is nan, then keep stacking more
#             # points to the current section
#             if np.isnan(matrix[i][0]):
#                 end = end + 1;
#                 i   = i + 1
                
#                 if(i == length):
                    
#                     if self.heights:
#                         height = self.findHeight(labels[start],default=matrix[start][3])
#                     else:
#                         height = matrix[start][3]
                    
#                     section = sec.Section(
#                         labels[start], matrix[start:end+1], labels[start:end+1],
#                         height, axis = matrix[start,1:3], vector = matrix[start,1:3],
#                         oriented = False
#                     )
                    
#                     self.sections.append(section)
#                     self.kms.append(matrix[start][0])
            
            
#             elif (not np.isnan(matrix[i][0])):
#                 end = end + 1;
                
#                 if self.heights :
#                     height = self.findHeight(labels[start],default=matrix[start][3])
#                 else:
#                     height = matrix[start][3]
                
#                 section = sec.Section(
#                     labels[start], matrix[start:end], labels[start:end],
#                     height, axis = matrix[start, 1:3], vector = matrix[start, 1:3],
#                     oriented = False
#                 )
                
#                 self.sections.append(section)
#                 self.kms.append(matrix[start][0])
#                 start = i
#                 end = i
#                 i = i + 1
    
    
    
    
    
    
#     def build_oriented (self,matrix,labels):
        
#         start = 0 # start index of matrix chunk copied
#         end = 0 # end index of matrix chunk copied
#         i = 1 # pointer to traverse the matrix 
#         length = matrix.shape[0] # vertical size of matrix
        
#         while i < length :
            
#             # If the value of km is nan, then keep stacking more
#             # points to the current section
#             if np.isnan(matrix[i][0]):
#                 end = end + 1;
#                 i   = i + 1;
                
#                 if(i == length):
                    
#                     if self.heights:
#                         height = self.findHeight(labels[start],default=matrix[start][3])
#                     else:
#                         height = matrix[matrix][3]
                    
#                     section = sec.Section(
#                         labels[start], matrix[start:end+1], labels[start:end+1],
#                         height, axis = matrix[start,1:3], vector = matrix[start,1:3],
#                         oriented = True
#                     )
                    
#                     self.sections.append(section)
#                     self.kms.append(matrix[start][0])
            
            
#             elif (not np.isnan(matrix[i][0])):
#                 end = end + 1;
#                 if self.heights:
#                     height = self.findHeight(labels[start],default=matrix[start][3])
#                 else:
#                     height = matrix[start][3]
                
#                 section = sec.Section(
#                     labels[start], matrix[start:end], labels[start:end],
#                     height, axis = matrix[start, 1:3], vector = matrix[start, 1:3],
#                     oriented = True
#                 )
                
#                 self.sections.append(section)
#                 self.kms.append(matrix[start][0])
#                 start = i
#                 end = i
#                 i = i + 1
 
 
 
#     def __iter__ (self):
#         return self
 
#     def __next__ (self):
#         if self.currSection >= self.size:
#             raise StopIteration
#         else:
#             i = self.currSection
#             self.currSection += 1
#             return self.sections[self.sectionIndex[i]]
