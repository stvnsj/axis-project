import level
import component 
import tkinter as tk
from tkinter import filedialog
import numpy as np
import reader as rd
import cad
import spreadsheet
import model as md
import command as cmd
import annex 
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import annex8

# import only asksaveasfile from filedialog 
# which is used to save file in any extension 
from tkinter.filedialog import asksaveasfile

# If I define commands in another file, what is the best way to pass a arguments
# to a function.
#
# IDEAS for COMMANDS:
#
#     file_selector
#     =============
# file_selector string_var -> ()

def generate_annex_2 ():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    
    annex2.generate(master_table.get(),filename)


def generate_annex_4 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex4.generate(master_table.get(),filename)


def generate_annex_5 ():
    pass

def generate_annex_8 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex8.generate(master_table.get(),filename)

def generate_annex_11 ():
    pass

def generate_report():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.csv *.txt"), ("All files", "*.*"))
    )
    
    if filename == "":
        return 
    
    cir = level.parser(circuit_file.get(),height_pr_file.get())
    cir.write_circuit_table(filename)
    
def generate_longitudinal():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.csv *.txt"), ("All files", "*.*"))
    )
    
    if filename == "":
        return 
    
    cir = level.parser(circuit_file.get(),height_pr_file.get())
    cir.write_longitudinal(filename)

def generate_height_cad():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.scr"), ("All files", "*.*"))
    )
    
    if filename == "":
        return 
    
    cir = level.parser(circuit_file.get(),height_pr_file.get())
    cir.plot(filename)
    




def generateCAD(inputs):
    
    m0 = inputs[0].get()
    m1 = inputs[1].get()
    stackLength = inputs[2].get()
    
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
    
    if file_path == "":
        return 
    
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





def complete_cad(inputs):
    stackLength = inputs[0].get()
    try:
        assert int(stackLength) > 0
    except:
        messagebox.showinfo("Alert", "El número de perfiles por fila debe ser un número >= 1")
        return
    
    file_path = filedialog.asksaveasfilename(
        title="Generar como",
        filetypes=(("Text files", "*.scr"), ("All files", "*.*"))
    )
    
    if file_path == "":
        return 
    
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    
    cadScript = cad.CadScript(model)
    cadScript.writeCompleteProject(
        file_path,
        stackSize=int(stackLength),
    )




def generateMOP ():
    
    
    file_path = filedialog.asksaveasfilename(
        title="Select or Enter File Name",
        filetypes=(("Text files", "*.csv *.txt"), ("All files", "*.*"))
    )
    
    if file_path == "":
        return
    
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    
    ss = spreadsheet.Spreadsheet(model)
    ss.writeKmMOP(fn=file_path)


def generateAnchos() :
 
    
    file_path = filedialog.asksaveasfilename(
        title="Select or Enter File Name",
        filetypes=(("Text files", "*.csv *.txt"), ("All files", "*.*"))
    )
    
    if file_path == "":
        return 
    
    
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    
    ss = spreadsheet.Spreadsheet(model)
    ss.writeKmWidth(fn=file_path)

def generate_anexo_trans() :
    
    file_path = filedialog.asksaveasfilename(
        title="Select or Enter File Name",
        filetypes=(("Excel", "*.xlsx"), ("All files", "*.*"))
    )
    
    if file_path == "":
        return 
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    annex.trans(model,file_path)


def generateFullCAD(inputs):
    try:
        assert int(inputs[0].get()) >0
    except:
        messagebox.showinfo("Alert", "\'Perfiles por fila\' debe ser un entero >0")
        return
    
    try:
        assert int(inputs[1].get()) >0
    except:
        messagebox.showinfo("Alert", "\'Perfiles por Archivo\' debe ser un entero >0")
        return
    
    try:
        assert inputs[2].get() != ""
    except:
        messagebox.showinfo("Alert", "Debe ingresar un nombre de proyecto")
        return
    
    directory = filedialog.askdirectory()
    
    if directory == "":
        return 
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    cadScript = cad.CadScript(model)
    cadScript.writeFull (directory, inputs[2].get(), fileSize = int(inputs[1].get()), stackSize = int(inputs[0].get()))


