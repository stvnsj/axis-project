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
import annex2
import annex5
import annex4
import annex8
import annex11
import annexLong
import axisCommands as ax_com
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk




# import only asksaveasfile from filedialog 
# which is used to save file in any extension 
from tkinter.filedialog import asksaveasfile
trans_model = None

def generate_annex_2 ():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    
    annex2.generate(master_table.get(),filename,src_dir=img_dir.get(), src_dir2=img_dir2.get())


def generate_annex_4 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex4.generate(master_table.get(),filename)


def generate_annex_5 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex5.generate(master_table.get(),filename,src_dir=img_dir.get(), src_dir2=img_dir2.get())

def generate_annex_8 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex8.generate(master_table.get(),filename)

def generate_annex_11 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex11.generate(level_annex.get(),filename)


def generate_report():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.csv *.txt"), ("All files", "*.*"))
    )
    
    if filename == "":
        return 
    
    cir = level.parser(circuit_file.get(),height_pr_file.get(),trigonometric_file.get())
    cir.write_circuit_table(filename)
    
def generate_longitudinal():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.csv *.txt"), ("All files", "*.*"))
    )
    
    if filename == "":
        return 
    
    cir = level.parser(circuit_file.get(),height_pr_file.get(), trigonometric_file.get())
    cir.write_longitudinal(filename)

def generate_height_cad():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.scr"), ("All files", "*.*"))
    )
    
    if filename == "":
        return 
    
    cir = level.parser(circuit_file.get(),height_pr_file.get(),trigonometric_file.get())
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
tab5 = ttk.Frame(notebook)
tab6 = ttk.Frame(notebook)

# Add tabs to the notebook (tabs container)
notebook.add(tab1, text='CAD')
notebook.add(tab2, text='NIVELACION')
notebook.add(tab3, text='ANEXO (Ante.)')
notebook.add(tab4, text='ANEXO (Def.)')
notebook.add(tab5, text='DM')
notebook.add(tab6, text='PLOT')


fileA = tk.StringVar() # TRANS DESCRIPTOR
fileB = tk.StringVar() # TRANS COORDENADA
fileC = tk.StringVar()

eje_estaca_file = tk.StringVar() 

img_dir = tk.StringVar()
img_dir2 = tk.StringVar()

master_table = tk.StringVar()
level_annex  = tk.StringVar() 

height_pr_file = tk.StringVar()
circuit_file   = tk.StringVar()
trigonometric_file = tk.StringVar()

meter0 = tk.StringVar()
meter1 = tk.StringVar()


################
# ############ #
# # CAD TAB1 # #
# ############ #
################

button_params = [
    {"label": "Estacado con Descriptor", "stringvar": fileA, "type":"file" },
    {"label": "Estacado con Coordenadas", "stringvar": fileB , "type":"file"},
    {"label": "Longitudinal", "stringvar": fileC , "type":"file"}
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
    {"label": "Cotas Topograficas", "stringvar": height_pr_file , "type":"file"},
    {"label": "Circuito Nivelación", "stringvar": circuit_file , "type":"file"},
    {"label": "Alturas Trigonométricas", "stringvar": trigonometric_file, "type":"file"}
]
component.LoadFileFrame(tab2, title="Carga de Archivos", button_params = button_params)


button_params = [
    {"label":"Anexo 2.5.3 (CSV)","command":generate_report},
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
    {"label": "Estacado con Descriptor", "stringvar": fileA , "type":"file"},
    {"label": "Estacado con Coordenadas", "stringvar": fileB, "type":"file" },
    {"label": "Longitudinal", "stringvar": fileC, "type":"file"}
]
component.LoadFileFrame(tab4, title="Carga de Archivos Estacado", button_params = button_params)


button_params = [
    {"label":"2 - Perfiles Transversales (2.5.2)", "command":generate_anexo_trans},
]
component.ButtonFrame(tab4, title="Generación de Anexos (DEFINITIVO)", button_params=button_params)


button_params = [
    {"label": "Cotas PR", "stringvar": height_pr_file , "type":"file"},
    {"label": "Libreta", "stringvar": circuit_file , "type":"file"},
    {"label": "Alturas Trigonométricas", "stringvar": trigonometric_file, "type":"file"}
]
component.LoadFileFrame(tab4, title="Carga de Archivos Nivelación", button_params = button_params)

button_params = [
    {"label":"3 - Nivelación Longitudinal del Eje Estacado (2.5.3)",
     "command": ax_com.generate_annex_long(circuit_file, height_pr_file, trigonometric_file)},
]
component.ButtonFrame(tab4, title="Generación de Anexos (DEFINITIVO)", button_params=button_params)




########################
# ANEXO ANTEPROYECTO   #
########################
button_params = [
    {"label":"Anexo 1 (Tabla Maestra)", "stringvar": master_table ,  "type":"file"},
    {"label":"Anexo 10 (Nivelación)"  , "stringvar": level_annex , "type":"file"},
    {"label":"Imagenes (Pan. Det.)"   , "stringvar": img_dir , "type":"dir"},
    {"label":"Imagenes (Geo.)"        , "stringvar": img_dir2 , "type":"dir"},
]

