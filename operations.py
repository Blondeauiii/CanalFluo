

import numpy as np

def findmax(listx,listy):
	maxx = 0.0
	kmax = 0.0
	for k in range(0,len(listy),1):
		if listy[k] > maxx :
			maxx = listy[k]
			kmax = listx[k]
	return (maxx,kmax)
	
def moyenne(listy):
	moy = 0
	for k in range(0,len(listy),1):
		moy = moy + listy[k]
	moy = moy / len(listy)
	return moy
	
def set_to_zero(listy,step,pentmax,fitmax): # Cette fonction cherche la partie plane d'une courbe pour donner sa valeur
	idpent = []
	for k in range(0,len(listy),step):         #On quadrille la courbe en prenant les dérivées
		for l in range(0,len(listy),step):
			if abs(listy[k] - listy[l]) <= pentmax :        #On ne garde que les dérivées suffisament petites
				idpent.append([k,l]) 
	for k in range(0,len(idpent),1): #On étudie le cas de chaque point gardé
		count = 0
		idin = idpent[k][0]
		for l in range(0,len(idpent),1):   #On cherche à connaître le nombre de connexions valides (1 seulement pour une parabole) et cela dépend de la tolérance
			if idpent[l][0] == idin and idpent[l][1] != idin: #on compte le nombre de connexions
				count = count + 1
		if count < fitmax:                 # La tolérance peut varier
			idpent[k]=[0,0]
	count = 0
	moy = 0
	for k in range(0,len(idpent),1): #on va moyenner les valeurs que l'on a gardé (là ou la courbe est suffisament plate)
		if idpent[k] != [0,0]:
			count = count + 1
			moy = moy + (listy[idpent[k][0]] + listy[idpent[k][1]])/2
	moy = moy/count
	return moy

def Integrate_over_zero(listx,listy,zeroset):
	surface = 0
	for k in range(0,len(listy)-1,1):
		surface = surface + ((listy[k+1]+listy[k]-2*zeroset)/2)*(listx[k+1]-listx[k])
	return(surface)

def Integrate(listx,listy):
	surface = 0
	for k in range(0,len(listy)-1,1):
		surface = surface + ((listy[k+1]+listy[k])/2)*(listx[k+1]-listx[k])
	return(surface)
	
def where_is_highfrac(listx,listy,frac,zeroset):
	points = []
	maxx = findmax(listx,listy)[0]-zeroset
	for k in range(0,len(listy)-1,1):
		if listy[k] <= maxx/frac + zeroset < listy[k+1]:
			points.append(listx[k])
		if listy[k] >= maxx/frac + zeroset > listy[k+1]:
			points.append(listx[k])
	return points
	
def Integratefrac(listx,listy):
	surface = 0
	for k in range(0,len(listy)-1,1):
		surface = surface + ((listy[k+1]+listy[k])/2)*(listx[k+1]-listx[k])
	return(surface)
	
def liss(listy,order):
	order = int(order)
	listy_liss = []
	for k in range(0,order,1):
		listy_liss.append(0.0)   #réajustement pour éviter le décalage du à la moyenne
	for k in range(order,len(listy)-order,1):
		moy = 0
		for l in range(-order,order+1,1):
			moy += listy[k + l]
		moy = moy/(2*order+1)
		listy_liss.append(moy)
	return listy_liss
	
def liss_ponder(listy,order):
	order = int(order)
	listy_liss = []
	for k in range(0,order,1):
		listy_liss.append(0.0)   #réajustement pour éviter le décalage du à la moyenne
	for k in range(order,len(listy)-order,1):
		moy = 0
		norm = 0
		for l in range(-order,order+1,1):
			moy += listy[k + l]/(np.exp(abs(l)))
			norm += np.exp(abs(l))
		moy = moy/norm
		listy_liss.append(moy)
	return listy_liss

def fft_convert(listx,listy):
	#ranje = listx[-1]-listx[0]
	#step = ranje / len(listx)
	#print("step = "+str(step))
	signal = np.array(listy)
	transformee = np.fft.fft(signal)
	frequence = np.fft.fftfreq(len(signal))#/step
	return([frequence,np.abs(transformee)])

def ifft_convert(listx,listy):
	#ranje = listx[-1]-listx[0]
	#step = ranje / len(listx)
	signal = np.array(listy)
	transformee = np.fft.fft(signal)
	frequence = np.fft.fftfreq(len(signal))#/step
	return([frequence,np.abs(transformee)])


