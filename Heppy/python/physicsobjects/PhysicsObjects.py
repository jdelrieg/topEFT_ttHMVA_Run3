import math
import fnmatch

from CMGTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

def printOut(objects):
    if len(objects)==0:
        return ''
    return '\n'.join( map( type(objects[0]).__str__, objects) )

from CMGTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from CMGTools.Heppy.physicsobjects.TriggerObject import TriggerObject
from CMGTools.Heppy.physicsobjects.Jet import Jet, GenJet
from CMGTools.Heppy.physicsobjects.Lepton import Lepton
from CMGTools.Heppy.physicsobjects.Photon import Photon
from CMGTools.Heppy.physicsobjects.Muon import Muon
# COLIN need to import MVA ID recipe. 
# from CMGTools.Heppy.physicsobjects.Electron import Electron
from CMGTools.Heppy.physicsobjects.Tau import Tau, isTau
from CMGTools.Heppy.physicsobjects.GenParticle import GenParticle 

