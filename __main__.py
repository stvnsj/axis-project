import cad   
import model as md
import reader as rd
import sys
import spreadsheet as ss


def main():
    
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    
    reader = rd.Reader (sys.argv[1],sys.argv[2])
    matrix, labels, heights = reader.getData()
    model = md.Model(heights,matrix,labels)
    
    #print(model.getkmRange("200.00000","1001.0001"))
    
    cadScript = cad.CadScript(model)
    cadScript.writeKm(km0="4975",km1="5504",stackSize=5)
    
    #spreadsheet = ss.Spreadsheet(model)
    #spreadsheet.writeKmMOP("testkmmop.csv" , "79.999","89.111")


if __name__ == "__main__":
    main()
