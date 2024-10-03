
import level
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


class LoadFileFrame(tk.Frame):
    
    def __init__ (self, parent, title="Load File", button_params = []):
        
        super().__init__(parent,pady=10,padx=10,bd=3,relief="groove")
        self.row = 0
        self.pack()
        self.insert_title(title)
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack()
        for param in button_params:
            self.insert_button(param["label"],param["stringvar"])
            self.row += 1
 
    def insert_title(self, title):
        label_title = tk.Label(self, text = title,pady=10,font='Helvetica 10 bold')
        label_title.pack()
 
    def insert_button (self, label, stringvar):
        button    = tk.Button(self.frame_grid, text="Cargar", command=lambda:self.load_file_command(stringvar))
        label     = tk.Label(self.frame_grid,  text=label, font='Helvetica 10 bold')
        filelabel = tk.Label(self.frame_grid, textvariable=stringvar)
        
        button.grid(row=self.row,column = 0)
        label.grid(row=self.row,column=1)
        filelabel.grid(row=self.row,column=2)
    
    def load_file_command(self,stringvar) :
        path = filedialog.askopenfilename(title="Seleccione archivo")
        stringvar.set(path)
    

class InputFrame(tk.Frame):
    
    def __init__ (self, parent , entry_params = [], command=lambda x:print("HELLO WORLD")):
        
        super().__init__(parent,pady=10,padx=10,bd=3,relief="groove")
        self.row = 0
        self.pack(pady=10, padx=20)
        self.insert_title()
        self.inputs = []
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack()
        
        for param in entry_params:
            self.inputs.append(self.insert_entry(param["label"]))
            self.row += 1
        
        self.insert_button(command=command) 
 
    def insert_entry(self,label):
        entry_box   = tk.Entry(self.frame_grid)
        entry_label = tk.Label(self.frame_grid, text = label)
        
        entry_box.grid(row=self.row,column = 0)
        entry_label.grid(row=self.row,column=1)
        return entry_box
    
    def insert_title(self):
        label_title = tk.Label(self, text = "Frame Title",pady=10,font='Helvetica 10 bold')
        label_title.pack()
 
 
    def insert_button(self,command,text="boton"):
        
        button = tk.Button(self, text=text, command=lambda:command(self.inputs), pady=10)
        button.pack()
        
    
    def get_input(self,i):
        return self.inputs[i]
 



