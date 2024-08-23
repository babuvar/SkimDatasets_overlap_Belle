import os
from ROOT import TFile, RDF
import uproot
import pandas as pd
import numpy as np

def split_prop(var):
	if isinstance(var, str):
		return (var, {})
	else:
		return var

skimList = ['Random', 'SystematicsTracking', 'Resonance', 'SystematicsRadMuMu', 'SystematicsEELL', 'SystematicsRadEE', 'SystematicsLambda', 'SystematicsPhiGamma', 'SystematicsFourLeptonFromHLTFlag', 'SystematicsRadMuMuFromHLTFlag', 'SystematicsJpsi', 'SystematicsKshort', 'SystematicsBhabha', 'SystematicsDstar', 'PRsemileptonicUntagged', 'LeptonicUntagged', 'dilepton', 'SLUntagged', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'BtoXgamma', 'BtoXll', 'BtoXll_LFV', 'inclusiveBplusToKplusNuNu', 'TDCPV_ccs', 'TDCPV_qqs', 'BtoD0h_Kspi0', 'BtoD0h_Kspipipi0', 'B0toDpi_Kpipi', 'B0toDpi_Kspi', 'B0toDstarPi_D0pi_Kpi', 'B0toDstarPi_D0pi_Kpipipi_Kpipi0', 'B0toDrho_Kpipi', 'B0toDrho_Kspi', 'B0toDstarRho_D0pi_Kpi', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'BtoD0h_hh', 'BtoD0h_Kpi', 'BtoD0h_Kpipipi_Kpipi0', 'BtoD0h_Kshh', 'BtoD0rho_Kpi', 'BtoD0rho_Kpipipi_Kpipi0', 'B0toDD_Kpipi_Kspi', 'B0toDstarD', 'InclusiveLambda', 'BottomoniumEtabExclusive', 'BottomoniumUpsilon', 'CharmoniumPsi', 'XToD0_D0ToHpJm', 'XToD0_D0ToNeutrals', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'XToDp_DpToHpHmJp', 'LambdacTopHpJm', 'DstToD0Pi_D0ToHpJm', 'DstToD0Pi_D0ToHpJmPi0', 'DstToD0Pi_D0ToHpHmPi0', 'DstToD0Pi_D0ToKsOmega', 'DstToD0Pi_D0ToHpJmEta', 'DstToD0Pi_D0ToNeutrals', 'DstToD0Pi_D0ToHpJmKs', 'EarlyData_DstToD0Pi_D0ToHpJmPi0', 'EarlyData_DstToD0Pi_D0ToHpHmPi0', 'DstToDpPi0_DpToHpPi0', 'DstToD0Pi_D0ToHpHmHpJm', 'SinglePhotonDark', 'GammaGammaControlKLMDark', 'ALP3Gamma', 'EGammaControlDark', 'InelasticDarkMatter', 'RadBhabhaV0Control', 'TauLFV', 'DimuonPlusMissingEnergy', 'ElectronMuonPlusMissingEnergy', 'DielectronPlusMissingEnergy', 'LFVZpVisible', 'TauGeneric', 'TauThrust', 'TwoTrackLeptonsForLuminosity', 'LowMassTwoTrack', 'SingleTagPseudoScalar', 'BtoPi0Pi0', 'BtoHadTracks', 'BtoHad1Pi0', 'BtoHad3Tracks1Pi0', 'BtoRhopRhom', 'SystematicsLambda']
skimList.remove('DstToD0Pi_D0ToRare')
skimList.remove('SystematicsLambda')

skimList = ['Random', 'SystematicsTracking', 'Resonance']

rootdir = 'skimFlag_rootFiles'
base_vars = ['__experiment__', '__run__', '__event__']
all_vars = base_vars.copy()
treeKey = 'variables'
count = -1

for skim in skimList:

	count = count + 1
	rootfile = '%s/%s.root'%(rootdir, skim)
	skim_vars = base_vars.copy()
	skim_vars.append('passes_%s'%skim)
	all_vars.append('passes_%s'%skim)

	if count == 0:
		df_all = uproot.open(rootfile)[treeKey].arrays([split_prop(i)[0] for i in skim_vars], library='pd')

	elif count > 0:
		df_skim = uproot.open(rootfile)[treeKey].arrays([split_prop(i)[0] for i in skim_vars], library='pd')
		df_all = pd.merge(df_all, df_skim, on=base_vars)
		
	print('added the %s skim'%skim)

print('\n---------- X 0 X ----------')
print('shape of merged skimFlag-dataFrame = ', df_all.shape)
data = {key: df_all[key].values for key in all_vars}
rdf = RDF.MakeNumpyDataFrame(data)
rdf.Snapshot(treeKey, '%s/merged_skimFkags.root'%rootdir)
#df_all.to_pickle('%s/merged_skimFkags.pkl'%rootdir)
print('Finished merging skim-rootFiles')
print('---------- X 0 X ----------\n')




