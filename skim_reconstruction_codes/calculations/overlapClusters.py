import uproot
import pandas as pd
from ROOT import TFile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def split_prop(var):

	if isinstance(var, str):
		return (var, {})
	else:
		return var

def getOverlapClusters(overlap_mat, skimList, overlap_Threshold):

	cluster_index = np.zeros((len(skimList),), dtype=int)
	#print(cluster_index.shape)
	# initialize cluster_index to be same as skimList-index
	for i in range(len(skimList)):
		cluster_index[i] = i
	#print(cluster_index)

	#Overlap-finding loop
	changes = 99 # initialize with random non-zero number
	while changes != 0:
		changes = clusterFind(overlap_mat, cluster_index, overlap_Threshold)

	unique_cluster_indicess = np.unique(cluster_index)
	num_clusters = unique_cluster_indicess.size
	#print(cluster_index)
	#print(unique_cluster_indicess)
	#print(num_clusters)

	#get list of clusters, each cluster being a list of skims
	cluster_list = []
	for unq_idx in unique_cluster_indicess:
		cluster = []
		for i, cl_idx in enumerate(cluster_index) :
			if unq_idx == cl_idx:
				cluster.append(skimList[i])
		cluster_list.append(cluster)


	return num_clusters, cluster_list


def clusterFind(overlap_mat, cluster_index, overlap_Threshold):

	changes = 0

	for i in range(len(skimList)):
		for j in range(i+1, len(skimList)):
			#check if overlap-threshold is surpassed for the i-j skim combination
			if (overlap_mat[i,j] > overlap_Threshold) and (cluster_index[i] != cluster_index[j]):
				changes = changes + 1
				lower_cluster_index = min(cluster_index[i], cluster_index[j])
				cluster_index[i] = lower_cluster_index
				cluster_index[j] = lower_cluster_index
	#print('changes = ',changes)
	#print(cluster_index)

	return changes		
	


skimList = ['Random', 'SystematicsTracking', 'Resonance', 'SystematicsRadMuMu', 'SystematicsEELL', 'SystematicsRadEE', 'SystematicsLambda', 'SystematicsPhiGamma', 'SystematicsFourLeptonFromHLTFlag', 'SystematicsRadMuMuFromHLTFlag', 'SystematicsJpsi', 'SystematicsKshort', 'SystematicsBhabha', 'SystematicsDstar', 'PRsemileptonicUntagged', 'LeptonicUntagged', 'dilepton', 'SLUntagged', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'BtoXgamma', 'BtoXll', 'BtoXll_LFV', 'inclusiveBplusToKplusNuNu', 'TDCPV_ccs', 'TDCPV_qqs', 'BtoD0h_Kspi0', 'BtoD0h_Kspipipi0', 'B0toDpi_Kpipi', 'B0toDpi_Kspi', 'B0toDstarPi_D0pi_Kpi', 'B0toDstarPi_D0pi_Kpipipi_Kpipi0', 'B0toDrho_Kpipi', 'B0toDrho_Kspi', 'B0toDstarRho_D0pi_Kpi', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'BtoD0h_hh', 'BtoD0h_Kpi', 'BtoD0h_Kpipipi_Kpipi0', 'BtoD0h_Kshh', 'BtoD0rho_Kpi', 'BtoD0rho_Kpipipi_Kpipi0', 'B0toDD_Kpipi_Kspi', 'B0toDstarD', 'InclusiveLambda', 'BottomoniumEtabExclusive', 'BottomoniumUpsilon', 'CharmoniumPsi', 'XToD0_D0ToHpJm', 'XToD0_D0ToNeutrals', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'XToDp_DpToHpHmJp', 'LambdacTopHpJm', 'DstToD0Pi_D0ToHpJm', 'DstToD0Pi_D0ToHpJmPi0', 'DstToD0Pi_D0ToHpHmPi0', 'DstToD0Pi_D0ToKsOmega', 'DstToD0Pi_D0ToHpJmEta', 'DstToD0Pi_D0ToNeutrals', 'DstToD0Pi_D0ToHpJmKs', 'EarlyData_DstToD0Pi_D0ToHpJmPi0', 'EarlyData_DstToD0Pi_D0ToHpHmPi0', 'DstToDpPi0_DpToHpPi0', 'DstToD0Pi_D0ToHpHmHpJm', 'SinglePhotonDark', 'GammaGammaControlKLMDark', 'ALP3Gamma', 'EGammaControlDark', 'InelasticDarkMatter', 'RadBhabhaV0Control', 'TauLFV', 'DimuonPlusMissingEnergy', 'ElectronMuonPlusMissingEnergy', 'DielectronPlusMissingEnergy', 'LFVZpVisible', 'TauGeneric', 'TauThrust', 'TwoTrackLeptonsForLuminosity', 'LowMassTwoTrack', 'SingleTagPseudoScalar', 'BtoPi0Pi0', 'BtoHadTracks', 'BtoHad1Pi0', 'BtoHad3Tracks1Pi0', 'BtoRhopRhom', 'SystematicsLambda']
skimList.remove('DstToD0Pi_D0ToRare')
skimList.remove('SystematicsLambda')


overlap_mat = np.load('overlap2.npy')

thresholds = []
num_clusterss = []

for threshold in np.arange(10.0, 100.0, 5.0):

	num_clusters, cluster_list = getOverlapClusters(overlap_mat, skimList, threshold)
	
	thresholds.append(threshold)
	num_clusterss.append(num_clusters)

	'''
	print('\n---------------------------------------')
	print('\nthreshold = %s %%'%threshold)
	print('num_clusters = ', num_clusters)
	print('\nclusters : ')
	for i, cluster in enumerate(cluster_list):
		print('cluster-%s ='%(i+1), cluster)
	'''


#print threshold vs num-clusters graph
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
plt.scatter(thresholds, num_clusterss, c='r')
plt.xlabel('overlap threshold (%)')
plt.ylabel('number of clusters')
plt.title('Overlap-threshold vs num-clusters')
plt.grid()
plt.savefig('threshold_vs_nClusters.png')
plt.close(fig)

















