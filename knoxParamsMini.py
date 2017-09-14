"""
knoxParams.py 

netParams is a dict containing a set of network parameters using a standardized structure

simConfig is a dict containing a set of simulation configurations using a standardized structure

refs:
Destexhe, A., Contreras, D., & Steriade, M. (1998). Mechanisms underlying the 
synchronizing action of corticothalamic feedback through inhibition of thalamic 
relay cells. Journal of neurophysiology, 79(2), 999-1016.

Destexhe, A. (1998). Spike-and-wave oscillations based on the properties of 
GABAB receptors. Journal of Neuroscience, 18(21), 9099-9111.


Contributors: xxx@xxxx.com
"""

from netpyne import specs
from netpyne import sim

netParams = specs.NetParams()   # object of class NetParams to store the network parameters
simConfig = specs.SimConfig()   # object of class SimConfig to store the simulation configuration

import random as rnd
import numpy as np


def printREinfo(cellParams):
    print " "
    print "------ RE Parameter values ---------"
    print " "
    
    print "diam=",cellParams.secs.soma.geom.diam,"\t L=",cellParams.secs.soma.geom.L," \t Cm=",cellParams.secs.soma.geom.cm," \t Ra=",cellParams.secs.soma.geom.Ra
    print "g_pas=",cellParams.secs.soma.mechs.pas.g," \t e_pas=",cellParams.secs.soma.mechs.pas.e," \t vinit=", cellParams.secs.soma.vinit
    print "gnabar_hh2=",cellParams.secs.soma.mechs.hh2.gnabar," \t ena=", cellParams.secs.soma.ions.na.e
    print "gkbar_hh2=",cellParams.secs.soma.mechs.hh2.gkbar," \t ek=",cellParams.secs.soma.ions.k.e," \t vtraub_hh2=", cellParams.secs.soma.mechs.hh2.vtraub
    print "gcabar_it2=",cellParams.secs.soma.mechs.it2.gcabar," \t eca=",cellParams.secs.soma.ions.ca.e," \t cai=", cellParams.secs.soma.ions.ca.i," \t cao=", cellParams.secs.soma.ions.ca.o
    print "shift_it2=",cellParams.secs.soma.mechs.it2.shift," \t taubase_it2=",cellParams.secs.soma.mechs.it2.taubase," \t qm_it2=", cellParams.secs.soma.mechs.it2.qm," \t qh_it2=", cellParams.secs.soma.mechs.it2.qh
    print "depth_cad=",cellParams.secs.soma.mechs.cad.depth," \t taur_cad=",cellParams.secs.soma.mechs.cad.taur," \t cainf_cad=", cellParams.secs.soma.mechs.cad.cainf," \t kt_cad=", cellParams.secs.soma.mechs.cad.kt
    
    print " "
    print "-------- RE Parameter values (end) --------"
    print " "



celsius = 36
v_init = -70

###############################################################################
# NETWORK PARAMETERS
###############################################################################
N=100; N_RE=N;


netParams.defaultThreshold = 0

###############################################################################
# Population parameters
###############################################################################
netParams.popParams['RE'] = {'cellType': 'RE', 'numCells': N_RE, 'cellModel': 'HH_RE', 'ynormRange': [0.8, 0.9]} 


###############################################################################
# Cell parameters list
###############################################################################

### RE (Destexhe et al., 1996; Bazhenov et al.,2002)
cellRule = netParams.importCellParams(label='RErule', conds={'cellType': 'RE', 'cellModel': 'HH_RE'}, fileName='RE.tem', cellName='sRE')

cellRule['secs']['soma']['vinit']=v_init
netParams.cellParams['RErule'] = cellRule


###############################################################################
# SIMULATION PARAMETERS
###############################################################################

#------------------------------------------------------------------------------
# SIMULATION CONFIGURATION
#------------------------------------------------------------------------------

# Simulation parameters
simConfig.checkErrors=False # True
simConfig.trans = 10000
simConfig.Dt = 0.1
simConfig.steps_per_ms = 1/simConfig.Dt
simConfig.npoints = 30000

simConfig.duration = 3*1000+10000*0 # simConfig.trans + simConfig.npoints * simConfig.Dt # Duration of the simulation, in ms
simConfig.dt = 0.1 # Internal integration timestep to use
simConfig.hParams['celsius'] = celsius
simConfig.hParams['v_init'] = v_init
#simConfig.seeds = {'conn': 1, 'stim': 1, 'loc': 1} # Seeds for randomizers (connectivity, input stimulation and cell locations)
simConfig.verbose = False # True  # show detailed messages 

# Recording 
simConfig.recordCells = []  # which cells to record from

simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}

simConfig.recordStim = True  # record spikes of cell stims
simConfig.recordStep = 0.1 # Step size in ms to save data (eg. V traces, LFP, etc)
#simConfig.cvode_active = True

# Saving
simConfig.simLabel = "knox"
simConfig.saveFolder = "data_knox_v1"
simConfig.filename = 'knox_v1'  # Set file output name
simConfig.saveFileStep = 1000 # step size in ms to save data to disk

# Analysis and plotting 
simConfig.analysis['plotRaster'] = {'include': ['RE'], 'orderInverse': False} #True # Whether or not to plot a raster

simConfig.analysis['plotTraces'] = {'include': [('RE',[0])]} # plot recorded traces for this list of cells


# netParams
simConfig.runStopAt = simConfig.duration


###############################################################################
# create, simulate, and analyse network
###############################################################################
(pops, cells, conns, stims, simData) = sim.create(netParams, simConfig, output=True)


#sim.h.cvode.re_init()
#sim.h.frecord_init()

##### sim.simulate() ################
##### sim.runSim()   ################
###############################################################################
### Run Simulation
###############################################################################
sim.pc.barrier()
sim.timing('start', 'runTime')
sim.preRun()
#sim.h.init()

sim.pc.set_maxstep(10)
sim.h.stdinit()
sim.h.dt = 0.1 # Fixed dt
sim.h.fcurrent()
sim.h.cvode.re_init()
sim.h.frecord_init()

printREinfo(sim.net.cells[0])


if sim.rank == 0: print('\nRunning simulation for %s ms...'%sim.cfg.duration)
sim.pc.psolve(sim.cfg.duration)

sim.pc.barrier() # Wait for all hosts to get to this point
sim.timing('stop', 'runTime')
if sim.rank==0:
    print('  Done; run time = %0.2f s; real-time ratio: %0.2f.' %
        (sim.timingData['runTime'], sim.cfg.duration/1000/sim.timingData['runTime']))
########################################
sim.gatherData()                  # gather spiking data and cell info from each node
#####################################
sim.analyze()



#sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)

