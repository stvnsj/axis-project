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
    
    # cadScript = cad.CadScript(model)
    # cadScript.write(7,11)

    spreadsheet = ss.Spreadsheet(model)
    
    spreadsheet.writeMOP()


if __name__ == "__main__":
    main()
