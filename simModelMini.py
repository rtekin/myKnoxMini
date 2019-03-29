# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 15:57:43 2017

@author: rt
"""

#from cellModels import sINpy
import numpy as np
from neuron import h, gui
from math import sin, cos, pi
from matplotlib import pyplot

from neuronpy.graphics import spikeplot
from neuronpy.util import spiketrain



def printREinfo(indx):
    index=indx
    print (" ")
    print ("------ RE Parameter values (index=",index,") ---------")
    print (" ")
    
    print "diam=",RE[index].soma.diam,"\t L=",RE[index].soma.L," \t Cm=",RE[index].soma.cm," \t Ra=",RE[index].soma.Ra
    print "g_pas=",RE[index].soma.g_pas," \t e_pas=",RE[index].soma.e_pas," \t vinit=", RE[index].soma(0.5).v
    print "gnabar_hh2=",RE[index].soma.gnabar_hh2," \t ena=", RE[index].soma.ena
    print "gkbar_hh2=",RE[index].soma.gkbar_hh2," \t ek=",RE[index].soma.ek," \t vtraub_hh2=", RE[index].soma.vtraub_hh2
    print "gcabar_it2=",RE[index].soma.gcabar_it2," \t eca=",RE[index].soma.eca," \t cai=", RE[index].soma.cai," \t cao=", RE[index].soma.cao
    print "shift_it2=",RE[index].soma.shift_it2," \t taubase_it2=",RE[index].soma.taubase_it2," \t qm_it2=", RE[index].soma.qm_it2," \t qh_it2=", RE[index].soma.qh_it2
    print "depth_cad=",RE[index].soma.depth_cad," \t taur_cad=",RE[index].soma.taur_cad," \t cainf_cad=", RE[index].soma.cainf_cad," \t kt_cad=", RE[index].soma.kt_cad
    
    print " "
    print "-------- RE Parameter values (end) --------"
    print " "


nthalamiccells = 10


watchneuron = 50*0


celsius = 36
v_init = -70

recncs = []

#----------------------------------------------------------------------------
#  Create Cells
#----------------------------------------------------------------------------
print " "
print "<<==================================>>"
print "<<            CREATE CELLS          >>"
print "<<==================================>>"
print " "

h.load_file("RE.tem")
#h.xopen("RE.tem")
RE = []     # create RE cells
REVtrace = [] 
for i in range(nthalamiccells):
    cell = h.sRE()
    #cell.soma.v = randvolt.repick()
    RE.append(cell)


#----------------------------------------------------------------------------
# set up recording stuff
#----------------------------------------------------------------------------


REtimevec = h.Vector()
REidvec = h.Vector()



h("objref nil")

for i in range(nthalamiccells):
    #
    VtraceRE = h.Vector()
    VtraceRE.record(RE[i].soma(0.5)._ref_v)
    REVtrace.append(VtraceRE)
    nc = h.NetCon(RE[i].soma(0.5)._ref_v, h.nil, sec=RE[i].soma)
    nc.record(REtimevec, REidvec, i+1)
    recncs.append(nc)


t_vec = h.Vector()        # Time stamp vector
t_vec.record(h._ref_t)


#h.tstop = 1000
tstop = 3000+10000*0


# run the simulation


def go():
    h.dt=0.1
    h.celsius=celsius
    h.finitialize(v_init)
    #neuron.init()

    
    h.fcurrent()
    h.cvode.re_init()
    h.frecord_init()

    printREinfo(0)

    while h.t<tstop:
        h.fadvance()

go()


# voltage traces

fig = pyplot.figure(figsize=(8,4))
ax1 = fig.add_subplot(1,1,1)
RE1 = ax1.plot(t_vec, REVtrace[0], color='black')
ax1.legend(RE1, ['RE[%d]'%(watchneuron)])
ax1.set_ylabel('mV')
ax1.set_xlabel('time (ms)')


#----------------------------------------------------------------------------
# Raster plot
#----------------------------------------------------------------------------
labels = ['RE']
y=[50]
fig_handle = pyplot.figure(figsize=(8,4))
ax = fig_handle.add_subplot(111)
ax.set_title('Raster plot')
ax.set_xlabel('$t$ (ms)') # Note LaTeX
ax.set_yticks([])


sp = spikeplot.SpikePlot(fig=fig_handle)
sp.set_markerscale(0.1)
sp.set_marker('.')

PYspikes = spiketrain.netconvecs_to_listoflists(REtimevec, REidvec)
sp.set_markercolor('black')
sp.plot_spikes(PYspikes, draw=False, label='RE')

pyplot.xlim(0,tstop)
pyplot.yticks(y, labels)
