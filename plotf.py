import matplotlib.pyplot as plt
import numpy as np
import os
import time

import dataf as dt
import tkinter as Tk
from tkinter import *
import tkinter.filedialog 
import windows as wd

def plot_list(workdir):
	date = time.strftime("%a%d%b%Y%H%M%S", time.gmtime())
	fig = plt.figure()
	listfiles = os.listdir(workdir)
	print(listfiles)
	for k in range(0,len(listfiles)):
		datalist = dt.list_datas(workdir + "/" + listfiles[k])
		plt.plot(datalist[0],datalist[1])
	
	plt.savefig(date + "_plot.svg")
	print("ok")
	plt.savefig(date + "_plot.png")
	plt.show()
	return(date + "_plot.png")
	
def save_plot(listx,listy):
	date = time.strftime("%a%d%b%Y%H%M%S", time.gmtime())
	fig = plt.figure()
	plt.plot(listx,listy)
	fig.savefig(date + "_plot.png")
	#fig.savefig(date + "_plot.svg")
	#plt.show()
	return(date + "_plot.png")
	
def plot_graph(listx,listy):
	fig, axe = plt.subplots()
	axe.plot(listx,listy)
	axe.set(xlabel="time",ylabel="Intensité",title = "impulsion")
	axe.grid()
	plt.show()
	return
