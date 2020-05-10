# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:36:38 2020

@author: Julien
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

def calcul(m, k, amort, deltat, time_sim, value_selected):
    p0=np.array([0.,0.,0.])
    p1=np.array([0.,-1.,0.])
    longueur_0 = np.sqrt(np.dot(p1-p0, p1-p0))
    p1 = np.array([0.,-1.1,0])
    v = np.array([0., 0., 0.])
    longueur = np.sqrt(np.dot(p1-p0, p1-p0))
    deltalong = longueur-longueur_0
    lacc = []
    laccnorme = []
    lv = []
    lvnorme = []
    lp = []
    lpnorme = []
    ldp = []
    acc= np.array([0., 0., 0.])
    at = np.arange(0, time_sim, deltat)
    for i in at:
        longueur = np.sqrt(np.dot(p1-p0,p1-p0))
        deltalong = longueur-longueur_0
               
        ldp.append(deltalong)
        lv.append(v)
        lacc.append(acc)
        lp.append(p1)
    
        acc=(1/m)*(-v*amort-k*deltalong*(p1-p0)/longueur)
        v=v+deltat*acc      
        p1=p1+deltat*v
        
        vnorme = np.linalg.norm(v)
        lvnorme.append(vnorme)
        
        accnorme = np.linalg.norm(acc)
        laccnorme.append(accnorme)
        
        p1norme = np.linalg.norm(p1)
        lpnorme.append(p1norme)
               
    if value_selected == 'Accélération':
        lreturn = laccnorme
    elif value_selected == 'Vitesse':
        lreturn = lvnorme
    elif value_selected == 'Position':
        lreturn = lpnorme      
    elif value_selected == 'Elongation':
        lreturn = ldp
    else: 
        lreturn = ldp
    return list(at), lreturn
    
m_init = 1.0
k_init = 0.1
amort_init = 0.1
deltat_init = 1.0
time_sim_init = 50
x, y = calcul(m_init, k_init, amort_init, deltat_init, time_sim_init, "Position")

fig, ax = plt.subplots()
fig.suptitle("Etude du comportement d'un ressort")
plt.subplots_adjust(left = 0.35, bottom = 0.6)
p, = plt.plot(x, y, linewidth=2, color = 'blue')
plt.axis([10, 50, -0.07, 0.15])
plt.xlim(0, time_sim_init)
plt.xlabel("t")
plt.ylabel("Position")
ax.grid()
ax.autoscale(enable=True, axis='both')

axSliderRaideur = plt.axes([0.2, 0.45, 0.7, 0.05], facecolor='lightcyan')
slder_raideur = Slider(axSliderRaideur, 'Raideur', valmin=0, valmax=1, valinit=k_init, valfmt='%1.2f', closedmin=True, closedmax=True, color='limegreen')

axSliderMasse = plt.axes([0.2, 0.35, 0.7, 0.05], facecolor='lightcyan')
slder_masse = Slider(axSliderMasse, 'Masse', valmin=0, valmax=5, valinit=m_init, valfmt='%1.2f', closedmin=False, closedmax=True,color='limegreen')

axSliderAmort = plt.axes([0.2, 0.25, 0.7, 0.05], facecolor='lightcyan')
slder_amort = Slider(axSliderAmort, 'Amortissement', valmin=0, valmax = 1, valinit=amort_init, valfmt='%1.2f', closedmin=False, closedmax=True, color='limegreen')

axSliderDeltatT = plt.axes([0.2, 0.15, 0.7, 0.05], facecolor='lightcyan')
slder_deltat = Slider(axSliderDeltatT, 'Delta_t', valmin=0, valmax=10, valinit=deltat_init, valfmt='%1.2f', closedmin=False, closedmax=True, color='limegreen')

axSliderDuree = plt.axes([0.2, 0.05, 0.7, 0.05], facecolor='lightcyan')
slder_duree = Slider(axSliderDuree, 'Durée', valmin=0, valmax=200, valinit=time_sim_init, valfmt='%1.2f', closedmin=False, closedmax=True, color='limegreen')

def update_plot(val):
    m = slder_masse.val
    k = slder_raideur.val
    amort = slder_amort.val
    deltat = slder_deltat.val
    time_sim = slder_duree.val
    type_plot = str(radio.value_selected)
    x, y = calcul(m, k, amort, deltat, time_sim, type_plot)
    p.set_xdata(x)
    p.set_ydata(y)
    ax.set_ylabel(type_plot)
    ax.set_xlim(xmin=0, xmax=time_sim)
    ax.set_ylim(ymin=min(y), ymax=max(y))
    plt.draw()

slder_masse.on_changed(update_plot)
slder_raideur.on_changed(update_plot)
slder_amort.on_changed(update_plot)
slder_deltat.on_changed(update_plot)
slder_duree.on_changed(update_plot)

axButton1 = plt.axes([0.01, 0.89, 0.22, 0.1])
btn1 = Button(axButton1, 'Reset', color='lightcyan')

def resetSlider(event):
    slder_raideur.reset()
    slder_masse.reset()
    slder_amort.reset()
    slder_deltat.reset()
    slder_duree.reset()
btn1.on_clicked(resetSlider)

rax = plt.axes([0.01, 0.60, 0.22, 0.25], facecolor='lightcyan')
radio = RadioButtons(rax, ('Position', 'Vitesse', 'Accélération', 'Elongation'))
radio.on_clicked(update_plot)
    
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.show()















