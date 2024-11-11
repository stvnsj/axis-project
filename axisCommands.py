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
import dm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import plotter




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

def get_dm_analysis (eje_estaca_file,trans_desc_file,trans_coor_file,libreta_file,trig_file):
    
    def fun ():
        
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
    
    return fun




# circuit_file.get(),height_pr_file.get(), trigonometric_file.get(), filename
def generate_annex_long (libreta_file, pr_file, trig_file):
    """Generates ANNEX 2.5.3"""
    
    def fun ():
        
        filename = filedialog.asksaveasfilename(
            title="Nombre de Archivo",
            filetypes=(("Excel", "*.xlsx"), ("All files", "*.*"))
        )
        
        if filename == "":
            return
        
        annexLong.generate(libreta_file.get(),pr_file.get(), trig_file.get(), filename)
    
    return fun
