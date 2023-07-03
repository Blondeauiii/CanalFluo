import tkinter as Tk
from tkinter import *
import tkinter.filedialog 
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import shutil as sh

import dataf as dt
import plotf as pl
import operations as op
import windows as wd

#définition des directories

main_path = os.getcwd()
datafiles_path = main_path + "/datafiles"
workdir_path = main_path + "/workdir"
results_path = main_path + "/results"

class App():								 #on définit l'appsous forme de classe
	def __init__(self):
			self.fen = Tk()							  #on créée la fenêtre
			self.fen.title("Analyse de données")
			self.fen.geometry("1500x700")
			self.create_menu()

			self.Frame1 = Frame(self.fen, borderwidth=2, relief=GROOVE) #fenêtre contenant l'historique et les commandes
			self.Frame1.grid(row=1, column=1)
			self.Frame2 = Frame(self.fen, borderwidth=2, relief=GROOVE) #fenêtre contenant l'espace de texte
			self.Frame2.grid(row=1, column=2)
			self.Frame3 = Frame(self.fen, borderwidth=2, relief=GROOVE) #fenêtre contenant l'espace de texte
			self.Frame3.grid(row=1, column=3)

			# définition en premier lieu des paramêtres graphiques

			label1 = Label(self.Frame1, text="Controls").grid(row = 0, column = 1)
			label2 = Label(self.Frame2, text="Text").grid(row = 0, column = 1)
			label3 = Label(self.Frame3, text="Plots").grid(row = 0, column = 1)


			self.datalist = []
			self.dataname = []
			self.zeroset = []
			self.parameters = []

			self.Notes = Text(self.Frame2,width = 90, height=60)
			self.Notes.grid(row = 1,column= 1, columnspan = 1)

			self.scrollbar_Notes = Scrollbar(self.Frame2, orient=VERTICAL , command = self.Notes.yview)
			self.scrollbar_Notes.grid(row = 1,column= 2,sticky = "nse")
			self.Notes.configure(yscrollcommand=self.scrollbar_Notes.set)

			self.Console = Text(self.Frame1,width = 40, height=20)
			self.Console.grid(row = 1,column= 1, columnspan = 1)

			self.scrollbar_Console = Scrollbar(self.Frame1, orient=VERTICAL , command = self.Console.yview)
			self.scrollbar_Console.grid(row = 1,column= 2,sticky = "nse")
			self.Console.configure(yscrollcommand=self.scrollbar_Console.set)

			self.charged_list = Text(self.Frame1,width = 40, height=20)
			self.charged_list.grid(row = 2,column= 1, columnspan = 1)

			self.scrollbar_charged_list = Scrollbar(self.Frame1, orient=VERTICAL , command = self.charged_list.yview)
			self.scrollbar_charged_list.grid(row = 2,column= 2,sticky = "nse")
			self.charged_list.configure(yscrollcommand=self.scrollbar_charged_list.set)

			self.ctrl_plots = Canvas(self.Frame3,bg="white",width = 600, height=600)
			self.ctrl_plots.grid(row = 1,column= 1, columnspan = 1)

			self.workdir = main_path + "/workdir/temp"

			return

	def run(self):
			self.fen.mainloop()
			return

	def create_menu(self):
			self.menu_bar = Menu(self.fen)

			self.menu_file = Menu(self.menu_bar, tearoff=0)
			self.menu_file.add_command(label="New",command=self.reset_all)
			self.menu_file.add_command(label="Open")
			self.menu_file.add_command(label="Save",command=lambda: wd.get_title(self,wd.save_txt))
			self.menu_bar.add_cascade(label="File", menu=self.menu_file)


			self.menu_help = Menu(self.menu_bar, tearoff=0)
			self.menu_help.add_command(label="About")
			self.menu_bar.add_cascade(label="Help", menu=self.menu_help)

			self.menu_data = Menu(self.menu_bar, tearoff=0)
			self.menu_data.add_command(label="new project",command = self.new_project)
			self.menu_data.add_command(label="open project",command = self.open_project)
			self.menu_data.add_command(label="charge datas",command = self.charge_datas)
			self.menu_data.add_command(label="view text",command = self.print_datas)
			self.menu_data.add_command(label="view plot",command = self.visu_plot)
			self.menu_bar.add_cascade(label="data", menu=self.menu_data)

			self.menu_plot = Menu(self.menu_bar, tearoff=0)
			self.menu_plot.add_command(label="exécuter un script")
			self.menu_plot.add_command(label="plot file", command = self.extract_and_plot)
			self.menu_plot.add_command(label="plot folder", command = self.plot_list)
			self.menu_bar.add_cascade(label="plot", menu=self.menu_plot)
			
			self.menu_operations = Menu(self.menu_bar, tearoff=0)
			self.menu_operations.add_command(label="find max", command = self.find_max)
			self.menu_operations.add_command(label="set to zero", command = self.set_to_zero)
			self.menu_operations.add_command(label="puls integration", command = self.integrate_over_zero)
			self.menu_operations.add_command(label="mi hauteur", command = self.find_midheight)
			self.menu_operations.add_command(label="lissage simple", command = self.simple_liss)
			self.menu_operations.add_command(label="spectral view", command =lambda: dt.write_spectal(self.workdir))
			self.menu_operations.add_command(label="remove noise", command =lambda: dt.remove_noise(self.workdir))
			self.menu_operations.add_command(label="moyenner les données", command =lambda: dt.moyen_fold(workdir_path))
			self.menu_operations.add_command(label="exécuter un script")
			self.menu_operations.add_command(label="clear lambda", command = self.remove_line)
			self.menu_operations.add_command(label="make sum", command = self.makesum)
			self.menu_bar.add_cascade(label="operation", menu=self.menu_operations)

			self.fen.config(menu=self.menu_bar)

			return

