#################################################################################

#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
from tkinter.filedialog import askopenfilename
from _ast import operator
from tkinter.messagebox import *
from VUtil import VerticalScrolledFrame


try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    
    import tkinter.filedialog as tkFileDialog
    import tkinter.simpledialog as tkSimpleDialog    #askstring()

################################################################################
##global variables

mainDir     = "f:/useless.txt"
Gentries    = []
Gtextvars   = []

dictionaries = []
dict_name    = []

################################################################################
def updateInfo(dir):
  global dict_number
  dict_number = -1
  if dir != "":
      fo      = open(dir, "r")
      fo.readline()
      for linea in fo:
        tag = linea[0:2]
        if tag == '#@':
          dict_number = dict_number + 1
          dictionaries.append({})
          dict_name.append(linea[2:])
        else:
          if linea[0] != "#" and linea[0] != "\n":
              pos = linea.find(":")
              key = linea[:pos]
              val = linea[pos+1:].strip()
              dictionaries[dict_number][key] = val
      fo.close()
#def updateinfo
################################################################################
def colectInfo(valu):
    out = ""
    pos = 0
    posd= 0
    for dictionary in dictionaries: 
      out   += '#@' + dict_name[posd]
      posd  += 1
      for name in sorted(dictionary):
        valf = Gentries[pos].get()
        valf = valf.replace("{i}",str(valu))
        out += name + ": " + valf + "\n"   
        pos += 1
    return out
#def updateinfo
#################################################################################
def save_olds() :
    fo      = open("./saveold", "w")
    fo.write(entry.get())
    fo.write("\n")
    fo.write(entry3.get())
    fo.close()

#def save_olds
#################################################################################

def xfrange(start, stop, step):
    while start < stop:
        yield start
        start += step
#def xrange
################################################################################
def generate() :
    out     = ""
    batOut  = "@echo off\n"
    pos     = 0
    fexe   = entry.get().replace("\n"," ")
    outbat  = entry3.get() + "/" + entry2.get() + ".bat"
    try:
        out_fileb = open(outbat, "w")
        out_fileb.write(batOut)
        
        ini = float( ent_ini.get() )
        fin = float( ent_fin.get() )
        incr = float( ent_incr.get() )
        
        if ini == fin:

          tok = str("{0:0.3f}".format(ini))
          tok = tok.replace('.','_')
          outyml  = entry3.get() + "/" + entry4.get() + tok +".yml"
          batOut  = fexe + " " + outyml + "\n"  
          out_fileb.write(batOut)  
  
          out = colectInfo(ini)
          out_filey = open(outyml, "w")
          out_filey.write('%YAML:1.0\n')
          out_filey.write(out)
          out_filey.close()
        #if
        else:
          r = xfrange(ini,fin,incr)
          for x in r:
            tok = str("{0:0.1f}".format(x))
            tok = tok.replace('.','_')
            outyml  = entry3.get() + "/" + entry4.get() + '_' + tok +".yml"
            batOut  = fexe + " " + outyml + "\n"  
            out_fileb.write(batOut)

            out = colectInfo(x)
            out_filey = open(outyml, "w")
            out_filey.write('%YAML:1.0\n')
            out_filey.write(out)
            out_filey.close()
          #for
        #else
        out_fileb.close()
        messagebox.showinfo("info", "All Saved")
    except:
        messagebox.showinfo("info", "No Info")   
    save_olds()

#def generate
#################################################################################
def load_olds() :
  fo    = open("./saveold", "r")
  vars  = [] 
  for line in fo:
    if len(line) > 1:
      vars.append(line)
    #
  #for
  fo.close()
  if len(vars) > 1:
    entry.insert(0,vars[0])
    entry3.insert(0,vars[1]) 
  #if
#def load_olds
###############################################################################
def createControlReg(frame, cmd, title):
    
  labelframe_ex = LabelFrame(frame, text = title)
  labelframe_ex.pack()
  
  entry = Entry(labelframe_ex, width=57)
  entry.pack(side = LEFT)

  Button(labelframe_ex,text="File .exe",command = cmd).pack(side = RIGHT, fill = Y)

  return entry
