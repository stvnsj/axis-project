import level
import component 
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


def selectFileC() :
    path = filedialog.askopenfilename(title="Seleccione archivo")
    if path:
        fileC.set(path)
        print(f"Selected File: {path}")
    else:
        print("No file selected")





def select_height_pr() :
    
    path = filedialog.askopenfilename(title="Seleccione archivo")
    if path:
        height_pr_file.set(path)
        print(f"Selected File: {path}")
    else:
        print("No file selected")


def select_circuit() :
    
    path = filedialog.askopenfilename(title="Seleccione archivo")
    if path:
        circuit_file.set(path)
        print(f"Selected File: {path}")
    else:
        print("No file selected")

def generate_report():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.csv"), ("All files", "*.*"))
    )
    
    cir = level.parser(circuit_file.get(),height_pr_file.get())
    cir.write_circuit_table(filename)
    
def generate_longitudinal():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.csv"), ("All files", "*.*"))
    )
    
    cir = level.parser(circuit_file.get(),height_pr_file.get())
    cir.write_longitudinal(filename)





def generateCAD():
    
    m0 = e1.get()
    m1 = e2.get()
    stackLength = e3.get()
    
    try:
        assert int(stackLength) > 0
    except:
        messagebox.showinfo("Alert", "El número de perfiles por fila debe ser un número >= 1")
        return
 
    try:
        assert float (m0) >= 0
    except:
        messagebox.showinfo("Alert", "Metros Inicio debe ser un número real >= 0")
        return
    
    try:
        assert float (m1) >= 0 and float (m0) < float(m1)
    except:
        messagebox.showinfo("Alert", "Metros Final debe ser un número real >=0 y > Metros Incio")
        return
    
    
    
    file_path = filedialog.asksaveasfilename(
        title="Select or Enter File Name",
        filetypes=(("Text files", "*.scr"), ("All files", "*.*"))
    )
    
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    
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
    
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    
    ss = spreadsheet.Spreadsheet(model)
    ss.writeKmMOP(fn=file_path)


def generateAnchos() :
 
    
    file_path = filedialog.asksaveasfilename(
        title="Select or Enter File Name",
        filetypes=(("Text files", "*.csv"), ("All files", "*.*"))
    )
 
    
    
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    
    ss = spreadsheet.Spreadsheet(model)
    ss.writeKmWidth(fn=file_path)


def generateFullCAD():
    
    try:
        assert int(input_1.get()) >0
    except:
        messagebox.showinfo("Alert", "\'Perfiles por fila\' debe ser un entero >0")
        return
    
    try:
        assert int(input_2.get()) >0
    except:
        messagebox.showinfo("Alert", "\'Perfiles por Archivo\' debe ser un entero >0")
        return
    
    try:
        assert input_3.get() != ""
    except:
        messagebox.showinfo("Alert", "Debe ingresar un nombre de proyecto")
        return
    
    print(int(input_1.get()))
    print(int(input_2.get()))
    print(input_3.get())

    directory = filedialog.askdirectory()
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    cadScript = cad.CadScript(model)
    cadScript.writeFull (directory, input_3.get(), fileSize = int(input_2.get()), stackSize = int(input_1.get()))


# Create main window
root = tk.Tk()
root.title("Proyecto AXIS")
root.geometry("1200x900")


# Create a Notebook widget (tabs container)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)


# Add tabs to the notebook (tabs container)
notebook.add(tab1, text='CAD')
notebook.add(tab2, text='Nivelación')
notebook.add(tab3, text='test')


def greet(inputs):
    print("First input :" , inputs[0].get())
    print("Second Input :" , inputs[1].get())
    print("Third Input :" , inputs[2].get())

entry_params = [{"label":"uno"},{"label":"dos"},{"label":"tres"}]
component.InputFrame(tab3,entry_params=entry_params, command=greet)



fileA = tk.StringVar()
fileB = tk.StringVar()
fileC = tk.StringVar()

height_pr_file = tk.StringVar()
circuit_file   = tk.StringVar()

meter0 = tk.StringVar()
meter1 = tk.StringVar()



##################
# ############## #
# # HEIGHT TAB # #
# ############## #
##################


button_params = [
    {"label": "Cotas Topograficas", "stringvar": height_pr_file },
    {"label": "Circuito Nivelación", "stringvar": circuit_file },
]
component.LoadFileFrame(tab2, title="Carga de Archivos", button_params = button_params)


button_params = [
    {"label": "Longitudinal", "command":generate_longitudinal} ,
    {"label":"Reporte","command":generate_report}
]