#//////////////////////////////////////////  fin de la mise en place des menus ////////////////////////////////////////////////
#//////////////////////////////////////////  debut de la mise en place des fonctions //////////////////////////////////////////


	def new_project(self):
		self.workdir = main_path
		import_dir = tkinter.filedialog.askdirectory()			   # On sélectionne le dossier de fichiers de données
		wd.get_title(self,wd.newdir_name)
		self.ask_name.wait_window()
		if os.path.exists(self.workdir + "/workdir/"+self.name_answer) == True :
			self.workdir = self.workdir + "/workdir/"+self.name_answer
			print("le dossier existe déjà")
		else :
			os.mkdir(self.workdir + "/workdir/"+self.name_answer)
			#os.mkdir(self.workdir + "/workdir/"+self.name_answer+"/datafiles/")
			self.workdir = self.workdir + "/workdir/"+self.name_answer	   # On crée un nouvel espace de travail
			self.Console.insert("1.0","new dir created " + self.workdir)       # On le signale dans la console
			sh.copytree(import_dir , self.workdir + "/datafiles")				 # On copie tout dans datafiles
			os.mkdir(self.workdir + "/dataconverted")				  # On crée un dossier pour les données
		#os.chdir(self.workdir + "/dataconverted")
		#self.workdir = (self.workdir + "/dataconverted")
		for filename in os.listdir(self.workdir + "/datafiles"):
			dt.extract_datas(filename , self.workdir)
		for filename in os.listdir(self.workdir + "/dataconverted"):
			self.datalist.append(dt.list_datas(self.workdir + "/dataconverted/"+filename))
			self.dataname.append(filename)
		 # format de daalist [filenumber][list_x,list_y][index]
		self.Console.insert("1.0","répertoire de données copié \n \n liste de données enregistrée \n \n" + self.workdir)
		return


	def open_project(self):
		self.workdir = tkinter.filedialog.askdirectory(initialdir = workdir_path)
		os.chdir(self.workdir)
		self.datalist = []
		self.dataname = []
		for filename in os.listdir(self.workdir + "/dataconverted"):
			self.datalist.append(dt.list_datas(self.workdir + "/dataconverted/"+filename))
			self.dataname.append(filename)
		self.Console.insert("1.0","répertoire ouvert \n \n liste de données enregistrée \n \n" + self.workdir + "\n")
		return
		
	def charge_datas(self):
		dirtocharge = tkinter.filedialog.askdirectory(initialdir = workdir_path)
		rapport = open(self.workdir+"/rapport",'a')
		rapport.write(" \n\n"+"Nom des fichiers:"+" \n\n")
		self.datalist = []
		self.dataname = []
		for filename in os.listdir(dirtocharge):
			self.datalist.append(dt.list_datas(dirtocharge +"/"+filename))
			self.dataname.append(filename)
			rapport.write(filename +" \n")
		self.Console.insert("1.0","liste de données chargée sur " + str(dirtocharge) +" \n \n")
		self.charged_list.delete("1.0","end")
		rapport.close()
		for filename in os.listdir(dirtocharge):
			self.charged_list.insert("1.0",  filename + "\n")
		return 
		
	
	def print_datas(self):
		os.chdir(self.workdir)
		filename = tkinter.filedialog.askopenfilename(initialdir = self.workdir , title = "Select file")
		datafile = open(filename,'r')
		text = datafile.read()
		self.Notes.insert("1.0",text)
		self.Frame1.update()
		return
		

	def get_name(self):  #crée une fenètre pour récupérer un nom , doit être exécuté au lieu de la fonction souhaitée
		self.ask_name = Tk()
		self.ask_name.title("Paramètres du plot")

		self.ask_name.answer = "none"

		label_axe_x = Label(self.ask_name, text="entrer un nom pour le fichier").grid(row = 0, column = 1)

		self.name_entry = Entry(self.ask_name, borderwidth=2, relief=GROOVE)
		self.name_entry.grid(row = 0, column = 2)

		self.valid_name = Button(self.ask_name, borderwidth=2, relief=GROOVE, command = self.save_txt)
		self.valid_name.grid(row = 0, column = 3)

		return()
		
	

	
	def visu_plot(self):   # sert à visualiser un plot
		filename = tkinter.filedialog.askopenfilename(initialdir = self.workdir , title = "Select file")
		plot = PhotoImage(file=filename)
		self.Plot.create_image(500,500,image=plot)
		self.Frame1.update()
		self.mainloop()
		return

	
	def reset_all(self):  # efface la fenètre de texte
		self.Notes.delete("1.0","end")
		self.Frame1.update()
		return

	def plot_list(self):   # plot un dossier de fichiers convertis
		os.chdir(main_path+"/results/plots")
		dirtoplot = tkinter.filedialog.askdirectory(initialdir = workdir_path)
		filename=pl.plot_list(dirtoplot)
		plot = PhotoImage(file= main_path +"/results/plots/"+ filename)
		self.ctrl_plots.create_image(300,300,image = plot,anchor=CENTER)
		return 0
		
	
	def extract_and_plot(self):   # plot un fichier converti
		filename = tkinter.filedialog.askopenfilename(initialdir = self.workdir , title = "Select file in a converted folder")
		#print(filename)
		(listx,listy) = dt.list_datas(filename)
		os.chdir(main_path+"/results/plots")
		pl.plot_graph(listx,listy)
		#pl.save_plot(listx,listy)
		return

