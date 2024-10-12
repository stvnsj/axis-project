import xlsxwriter

class Writer :
    def __init__ (self,workbook,worksheet):
        self.workbook = workbook
        self.worksheet = worksheet
        
    def set_worksheet (self,ws):
        self.worksheet = ws
        

    def merge (self,ran,dat,dic):
        self.worksheet.merge_range(
            ran,
            dat,
            self.workbook.add_format(dic)
        )

    def write (self,cell,dat,dic):
        self.worksheet.write(
            cell,
            dat,
            self.workbook.add_format(dic)
        )
        

def level () :
    
    workbook = xlsxwriter.Workbook('trans.xlsx')
    worksheet = workbook.add_worksheet()
    writer = Writer(workbook,worksheet)
    worksheet.hide_gridlines(2)  # 2 hides both the printed and visible gridlines
    
    format_bold = workbook.add_format({'bold': True})
    format_border = workbook.add_format({'border': 1})
    border_top    = workbook.add_format({'top': 1})
    border_bottom = workbook.add_format({'bottom': 1})
    border_left   = workbook.add_format({'left': 1})
    border_right  = workbook.add_format({'right': 1})
    border_top_left_right = workbook.add_format({'top':1,'left':1,'right':1})

    writer.merge('B2:D6', '', {'border':1})
    writer.merge('E2:I2', '', {'right':1,'top':1,'left':1})
    writer.merge('E3:I3', 'PERFILES TRANSVERSALES', {'right':1,'left':1,'bold':True,'font_size':12,'align':'center'})
    writer.merge('E4:I5', '', {'right':1,'left':1,'bold':True,'font_size':12})
    writer.merge('E6:I6', 'FORMULARIO N° 2.5.2', {'left':1,'bottom':1,'right':1,'bold':True,'font_size':12,'align':'center'})
    
    writer.write('B8', 'PROYECTO', {'left':1,'top':1,'bold':True,'font_size':10})
    writer.write('B9', 'SECTOR', {'left':1,'bold':True,'font_size':10})
    writer.write('B10', 'TRAMO', {'left':1,'bold':True,'font_size':10})
    writer.write('B12', 'REALIZADO', {'left':1,'bottom':1,'bold':True,'font_size':10})

    writer.merge('C8:I8', ': Nombre proyecto', {'right':1,'top':1,'font_size':10,'align':'left'})
    writer.merge('C9:I9', ': Nombre del sector', {'right':1,'font_size':10,'align':'left'})
    writer.merge('C10:I10', ': Dm', {'right':1,'font_size':10,'align':'left'})
    writer.merge('B11:I11', '', {'right':1,'left':1})
    writer.merge('C12:G12', ': TOPOGRAFIA', {'bottom':1,'font_size':10,'align':'left'})
    writer.merge('H12:I12', 'FECHA: ', {'right':1,'bottom':1,'align':'right','font_size':10})

    writer.write('D14','DM',{'border':1,'font_size':10,'align':'center'})
    writer.write('E14','DIST_EJE',{'border':1,'font_size':10,'align':'center'})
    writer.write('F14','COTA',{'border':1,'font_size':10,'align':'center'})
    writer.write('G14','IDENTIFICADOR',{'border':1,'font_size':10,'align':'center'})
    
    
    
    workbook.close()

level()

