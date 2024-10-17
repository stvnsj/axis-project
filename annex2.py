import xlsxwriter
import openpyxl
import numpy as np
import model as mdl
import utils
import sys
import reader as rd
import re
from annexUtils import Format 
from annexUtils import Writer
from annexUtils import Formatter
import annexUtils
from openpyxl import load_workbook


OFFSET   = 38
PAGEBREAKS = []

def generate () :
    
    workbook = xlsxwriter.Workbook("test2.xlsx")
    worksheet = workbook.add_worksheet("PERFILES")
    writer = Writer(workbook,worksheet)
    
    COL_WIDTHS = [
        0.10, #A 
        0.30, #B
        0.75, #C
        0.25, #D
        0.35, #E
        0.18, #F
        0.19, #G
        0.19, #H
        0.25, #I
        0.22, #J
        0.30, #K
        0.25, #L
        0.15, #M
        0.35, #N
        0.15, #O
        0.20, #P
        0.20, #Q
        0.33, #R
        0.25, #S
        0.15, #T
        0.25, #U
        0.15, #V
        0.33, #W
        0.19, #X
        0.46, #Y
        0.25, #Z
        0.10, #AA
    ]
    
    ROW_DICT = {
        0 :0.1,  
        6 :0.1,  
        7 :0.18, 
        8 :0.18, 
        9 :0.19, 
        10:0.1,
        12:0.12,
        13:0.12
        
    }
    
    ROW_DICT[1 - 1]  = 0.1
    ROW_DICT[7 - 1]  = 0.1
    ROW_DICT[11 - 1] = 0.1 
    
    #worksheet.autofit()
    annexUtils.set_column(worksheet,COL_WIDTHS)
    
    worksheet.hide_gridlines(2)
    worksheet.set_portrait()
    worksheet.set_page_view(2)
    worksheet.set_paper(9)
    worksheet.set_margins(left=0.71, right=0.71, top=0.95, bottom=0.75)
    
    # FIXED CONTENT
    writer.merge(f"B2:F6","",Format.BORDER)
    writer.merge(f"G2:Z3","PUNTOS DE LA RED DE REFERENCIA PRINCIPAL",
                 {"top":1, "right":1,"font_size":12,"bold":True,"align":"center","valign":"vcenter"})
    
    writer.merge(f"G4:Z6","FORMULARIO N° 2.903.3.F",
                 {"bottom":1,"right":1, "font_size":12,"bold":True,"align":"center","valign":"vcenter"})
    
    writer.write(f"AA2","",Format.LEFT)

    writer.merge(f"B7:Z7","",{"bottom":1})
    writer.merge(f"A8:A12","",{"right":1})
    writer.merge(f"AA8:AA12","",{"left":1})
    writer.merge(f"B13:Z13", "",{"top":1})

    writer.merge(f"B8:D8","PROYECTO",Format.SIZE(10), Format.BOLD, Format.LEFT, Format.VCENTER)
    writer.merge(f"B9:D9","SECTOR", Format.SIZE(10),Format.BOLD, Format.LEFT, Format.VCENTER)
    writer.merge(f"B10:D10","TRAMO", Format.SIZE(10),Format.BOLD, Format.LEFT, Format.VCENTER)
    writer.merge(f"B12:D12","REALIZADO",Format.SIZE(10), Format.BOLD, Format.LEFT, Format.VCENTER)
    writer.merge(f"U12:Z12","FECHA:",Format.SIZE(10),Format.RIGHT,Format.VCENTER)
  
    

    
    
    wb = load_workbook('anexos/anteproyecto/anexo1.xlsx')
    ws = wb.active
    VALUE = ws['C22'].value
    FRST_ROW = 0
    LST_ROW  = 0
    
    # Iterate through merged cell ranges
    for merged_cell_range in ws.merged_cells.ranges:
        # Check if the merged region is in column B
        if merged_cell_range.min_col == 2 and merged_cell_range.max_col == 2:  # Column B has index 2
            # Get the first cell of the merged region
            first_cell = ws.cell(row=merged_cell_range.min_row, column=2).value
            print(first_cell)
            # Check if the first cell contains the text "RBP"
            if first_cell == "RRP":
                # Get the first and last rows of the merged region
                FRST_ROW = merged_cell_range.min_row
                LST_ROW  = merged_cell_range.max_row
                first_row = merged_cell_range.min_row
                last_row = merged_cell_range.max_row
                print(f"Merged region with 'RBP' starts at row {first_row} and ends at row {last_row}")
                break
    
    
    # LOOP THE FOLLOWING CELLS 
    for i,r in enumerate(range(FRST_ROW,LST_ROW+1)):
        
        CELL_nombre = ws[f'C{r}'].value # DONE
        
        CELL_f      = ws[f'D{r}'].value
        CELL_l      = ws[f'E{r}'].value
        CELL_h      = ws[f'M{r}'].value
        
        CELL_X      = ws[f'H{r}'].value
        CELL_Y      = ws[f'I{r}'].value
        CELL_Z      = ws[f'J{r}'].value
        
        CELL_N      = ws[f'F{r}'].value
        CELL_E      = ws[f'G{r}'].value

        CELL_altura = ws[f'N{r}'].value
        CELL_cota   = ws[f'O{r}'].value

        CELL_NL     = ws[f'K{r}'].value
        CELL_EL     = ws[f'L{r}'].value

        CELL_MCL    = ws['H9'].value
        CELL_Ko     = ws['H12'].value
        
        
        
        writer.write(f"B{15 + i * OFFSET}","Identificación del Punto",Format.BOLD, Format.ITALIC, Format.SIZE(10))
        writer.write(f"F{15 + i * OFFSET}", "Nombre:", Format.SIZE(10))
        writer.write(f"N{15 + i * OFFSET}", "Dm. Ref.:",Format.SIZE(10))
        
        writer.merge(
            f"I{15 + i * OFFSET}:L{15 + i * OFFSET}",
            CELL_nombre,
            Format.SIZE(11), Format.BOTTOM, Format.CENTER
        )
        
        writer.write(
            f"C{21 + i * OFFSET}",
            CELL_f,
        )
        
        writer.write(
            f"C{22 + i * OFFSET}",
            CELL_l,
        )
        
        writer.write(
            f"C{23 + i * OFFSET}",
            CELL_h,
            Format.CENTER
        )
        
        writer.merge(
            f"H{21 + i * OFFSET}:K{21 + i * OFFSET}",
            CELL_X,
            Format.RIGHT
        )
        
        writer.merge(
            f"H{22 + i * OFFSET}:K{22 + i * OFFSET}",
            CELL_Y,
            Format.RIGHT
        )
        
        writer.merge(
            f"H{23 + i * OFFSET}:K{23 + i * OFFSET}",
            CELL_Z,
            Format.RIGHT
        )
        
        writer.merge(
            f"N{25 + i * OFFSET}:P{25 + i * OFFSET}",
            CELL_altura,
            Format.RIGHT
        )
        
        writer.merge(
            f"X{25 + i * OFFSET}:Y{25 + i * OFFSET}",
            CELL_cota,
            Format.RIGHT
        )
        
        writer.merge(
            f"O{22 + i * OFFSET}:R{22 + i * OFFSET}",
            CELL_N,
            Format.RIGHT
        )
        
        writer.merge(
            f"O{23 + i * OFFSET}:R{23 + i * OFFSET}",
            CELL_E,
            Format.RIGHT
        )
        
        writer.merge(
            f"V{22 + i * OFFSET}:Y{22 + i * OFFSET}",
            CELL_NL,
            Format.RIGHT
        )
        
        writer.merge(
            f"V{23 + i * OFFSET}:Y{23 + i * OFFSET}",
            CELL_EL,
            Format.RIGHT
        )
        
        writer.merge(
            f"W{20 + i * OFFSET}:Z{20 + i * OFFSET}",
            CELL_MCL,
            Format.LEFT
        )
        
        writer.merge(
            f"W{21 + i * OFFSET}:Z{21 + i * OFFSET}",
            CELL_Ko,
            Format.LEFT
        )
        
        
        
        
        writer.merge(f"Q{15 + i * OFFSET}:T{15 + i * OFFSET}", "",Format.CENTER,Format.SIZE(10),Format.BOTTOM)
        writer.write(f"W{15 + i * OFFSET}","Fecha:",Format.SIZE(10))
        writer.merge(f"Y{15 + i * OFFSET}:Z{15 + i * OFFSET}", "",Format.BOTTOM,Format.CENTER,Format.SIZE(10))
        
        writer.merge(f"B{17 + i * OFFSET}:Z{17 + i * OFFSET}", "Coordenadas",Format.SIZE(11),Format.CENTER)
        writer.merge(f"B{18 + i * OFFSET}:F{18 + i * OFFSET}", "Geodésicas",Format.SIZE(11),Format.CENTER)
        writer.merge(f"B{19 + i * OFFSET}:F{19 + i * OFFSET}", "Ref. SIRGAS", Format.SIZE(11),Format.CENTER)
        
        writer.merge(f"G{18 + i * OFFSET}:L{19 + i * OFFSET}", "Geocéntricas",Format.SIZE(11), Format.CENTER, Format.VCENTER )
        writer.merge(f"N{18 + i * OFFSET}:S{19 + i * OFFSET}", "UTM",Format.SIZE(11),Format.CENTER,Format.VCENTER)
        writer.merge(f"U{18 + i * OFFSET}:Z{19 + i * OFFSET}", "PTL-1",Format.SIZE(11),Format.CENTER,Format.VCENTER)
        
        writer.write(f"B{21 + i * OFFSET}","f:",Format.SIZE(11),Format.LEFT)
        writer.write(f"B{22 + i * OFFSET}","l:",Format.SIZE(11),Format.LEFT)
        writer.write(f"B{23 + i * OFFSET}","h:",Format.SIZE(10),Format.LEFT)
        
        writer.write(f"G{21 + i * OFFSET}","X:",Format.SIZE(11),Format.LEFT)
        writer.write(f"G{22 + i * OFFSET}","Y:",Format.SIZE(11),Format.LEFT)
        writer.write(f"G{23 + i * OFFSET}","Z:",Format.SIZE(11),Format.LEFT)
        
        writer.write(f"L{21 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        writer.write(f"L{22 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        writer.write(f"L{23 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        writer.write(f"D{23 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        writer.write(f"Q{25 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        writer.write(f"Z{25 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        writer.write(f"S{22 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        writer.write(f"S{23 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        writer.write(f"Z{22 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        writer.write(f"Z{23 + i * OFFSET}","m",Format.SIZE(11),Format.LEFT)
        
        
        
        writer.write(f"N{20 + i * OFFSET}","Huso:",Format.SIZE(11),Format.LEFT)
        writer.write(f"N{21 + i * OFFSET}","MC:",Format.SIZE(11),Format.LEFT)
        writer.write(f"N{22 + i * OFFSET}","N:",Format.SIZE(11),Format.LEFT)
        writer.write(f"N{23 + i * OFFSET}","E:",Format.SIZE(11),Format.LEFT)
        
        writer.write(f"U{20 + i * OFFSET}","MCL:",Format.SIZE(11),Format.LEFT)
        writer.write(f"U{21 + i * OFFSET}","Ko:",Format.SIZE(11),Format.LEFT)
        writer.write(f"U{22 + i * OFFSET}","NL:",Format.SIZE(11),Format.LEFT)
        writer.write(f"U{23 + i * OFFSET}","EL:",Format.SIZE(11),Format.LEFT)
        
        writer.write(f"F{25 + i * OFFSET}","Altura (n.m.m. modelada):",Format.SIZE(11))
        writer.write(f"S{25 + i * OFFSET}","Cota (nivelada):",Format.SIZE(11),Format.BOLD)
        
        writer.merge(f"B{27 + i * OFFSET}:K{39 + i * OFFSET}","Fotografía\nPanorámica",Format.BORDER,Format.CENTER,Format.VCENTER)
        writer.merge(f"M{27 + i * OFFSET}:Z{39 + i * OFFSET}","Vista\nAérea",Format.BORDER,Format.CENTER,Format.VCENTER)
        writer.merge(f"B{41 + i * OFFSET}:F{48 + i * OFFSET}","Fotografía\nDetalle",Format.BORDER,Format.CENTER,Format.VCENTER)
        
        
        writer.merge(f"H{41 + i * OFFSET}:Z{41 + i * OFFSET}","Descripción",Format.BOTTOM,Format.LEFT,Format.SIZE(10))
        
        writer.write(
            f'I{43 + i * OFFSET}', "Materialidad:",
            Format.SIZE(9)
        )
        
        writer.write(
            f'I{44 + i * OFFSET}', "Dimensiones:",
            Format.SIZE(9)
        )
        
        writer.write(
            f'I{45 + i * OFFSET}', "Distancia a :",
            Format.SIZE(9)
        )
        
        
        writer.merge(f"G{42 + i * OFFSET}:G{48 + i * OFFSET}","",Format.BRIGHT)
        writer.merge(f"AA{42 + i * OFFSET}:AA{48 + i * OFFSET}","",Format.BLEFT)
        writer.merge(f"H{49 + i * OFFSET}:Z{49 + i * OFFSET}","",Format.TOP)
        writer.merge(f"A{50 + i * OFFSET}:AA{50 + i * OFFSET}","",{})
        PAGEBREAKS.append(50 + i * OFFSET)
    
    worksheet.set_h_pagebreaks(PAGEBREAKS)
    annexUtils.set_row_dict(worksheet,ROW_DICT)
    
    
    
    

    # formatter.set_rows({0:2,1:2,2:2, 4:2})
    workbook.close()




if __name__ == "__main__":
    
    generate()
    #f1 = sys.argv[1]
    #f2 = sys.argv[2]
    
    #reader = rd.Reader (f1, "", f2)
    #matrix, labels, om, ol, heights = reader.getData()
    #model = mdl.Model(heights,matrix,labels, om, ol)
    
    #trans (model)

