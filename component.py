
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

class ButtonFrame(tk.Frame):
        
    def __init__ (self, parent, title="Load File", button_params = [],side="top"):
        
        super().__init__(parent,pady=3,padx=3,bd=3,relief="groove")
        self.row = 0
        self.pack(side=side,pady=5)
        self.insert_title(title)
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack()
        for param in button_params:
            self.insert_button(param["label"],param["command"])
            self.row += 1
 
    def insert_title(self, title):
        label_title = tk.Label(self, text = title,font='Helvetica 10 bold', pady=4,padx=4,bd=3, relief="ridge")
        label_title.pack(pady=3,padx=3)
 
    def insert_button (self, label, command=lambda:print("ButtonFrame button")):
        
        label     = tk.Label(self.frame_grid,  text=label, font='Helvetica 10 italic', width=26, anchor="w")
        button    = tk.Button(self.frame_grid, text="Generar", command=command)
        
        label.grid(row=self.row,column=0)
        button.grid(row=self.row,column=1)
        
    
    def load_file_command(self,stringvar) :
        pass
    
    

class LoadFileFrame(tk.Frame):
    
    def __init__ (self, parent, title="Load File", button_params = [], pady = 3):
        
        super().__init__(parent,pady=pady,padx=3,bd=3,relief="groove")
        self.row = 0
        self.pack(pady=5)
        self.insert_title(title)
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack()
        for param in button_params:
            self.insert_button(param["label"],param["stringvar"],typ=param["type"])
            self.row += 1
 
    def insert_title(self, title):
        label_title = tk.Label(self, text = title,font='Helvetica 10 bold', pady=4,padx=4,bd=3, relief="ridge")
        label_title.pack(pady=3,padx=3)
 
    def insert_button (self, label, stringvar, typ = "file"):
        if typ == "file":
            button    = tk.Button(self.frame_grid, text="Cargar", command=lambda:self.load_file_command(stringvar))
        elif typ == "dir":
            button    = tk.Button(self.frame_grid, text="Cargar", command=lambda:self.load_dir_command(stringvar))            
        label     = tk.Label(self.frame_grid,  text=label, font='Helvetica 10 italic', width=26, anchor="w")
        filelabel = tk.Label(self.frame_grid, textvariable=stringvar, bg='white', bd=1, relief="solid", width=50,anchor="w")
        
        button.grid(row=self.row,column = 0)
        label.grid(row=self.row,column=1)
        filelabel.grid(row=self.row,column=2)
    
    def load_file_command(self,stringvar) :
        path = filedialog.askopenfilename(
            title="Seleccione archivo",
            filetypes=(("Text files", "*.csv *.txt *.CSV *.TXT *.xlsx"), ("All files", "*.*"))
        )
        stringvar.set(path)
 
    def load_dir_command(self,stringvar) :
        path = filedialog.askdirectory(title="Seleccionar Directorio")
        stringvar.set(path)
    
    

class InputFrame(tk.Frame):
    
    
    
    def __init__ (self, parent , title="Input Frame", entry_params = [], command=lambda x:print("HELLO WORLD"),side="top"):
        
        super().__init__(parent,pady=3,padx=3,bd=3,relief="groove")
        self.row = 0
        self.pack(side=side,pady=5, padx=20)
        self.insert_title(title)
        self.inputs = []
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack()
        
        for param in entry_params:
            self.inputs.append(self.insert_entry(param["label"]))
            self.row += 1
        
        self.insert_button(command=command) 
 
    def insert_entry(self,label):
        
        entry_box   = tk.Entry(self.frame_grid)
        entry_label = tk.Label(self.frame_grid, text = label,width=15, anchor="w")
        
        entry_box.grid(row=self.row,column = 0)
        entry_label.grid(row=self.row,column=1)
        return entry_box
    
    def insert_title(self, title):
        label_title = tk.Label(self, text = title, font='Helvetica 10 bold', pady=4,padx=4,bd=3, relief="ridge")
        label_title.pack(pady=3,padx=3)
 
 
    def insert_button(self,command,text="Generar"):
        
        button = tk.Button(self, text=text, command=lambda:command(self.inputs), pady=5)
        button.pack()
        
    
    def get_input(self,i):
        return self.inputs[i]



