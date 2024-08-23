import numpy as np

def return_list_subset_indices(full_list, subset_list):

	index_list = []
	for item in subset_list:
		index_list.append(full_list.index(item))

	return index_list

def return_reduced_overlap_matrix(full_mat, full_list, subset_list):

	sublist_indices = return_list_subset_indices(full_list, subset_list)

	ix_grid = np.ix_(sublist_indices, sublist_indices)
	subset_mat = full_mat[ix_grid]

	return subset_mat



FullskimList = ['Random', 'SystematicsTracking', 'Resonance', 'SystematicsRadMuMu', 'SystematicsEELL', 'SystematicsRadEE', 'SystematicsLambda', 'SystematicsPhiGamma', 'SystematicsFourLeptonFromHLTFlag', 'SystematicsRadMuMuFromHLTFlag', 'SystematicsJpsi', 'SystematicsKshort', 'SystematicsBhabha', 'SystematicsDstar', 'PRsemileptonicUntagged', 'LeptonicUntagged', 'dilepton', 'SLUntagged', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'BtoXgamma', 'BtoXll', 'BtoXll_LFV', 'inclusiveBplusToKplusNuNu', 'TDCPV_ccs', 'TDCPV_qqs', 'BtoD0h_Kspi0', 'BtoD0h_Kspipipi0', 'B0toDpi_Kpipi', 'B0toDpi_Kspi', 'B0toDstarPi_D0pi_Kpi', 'B0toDstarPi_D0pi_Kpipipi_Kpipi0', 'B0toDrho_Kpipi', 'B0toDrho_Kspi', 'B0toDstarRho_D0pi_Kpi', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'BtoD0h_hh', 'BtoD0h_Kpi', 'BtoD0h_Kpipipi_Kpipi0', 'BtoD0h_Kshh', 'BtoD0rho_Kpi', 'BtoD0rho_Kpipipi_Kpipi0', 'B0toDD_Kpipi_Kspi', 'B0toDstarD', 'InclusiveLambda', 'BottomoniumEtabExclusive', 'BottomoniumUpsilon', 'CharmoniumPsi', 'XToD0_D0ToHpJm', 'XToD0_D0ToNeutrals', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'XToDp_DpToHpHmJp', 'LambdacTopHpJm', 'DstToD0Pi_D0ToHpJm', 'DstToD0Pi_D0ToHpJmPi0', 'DstToD0Pi_D0ToHpHmPi0', 'DstToD0Pi_D0ToKsOmega', 'DstToD0Pi_D0ToHpJmEta', 'DstToD0Pi_D0ToNeutrals', 'DstToD0Pi_D0ToHpJmKs', 'EarlyData_DstToD0Pi_D0ToHpJmPi0', 'EarlyData_DstToD0Pi_D0ToHpHmPi0', 'DstToDpPi0_DpToHpPi0', 'DstToD0Pi_D0ToHpHmHpJm', 'SinglePhotonDark', 'GammaGammaControlKLMDark', 'ALP3Gamma', 'EGammaControlDark', 'InelasticDarkMatter', 'RadBhabhaV0Control', 'TauLFV', 'DimuonPlusMissingEnergy', 'ElectronMuonPlusMissingEnergy', 'DielectronPlusMissingEnergy', 'LFVZpVisible', 'TauGeneric', 'TauThrust', 'TwoTrackLeptonsForLuminosity', 'LowMassTwoTrack', 'SingleTagPseudoScalar', 'BtoPi0Pi0', 'BtoHadTracks', 'BtoHad1Pi0', 'BtoHad3Tracks1Pi0', 'BtoRhopRhom', 'SystematicsLambda']

fulloverlap_mat = np.load('overlap2.npy')


sublist = ['Random', 'Resonance', 'SystematicsEELL']



subset_mat = return_reduced_overlap_matrix(fulloverlap_mat, FullskimList, sublist)


print(subset_mat)











