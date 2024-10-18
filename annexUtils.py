

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
