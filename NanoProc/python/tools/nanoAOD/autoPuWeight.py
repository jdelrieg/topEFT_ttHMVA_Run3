from CMGTools.NanoProc.tools.nanoAOD.componentDependentModuleWrapper import componentDependentModuleWrapper
from CMGTools.NanoProc.tools.nanoAOD.puWeightProducer import puWeight_UL2016, puWeight_UL2017, puWeight_UL2018, puAutoWeight_2022, puAutoWeight_2022EE

class autoPuWeightModule( componentDependentModuleWrapper ):
    def __init__(self, w2016, w2017, w2018, w2022, w2022EE):
        self._w2016 = w2016
        self._w2017 = w2017
        self._w2018 = w2018
        self._w2022   = w2022
        self._w2022EE = w2022EE
        

    def initComponent(self, component):
        if component.isData:
            self._worker = None
        elif "Fall17" in component.dataset or 'UL17' in component.dataset:
            self._worker = self._w2017()
        elif "Autumn18" in component.dataset  or 'UL18' in component.dataset:
            self._worker = self._w2018()
        elif "Summer16" in component.dataset  or 'UL16' in component.dataset:
            self._worker = self._w2016()
        elif ("Summer22EE" in component.dataset):
            self._worker = self._w2022EE()
        elif ("Summer22" in component.dataset):
            self._worker = self._w2022()
        else:
            raise RuntimeError("Can't detect PU scenario for %s, %s" % (component.name, component.dataset))


autoPuWeight = lambda : autoPuWeightModule(puWeight_UL2016, puWeight_UL2017, puWeight_UL2018, puAutoWeight_2022, puAutoWeight_2022EE)
