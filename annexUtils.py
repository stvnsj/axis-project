import re
from datetime import datetime

INCH_COL = 10
INCH_ROW = 72
OFFSET   = 38
PAGEBREAKS = []


class Writer :
    def __init__ (self,workbook,worksheet):
        self.workbook = workbook
        self.worksheet = worksheet
    
    def set_worksheet (self,ws):
        self.worksheet = ws
    
    def merge (self,ran,dat,*dic):
        
        
        CELL_FORMAT = {}
        for f in dic :
            CELL_FORMAT = CELL_FORMAT | f
            
        self.worksheet.merge_range(
            ran,
            dat,
            self.workbook.add_format(CELL_FORMAT)
        )
    
    def write (self,cell,dat,*dic):
        
        CELL_FORMAT = {}
        for f in dic :
            CELL_FORMAT = CELL_FORMAT | f
            
        self.worksheet.write(
            cell,
            dat,
            self.workbook.add_format(CELL_FORMAT)
        )


class Format :
    
    def SIZE(n):
        return {"font_size":n}
    
    BOLD = {"bold":True}
    ITALIC = {"italic":True}
    
    TOP  = {"top" :1}
    BTOP = {"top" :1}
    BBOTTOM = {"bottom" :1}
    BOTTOM = {"bottom":1}
    BLEFT = {"left": 1}
    BRIGHT = {"right": 1}
    
    BORDER = {"border":1}
    
    LEFT = {"align":"left"}
    RIGHT = {"align":"right"}
    
    CENTER = {"align":"center"}
    VCENTER = {"valign":"vcenter"}




class Formatter :
    
    def __init__(self, ws):
        self.ws = ws
        
    
    def set_cols(self,dic):
        for col in dic:
            size = dic[col]
            self.ws.set_column(col,col,size*INCH_COL) 
            
    
    def set_rows(self,dic):
        for row in dic:
            size = dic[row]
            self.ws.set_row(row,size*INCH_ROW)

def set_column (ws,widths,INCH_COL=10):
    for col , w in enumerate(widths):
        ws.set_column(col,col,w*INCH_COL)

def set_row (ws, heights) :
    for row , h in enumerate(heights) :
        ws.set_row(row,h*INCH_ROW)

def set_row_dict (ws, heights={}) :
    for h in heights:
        ws.set_row(h, heights[h] * INCH_ROW)



def is_g (s):
    if s.startswith("G"):
        return True
    else:
        False


def is_t (s):
    if s.startswith("T"):
        return True
    else:
        return False

def curr_date (opt=0) :
    
    if opt  == 0:
        MES = {
            1 : "ENERO",
            2 : "FEBRERO",
            3 : "MARZO",
            4 : "ABRIL",
            5 : "MAYO",
            6 : "JUNIO",
            7 : "JULIO",
            8 : "AGOSTO",
            9 : "SEPTIEMBRE",
            10 : "OCTUBRE",
            11 : "NOVIEMBRE"
        }
        return f'{MES[datetime.now().month]} {datetime.now().year}'
    
    else :
        MES  = {
            1 : "EN",
            2 : "FEBR",
            3 : "MAR",
            4 : "ABR",
            5 : "MAY",
            6 : "JUN",
            7 : "JUL",
            8 : "AGO",
            9 : "SEPT",
            10 : "OCT",
            11 : "NOV"
        }
        return f'{MES[datetime.now().month]} {datetime.now().year}'

class Scanner :
    
    def __init__ (self,ws) :
        self.ws = ws
        self.row = self.__find_row__()
        
        self.PRO       = None
        self.EST       = None
        self.GEO_S     = None
        self.GEO_W     = None
        self.UTM_N     = None
        self.UTM_E     = None
        self.GEO_X     = None
        self.GEO_Y     = None
        self.GEO_Z     = None
        self.PTL_N     = []
        self.PTL_E     = []
        self.ELIP      = None
        self.COTA_ORTO = None
        self.COTA_GEO  = None
        
        self.__find_field__()
 
    def __find_row__ (self) :
        for col in self.ws.iter_cols(min_col=1):
            for cell in col:
                if cell.value == "MASTER":
                    return cell.row
        raise Exception("No row starting with \'MASTER\' cell")
    
    def __find_field__ (self) :
        for row in self.ws.iter_rows(min_row=self.row,max_row=self.row):
            for cell in row:
                if cell.value == "PRO":
                    self.PRO = cell
                    continue
                if cell.value == "EST":
                    self.EST = cell
                    continue
                if cell.value == "GEO-S":
                    self.GEO_S = cell
                    continue
                if cell.value == "GEO-W":
                    self.GEO_W = cell
                    continue
                if cell.value == "UTM-N":
                    self.UTM_N = cell
                    continue
                if cell.value == "UTM-E":
                    self.UTM_E = cell
                    continue
                if cell.value == "GEO-X":
                    self.GEO_X = cell
                    continue
                if cell.value == "GEO-Y":
                    self.GEO_Y = cell
                    continue
                if cell.value == "GEO-Z":
                    self.GEO_Z = cell
                    continue
                if  bool(re.match(r"^PTL\d*-N", str(cell.value))):
                    self.PTL_N.append(cell)
                    continue
                if  bool(re.match(r"^PTL\d*-E", str(cell.value))):
                    self.PTL_E.append(cell)
                    continue
                if cell.value == "ELIP":
                    self.ELIP = cell
                    continue
                if cell.value == "COTA-ORTO":
                    self.COTA_ORTO = cell
                    continue
                if cell.value == "COTA-GEO":
                    self.COTA_GEO =  cell
                    continue


if __name__ == "__main__":
    
    print(curr_date())
