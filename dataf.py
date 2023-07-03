import tkinter as Tk
from tkinter import *
import tkinter.filedialog 
import operations as op

import re
import os
import numpy as np

main_path = os.getcwd()

def extract_datas(filename,workdir):  
	datafile = open(workdir+"/datafiles/"+filename,'r')
	print(workdir+"/datafiles/"+filename)
	while 1 :
		data = datafile.readline()
		
		if len(data) != 0:
			if data[0] == ">" or data == "Time Ampl\n":     #trouve >>>>>Begin Spectral Data<<<<< pour commencer l'acquisition
				break
		else:
			data = datafile.readline()
			if data == "":
				break
	datafile.readline()
	data = datafile.read()
	datafile.close()
	only_datas = open(workdir+"/dataconverted/"+filename,'w')
	for k in range(len(data)):
		if data[k] == ",":
			a = "."
			only_datas.write(str(a))
		else :
			only_datas.write(data[k])
	only_datas.close()
	return 
	
def list_datas(filename):
	filetoread = open(filename,'r')
	datalist = []
	linesplitted = []
	while 1 :	
		dataline = filetoread.readline()
		dataline.splitlines()
		linesplitted.append(dataline.splitlines())
		if dataline == "" :
			break
	for k in range(0,len(linesplitted)-1):
		print(linesplitted[k])
		linesplitted[k] = re.split(r'\s|\t',linesplitted[k][0])  # \t est une tabulation
		#linesplitted[k] = linesplitted[k].split()
		
	data_x = []
	data_y = []
	for k in range(0,len(linesplitted)-1):
		data_x.append(float(linesplitted[k][0]))
		data_y.append(float(linesplitted[k][1]))
	return[data_x,data_y]
	
def extract_datas_brut(filename):  
	datafile = open(filename,'r')
	datalist = []
	linesplitted = []
	while 1 :
		data = datafile.readline()
		if data[0] == ">":     #trouve >>>>>Begin Spectral Data<<<<< pour commencer l'acquisition
			break
	datafile.readline()
	data = datafile.read()
	datafile.close()
	only_datas = [[]]
	i=0
	for k in range(len(data)):
		if data[k] == ",":
			a = "."
			only_datas[i].append(str(a))
			#print(type(datas[k]))
		elif data[k] == "\n":
			only_datas.append([])
			i+=1
		else :
			only_datas[i].append(data[k])
	for k in range(len(only_datas)):
		only_datas[k] = ''.join(only_datas[k])
		linesplitted.append(re.split("\t",only_datas[k]))
	data_x = []
	data_y = []
	for k in range(0,len(linesplitted)-1):
		data_x.append(float(linesplitted[k][0]))
		data_y.append(float(linesplitted[k][1]))
	return[data_x,data_y]

def moyen_fold(workdir):
	datadir = tkinter.filedialog.askdirectory()  #on demande un fichier de données brut
	newdir = workdir +"/"+ os.path.basename(datadir) + "_moy/dataconverted"
	if os.path.exists(newdir) == True :
		print("le dossier existe déjà")
	else :
		os.mkdir(workdir +"/"+ os.path.basename(datadir) + "_moy/")
		os.mkdir(newdir)
	os.chdir(datadir)
	filelist = os.listdir()
	subfilelist = []
	while(filelist != []):   #tant qu'on n'a pas traité tout les fichiers
		indlist = []
		subfilelist.append([filelist[0]])
		indlist.append(0)
		for k in range(1,len(filelist)):
			marq = 0
			for i in range(0,len(filelist[0])-10):
				if(filelist[0][i] != filelist[k][i]):
					marq = 1
			if(marq == 0):
				subfilelist[-1].append(filelist[k])
				indlist.append(k)
		for k in range(len(indlist)):
			filelist[indlist[k]] = 0
		for k in range(len(indlist)):
			filelist.remove(0)
	for k in range(len(subfilelist)):     #On traite maintenant les fichiers similaires séparément
		datas = []
		xmoy = []
		ymoy = []
		for i in range(0,len(subfilelist[k])):
			datas.append(extract_datas_brut(datadir+"/"+subfilelist[k][i]))
		for i in range(len(datas[i][0])):
			xmoy_val = 0
			ymoy_val = 0
			for j in range(len(datas)):
				xmoy_val += datas[j][0][i]
				ymoy_val += datas[j][1][i]
			xmoy.append(xmoy_val/len(datas))
			ymoy.append(ymoy_val/len(datas))
		datafile = open(newdir+"/"+subfilelist[k][0],'w')
		ecart_type = []
		for i in range(len(ymoy)):
			sigma = 0
			for j in range(len(datas)):
				sigma += abs(ymoy[i]-datas[j][1][i])#*(ymoy[i]-datas[j][1][i])
			ecart_type.append(sigma/len(datas))
		for i in range(len(xmoy)):
			datafile.write(str(xmoy[i]) + "\t" + str(ymoy[i]) + "\t" + str(ecart_type[i]) + "\n")
		datafile.close()
	return(newdir)

def write_spectal(workdir):
	datadir = tkinter.filedialog.askdirectory()  #on demande un fichier de données brut
	newdir = workdir +"/"+ os.path.basename(datadir) + "_spectral"
	if os.path.exists(newdir) == True :
		print("le dossier existe déjà")
	else :
		os.mkdir(newdir)
	os.chdir(datadir)
	for filename in os.listdir(datadir):
		datas = list_datas(filename)
		datas_freq = op.fft_convert(datas[0],datas[1])
		datafile = open(newdir+"/"+filename,'w')
		for j in range(len(datas_freq[0])):
			datafile.write(str(datas_freq[0][j]) + "\t" + str(datas_freq[1][j]) + "\n")
		datafile.close()
	return

def remove_noise(workdir):
	noisefile = tkinter.filedialog.askopenfilename(initialdir = workdir , title = "Select noise file")
	datadir = tkinter.filedialog.askdirectory()  #on demande un fichier de données brut
	newdir = workdir +"/"+ os.path.basename(datadir) + "_withoutnoise"
	if os.path.exists(newdir) == True :
		print("le dossier existe déjà")
	else :
		os.mkdir(workdir +"/"+ os.path.basename(datadir) + "_withoutnoise")
	os.chdir(datadir)
	noisedatas = list_datas(noisefile)
	noisedatas_freq = op.fft_convert(noisedatas[0],noisedatas[1])
	for filename in os.listdir(datadir):
		datas = list_datas(filename)
		datas_freq = op.fft_convert(datas[0],datas[1])
		if len(datas[0]) == len(noisedatas[0]):
			datas_conv = []
			norm = op.Integrate(datas[0],datas[1])
			norm_noise = op.Integrate(noisedatas[0],noisedatas[1])
			for k in range(len(datas_freq[0])):
				datas_conv.append(datas_freq[1][k] + noisedatas_freq[1][k])

			new_datas = op.ifft_convert(datas_freq[0],datas_conv)
			datafile = open(newdir+"/"+filename,'w')
			for j in range(len(datas[0])):
				datafile.write(str(new_datas[0][j]) + "\t" + str(new_datas[1][j]) + "\n")
			datafile.close()
		else :
			print("pas la même longueur")
	return
