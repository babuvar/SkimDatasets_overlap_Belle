import uproot
import pandas as pd
from ROOT import TFile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import glob
import os
from  subclusterizer import getOverlapClusters 


#################################################################################################################
#                                           CONFIGURATION
#################################################################################################################

conres_dir = '/group/belle/users/varghese/skim_codes/SkimOverlapTools/1_Calculations/consolidated_results'

fullSkimDic = np.load('%s/skim_dic.npy'%conres_dir, allow_pickle=True).item()

#################################################################################################################
#                                           FUNCTION DEFINITIONS
#################################################################################################################

def get_skimRetention(skim_index, retentions):

	return retentions[skim_index]


def get_skimUniqueness(skim_index, uniqueness):

	return uniqueness[skim_index]

def print_skimRetentions(skimList, conres_dir=conres_dir, fullSkimDic=fullSkimDic):

	#load retention file
	retentions = np.load('%s/skim_retentions.npy'%conres_dir)	

	for skim in skimList:
		skim_index = fullSkimDic[skim]
		print('%s skim retention = '%skim,'{:0.2e}'.format(get_skimRetention(skim_index, retentions)), ' %')

	return

def print_skimUniquenesses(skimList, conres_dir=conres_dir, fullSkimDic=fullSkimDic):
	
	#load uniqueness file
	uniqueness = np.load('%s/uniqueness_skim.npy'%conres_dir)

	for skim in skimList:
		skim_index = fullSkimDic[skim]
		print('%s skim uniqueness = '%skim,'{:0.2e}'.format(get_skimUniqueness(skim_index, uniqueness)), ' %')

	return

def get_skimRetUniq_sorted(skimList, conres_dir=conres_dir, fullSkimDic=fullSkimDic):

	#load retention and uniqueness
	retentions = np.load('%s/skim_retentions.npy'%conres_dir)
	uniqueness = np.load('%s/uniqueness_skim.npy'%conres_dir)

	
	ret_list=[]; uniq_list =[]
	for skim in skimList:
		skim_index = fullSkimDic[skim]
		uniq_list.append(get_skimUniqueness(skim_index, uniqueness))
		ret_list.append(get_skimRetention(skim_index, retentions))
		
	order = np.argsort(ret_list)
	order = np.flip(order)
	skimList_ordered = [skimList[i] for i in order]
	uniq_list_ordered = [uniq_list[i] for i in order]
	ret_list_ordered = [ret_list[i] for i in order]

	return skimList_ordered, uniq_list_ordered, ret_list_ordered


def get_skimOverlap(skim_index1, skim_index2, overlaps):

	return overlaps[skim_index1, skim_index2]


def print_skimOverlaps(skimList1, skimList2, conres_dir=conres_dir, fullSkimDic=fullSkimDic):

	#load overlap file
	overlaps = np.load('%s/skim_overlaps.npy'%conres_dir)

	for skim1 in skimList1:
		skim_index1 = fullSkimDic[skim1]
		for skim2 in skimList2:
			skim_index2 = fullSkimDic[skim2]
			print('Overlap(%s, %s) = '%(skim1, skim2),'{:0.2e}'.format(get_skimOverlap(skim_index1, skim_index2, overlaps)), ' %')

	return

def get_skimOverlapMatrix(skimList1, skimList2, conres_dir=conres_dir, fullSkimDic=fullSkimDic):

	#load overlap file
	overlaps = np.load('%s/skim_overlaps.npy'%conres_dir)
	len1 = len(skimList1); len2 = len(skimList2)
	overlapMatrix = np.zeros((len1, len2))	

	for i_skim1, skim1 in enumerate(skimList1):
		skim_index1 = fullSkimDic[skim1]
		for i_skim2, skim2 in enumerate(skimList2):
			skim_index2 = fullSkimDic[skim2]
			overlapMatrix[i_skim1, i_skim2] = get_skimOverlap(skim_index1, skim_index2, overlaps)

	return overlapMatrix


