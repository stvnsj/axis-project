import level
import component 
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage,Label
import numpy as np
import reader as rd
import cad
import spreadsheet
import model as md
import command as cmd
import annex 
from tkinter import ttk
from tkinter.ttk import Style
from tkinter import messagebox
from tkinter import filedialog
import annex2
import annex5
import annex4
import annex8
import annex9
import annex11
import annexLong
import axisCommands as ax_com
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from tkinter.filedialog import asksaveasfile
import sys
from gui import root


trans_model = None


class RedirectStdoutToText:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.configure(state="normal")
        self.text_widget.delete(1.0, tk.END)  # Clear previous output
        self.text_widget.configure(state="disabled")
    
    def write(self, message):
        # Append text to the Text widget
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, message)
        self.text_widget.configure(state="normal")
        self.text_widget.see(tk.END)  # Scroll to the end
    
    def flush(self):
        pass  # Required for compatibility with Python's stdout


def generate_annex_2 ():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    
    annex2.generate(master_table_file.get(),filename,src_dir=img_dir1.get(), src_dir2=img_dir2.get())
    



def generate_annex_4 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex4.generate(master_table_file.get(),filename)



class Notifier :
    def __init__ (self,root):
        pass
    
    

#COMMAND NEEDS A ROOT
def generate_annex_5 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex5.generate(master_table_file.get(),filename,src_dir=img_dir1.get(), src_dir2=img_dir2.get())
    
    new_window = tk.Toplevel(root)
    new_window.title("EQC - Reporte")
    new_window.geometry("400x300")
    
    # Add a Text widget for displaying output
    text_area = tk.Text(new_window, bg="lightyellow", wrap="word", state="normal")
    text_area.pack(expand=True, fill="both")
    
    # Redirect stdout to the Text widget
    sys.stdout = RedirectStdoutToText(text_area)
    annex5.generate(master_table_file.get(),filename,src_dir=img_dir1.get(), src_dir2=img_dir2.get())
    sys.stdout = sys.__stdout__



def generate_annex_8 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex8.generate(master_table_file.get(),filename)

def generate_annex_9 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex9.generate(master_pr_file.get(),filename)

def generate_annex_11 ():
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.xlsx"), ("All files", "*.*"))
    )
    if filename == "":
        return 
    annex11.generate(pr_level_file.get(),filename)


def generate_report():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.csv *.txt"), ("All files", "*.*"))
    )
    
    if filename == "":
        return 
    
    cir = level.parser(libreta_file.get(),pr_height_file.get(),trigonometric_file.get())
    cir.write_circuit_table(filename)
    
def generate_longitudinal():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.csv *.txt"), ("All files", "*.*"))
    )
    
    if filename == "":
        return 
    
    cir = level.parser(libreta_file.get(),pr_height_file.get(), trigonometric_file.get())
    cir.write_longitudinal(filename)

