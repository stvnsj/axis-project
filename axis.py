import tkinter as tk
from tkinter import filedialog
import numpy as np
import reader as rd
import cad
import spreadsheet
import model as md


from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
  
# import only asksaveasfile from filedialog 
# which is used to save file in any extension 
from tkinter.filedialog import asksaveasfile



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
    
    m0 = e1.get()
    m1 = e2.get()
    stackLength = e3.get()
    
    try:
        assert int(stackLength) > 0
        float(m0)
        float(m0)
    except:
        messagebox.showinfo("Alert", "Argumento Inválido")
        return
    
    file_path = filedialog.asksaveasfilename(
        title="Select or Enter File Name",
        filetypes=(("Text files", "*.scr"), ("All files", "*.*"))
    )
    
    
    reader = rd.Reader (fileA.get(),fileB.get())
    matrix, labels, heights = reader.getData()
    model = md.Model(heights,matrix,labels)
    
    
    cadScript = cad.CadScript(model)
    cadScript.writeKm(
        km0 = m0,
        km1 = m1,
        stackSize=int(stackLength),
        fn=file_path
    )




def generateMOP ():

    
    file_path = filedialog.asksaveasfilename(
        title="Select or Enter File Name",
        filetypes=(("Text files", "*.csv"), ("All files", "*.*"))
    )
    
    
    reader = rd.Reader (fileA.get(),fileB.get())
    matrix, labels, heights = reader.getData()
    model = md.Model(heights,matrix,labels)
    
    
    ss = spreadsheet.Spreadsheet(model)
    ss.writeKmMOP(
        fn=file_path)


def generateAnchos() :

    
    file_path = filedialog.asksaveasfilename(
        title="Select or Enter File Name",
        filetypes=(("Text files", "*.csv"), ("All files", "*.*"))
    )
    
    
    reader = rd.Reader (fileA.get(),fileB.get())
    matrix, labels, heights = reader.getData()
    model = md.Model(heights,matrix,labels)
    
    
    ss = spreadsheet.Spreadsheet(model)
    ss.writeKmWidth(
        fn=file_path)


    
# Create main window
root = tk.Tk()
root.title("Proyecto AXIS")
root.geometry("700x900")


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
label_meter_1_input = tk.Label(frame_meter_grid, text="Metros Inicio",width=15, anchor="w")
label_meter_2_input = tk.Label(frame_meter_grid, text="Metros Final",width=15, anchor="w")
label_meter_3_input = tk.Label(frame_meter_grid, text="Perfiles por fila",width=15, anchor="w")

e1 = tk.Entry(frame_meter_grid)
e2 = tk.Entry(frame_meter_grid)
e3 = tk.Entry(frame_meter_grid)

label_meter_1_input.grid(row=0,column=1)
label_meter_2_input.grid(row=1,column=1)
label_meter_3_input.grid(row=2,column=1)

e1.grid(row=0, column=0)
e2.grid(row=1, column=0)
e3.grid(row=2, column=0)





#############
# CAD FRAME #
#############

frame_cad = tk.Frame(root, bd=3, relief="groove")
frame_cad.pack()

label_cad_title = tk.Label(frame_cad, text="CAD",width=15, anchor="w")
label_cad_title.pack(side="left")



button_generate_cad = tk.Button(frame_cad, text="GENERAR", command=generateCAD)
button_generate_cad.pack(side="right")























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

label_mop = tk.Label(frame_mop, text="MOP",width=15, anchor="w" )
label_mop.pack(side="left")

button_generate_spreadsheet1 = tk.Button(frame_mop, text="GENERAR", command=generateMOP)
button_generate_spreadsheet1.pack(side="right")


#########
# WIDTH #
#########
frame_ancho = tk.Label(frame_spreadsheet, bd=5, relief="groove")
frame_ancho.pack()

label_ancho = tk.Label(frame_ancho, text="Anchos",width=15, anchor="w")
label_ancho.pack(side="left")

button_generate_spreadsheet2 = tk.Button(frame_ancho, text="GENERAR", command=generateAnchos)
button_generate_spreadsheet2.pack(side="right")


# Main loop
root.mainloop()


