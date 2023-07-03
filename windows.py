import tkinter as Tk
from tkinter import *
import tkinter.filedialog 
import os


def save_txt(parent):
	os.chdir(parent.workdir)
	text=parent.Notes.get("1.0","end")
	name_answer = str(parent.name_entry.get())
	filetowrite = open(name_answer,'a')
	filetowrite.write(text)
	parent.ask_name.destroy()
	return
	
def newdir_name(parent):
	parent.name_answer = str(parent.name_entry.get())
	parent.ask_name.destroy()
	print("pret")
	return
	
def plot_name(parent):
	return

def get_title(parent,fonction):
	parent.ask_name = Tk()
	parent.ask_name.title("Paramètres")
	label_axe_x = Label(parent.ask_name, text="entrer un nom pour le fichier").grid(row = 0, column = 1)
	parent.name_entry = Entry(parent.ask_name, borderwidth=2, relief=GROOVE)
	parent.name_entry.grid(row = 0, column = 2)
	parent.valid_name = Button(parent.ask_name, borderwidth=2, relief=GROOVE, command =lambda: fonction(parent))
	parent.valid_name.grid(row = 0, column = 3)
	return()


def get_liss_params():
	liss_params = Tk()
	data = Data_temp()
	liss_params.title("Paramètres du lissage")
	liss_params.order = 1
	label_ask_order = Label(liss_params, text="entrer un ordre pour le lissage").grid(row = 0, column = 1)
	is_ponderated = Checkbutton(liss_params)
	is_ponderated.grid(row = 0, column = 3)
	name_entry = Entry(liss_params, borderwidth=2, relief=GROOVE)
	name_entry.grid(row = 1, column = 2)
	def print_close():
		liss_params.name=(str(name_entry.get()))
		data.value = (str(name_entry.get()))
		liss_params.destroy()
		return 
	valid_name = Button(liss_params, borderwidth=2, relief=GROOVE, command = simple_liss)
	valid_name.grid(row = 1, column = 3)
	liss_params.mainloop()
	return int(liss_params.order)

def set_params_graph(parent):
	settings = Tk()
	settings.title("Paramètres de plot")

	plot_title = Entry(liss_params, borderwidth=2, relief=GROOVE)
	plot_title.grid(row = 1, column = 2)
	axex_label = Entry(liss_params, borderwidth=2, relief=GROOVE)
	axex_label.grid(row = 1, column = 2)
	axey_label = Entry(liss_params, borderwidth=2, relief=GROOVE)
	axey_label.grid(row = 1, column = 2)

	valid_params = Button(parent.ask_name, borderwidth=2, relief=GROOVE, command =lambda: fonction(parent))
	valid_params.grid(row = 0, column = 3)


	def get_title():
		parent.parameters.append(plot_title.get())
		return

	def get_axex():
		parent.parameters.append(axex_label.get())
		return

	def get_axey():
		parent.parameters.append(axey_label.get())
		return

	return