# Create main window
root = tk.Tk()
root.title("Proyecto AXIS")
root.geometry("1200x950")


# Create a Notebook widget (tabs container)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)


# Add tabs to the notebook (tabs container)
notebook.add(tab1, text='CAD')
notebook.add(tab2, text='NIVELACION')
notebook.add(tab3, text='ANEXO')
notebook.add(tab4, text='ANEXO Anteproyecto')

# def greet(inputs):
#     print("First input :" , inputs[0].get())
#     print("Second Input :" , inputs[1].get())
#     print("Third Input :" , inputs[2].get())

# entry_params = [{"label":"uno"},{"label":"dos"},{"label":"tres"}]
# component.InputFrame(tab3,entry_params=entry_params, command=greet)



fileA = tk.StringVar()
fileB = tk.StringVar()
fileC = tk.StringVar()

master_table = tk.StringVar()
level_annex  = tk.StringVar() 

height_pr_file = tk.StringVar()
circuit_file   = tk.StringVar()

meter0 = tk.StringVar()
meter1 = tk.StringVar()


################
# ############ #
# # CAD TAB1 # #
# ############ #
################

button_params = [
    {"label": "Estacado con Descriptor", "stringvar": fileA },
    {"label": "Estacado con Coordenadas", "stringvar": fileB },
    {"label": "Longitudinal", "stringvar": fileC}
]
component.LoadFileFrame(tab1, title="Carga de Archivos", button_params = button_params)

entry_params = [
    {"label":"Perfiles por Fila"}
]
component.InputFrame(tab1,entry_params=entry_params, command=complete_cad, title="CAD Proyecto Completo")

entry_params = [
    {"label":"Perfiles por Fila"},
    {"label":"Perfiles por Archivo"},
    {"label":"Nombre Proyecto"}
]
component.InputFrame(tab1,entry_params=entry_params, command=generateFullCAD, title="CAD Proyecto Fragmentado")

entry_params = [
    {"label":"Metros Inicio"},
    {"label":"Metros Final"},
    {"label":"Perfiles por fila"}
]
component.InputFrame(tab1,entry_params=entry_params, command=generateCAD, title="CAD de Tramo")


button_params = [
    {"label":"MOP", "command":generateMOP},
    {"label":"Anchos", "command":generateAnchos}
]
component.ButtonFrame(tab1, title="Planillas", button_params=button_params)



#######################
# ################### #
# # NIVELACION TAB2 # #
# ################### #
#######################

button_params = [
    {"label": "Cotas Topograficas", "stringvar": height_pr_file },
    {"label": "Circuito Nivelación", "stringvar": circuit_file },
]
component.LoadFileFrame(tab2, title="Carga de Archivos", button_params = button_params)


button_params = [
    {"label":"Reporte","command":generate_report},
    {"label":"Longitudinal", "command":generate_longitudinal},
    {"label":"CAD" , "command":generate_height_cad}
]
component.ButtonFrame(tab2, title="Planillas", button_params=button_params)



####################
# ################ #
# # ANEXOS TAB 3 # #
# ################ #
####################
button_params = [
    {"label": "Estacado con Descriptor", "stringvar": fileA },
    {"label": "Estacado con Coordenadas", "stringvar": fileB },
    {"label": "Longitudinal", "stringvar": fileC}
]
component.LoadFileFrame(tab3, title="Carga de Archivos", button_params = button_params)


button_params = [
    {"label":"Perfiles Transversales", "command":generate_anexo_trans},
]
component.ButtonFrame(tab3, title="FORMULARIO N° 2.5.3", button_params=button_params)


########################
# ANEXO ANTEPROYECTO 4 #
########################
button_params = [
    {"label":"Anexo 1 (Tabla Maestra)", "stringvar": master_table},
    {"label":"Anexo 10 (Nivelación)"  , "stringvar": level_annex}
]
component.LoadFileFrame(tab4, title='Carga de Anexos', button_params=button_params)


button_params = [
    {"label":"Anexo 8", "command":generate_annex_8},
]
component.ButtonFrame(tab4, title="Generación de Anexos", button_params=button_params)





# Main loop
root.mainloop()


