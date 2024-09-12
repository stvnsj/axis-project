
import model as md
import reader as rd
import sys


def main():
    
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

 

    
    reader = rd.Reader (sys.argv[1],sys.argv[2])
    matrix, labels, heights = reader.getData()
    
    model = md.Model(heights,matrix,labels)

    print(model.getSection(0).getId())
    print(model.getSection(1).getId())
    print(model.getSection(2).getId())
    

if __name__ == "__main__":
    main()
