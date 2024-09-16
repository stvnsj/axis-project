import tkinter as tk
from tkinter import filedialog
import numpy as np
import reader as rd
import cad
import model as md


    
    # reader = rd.Reader (fileA.get,sys.argv[2])
    # matrix, labels, heights = reader.getData()
    # model = md.Model(heights,matrix,labels)
    
    # #print(model.getkmRange("200.00000","1001.0001"))
    
    # cadScript = cad.CadScript(model)
    # cadScript.writeKm("4785","5004")
    
    #spreadsheet = ss.Spreadsheet(model)
    #spreadsheet.writeKmMOP("testkmmop.csv" , "79.999","89.111")


def selectFileA() :
    path = filedialog.askopenfilename(title="Seleccione archivo")
    if path:
        fileA.set(path)
        print(f"Selected File: {path}")
    else:
        print("No file selected")

def selectFileB() :
    path = filedialog.askopenfilename(title="Seleccione archivo")
    if path:
        fileB.set(path)
        print(f"Selected File: {path}")
    else:
        print("No file selected")


def generateCAD():

    meter0.set(e1.get())
    meter1.set(e2.get())

    
    
    reader = rd.Reader (fileA.get(),fileB.get())
    matrix, labels, heights = reader.getData()
    model = md.Model(heights,matrix,labels)
    
    # #print(model.getkmRange("200.00000","1001.0001"))
    
    cadScript = cad.CadScript(model)
    cadScript.writeKm(e1.get(),e2.get())
    
    #spreadsheet = ss.Spreadsheet(model)
    #spreadsheet.writeKmMOP("testkmmop.csv" , "79.999","89.111")
    

def generateMOP():
    print(e1.get())
    print(e2.get())

# Create main window
root = tk.Tk()
root.title("Proyecto AXIS")
root.geometry("500x900")


fileA = tk.StringVar()
fileB = tk.StringVar()

meter0 = tk.StringVar()
meter1 = tk.StringVar()


# (e1.get(), e2.get()))



################
# File-loading #
################

# Frame using pack() for stacking
frame_load = tk.Frame(root, pady=20 , bd=3, relief="groove")
frame_load.pack()  # Stack at the top

# FRAME: Load Title
frame_load_title = tk.Frame(frame_load)
frame_load_title.pack()
label_load_title = tk.Label(frame_load_title, text="Carga de Archivos")
label_load_title.pack()

# FRAME: Load Grid
frame_load_grid = tk.Frame(frame_load)
frame_load_grid.pack()

# Buttons 
# =======
button1 = tk.Button(frame_load_grid, text="Cargar", command=selectFileA)
button2 = tk.Button(frame_load_grid, text="Cargar", command=selectFileB)
button1.grid(row=0, column=0)
button2.grid(row=1, column=0)

# Description 
# ============

label1 = tk.Label(frame_load_grid, text="Datos de estacado   ", font='Helvetica 10 bold')
label2 = tk.Label(frame_load_grid, text="Datos de nivelación ", font='Helvetica 10 bold')
label1.grid(row=0, column=1)
label2.grid(row=1, column=1)

# Filenames
# =========
labelA = tk.Label(frame_load_grid, textvariable=fileA)
labelB = tk.Label(frame_load_grid, textvariable=fileB)
labelA.grid(row=0, column=2)
labelB.grid(row=1, column=2)






################
# METERS FRAME #
################

frame_meter = tk.Frame(root, pady=20 , bd=3, relief="groove")
frame_meter.pack()  # Stack at the top

# FRAME: meter Title
frame_meter_title = tk.Frame(frame_meter)
frame_meter_title.pack()
label_meter_title = tk.Label(frame_meter_title, text="Límites del camino")
label_meter_title.pack()


# FRAME: meter Grid
frame_meter_grid = tk.Frame(frame_meter)
frame_meter_grid.pack()

# Input Boxes
label_meter_1_input = tk.Label(frame_meter_grid, text="metros inicio")
label_meter_2_input = tk.Label(frame_meter_grid, text="metros final")

e1 = tk.Entry(frame_meter_grid)
e2 = tk.Entry(frame_meter_grid)

label_meter_1_input.grid(row=0,column=1)
label_meter_2_input.grid(row=1,column=1)
e1.grid(row=0, column=0)
e2.grid(row=1, column=0)





#############
# CAD FRAME #
#############

frame_cad = tk.Frame(root, pady=20, bd=3, relief="groove")
frame_cad.pack()

frame_cad_title = tk.Frame(frame_cad,pady=10)
frame_cad_title.pack()
label_cad_title = tk.Label(frame_cad_title, text="CAD")
label_cad_title.pack()


# FRAME: meter Grid
frame_cad_grid = tk.Frame(frame_cad)
frame_cad_grid.pack()

# Input Boxes
label_cad_input = tk.Label(frame_cad_grid, text="Nombre del Archivo")
e3 = tk.Entry(frame_cad_grid)
button_generate_cad = tk.Button(frame_cad_grid, text="GENERAR", command=generateCAD)

label_cad_input.grid(row=0, column=0)
e3.grid(row=1, column=0)
button_generate_cad.grid(row=1, column=1)




######################
# FRAME: spreadsheet #
######################
frame_spreadsheet = tk.Frame(root, pady=20, bd=3, relief="groove")
frame_spreadsheet.pack()

frame_spreadsheet_title = tk.Frame(frame_spreadsheet)
frame_spreadsheet_title.pack()

label_spreadsheet_title = tk.Label(frame_spreadsheet_title, text="Planillas")
label_spreadsheet_title.pack()

#######
# MOP #
#######
frame_mop = tk.Label(frame_spreadsheet, bd=5, relief="groove")
frame_mop.pack()

label_mop = tk.Label(frame_mop, text="MOP")
label_mop.pack(side="top")

frame_spreadsheet_grid1 = tk.Frame(frame_mop)
frame_spreadsheet_grid1.pack(side="top")

# Input Boxes
label_spreadsheet_input1 = tk.Label(frame_spreadsheet_grid1, text="Nombre del Archivo")
e51 = tk.Entry(frame_spreadsheet_grid1)
button_generate_spreadsheet1 = tk.Button(frame_spreadsheet_grid1, text="GENERAR", command=generateMOP)

label_spreadsheet_input1.grid(row=0,column=0)
e51.grid(row=1, column=0)
button_generate_spreadsheet1.grid(row=1, column=1)

#########
# WIDTH #
#########
frame_ancho = tk.Label(frame_spreadsheet, bd=5, relief="groove")
frame_ancho.pack()

label_ancho = tk.Label(frame_ancho, text="Anchos")
label_ancho.pack(side="top")

frame_spreadsheet_grid2 = tk.Frame(frame_ancho)
frame_spreadsheet_grid2.pack(side="top")

# Input Boxes
label_spreadsheet_input2 = tk.Label(frame_spreadsheet_grid2, text="Nombre del Archivo")
e52 = tk.Entry(frame_spreadsheet_grid2)
button_generate_spreadsheet2 = tk.Button(frame_spreadsheet_grid2, text="GENERAR", command=generateMOP)

label_spreadsheet_input2.grid(row=0,column=0)
e52.grid(row=1, column=0)
button_generate_spreadsheet2.grid(row=1, column=1)



# Main loop
root.mainloop()


