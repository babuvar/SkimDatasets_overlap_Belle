#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steering file to get all skim flags and store in an ntuple to be used later to calculate various metrics of intersectionality.
"""
import basf2 as b2
import modularAnalysis as ma
import os
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

os.system('b2skim-run single feiHadronic --analysis-globaltag analysis_tools_light-2203-zeus')

TestFiles = ["/group/belle2/dataprod/MC/SkimTraining/proc11_exp10.mdst.root"]
path = b2.Path()


#skimNames = ['Random', 'SystematicsTracking', 'Resonance', 'SystematicsRadMuMu', 'SystematicsEELL', 'SystematicsRadEE', 'SystematicsLambda', 'SystematicsPhiGamma', 'SystematicsFourLeptonFromHLTFlag', 'SystematicsRadMuMuFromHLTFlag', 'SystematicsJpsi', 'SystematicsKshort', 'SystematicsBhabha', 'SystematicsDstar', 'PRsemileptonicUntagged', 'LeptonicUntagged', 'dilepton', 'SLUntagged', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'BtoXgamma', 'BtoXll', 'BtoXll_LFV', 'inclusiveBplusToKplusNuNu', 'TDCPV_ccs', 'TDCPV_qqs', 'BtoD0h_Kspi0', 'BtoD0h_Kspipipi0', 'B0toDpi_Kpipi', 'B0toDpi_Kspi', 'B0toDstarPi_D0pi_Kpi', 'B0toDstarPi_D0pi_Kpipipi_Kpipi0', 'B0toDrho_Kpipi', 'B0toDrho_Kspi', 'B0toDstarRho_D0pi_Kpi', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'BtoD0h_hh', 'BtoD0h_Kpi', 'BtoD0h_Kpipipi_Kpipi0', 'BtoD0h_Kshh', 'BtoD0rho_Kpi', 'BtoD0rho_Kpipipi_Kpipi0', 'B0toDD_Kpipi_Kspi', 'B0toDstarD', 'InclusiveLambda', 'BottomoniumEtabExclusive', 'BottomoniumUpsilon', 'CharmoniumPsi', 'XToD0_D0ToHpJm', 'XToD0_D0ToNeutrals', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'XToDp_DpToHpHmJp', 'LambdacTopHpJm', 'DstToD0Pi_D0ToHpJm', 'DstToD0Pi_D0ToHpJmPi0', 'DstToD0Pi_D0ToHpHmPi0', 'DstToD0Pi_D0ToKsOmega', 'DstToD0Pi_D0ToHpJmEta', 'DstToD0Pi_D0ToNeutrals', 'DstToD0Pi_D0ToHpJmKs', 'EarlyData_DstToD0Pi_D0ToHpJmPi0', 'EarlyData_DstToD0Pi_D0ToHpHmPi0', 'DstToDpPi0_DpToHpPi0', 'DstToD0Pi_D0ToHpHmHpJm', 'SinglePhotonDark', 'GammaGammaControlKLMDark', 'ALP3Gamma', 'EGammaControlDark', 'InelasticDarkMatter', 'RadBhabhaV0Control', 'TauLFV', 'DimuonPlusMissingEnergy', 'ElectronMuonPlusMissingEnergy', 'DielectronPlusMissingEnergy', 'LFVZpVisible', 'TauGeneric', 'TauThrust', 'TwoTrackLeptonsForLuminosity', 'LowMassTwoTrack', 'SingleTagPseudoScalar', 'BtoPi0Pi0', 'BtoHadTracks', 'BtoHad1Pi0', 'BtoHad3Tracks1Pi0', 'BtoRhopRhom']#, 'SystematicsLambda']

#skimNames = ['SystematicsLambda']

skimNames = ['feiHadronicB0', 'feiHadronicBplus', 'feiSLB0', 'feiSLBplus', 'feiHadronic', 'feiSL']

all_skims = [Registry.get_skim_function(skim)() for skim in skimNames]


skim = CombinedSkim(*all_skims, udstOutput=False)

variables = skim.flags
variables = []
variables.append("SoftwareTriggerResult(software_trigger_cut&skim&accept_hadron)")

ma.inputMdstList("default", TestFiles, path=path)
skim(path)
ma.variablesToNtuple("", variables, filename="skim_flag_ntuple.root", path=path)
b2.process(path, max_event=1000)





