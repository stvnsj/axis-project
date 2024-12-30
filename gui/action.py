import model as md
import spreadsheet
import plotter
import reader as rd

# ANNEX
import annex.annex2    as annex2
import annex.annex4    as annex4
import annex.annex5    as annex5
import annex.annex8    as annex8
import annex.annex11   as annex11
import annex.annexAxis as annexAxis
import annex.annex     as annex
import annex.annexLong as annexLong


import config
import level
import dm


import refactorModel.model as model
import refactorCad.cad as cad

import spreadsheet.coordinates as coor
import spreadsheet.mop as mop
import spreadsheet.width as width

################
# GUI IMPORTS  #
################
from .notifier import Notifier
from .rootFrame import root
from .stringvar import *

####################
# EXTERNAL IMPORTS #
####################
from pathlib import Path
import traceback
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
from tkinter import filedialog

notif = Notifier(root)

#############
# FILENAMES #
#############
SAVE_FILENAME = {
    'name' : '',
    'extension' : '',
    'path' : '',
    'type' : '',
    'fullname' : ''
}

def notify_action (fun):
    def wrapper (*args, **kwargs):
        notif.open_output_window()
        notif.redirect_stdout()
        notif.redirect_stderr()
        try:
            fun(*args, **kwargs)
        except Exception as e:
            print(f'\n>> Error: {e}')
            traceback.print_exc()
        else:
            print("\n>> OPERACION TERMINADA CON EXITO")
            print(f"Archivo: {SAVE_FILENAME['name']}")
            print(f"Ruta: {SAVE_FILENAME['fullname']}")
        finally:
            notif.restore_stdout_stderr()   
    return wrapper



def save_filename (type,ext) :
    
    full_path = filedialog.asksaveasfilename(
        title="Nombre del Archivo",
        filetypes=((type, f"*.{ext}"), ("All files", "*.*"))
    )
    
    if full_path: 
        # Convert to a Path object
        path = Path(full_path)
        SAVE_FILENAME['path'] = str(path.parent)
        SAVE_FILENAME['name'] = path.name
        SAVE_FILENAME['extension'] = path.suffix
        SAVE_FILENAME['type'] = type
        SAVE_FILENAME['fullname'] = str(path)
        return SAVE_FILENAME
    
    else:
        return None
    


def save_action_factory (filetype='Text', extension='csv'):
    def action (func) :
        def wrapper (*args, **kwargs):
            if save_filename(filetype,extension) is None:
                return
            func(*args,**kwargs)
        return wrapper
    return action


def delete_load_file(field,stringvar):
    stringvar.set("")
    config.write_loaded_files(field, "")




######################################################
#  _______       ____      _____          _____      #
# |__   __|/\   |  _ \    / ____|   /\   |  __ \     #
#    | |  /  \  | |_) |  | |       /  \  | |  | |    #
#    | | / /\ \ |  _ <   | |      / /\ \ | |  | |    #
#    | |/ ____ \| |_) |  | |____ / ____ \| |__| |    #
#    |_/_/    \_\____/    \_____/_/    \_\_____/     #
######################################################
@save_action_factory("CAD Script" , 'scr')
@notify_action
def complete_cad():
    
    sl = stackLength.get()
    
    try:
        assert int(sl) > 0
    except:
        messagebox.showinfo("Alert", "El número de perfiles por fila debe ser un número >= 1")
        return
    
    model1 = model.Model(
        descriptor_file.get(),
        coordinate_file.get(),
        longitudinal_file.get()
    )
    
    cadScript = cad.CadScript(model1)
    cadScript.writeCompleteProject(
        SAVE_FILENAME['fullname'],
        stackSize=int(sl)
    )

@save_action_factory("CAD Script" , 'scr')
@notify_action
def generateCAD():
    
    m0 = meter0.get()
    m1 = meter1.get()
    sl = stackLength.get()
    
    try:
        assert int(sl) > 0
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
    
    
    model1 = model.Model(
        filename1 = descriptor_file.get(),   # DESCR
        filename2 = coordinate_file.get(),   # COOR
        filename3 = longitudinal_file.get(), # LONG
    )
    
    cadScript = cad.CadScript(model1)
    cadScript.writeKm(
        dm0 = m0,
        dm1 = m1,
        stackSize=int(sl),
        fn=SAVE_FILENAME['fullname']
    )


