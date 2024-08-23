import uproot
import pandas as pd
from ROOT import TFile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from reduced_overlap_matrix import return_reduced_overlap_matrix

def plot_overlap(overlap_matrix, skimList, name):

	fig = plt.figure(figsize=(20, 16))
	ax = fig.add_subplot(111)
	cax = ax.matshow(overlap_matrix, cmap=plt.get_cmap('Reds'), norm=LogNorm(vmin=0.01, vmax=100))
	for (i, j), z in np.ndenumerate(overlap_matrix):
		ax.text(j, i, '{:0.2f}'.format(z), ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white', edgecolor='white'))
	plt.title('Overlap matrix of various %s skims (percentage)'%name)
	fig.colorbar(cax)
	tick_marks = np.arange(overlap_matrix.shape[0])
	plt.xticks(tick_marks, skimList, rotation=45, ha='left')
	plt.yticks(tick_marks, skimList)
	plt.tight_layout()
	plt.savefig('ov_plots/%s.png'%name)
	plt.close(fig)


skimList = ['Random', 'SystematicsTracking', 'Resonance', 'SystematicsRadMuMu', 'SystematicsEELL', 'SystematicsRadEE', 'SystematicsLambda', 'SystematicsPhiGamma', 'SystematicsFourLeptonFromHLTFlag', 'SystematicsRadMuMuFromHLTFlag', 'SystematicsJpsi', 'SystematicsKshort', 'SystematicsBhabha', 'SystematicsDstar', 'PRsemileptonicUntagged', 'LeptonicUntagged', 'dilepton', 'SLUntagged', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'BtoXgamma', 'BtoXll', 'BtoXll_LFV', 'inclusiveBplusToKplusNuNu', 'TDCPV_ccs', 'TDCPV_qqs', 'BtoD0h_Kspi0', 'BtoD0h_Kspipipi0', 'B0toDpi_Kpipi', 'B0toDpi_Kspi', 'B0toDstarPi_D0pi_Kpi', 'B0toDstarPi_D0pi_Kpipipi_Kpipi0', 'B0toDrho_Kpipi', 'B0toDrho_Kspi', 'B0toDstarRho_D0pi_Kpi', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'BtoD0h_hh', 'BtoD0h_Kpi', 'BtoD0h_Kpipipi_Kpipi0', 'BtoD0h_Kshh', 'BtoD0rho_Kpi', 'BtoD0rho_Kpipipi_Kpipi0', 'B0toDD_Kpipi_Kspi', 'B0toDstarD', 'InclusiveLambda', 'BottomoniumEtabExclusive', 'BottomoniumUpsilon', 'CharmoniumPsi', 'XToD0_D0ToHpJm', 'XToD0_D0ToNeutrals', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'XToDp_DpToHpHmJp', 'LambdacTopHpJm', 'DstToD0Pi_D0ToHpJm', 'DstToD0Pi_D0ToHpJmPi0', 'DstToD0Pi_D0ToHpHmPi0', 'DstToD0Pi_D0ToKsOmega', 'DstToD0Pi_D0ToHpJmEta', 'DstToD0Pi_D0ToNeutrals', 'DstToD0Pi_D0ToHpJmKs', 'EarlyData_DstToD0Pi_D0ToHpJmPi0', 'EarlyData_DstToD0Pi_D0ToHpHmPi0', 'DstToDpPi0_DpToHpPi0', 'DstToD0Pi_D0ToHpHmHpJm', 'SinglePhotonDark', 'GammaGammaControlKLMDark', 'ALP3Gamma', 'EGammaControlDark', 'InelasticDarkMatter', 'RadBhabhaV0Control', 'TauLFV', 'DimuonPlusMissingEnergy', 'ElectronMuonPlusMissingEnergy', 'DielectronPlusMissingEnergy', 'LFVZpVisible', 'TauGeneric', 'TauThrust', 'TwoTrackLeptonsForLuminosity', 'LowMassTwoTrack', 'SingleTagPseudoScalar', 'BtoPi0Pi0', 'BtoHadTracks', 'BtoHad1Pi0', 'BtoHad3Tracks1Pi0', 'BtoRhopRhom', 'SystematicsLambda']
skimList.remove('DstToD0Pi_D0ToRare')
skimList.remove('SystematicsLambda')


overlap_mat = np.load('overlap2.npy')


syst = ['SystematicsPhiGamma',  'SystematicsLambda']
SL_ME = ['LeptonicUntagged',  'B0toDstarl_Kpi_Kpipi0_Kpipipi',  'dilepton']
EWP = ['BtoXgamma',  'BtoXll',  'BtoXll_LFV',  'inclusiveBplusToKplusNuNu']
TDCPV = ['TDCPV_ccs',  'TDCPV_qqs']
Charmed_B = ['BtoD0h_Kpi',  'BtoD0h_Kpipipi_Kpipi0',  'B0toDpi_Kpipi',  'BtoD0rho_Kpi',  'BtoD0rho_Kpipipi_Kpipi0',  'B0toDrho_Kpipi',  'BtoD0h_hh',  'BtoD0h_Kshh',  'BtoD0h_Kspi0',  'B0toDstarPi_D0pi_Kpi',  'B0toDstarPi_D0pi_Kpipipi_Kpipi0',  'B0toDstarRho_D0pi_Kpi',  'B0toDstarRho_D0pi_Kpipipi_Kpipi0',  'B0toDstarD',  'BtoD0h_Kspipipi0',  'B0toDpi_Kspi',  'B0toDrho_Kspi',  'B0toDD_Kpipi_Kspi']  
Quarkonium = ['BottomoniumUpsilon',  'InclusiveLambda',  'CharmoniumPsi',  'BottomoniumEtabExclusive']
Charm = ['DstToD0Pi_D0ToHpJm',  'DstToD0Pi_D0ToHpHmPi0',  'LambdacTopHpJm',  'DstToD0Pi_D0ToHpJmPi0',  'DstToD0Pi_D0ToHpJmKs',  'XToDp_DpToKsHp',  'XToD0_D0ToHpJm',  'XToDp_DpToHpHmJp',  'DstToD0Pi_D0ToHpJmEta',  'DstToD0Pi_D0ToKsOmega',  'DstToD0Pi_D0ToHpHmHpJm',  'XToD0_D0ToNeutrals',  'DstToDpPi0_DpToHpPi0',  'DstToD0Pi_D0ToNeutrals']
Dark_Tau = ['DimuonPlusMissingEnergy',  'ElectronMuonPlusMissingEnergy',  'LFVZpVisible',  'SinglePhotonDark',  'GammaGammaControlKLMDark',  'EGammaControlDark',  'InelasticDarkMatter',  'LowMassTwoTrack',  'RadBhabhaV0Control',  'SingleTagPseudoScalar',  'TauLFV',  'TauGeneric',  'TauThrust']
Charmless_B = ['BtoHad1Pi0',  'BtoHadTracks',  'BtoRhopRhom',  'BtoPi0Pi0']

 

overlap_syst = return_reduced_overlap_matrix(overlap_mat, skimList, syst)
overlap_SL_ME = return_reduced_overlap_matrix(overlap_mat, skimList, SL_ME)
overlap_EWP = return_reduced_overlap_matrix(overlap_mat, skimList, EWP)
overlap_TDCPV = return_reduced_overlap_matrix(overlap_mat, skimList, TDCPV)
overlap_Charmed_B = return_reduced_overlap_matrix(overlap_mat, skimList, Charmed_B)
overlap_Quarkonium = return_reduced_overlap_matrix(overlap_mat, skimList, Quarkonium)
overlap_Charm = return_reduced_overlap_matrix(overlap_mat, skimList, Charm)
overlap_Dark_Tau = return_reduced_overlap_matrix(overlap_mat, skimList, Dark_Tau)
overlap_Charmless_B = return_reduced_overlap_matrix(overlap_mat, skimList, Charmless_B)


plot_overlap(overlap_syst, syst, 'syst')
plot_overlap(overlap_SL_ME, SL_ME, 'SL_ME')
plot_overlap(overlap_EWP, EWP, 'EWP')
plot_overlap(overlap_TDCPV, TDCPV, 'TDCPV')
plot_overlap(overlap_Charmed_B, Charmed_B, 'Charmed_B')
plot_overlap(overlap_Quarkonium, Quarkonium, 'Quarkonium')
plot_overlap(overlap_Charm, Charm, 'Charm')
plot_overlap(overlap_Dark_Tau, Dark_Tau, 'Dark_Tau')
plot_overlap(overlap_Charmless_B, Charmless_B, 'Charmless_B')




