#end createcontrolreg
###############################################################################
def createControlInputs(frame):
  global ent_ini, ent_fin, ent_incr, entry2, entry4

  labelframe_vals = LabelFrame(frame, text = "Output Values")
  labelframe_vals.pack(fill = BOTH)

  line = 0
  Label(labelframe_vals, text="Bat file out:").grid(row = line, column = 0, padx = 5)
  entry2 = Entry(labelframe_vals, width = 55)
  entry2.grid(row = line, column = 1)
  entry2.insert(0,"batOut")
  line +=1
  
  Label(labelframe_vals, text="Yml file out:").grid(row = line, column = 0, padx = 5)
  entry4 = Entry(labelframe_vals, width = 55)
  entry4.grid(row = line, column = 1)
  entry4.insert(0,"test")
  line +=1

  Label(labelframe_vals, text="Start:            ").grid(row = line, column = 0, padx = 5)
  ent_ini = Entry(labelframe_vals, width=55)
  ent_ini.grid(row = line, column = 1)
  ent_ini.insert(0,"1")
  line +=1

  Label(labelframe_vals, text="Increment:  ").grid(row = line, column = 0, padx = 5)
  ent_incr = Entry(labelframe_vals, width=55)
  ent_incr.grid(row = line, column = 1)
  ent_incr.insert(0,"1")
  line +=1

  Label(labelframe_vals, text="Final:            ").grid(row = line, column = 0, padx = 5)
  ent_fin = Entry(labelframe_vals, width=55)
  ent_fin.grid(row = line, column = 1)
  ent_fin.insert(0,"1")
  line +=1
#def createControlInputs
###############################################################################
def createControlButtons(frame):

  labelframe_butt = LabelFrame(frame, text = "Buttons")
  labelframe_butt.pack(fill = BOTH)
  b2 = Button(labelframe_butt,text="Generate \n Bat files",command=generate, width = 10).pack(fill= BOTH)

#def createControlButtons
###############################################################################
def createHeader(frame) :

    global entry, entry3

    #executable file...........................................................
    entry   = createControlReg(frame, load_file, "Executable file")    

    #directory out.............................................................
    entry3  = createControlReg(frame, load_file2, "Directory Output")    
    
    #main input................................................................
    createControlInputs(frame)

    #buttons...................................................................
    createControlButtons(frame)
           
    load_olds()
#def createHeader        
################################################################################
def createGrid(frame, dict_cont):
  
  cont = 1

  Label(frame, text="Variables").grid(row=cont, column=0, sticky=W, padx = 10, pady =2)
  Label(frame, text="Values").grid(row=cont, column=1, sticky=W, padx = 10, pady =2)
  cont += 1

  for name in sorted(dictionaries[dict_cont]) :
      Label(frame, text=name).grid(row=cont, column=0, sticky=W, padx = 10, pady = 2)
      nameVar = StringVar(value = dictionaries[dict_cont][name])
      Gtextvars.append(nameVar)
      entryg = Entry(frame, textvariable= nameVar, width=35)
      entryg.grid(row=cont, column=1, sticky=W, columnspan = 3)
      Gentries.append(entryg)
      cont    += 1
  #for
  
  Label(frame, text="").grid(row=cont, column=0, sticky=W, padx = 10, pady =2)

#def reategrid
################################################################################
def load_file():
    fname = tkFileDialog.askopenfilename()
    if fname !="":
        #try:
        print(fname)
        entry.delete(0,END)
        entry.insert(0,fname)
        #except:                     # <- naked except is a bad idea
        #showerror("Open Source File", "Failed to read file\n'%s'" % fname)
    return fname
################################################################################
def load_file2():
    fname = tkFileDialog.askdirectory()
    if fname !="":
        #try:
        print(fname)
        entry3.delete(0,END)
        entry3.insert(0,fname)
        #except:                     # <- naked except is a bad idea
        #showerror("Open Source File", "Failed to read file\n'%s'" % fname)
    return fname
################################################################################
# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
######################################################################################
######################################################################################
######################################################################################

class SampleApp(Tk): 
  def __init__(self, *args, **kwargs):
    root = Tk.__init__(self, *args, **kwargs)

    master = Frame(root, name='master') # create Frame in "root"
    master.pack(fill=BOTH) # fill both sides of the parent
     
               
    nb = Notebook(master, name='nb') # create Notebook in "master"
    nb.pack(fill=BOTH, padx=2, pady=3) # fill "master" but pad sides
     
    master_buttons = Frame(nb, name='master-foo')
    
    nb.add(master_buttons, text="Actions\n") # add tab to Notebook

    createHeader(master_buttons)   
    
    #tabs build
    dict_cont = 0
    for dict in dictionaries:
      master_bar = VerticalScrolledFrame(master, name='master-bar'+str(dict_cont))
      createGrid(master_bar.interior, dict_cont)
      nb.add(master_bar, text=dict_name[dict_cont])
      dict_cont += 1
#class sampleapp
######################################################################################
######################################################################################

if __name__ == "__main__":
   
    
  #................................................................................
  updateInfo(mainDir)
  app = SampleApp()
  app.mainloop()   
            