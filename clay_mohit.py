
# This Python code reproduces the upper and low panel of Fig. 6 in Clay et. al. (2008). 

#Save the voltage nd time series csv files as v1.csv for the standard HH model (top panel of fig.6 and v2.csv for the revised model (bottom panel for of fig. 6)


from __future__ import division
from neuron import h
import numpy as np
import matplotlib.pyplot as plt
import timeit
import subprocess
import math


def initialize():
	h.finitialize()
	h.fcurrent()
def integrate():
	#g.begin()
	
	h.finitialize()
	while h.t<tstop:
		h.fadvance()

cell=h.Section()

nseg=9
cell.nseg=nseg   # number of segments
cell.Ra=35.4 # ohm*cm  # cable resistance
cell.cm=1


l=1# length of the axon in mm
cell.L=l*1000  # length of the axon in um to be read into NEURON 
cell.diam=500 # diameter of the axon in um


#insert the mechanism


#cell.insert('kext_clay') #in case the potassium accumulation is used. 
cell.insert('hh') #inserting  Clay revised HH model
#cell.insert('hh') # Standard Hodgkin Huxley model 
cell.ek = -72
cell.ena = 55


#Stimulation current 
stim1=h.IClamp(0,sec=cell)
stim1.delay=100 #ms
stim1.dur=80 #ms
stim1.amp= 250 #nA

#print stim_density * 1000 * area


vec={}
for var in 'i','t','v':
	vec[var]=h.Vector()
	
vec['t'].record(h._ref_t)

vec['v'].record(cell(0.99)._ref_v)

vec['i'].record(stim1._ref_i)


tstop=200
h.dt=0.01


		


initialize()
integrate()

np.savetxt('v1.csv', vec['v'], delimiter= ',')
np.savetxt('time.csv', vec['t'], delimiter= ',') # saving the time series

cell2=h.Section()

nseg=9
cell2.nseg=nseg   # number of segments
cell2.Ra=35.4 # ohm*cm  # cable resistance
cell2.cm=1


l=1# length of the axon in mm
cell2.L=l*1000  # length of the axon in um to be read into NEURON 
cell2.diam=500 # diameter of the axon in um


#insert the mechanism



cell2.insert('hhrx_clay_2') #inserting  Clay revised HH model

cell2.ek = -72
cell2.ena = 55


vec['v2'] = h.Vector()
vec['v2'].record(cell2(0.99)._ref_v)

#Stimulation current 
stim1=h.IClamp(0,sec=cell2)
stim1.delay=100 #ms
stim1.dur=80 #ms
stim1.amp= 250 #nA


tstop=200
h.dt=0.01

initialize()
integrate()

np.savetxt('v2.csv', vec['v2'], delimiter= ',')

## code for plotting the results

v1 = np.genfromtxt('v1.csv',delimiter=',')
v2 = np.genfromtxt('v2.csv',delimiter=',')
time = np.genfromtxt('time.csv', delimiter= ',')


fig = plt.figure()
ax = fig.add_subplot(2,1,1)
plt.plot(time,v1)
plt.xlabel( 'Time (ms)')
plt.ylabel(' Voltage (mV)')
plt.text(140,20, 'HH', fontsize = 12)
plt.xlim(80,200)
ax.set_xticklabels([])
ax.set_xticks([])
ax.set_yticklabels([])
ax.set_yticks([])
plt.ylim(-75,60)
plt.plot((100,180), (50,50), color = 'k', linewidth = 2)
plt.plot((185,185), (-50,0), color = 'k', linewidth = 2)
plt.text(187,-50, '-50', fontsize = 12)
plt.text(187,0, '0 mV', fontsize = 12)

ax = fig.add_subplot(2,1,2)
plt.plot(time,v2)
plt.xlim(80,200)
plt.xlabel( 'Time (ms)')
plt.ylabel(' Voltage (mV)')
plt.text(140,20, 'Clay, et. al. (2008)', fontsize = 12)
ax.set_xticklabels([])
ax.set_xticks([])
ax.set_yticklabels([])
ax.set_yticks([])
plt.ylim(-75,60)
plt.plot((185,185), (-50,0), color = 'k', linewidth = 2)
plt.plot((125,175), (0,0), color = 'k', linewidth = 2)
plt.text(187,-50, '-50', fontsize = 12)
plt.text(187,0, '0 mV', fontsize = 12)
plt.text(145,-15, '50 ms', fontsize = 12)

plt.savefig('clay_mohit.jpeg',dpi=600, format='jpeg', bbox_inches='tight')

plt.show()