def get_clusterRetention(skimList, conres_dir=conres_dir, fullSkimDic=fullSkimDic):

	if len(skimList) == 1 :
		retentions = np.load('%s/skim_retentions.npy'%conres_dir)
		skim_index = fullSkimDic[skimList[0]]
		clusterRetention = get_skimRetention(skim_index, retentions)
		return clusterRetention

	#load nonzero skim file
	df_nonzero = np.load('%s/nonzero_skim_events.npy'%conres_dir)
	ntot = np.load('%s/ntot.npy'%conres_dir)
	#get cluster indices w.r.t. original skim-list
	clusterindices=[]
	for skim in skimList:
		skimIndex = fullSkimDic[skim]
		clusterindices.append(skimIndex)
	df_nonzero = df_nonzero[:, clusterindices]	

	events_nonzero = df_nonzero.any(axis=1) 
	n_nonZeroEvents = events_nonzero.sum()

	clusterRetention = (n_nonZeroEvents*100)/ntot

	return clusterRetention

def print_cluster_properties(skimList, subclustering_threshold=80, printFullOverlap=True):

	#Print overall cluster retention
	clusterRetention = get_clusterRetention(skimList)
	print('Overall cluster retention = {:0.2e}'.format(clusterRetention),' %\n')

	skimList_ordered, uniq_list_ordered, ret_list_ordered = get_skimRetUniq_sorted(skimList)
	#Print out retentions and uniqueness
	print('{: <35}'.format('Skim'),'retention (%)\tuniqueness (%)\n')
	for i_skim, skim in enumerate(skimList_ordered):
		print('{: <35}'.format(skim), '{:0.2e}'.format(ret_list_ordered[i_skim]), '\t\t{:0.2e}'.format(uniq_list_ordered[i_skim]))


	overlapMatrix = get_skimOverlapMatrix(skimList_ordered, skimList_ordered)
	if printFullOverlap:
		#print overlaps
		print('\n\n     {: <39}'.format('Skim'), end='')
		for i_skim, skim in enumerate(skimList_ordered):
			print('({: >2})       '.format(i_skim), end='')
		print('')
		for i_skim, skim in enumerate(skimList_ordered):
			print('({: >2}) {: <35}'.format(i_skim, skim), end='')
			for j_skim, skim2 in enumerate(skimList_ordered):
				print('   {:0.2e}'.format(overlapMatrix[i_skim, j_skim]), end='')	
			print('')


	#Look for sub-clusters and print them
	num_clusters, cluster_list = getOverlapClusters(overlapMatrix, skimList, subclustering_threshold)
	print('\nNumber of clusters for threshold %s-percent overlap= '%subclustering_threshold, num_clusters)
	print('\nclusters : ')
	for i, cluster in enumerate(cluster_list):
		print('cluster-%s ='%(i+1), cluster, end='')
		print(', retention = {:0.2e}'.format(get_clusterRetention(cluster)), ' %\n')

	return	


#################################################################################################################
#                                           MAIN
#################################################################################################################


if __name__ == '__main__':


	#myskimlist = ['B0toDstarRho_D0pi_Kpi', 'BtoPi0Pi0', 'B0toDD_Kpipi_Kspi', 'TDCPV_qqs']
	myskimlist = ['SinglePhotonDark', 'DielectronPlusMissingEnergy', 'BottomoniumUpsilon', 'TauThrust']
	myskimlist2 = ['DstToD0Pi_D0ToHpHmPi0', 'RadBhabhaV0Control', 'BtoHadTracks']	
	bigSkimList = ['BtoXgamma', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'SystematicsPhiGamma', 'DstToD0Pi_D0ToKsOmega', 'BtoD0h_Kpi', 'SystematicsBhabha', 'BtoHad1Pi0', 'DstToDpPi0_DpToHpPi0', 'BtoD0h_Kpipipi_Kpipi0', 'LeptonicUntagged', 'LFVZpVisible', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'B0toDpi_Kspi', 'BtoD0rho_Kpi', 'BottomoniumUpsilon', 'XToD0_D0ToNeutrals', 'DstToD0Pi_D0ToNeutrals', 'BtoD0h_Kspipipi0', 'BtoXll', 'BtoRhopRhom', 'DimuonPlusMissingEnergy']
	#print_skimRetentions(myskimlist)
	#print_skimUniquenesses(myskimlist)
	#print_skimOverlaps(myskimlist, myskimlist)
	#get_skimOverlapMatrix(myskimlist, myskimlist2)
	print_cluster_properties(bigSkimList, printFullOverlap=False)
	
	'''
	numblocks = np.divmod(len(bigSkimList,), 12)[0] + 1
	blocks = np.array_split(bigSkimList, 5)
	for i in range(5):
		print('\n\n\n%s'%blocks[i])	
	'''