component.LoadFileFrame(tab3, title='Carga de Anexos', button_params=button_params)

# 2 , 4 , 8 , 11
button_params = [
    {"label":"2 - Puntos de la Red de Referencia Principal (2.903.3.F)", "command":generate_annex_2},
    {"label":"4 - Resumen de Coordenadas de la Red de Referencia Principal (2.903.3.G)", "command":generate_annex_4},
    {"label":"5 - Formulario de Ubicación de Vértices del STC (2.303.104.A)", "command":generate_annex_5},
    {"label":"8 - Coordenadas de Vértices del STC (2.303.104.B)", "command":generate_annex_8},
    {"label":"11 - Cotas de PR (2.903.3.I)", "command":generate_annex_11},
]
component.ButtonFrame(tab3, title="Generación de Anexos (ANTEPROYECTO)", button_params=button_params)


###############
# DM ANALYSIS #
###############
button_params = [
    {"label":"Eje Estaca", "stringvar": eje_estaca_file, "type":"file"},
    {"label": "Estacado con Descriptor", "stringvar": fileA, "type":"file" },
    {"label": "Estacado con Coordenadas", "stringvar": fileB , "type":"file"},
    {"label": "Libreta", "stringvar": circuit_file , "type":"file"},
    {"label": "Alturas Trigonométricas", "stringvar": trigonometric_file, "type":"file"}
    
]  
component.LoadFileFrame(tab5, title='Carga de Archivos', button_params=button_params)

button_params = [
    {"label":"Analisis DM", "command":ax_com.get_dm_analysis(eje_estaca_file,fileA,fileB,circuit_file,trigonometric_file)},
]
component.ButtonFrame(tab5, title="Análisis", button_params=button_params)






################################
#  _____  _      ____ _______  #
# |  __ \| |    / __ \__   __| #
# | |__) | |   | |  | | | |    #
# |  ___/| |   | |  | | | |    #
# | |    | |___| |__| | | |    #
# |_|    |______\____/  |_|    #
################################


fig, ax = plt.subplots(figsize=(13, 13))


canvasFrame = tk.Frame(tab6,bd=3,relief='groove',bg='#AAAAAA')

canvas = FigureCanvasTkAgg(fig, master=canvasFrame)


toolbar = NavigationToolbar2Tk(canvas, canvasFrame)







plot_frame = tk.Frame(tab6)
combobox_frame = ttk.LabelFrame(plot_frame, text="Perfil Transversal")
combobox = ttk.Combobox(combobox_frame, values=[])

navigation_frame = ttk.LabelFrame(plot_frame, text="Navegar Perfiles")

next_button = tk.Button(navigation_frame, text="siguiente", command=lambda: ax_com.next_section_index(fig,ax,canvas))
prev_button = tk.Button(navigation_frame, text="previo", command=lambda: ax_com.prev_section_index(fig,ax,canvas))
examine_button = tk.Button(navigation_frame, text="examinar", command=lambda: ax_com.prev_section_index(fig,ax,canvas))






def on_combobox_select(event):
    dm = combobox.get()
    i  = ax_com.km_idx_dict.get(dm)
    ax_com.update_section_index(i)
    ax_com.plot_test(fig,ax,canvas)
    

combobox.bind("<<ComboboxSelected>>", on_combobox_select)


button_params = [
    {"label": "Estacado con Descriptor", "stringvar": fileA, "type":"file" },
    {"label": "Estacado con Coordenadas", "stringvar": fileB , "type":"file"},
    {"label": "Longitudinal", "stringvar": fileC , "type":"file"}
]

component.LoadFileFrame(tab6, title="Carga de Archivos", button_params = button_params)


button_params = [
    {"label":"Generar Modelo", "command":  lambda : ax_com.generate_model(fileA, fileB, fileC, combobox,fig, ax, canvas)},
#    {"label":"Graficar",       "command":  lambda : ax_com.plot_test(fig,ax,canvas)}
]
component.ButtonFrame(tab6, title="Generar Modelo", button_params=button_params)

combobox_frame.grid(column=0,row=0, padx=10, pady=10,)
navigation_frame.grid(column=1,row=0, padx=10, pady=10)

# canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)


combobox.pack(padx = 5, pady = 5)
plot_frame.pack()



#canvas.get_tk_widget().pack()
prev_button.grid(column=0,row=0)
next_button.grid(column=1,row=0)
canvas.get_tk_widget().pack(fill='both' , expand=True)
toolbar.pack()
canvasFrame.pack(fill='both',expand=True)




def on_closing():
    plt.close("all")  # Close all Matplotlib figures
    root.quit()       # Quit the Tkinter main loop
    root.destroy()    # Destroy the Tkinter root window

root.protocol("WM_DELETE_WINDOW", on_closing)  # Bind the close button to `on_closing`

# Main loop
root.mainloop()