def generateFullCAD():
    
    try:
        assert int(stackLength.get()) >0
    except:
        messagebox.showinfo("Alert", "\'Perfiles por fila\' debe ser un entero >0")
        return
    
    
    try:
        assert int(chunkSize.get()) >0
    except:
        messagebox.showinfo("Alert", "\'Perfiles por Archivo\' debe ser un entero >0")
        return
    
    
    try:
        assert projectName.get() != ""
    except:
        messagebox.showinfo("Alert", "Debe ingresar un nombre de proyecto")
        return
    
    directory = filedialog.askdirectory()
    
    if directory == "":
        return 
    
    model1 = model.Model(
        descriptor_file.get(),
        coordinate_file.get(),
        longitudinal_file.get(),
    )
    
    cadScript = cad.CadScript(model1)
    cadScript.writeFull (directory, projectName.get(), fileSize = int(chunkSize.get()), stackSize = int(stackLength.get()))




@save_action_factory("Text",'csv')
@notify_action
def generateMOP ():
    "Generates the csv version of the 5.2.2 (MOP) annex."
    
    model1 = model.Model(
        filename1 = descriptor_file.get(),   # DESCR
        filename2 = coordinate_file.get(),   # COOR
        filename3 = longitudinal_file.get(), # LONG
    )
    
    coordinate_model = mop.MopFormat(model1)
    coordinate_model.write(SAVE_FILENAME['fullname'])

@save_action_factory("Text",'csv')
@notify_action
def action_coordinate_z() :
    "Generates the input coordinate file, with adjusted heights of the longitudinal file"
    
    model1 = model.Model(
        filename1 = descriptor_file.get(),   # DESCR
        filename2 = coordinate_file.get(),   # COOR
        filename3 = longitudinal_file.get(), # LONG
    )
    
    coordinate_model = coor.AdjustedCoordinateModel(model1)
    coordinate_model.writeCsv(SAVE_FILENAME['fullname'])

@save_action_factory("Text",'csv')
@notify_action
def generateAnchos() :
    
    model1 = model.Model(
        filename1 = descriptor_file.get(),   # DESCR
        filename2 = coordinate_file.get(),   # COOR
        filename3 = longitudinal_file.get(), # LONG
    )
    
    width_model = width.ModelWidth(model1)
    width_model.write(SAVE_FILENAME['fullname'])



####################################################################
#  _______       ____     _      ________      ________ _          #
# |__   __|/\   |  _ \   | |    |  ____\ \    / /  ____| |         #
#    | |  /  \  | |_) |  | |    | |__   \ \  / /| |__  | |         #
#    | | / /\ \ |  _ <   | |    |  __|   \ \/ / |  __| | |         #
#    | |/ ____ \| |_) |  | |____| |____   \  /  | |____| |____     #
#    |_/_/    \_\____/   |______|______|   \/   |______|______|    #
####################################################################

@save_action_factory("Text",'csv')
@notify_action
def generate_report():
    cir = level.parser(
        libreta_file.get(),
        pr_height_file.get(),
        trigonometric_file.get()
    )
    cir.write_circuit_table(SAVE_FILENAME['fullname'])

@save_action_factory("Text",'csv')
@notify_action
def generate_longitudinal(): 
    cir = level.parser(
        libreta_file.get(),
        pr_height_file.get(),
        trigonometric_file.get()
    )
    cir.write_longitudinal(SAVE_FILENAME['fullname'])

@save_action_factory("CAD Script",'scr')
@notify_action
def generate_height_cad():    
    cir = level.parser(
        libreta_file.get(),
        pr_height_file.get(),
        trigonometric_file.get()
    )
    cir.plot(SAVE_FILENAME['fullname'])











################################
#  _____  _      ____ _______  #
# |  __ \| |    / __ \__   __| #
# | |__) | |   | |  | | | |    #
# |  ___/| |   | |  | | | |    #
# | |    | |___| |__| | | |    #
# |_|    |______\____/  |_|    #
################################

trans_model = None
min_index = 0
max_index = 0
section_index = 0
km_idx_dict = {}

def update_section_index (new_index) :
    global section_index
    section_index = new_index

def examine_section (fig,ax):
    global trans_model
    global section_index
    if trans_model is None:
        return
    plttr = plotter.Plotter(trans_model)
    plttr.plot_section2(section_index,fig,ax)

def get_plot_dm (PLOT_DM) :
    global trans_model
    global section_index
    if trans_model is not None:
        PLOT_DM.set(trans_model.getSection(i).km)

def next_section_index (fig,ax,canvas, plot_dm):
    global trans_model
    global section_index
    global max_index
    if trans_model is None or section_index == max_index:
        return
    section_index += 1
    plot_test(fig,ax,canvas)
    plot_dm.set(trans_model.getSection(section_index).km)

def prev_section_index (fig,ax,canvas,plot_dm) :
    global trans_model
    global section_index
    global min_index
    if trans_model is None or section_index == min_index:
        return
    section_index -= 1
    plot_test(fig,ax,canvas)
    plot_dm.set(trans_model.getSection(section_index).km)