def generate_height_cad():
    
    filename = filedialog.asksaveasfilename(
        title="Nombre de Archivo",
        filetypes=(("Text files", "*.scr"), ("All files", "*.*"))
    )
    
    if filename == "":
        return 
    
    cir = level.parser(libreta_file.get(),pr_height_file.get(),trigonometric_file.get())
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
    
    reader = rd.Reader (descriptor_file.get(), coordinate_file.get(), longitudinal_file.get())
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
    
    
    reader = rd.Reader (descriptor_file.get(), coordinate_file.get(), longitudinal_file.get())
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
    
    
    reader = rd.Reader (descriptor_file.get(), coordinate_file.get(), longitudinal_file.get())
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
    
    
    
    reader = rd.Reader (descriptor_file.get(), coordinate_file.get(), longitudinal_file.get())
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
    
    reader = rd.Reader (descriptor_file.get(), coordinate_file.get(), longitudinal_file.get())
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
    
    reader = rd.Reader (descriptor_file.get(), coordinate_file.get(), longitudinal_file.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    
    cadScript = cad.CadScript(model)
    cadScript.writeFull (directory, inputs[2].get(), fileSize = int(inputs[1].get()), stackSize = int(inputs[0].get()))


# Create main window

root.title("Proyecto AXIS")
root.geometry("1200x950")


# Create a Notebook widget (tabs container)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

#s = Style()
#s.configure('My.TFrame', background='#111111')


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

# bg = PhotoImage(file = "G94_g.png")
# bg_image = Label( tab1, image = bg) 
# bg_image.place(x = 0, y = 0) 


descriptor_file = tk.StringVar() # TRANS DESCRIPTOR
coordinate_file = tk.StringVar() # TRANS COORDENADA
longitudinal_file = tk.StringVar() # Longitudinal FILE

plot_index = tk.StringVar() # Current 

eje_estaca_file = tk.StringVar() 

img_dir1 = tk.StringVar()
img_dir2 = tk.StringVar()

master_table_file = tk.StringVar()
pr_level_file  = tk.StringVar() 

pr_height_file = tk.StringVar()
libreta_file   = tk.StringVar()
trigonometric_file = tk.StringVar()

master_pr_file = tk.StringVar()

meter0 = tk.StringVar()
meter1 = tk.StringVar()


descriptor_file_param = {"label": "Estacado con Descriptor", "stringvar": descriptor_file, "type":"file" , "field": 'estacado-descriptor'}
coordinate_file_param = {"label": "Estacado con Coordenadas", "stringvar": coordinate_file , "type":"file", 'field': "estacado-coordenadas"}
longitudinal_file_param = {"label": "Longitudinal", "stringvar": longitudinal_file , "type":"file", 'field': 'longitudinal'}
pr_height_file_param = {"label": "Cotas Topograficas", "stringvar": pr_height_file , "type":"file", 'field':'cotas-pr'}
libreta_file_param = {"label": "Circuito Nivelación", "stringvar": libreta_file , "type":"file", 'field':'libreta'}
trigonometric_file_param = {"label": "Alturas Trigonométricas", "stringvar": trigonometric_file, "type":"file", 'field':'trigonometrica'}
master_table_file_param = {"label":"Anexo 1 (Tabla Maestra)", "stringvar": master_table_file ,  "type":"file", "field":"anexo-1"}
master_pr_file_param = {"label":"Tabla Maestra PR", "stringvar": master_pr_file ,  "type":"file", "field":"master-pr"}
pr_level_file_param = {"label":"Anexo 10 (Nivelación)"  , "stringvar": pr_level_file , "type":"file", "field":"anexo-10"}
img_dir1_param = {"label":"Imagenes (Pan. Det.)"   , "stringvar": img_dir1 , "type":"dir", "field":'fotos'}
img_dir2_param = {"label":"Imagenes (Geo.)"        , "stringvar": img_dir2 , "type":"dir", "field":'georef'}
eje_estaca_file_param = {"label":"Eje Estaca", "stringvar": eje_estaca_file, "type":"file", "field":'eje-estaca'}


################
# ############ #
# # CAD TAB1 # #
# ############ #
################

button_params = [
    descriptor_file_param,
    coordinate_file_param,
    longitudinal_file_param
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
    pr_height_file_param,
    libreta_file_param,
    trigonometric_file_param,
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

button_params = [descriptor_file_param, coordinate_file_param, longitudinal_file_param]
component.LoadFileFrame(tab4, title="Carga de Archivos Estacado", button_params = button_params)


button_params = [
    {"label":"2 - Perfiles Transversales (2.5.2)", "command":generate_anexo_trans},
]
component.ButtonFrame(tab4, title="Generación de Anexos (DEFINITIVO)", button_params=button_params)


button_params = [pr_height_file_param,libreta_file_param,trigonometric_file_param]
component.LoadFileFrame(tab4, title="Carga de Archivos Nivelación", button_params = button_params)

button_params = [
    {"label":"3 - Nivelación Longitudinal del Eje Estacado (2.5.3)",
     "command": ax_com.generate_annex_long(libreta_file, pr_height_file, trigonometric_file)},
]
component.ButtonFrame(tab4, title="Generación de Anexos (DEFINITIVO)", button_params=button_params)



########################
# ANEXO ANTEPROYECTO   #
########################
button_params = [
    master_table_file_param,
    master_pr_file_param,
    pr_level_file_param,
    img_dir1_param,
    img_dir2_param,
]

component.LoadFileFrame(tab3, title='Carga de Anexos', button_params=button_params)

# 2 , 4 , 8 , 11
button_params = [
    {"label":"2 - Puntos de la Red de Referencia Principal (2.903.3.F)", "command":generate_annex_2},
    {"label":"4 - Resumen de Coordenadas de la Red de Referencia Principal (2.903.3.G)", "command":generate_annex_4},
    {"label":"5 - Formulario de Ubicación de Vértices del STC (2.303.104.A)", "command":generate_annex_5},
    {"label":"8 - Coordenadas de Vértices del STC (2.303.104.B)", "command":generate_annex_8},
    {"label":"9 - Monografías de PR", "command":generate_annex_9},
    {"label":"11 - Cotas de PR (2.903.3.I)", "command":generate_annex_11},
]
component.ButtonFrame(tab3, title="Generación de Anexos (ANTEPROYECTO)", button_params=button_params)


###############
# DM ANALYSIS #
###############



button_params = [
    eje_estaca_file_param,
    descriptor_file_param,
    coordinate_file_param,
    libreta_file_param,
    trigonometric_file_param,
]  
component.LoadFileFrame(tab5, title='Carga de Archivos', button_params=button_params)

button_params = [
    {"label":"Analisis DM", "command":ax_com.get_dm_analysis(eje_estaca_file,descriptor_file,coordinate_file,libreta_file,trigonometric_file)},
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


fig, ax = plt.subplots(figsize=(11, 11))
# Contains the PLOT buttons and menus.
plot_frame = tk.Frame(tab6)
# Contains the combobox menu.
combobox_frame = ttk.LabelFrame(plot_frame, text="Perfil Transversal")
# Combox menu to select a cross section DM.
combobox = ttk.Combobox(combobox_frame, values=[])
# Contains the "siguiente" and "previo" buttons.
navigation_frame = ttk.LabelFrame(plot_frame, text="Navegar Perfiles")
# Plots the next cross section.
next_button = tk.Button(navigation_frame, text="siguiente", command=lambda: ax_com.next_section_index(fig,ax,canvas,plot_index))
# Plots the previous cross section
prev_button = tk.Button(navigation_frame, text="previo", command=lambda: ax_com.prev_section_index(fig,ax,canvas, plot_index))

# DM Frame.
dm_frame   = ttk.LabelFrame(plot_frame, text="DM")
dm_display = tk.Label(dm_frame, textvariable=plot_index, bg='white', bd=1, relief="solid", width=10,anchor="w")


# Contains the PLOT and the Matplotlib Navigation Bar
canvasFrame = tk.Frame(tab6,bd=5,relief='groove',bg='#BBBBBB')
# This frame contains the PLOT
canvas = FigureCanvasTkAgg(fig, master=canvasFrame)
# Contains the Navigation BAR
toolbar = NavigationToolbar2Tk(canvas, canvasFrame)

def on_combobox_select(event):
    dm = combobox.get()
    i  = ax_com.km_idx_dict.get(dm)
    ax_com.update_section_index(i)
    ax_com.plot_test(fig,ax,canvas)
    plot_index.set(dm)

combobox.bind("<<ComboboxSelected>>", on_combobox_select)

button_params = [
    descriptor_file_param,
    coordinate_file_param,
    longitudinal_file_param,
]
component.LoadFileFrame(tab6, title="Carga de Archivos", button_params = button_params)

button_params = [
    {"label":"Generar Modelo", "command":  lambda : ax_com.generate_model(descriptor_file, coordinate_file, longitudinal_file, combobox,fig, ax, canvas)},
#    {"label":"Graficar",       "command":  lambda : ax_com.plot_test(fig,ax,canvas)}
]
component.ButtonFrame(tab6, title="Generar Modelo", button_params=button_params)

combobox_frame.grid(column=0,row=0, padx=10, pady=10,)
navigation_frame.grid(column=1,row=0, padx=10, pady=10)
dm_frame.grid(column=2, row=0, padx = 10, pady=10)

# canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)


plot_frame.pack()


combobox.pack(padx = 5, pady = 5)
#canvas.get_tk_widget().pack()
prev_button.grid(column=0,row=0)
next_button.grid(column=1,row=0)
dm_display.pack()
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


