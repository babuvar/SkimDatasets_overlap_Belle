from clusterTools import *

'''
#Convenience lists to work with:

fullSkimList = ['B0toDstarRho_D0pi_Kpi', 'BtoPi0Pi0', 'B0toDD_Kpipi_Kspi', 'TDCPV_qqs', 'BtoHad3Tracks1Pi0', 'BtoD0h_hh', 'B0toDpi_Kpipi', 'TauThrust', 'ALP3Gamma', 'SystematicsDstar', 'B0toDstarD', 'dilepton', 'SystematicsRadMuMuFromHLTFlag', 'InclusiveLambda', 'DstToD0Pi_D0ToHpHmHpJm', 'DstToD0Pi_D0ToHpJmEta', 'XToD0_D0ToHpJm', 'DielectronPlusMissingEnergy', 'SinglePhotonDark', 'TauLFV', 'DstToD0Pi_D0ToHpJm', 'EGammaControlDark', 'InelasticDarkMatter', 'SingleTagPseudoScalar', 'DstToD0Pi_D0ToHpJmKs', 'inclusiveBplusToKplusNuNu', 'B0toDstarPi_D0pi_Kpi', 'PRsemileptonicUntagged', 'SystematicsFourLeptonFromHLTFlag', 'TauGeneric', 'B0toDrho_Kspi', 'BtoD0rho_Kpipipi_Kpipi0', 'BtoXgamma', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'SystematicsPhiGamma', 'DstToD0Pi_D0ToKsOmega', 'BtoD0h_Kpi', 'SystematicsBhabha', 'BtoHad1Pi0', 'DstToDpPi0_DpToHpPi0', 'BtoD0h_Kpipipi_Kpipi0', 'LeptonicUntagged', 'LFVZpVisible', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'B0toDpi_Kspi', 'BtoD0rho_Kpi', 'BottomoniumUpsilon', 'XToD0_D0ToNeutrals', 'DstToD0Pi_D0ToNeutrals', 'BtoD0h_Kspipipi0', 'BtoXll', 'BtoRhopRhom', 'DimuonPlusMissingEnergy', 'DstToD0Pi_D0ToHpJmPi0', 'ElectronMuonPlusMissingEnergy', 'LowMassTwoTrack', 'BottomoniumEtabExclusive', 'BtoD0h_Kspi0', 'SystematicsLambda', 'B0toDrho_Kpipi', 'BtoXll_LFV', 'CharmoniumPsi', 'LambdacTopHpJm', 'SLUntagged', 'BtoD0h_Kshh', 'B0toDstarPi_D0pi_Kpipipi_Kpipi0', 'TDCPV_ccs', 'GammaGammaControlKLMDark', 'SystematicsJpsi', 'SystematicsKshort', 'DstToD0Pi_D0ToHpHmPi0', 'RadBhabhaV0Control', 'BtoHadTracks', 'XToDp_DpToHpHmJp']

syst = ['SystematicsPhiGamma',  'SystematicsLambda']
SL_ME = ['LeptonicUntagged',  'B0toDstarl_Kpi_Kpipi0_Kpipipi',  'dilepton']
EWP = ['BtoXgamma',  'BtoXll',  'BtoXll_LFV',  'inclusiveBplusToKplusNuNu']
TDCPV = ['TDCPV_ccs',  'TDCPV_qqs']
Charmed_B = ['BtoD0h_Kpi',  'BtoD0h_Kpipipi_Kpipi0',  'B0toDpi_Kpipi',  'BtoD0rho_Kpi',  'BtoD0rho_Kpipipi_Kpipi0',  'B0toDrho_Kpipi',  'BtoD0h_hh',  'BtoD0h_Kshh',  'BtoD0h_Kspi0',  'B0toDstarPi_D0pi_Kpi',  'B0toDstarPi_D0pi_Kpipipi_Kpipi0',  'B0toDstarRho_D0pi_Kpi',  'B0toDstarRho_D0pi_Kpipipi_Kpipi0',  'B0toDstarD',  'BtoD0h_Kspipipi0',  'B0toDpi_Kspi',  'B0toDrho_Kspi',  'B0toDD_Kpipi_Kspi']  
Quarkonium = ['BottomoniumUpsilon',  'InclusiveLambda',  'CharmoniumPsi',  'BottomoniumEtabExclusive']
Charm = ['DstToD0Pi_D0ToHpJm',  'DstToD0Pi_D0ToHpHmPi0',  'LambdacTopHpJm',  'DstToD0Pi_D0ToHpJmPi0',  'DstToD0Pi_D0ToHpJmKs',  'XToDp_DpToKsHp',  'XToD0_D0ToHpJm',  'XToDp_DpToHpHmJp',  'DstToD0Pi_D0ToHpJmEta',  'DstToD0Pi_D0ToKsOmega',  'DstToD0Pi_D0ToHpHmHpJm',  'XToD0_D0ToNeutrals',  'DstToDpPi0_DpToHpPi0',  'DstToD0Pi_D0ToNeutrals']
Dark_Tau = ['DimuonPlusMissingEnergy',  'ElectronMuonPlusMissingEnergy',  'LFVZpVisible',  'SinglePhotonDark',  'GammaGammaControlKLMDark',  'EGammaControlDark',  'InelasticDarkMatter',  'LowMassTwoTrack',  'RadBhabhaV0Control',  'SingleTagPseudoScalar',  'TauLFV',  'TauGeneric',  'TauThrust']
Charmless_B = ['BtoHad1Pi0',  'BtoHadTracks',  'BtoRhopRhom',  'BtoPi0Pi0']


WG_names = ['syst', 'SL_ME', 'EWP', 'TDCPV', 'Charmed_B', 'Quarkonium', 'Charm', 'Dark_Tau', 'Charmless_B']
WG_dic = {'syst' : syst,
          'SL_ME' : SL_ME,
          'EWP' : EWP,
          'TDCPV' : TDCPV,
          'Charmed_B' : Charmed_B,
          'Quarkonium' : Quarkonium,
          'Charm' : Charm,
          'Dark_Tau' : Dark_Tau,
          'Charmless_B' : Charmless_B}
'''





myskimlist = ['BtoXgamma', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'SystematicsPhiGamma', 'DstToD0Pi_D0ToKsOmega', 'BtoD0h_Kpi', 'SystematicsBhabha', 'BtoHad1Pi0', 'DstToDpPi0_DpToHpPi0', 'BtoD0h_Kpipipi_Kpipi0', 'LeptonicUntagged', 'LFVZpVisible', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'B0toDpi_Kspi', 'BtoD0rho_Kpi']

#require an overlap threshold of 80% between two skims to look for sub-clusters
print_cluster_properties(myskimlist, subclustering_threshold=80, printFullOverlap=False)