#/////////////////////////////////////////////////////////////////////:



	def find_max(self):   # imprime les maxiums des fichiers d'un répertoire
		rapport = open(self.workdir+"/rapport",'a')
		rapport.write(" \n\n"+"maximums:"+" \n\n")
		for k in range(0,len(self.datalist)):
			(xmax,ymax) = op.findmax(self.datalist[k][0],self.datalist[k][1])
			self.Notes.insert("1.0","Maximum en "+str(ymax)+" de "+str(xmax)+" \n")
			rapport.write(str(ymax)+" en "+str(xmax)+" \n")
		rapport.close()
		return

	def set_to_zero(self):
		rapport = open(self.workdir+"/rapport",'a')
		rapport.write(" \n\n"+"bruit:"+" \n\n")
		for k in range(0,len(self.datalist)):
			moy=op.set_to_zero(self.datalist[k][1],int(len(self.datalist[k][1])/20),20,10)
			self.zeroset.append(moy)
			self.Notes.insert("1.0","Moyenne du blanc = "+str(moy)+" \n")
			rapport.write(str(moy)+" \n")
		rapport.close()
		return moy
		
	def integrate_over_zero(self):
		if self.zeroset != []:
			for k in range(0,len(self.datalist)):
				surface = op.Integrate_over_zero(self.datalist[k][0],self.datalist[k][1],self.zeroset[k])
				self.Notes.insert("1.0","Surface mesurée = "+str(surface)+" \n")
		else :
			self.Console.insert("1.0","Bruit non calculé \n\n")
		return

	def find_midheight(self):
		rapport = open(self.workdir+"/rapport",'a')
		rapport.write(" \n\n"+"mi hauteurs:"+" \n\n")
		for k in range(0,len(self.datalist)):
			midpoints = op.where_is_highfrac(self.datalist[k][0],self.datalist[k][1],2,self.zeroset[k])
			self.Notes.insert("1.0","les points de mi hauteur ont pour abscisse "+str(midpoints)+" \n")
			rapport.write(str(midpoints)+" \n")
		rapport.write("\n")
		rapport.close()
		return

	def get_liss_params(self):
		self.liss_params = Tk()
		self.liss_params.title("Paramètres du lissage")

		self.liss_params.order = 1

		label_ask_order = Label(self.liss_params, text="entrer un ordre pour le lissage").grid(row = 0, column = 1)

		self.is_ponderated = Checkbutton(self.liss_params)
		self.is_ponderated.grid(row = 0, column = 3)

		self.name_entry = Entry(self.liss_params, borderwidth=2, relief=GROOVE)
		self.name_entry.grid(row = 1, column = 2)

		self.valid_name = Button(self.liss_params, borderwidth=2, relief=GROOVE, command = self.simple_liss)
		self.valid_name.grid(row = 1, column = 3)
		return

	def simple_liss(self):
		if os.path.exists(self.workdir + "/datalissed") == True :
			print("le dossier existe déjà")
		else :
			os.mkdir(self.workdir + "/datalissed")
		os.chdir(self.workdir + "/datafiles")
		namelist = os.listdir()
		os.chdir(self.workdir + "/datalissed")
		order = float(self.name_entry.get())

		self.liss_params.destroy()
		for k in range(0,len(self.datalist)):
			data = op.liss(self.datalist[k][1],order)
			datafile = open(self.workdir+"/datalissed/"+namelist[k],'w')
			for j in range(len(data)):
				datafile.write(str(self.datalist[k][0][j+int(order)]) + "\t" + str(data[j]) + "\n")

			datafile.close()
		self.Console.insert("1.0","les données sont lissées \n \n")
		return

	def makesum(self):
		rapport = open(self.workdir+"/rapport",'a')
		rapport.write(" \n\n"+self.workdir+" \n\n")
		rapport.close()
		self.charge_datas()
		self.find_max()
		self.set_to_zero()
		self.find_midheight()
		
		return
		
	def remove_line(self):
		linetoclear = [496 , 525 , 524 , 526, 523 , 526]
		if os.path.exists(self.workdir + "/datacleared") == True :
			print("le dossier existe déjà")
		else :
			os.mkdir(self.workdir + "/datacleared")
		for filename in os.listdir(self.workdir + "/dataconverted"):
			datafile = open(self.workdir+"/dataconverted/"+filename,'r')
			datacleared = open(self.workdir+"/datacleared/"+filename,'w')
			nline = 0
			while 1 :
				nline +=1
				data = datafile.readline()
				if data == "":
					break
				flag = 0
				for clline in linetoclear:
					if nline == clline:
						flag = 1
				if flag == 0:
					datacleared.write(data)
						
			datafile.close()
			datacleared.close()
		return

App().run()