def generate_model (fileA,fileB,fileC,combobox, fig, ax, canvas):
    global max_index
    global trans_model
    global km_idx_dict
    if not (fileA.get() or fileB.get()):
        return
    
    reader = rd.Reader (fileA.get(), fileB.get(), fileC.get())
    matrix, labels, om, ol, heights = reader.getData()
    trans_model = md.Model(heights,matrix,labels, om, ol)
    max_index = len(trans_model.sectionIndex) - 1
    km_idx_dict.update(trans_model.get_km_index_dict())
    options = [km for km in km_idx_dict]
    combobox['values'] = options
    plot_test(fig,ax,canvas)
    


def plot_test (fig,ax,canvas):
    global trans_model
    plttr = plotter.Plotter(trans_model)
    plttr.plot_section(section_index,fig,ax,canvas)




#############################################################################
#  _____  __  __            _   _          _  __     _______ _____  _____   #
# |  __ \|  \/  |     /\   | \ | |   /\   | | \ \   / / ____|_   _|/ ____|  #
# | |  | | \  / |    /  \  |  \| |  /  \  | |  \ \_/ / (___   | | | (___    #
# | |  | | |\/| |   / /\ \ | . ` | / /\ \ | |   \   / \___ \  | |  \___ \   #
# | |__| | |  | |  / ____ \| |\  |/ ____ \| |____| |  ____) |_| |_ ____) |  #
# |_____/|_|  |_| /_/    \_\_| \_/_/    \_\______|_| |_____/|_____|_____/   #
#############################################################################
def get_dm_analysis ():
        
    filename = filedialog.asksaveasfilename(
        
        title="Nombre de Archivo",
        filetypes=(("Excel", "*.xlsx"), ("All files", "*.*"))
    )
        
    if filename == "":
        return
        
    dm.process_dm (
        f1=eje_estaca_file.get(),   #Archivo de "EJE ESTACA"
        f2=trans_coor_file.get(),   #Archivo de Perfiles transversales con coordenadas
        f3=trans_desc_file.get(),   #Archivo de Perfiles Transversales con descriptor
        f4=libreta_file.get(),      #Archivo de Libreta
        f5=trig_file.get(),         #Archivo de Parche Trigonometrico
        filename = filename 
    )  



#################################################################
#  _______       ____              _   _ _   _ ________   __    #
# |__   __|/\   |  _ \       /\   | \ | | \ | |  ____\ \ / /    #
#    | |  /  \  | |_) |     /  \  |  \| |  \| | |__   \ V /     #
#    | | / /\ \ |  _ <     / /\ \ | . ` | . ` |  __|   > <      #
#    | |/ ____ \| |_) |   / ____ \| |\  | |\  | |____ / . \     #
#    |_/_/    \_\____/   /_/    \_\_| \_|_| \_|______/_/ \_\    #
#################################################################

@save_action_factory("Excel",'xlsx')
@notify_action
def generate_eje_estaca():
    annexAxis.generate(eje_estaca_file.get(), SAVE_FILENAME['fullname'])

@save_action_factory("Excel",'xlsx')
@notify_action
def generate_anexo_trans() :
    reader = rd.Reader (descriptor_file.get(), coordinate_file.get(), longitudinal_file.get())
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    annex.trans(model,SAVE_FILENAME['fullname'])
    
@save_action_factory('Excel','xlsx')
@notify_action
def generate_annex_long ():
    """Generates ANNEX 2.5.3"""
    annexLong.generate(
        libreta_file.get(),
        pr_height_file.get(),
        trigonometric_file.get(),
        SAVE_FILENAME['fullname']
    )

@save_action_factory("Excel",'xlsx')
@notify_action
def generate_annex_2 ():
    annex2.generate(
        master_table_file.get(),
        SAVE_FILENAME['fullname'],
        src_dir=img_dir1.get(),
        src_dir2=img_dir2.get()
    )

@save_action_factory("Excel",'xlsx')
@notify_action
def generate_annex_4 ():
    annex4.generate(
        master_table_file.get(),
        SAVE_FILENAME['fullname']
    )

@save_action_factory("Excel",'xlsx')
@notify_action
def generate_annex_5 ():
    annex5.generate(
        master_table_file.get(),
        SAVE_FILENAME['fullname'],
        src_dir=img_dir1.get(),
        src_dir2=img_dir2.get()
    )

@save_action_factory("Excel",'xlsx')
@notify_action
def generate_annex_8 ():
    annex8.generate(
        master_table_file.get(),
        SAVE_FILENAME['fullname']
    )

@save_action_factory("Excel",'xlsx')
@notify_action
def generate_annex_9 ():
    annex9.generate(
        master_pr_file.get(),
        SAVE_FILENAME['fullname']
    )

@save_action_factory("Excel",'xlsx')
@notify_action
def generate_annex_11 ():
    annex11.generate(
        pr_level_file.get(),
        SAVE_FILENAME['fullname']
    )