component.ButtonFrame(tab2, title="Planillas", button_params=button_params)


################
# File-loading #
################

button_params = [
    {"label": "Estacado con Descriptor", "stringvar": fileA },
    {"label": "Estacado con Coordenadas", "stringvar": fileB },
    {"label": "Longitudinal", "stringvar": fileC}
]
component.LoadFileFrame(tab1, title="Carga de Archivos", button_params = button_params)


#################
# CAD por TRAMO #
#################
frame_meter = tk.Frame(tab1, pady=10, padx=10, bd=3, relief="groove")
frame_meter.pack(pady = 10, padx=20)  # Stack at the top

# FRAME: meter Title
frame_meter_title = tk.Frame(frame_meter)
frame_meter_title.pack()
label_meter_title = tk.Label(frame_meter_title, text="CAD de un Tramo", font='Helvetica 10 bold')
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
button_generate_cad = tk.Button(frame_meter_grid, text="GENERAR", command=generateCAD)


label_meter_1_input.grid(row=0,column=1)
label_meter_2_input.grid(row=1,column=1)
label_meter_3_input.grid(row=2,column=1)

e1.grid(row=0, column=0, pady=5, padx=5)
e2.grid(row=1, column=0, pady=5, padx=5)
e3.grid(row=2, column=0, pady=5, padx=5)
button_generate_cad.grid(row=3,column=0, pady=5)




#################
# FULL CAD      #
#################
frame_full_cad = tk.Frame(tab1, pady=10, padx=10, bd=3, relief="groove")
frame_full_cad.pack(pady = 10, padx=20)  # Stack at the top

# FRAME: meter Title
frame_full_cad_title = tk.Frame(frame_full_cad)
frame_full_cad_title.pack()

label_full_cad_title = tk.Label(frame_full_cad_title, text="CAD Proyecto Completo", font='Helvetica 10 bold')
label_full_cad_title.pack()


# FRAME: meter Grid
grid_full_cad = tk.Frame(frame_full_cad)
grid_full_cad.pack()

# Input Boxes
label_input_1 = tk.Label(grid_full_cad, text="Perfiles por Fila",width=15, anchor="w")
label_input_2 = tk.Label(grid_full_cad, text="Perfiles por Archivo",width=15, anchor="w")
label_input_3 = tk.Label(grid_full_cad, text="Nombre Proyecto",width=15, anchor="w")

input_1 = tk.Entry(grid_full_cad)
input_2 = tk.Entry(grid_full_cad)
input_3 = tk.Entry(grid_full_cad)
button_generate_full_cad = tk.Button(grid_full_cad, text="GENERAR", command=generateFullCAD)


label_input_1.grid(row=0,column=1)
label_input_2.grid(row=1,column=1)
label_input_3.grid(row=2,column=1)

input_1.grid(row=0, column=0, pady=5, padx=5)
input_2.grid(row=1, column=0, pady=5, padx=5)
input_3.grid(row=2, column=0, pady=5, padx=5)
button_generate_full_cad.grid(row=3,column=0, pady=5)











######################
# FRAME: spreadsheet #
######################
frame_spreadsheet = tk.Frame(tab1, pady=20, bd=3, relief="groove")
frame_spreadsheet.pack(pady=10,padx=20)

frame_spreadsheet_title = tk.Frame(frame_spreadsheet)
frame_spreadsheet_title.pack()

label_spreadsheet_title = tk.Label(frame_spreadsheet_title, text="Planillas", font='Helvetica 10 bold')
label_spreadsheet_title.pack()

#######
# MOP #
#######
frame_mop = tk.Label(frame_spreadsheet)
frame_mop.pack()

label_mop = tk.Label(frame_mop, text="MOP",width=15, anchor="w" )
label_mop.grid(row=0,column=0, padx=5, pady=5)

button_generate_spreadsheet1 = tk.Button(frame_mop, text="GENERAR", command=generateMOP)
button_generate_spreadsheet1.grid(row=0,column=1,padx=5,pady=5)

#########
# WIDTH #
#########
label_ancho = tk.Label(frame_mop, text="Anchos",width=15, anchor="w")
label_ancho.grid(row=1,column=0,padx=5,pady=5)

button_generate_spreadsheet2 = tk.Button(frame_mop, text="GENERAR", command=generateAnchos)
button_generate_spreadsheet2.grid(row=1,column=1,padx=5,pady=5)


# Main loop
root.mainloop()


