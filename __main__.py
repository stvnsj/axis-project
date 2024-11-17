import cad   
import model as md
import reader as rd
import sys
import spreadsheet as ss
import gui.test as test



def main():
    
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    filename3 = sys.argv[3]
    
    reader = rd.Reader (sys.argv[1],sys.argv[2],sys.argv[3])
    matrix, labels, orientedMatrix, orientedLabels, heights = reader.getData()
    model = md.Model(heights,matrix,labels,orientedMatrix,orientedLabels)
    
    #print(model.getkmRange("200.00000","1001.0001"))
    
    # cadScript = cad.CadScript(model)
    # cadScript.writeFull("~/path")
    
    spreadsheet = ss.Spreadsheet(model)
    spreadsheet.writeMOP("mop.csv")


if __name__ == "__main__":
    test.X = 3
    test.print_x()
