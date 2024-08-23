#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steering file to get all skim flags and store in an ntuple to be used later to calculate various metrics of intersectionality.
"""
import basf2 as b2
import modularAnalysis as ma
import os
import sys
from skim.registry import Registry

# For backward compatibility, wrap skim imports in try-except block
try:
    # release 6+ imports
    from skim import CombinedSkim
    from skim.WGs.systematics import SystematicsFourLeptonFromHLTFlag, SystematicsRadMuMuFromHLTFlag, SystematicsPhiGamma

except (ImportError, ModuleNotFoundError):
    # release 5 imports
    from skimExpertFunctions import CombinedSkim
    from skim.systematics import SystematicsFourLeptonFromHLTFlag, SystematicsRadMuMuFromHLTFlag, SystematicsPhiGamma

#os.system('b2skim-run single feiHadronic --analysis-globaltag analysis_tools_light-2203-zeus')

TestFiles = ["/group/belle2/dataprod/MC/SkimTraining/proc11_exp10.mdst.root"]
path = b2.Path()

#read system arguments
outDir = sys.argv[1]
skimName = sys.argv[2]

all_skims = []
all_skims.append(Registry.get_skim_function(skimName)())
skim = CombinedSkim(*all_skims, udstOutput=False)

variables = skim.flags
#variables = []
#variables.append("SoftwareTriggerResult(software_trigger_cut&skim&accept_hadron)")

ma.inputMdstList("default", TestFiles, path=path)
skim(path)
ma.variablesToNtuple("", variables, filename="%s/%s.root"%(outDir, skimName), path=path)
b2.process(path)





