#################################################################################################################
# This file will have the capability to produce the following pre-calculation results : 
# 0) Dictionary of list-index of skim in original skimlist used to calculate and store intermediate results.
#    This will enable usage of intermediate results without the knowledge of the skim-order of the original list
# 1) Total number of events in per index file : 1 number per index file
# 2) Total number of passed-events for each skim : array[76] per index-file 
# 3) Total number of intersection and union events between any two skims : 2 x array[76][76] per index-file
# 4) Per-event skim multiplicity : array[50] per index-file (Go from 0 upto 49 multiplicity)
# 5) Unique events for each skim :  array[76] per index-file
#################################################################################################################


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



#################################################################################################################
#                                           CONFIGURATION
#################################################################################################################

#Note that this is the original list of skims and the order of skims matter when storing numpy-result-arrays in the precalcuations step
skimList = ['B0toDstarRho_D0pi_Kpi', 'BtoPi0Pi0', 'B0toDD_Kpipi_Kspi', 'TDCPV_qqs', 'BtoHad3Tracks1Pi0', 'BtoD0h_hh', 'B0toDpi_Kpipi', 'TauThrust', 'ALP3Gamma', 'SystematicsDstar', 'B0toDstarD', 'dilepton', 'SystematicsRadMuMuFromHLTFlag', 'InclusiveLambda', 'DstToD0Pi_D0ToHpHmHpJm', 'DstToD0Pi_D0ToHpJmEta', 'XToD0_D0ToHpJm', 'DielectronPlusMissingEnergy', 'SinglePhotonDark', 'TauLFV', 'DstToD0Pi_D0ToHpJm', 'EGammaControlDark', 'InelasticDarkMatter', 'SingleTagPseudoScalar', 'DstToD0Pi_D0ToHpJmKs', 'inclusiveBplusToKplusNuNu', 'B0toDstarPi_D0pi_Kpi', 'PRsemileptonicUntagged', 'SystematicsFourLeptonFromHLTFlag', 'TauGeneric', 'B0toDrho_Kspi', 'BtoD0rho_Kpipipi_Kpipi0', 'BtoXgamma', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'SystematicsPhiGamma', 'DstToD0Pi_D0ToKsOmega', 'BtoD0h_Kpi', 'SystematicsBhabha', 'BtoHad1Pi0', 'DstToDpPi0_DpToHpPi0', 'BtoD0h_Kpipipi_Kpipi0', 'LeptonicUntagged', 'LFVZpVisible', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'B0toDpi_Kspi', 'BtoD0rho_Kpi', 'BottomoniumUpsilon', 'XToD0_D0ToNeutrals', 'DstToD0Pi_D0ToNeutrals', 'BtoD0h_Kspipipi0', 'BtoXll', 'BtoRhopRhom', 'DimuonPlusMissingEnergy', 'DstToD0Pi_D0ToHpJmPi0', 'ElectronMuonPlusMissingEnergy', 'LowMassTwoTrack', 'BottomoniumEtabExclusive', 'BtoD0h_Kspi0', 'SystematicsLambda', 'B0toDrho_Kpipi', 'BtoXll_LFV', 'CharmoniumPsi', 'LambdacTopHpJm', 'SLUntagged', 'BtoD0h_Kshh', 'B0toDstarPi_D0pi_Kpipipi_Kpipi0', 'TDCPV_ccs', 'GammaGammaControlKLMDark', 'SystematicsJpsi', 'SystematicsKshort', 'DstToD0Pi_D0ToHpHmPi0', 'RadBhabhaV0Control', 'BtoHadTracks', 'XToDp_DpToHpHmJp']


rootdir = '/group/belle/users/varghese/skim_codes/high_stat/merged_rootfiles'
outdir = '/group/belle/users/varghese/skim_codes/SkimOverlapTools/1_Calculations/results'
indices = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 38, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 73, 74, 76, 77, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 99, 100, 101, 102, 103, 104, 105, 106, 109, 110, 112, 113, 114, 115, 116, 117, 118]



treeKey = 'variables'

#################################################################################################################
#                                           FUNCTION DEFINITIONS
#################################################################################################################


def split_prop(var):
	if isinstance(var, str):
		return (var, {})
	else:
		return var


#Save skim-ordering in original skim-list
def save_skim_order(skimList, outdir):

	skim_order = {}
	for i_skim, skim in enumerate(skimList):
		skim_order[skim] = i_skim
	np.save('%s/skim_dic.npy'%outdir, skim_order, allow_pickle=True)
	print('Skim order saved')

	return

#load rootfile corresponding to an index and return it as an numpy array
def loadFile(rootdir, index, treeKey, skimListi):

	all_vars = ['__experiment__', '__run__', '__event__']
	for skim in skimList:
		all_vars.append('passes_%s'%skim)
	df_index = uproot.open('%s/merged_skimFlags_%s.root'%(rootdir, index))[treeKey].arrays([split_prop(i)[0] for i in all_vars], library='pd')
	
	return df_index


#total number of events per file
def save_ntot(rootdir, index, treeKey, skimList, outdir):

	df_index = loadFile(rootdir, index, treeKey, skimList)
	ntot = df_index.shape[0]
	print('total number of events of file-%s = '%index, ntot)
	np.save('%s/ntot_file%s.npy'%(outdir,index), ntot, allow_pickle=True)

	return


#total number of passes events per skim per file
def save_npass(rootdir, index, treeKey, skimList, outdir):

	df_index = loadFile(rootdir, index, treeKey, skimList)
	npass_array = np.zeros((76))
	for i_skim, skim in enumerate(skimList):
		npass_array[i_skim] = df_index['passes_%s'%skim].sum()	
	print('Saved n-pass array for file-%s'%index)	
	np.save('%s/npass_file%s.npy'%(outdir, index), npass_array, allow_pickle=True)

	return


#number of union and intersection events of two skims
def save_union_intersection(rootdir, index, treeKey, skimList, outdir):
	
	df_index = loadFile(rootdir, index, treeKey, skimList)	
	intersection_matrix = np.zeros((76, 76)) 
	union_matrix = np.zeros((76, 76)) 

	for i_skim, skim in enumerate(skimList):
		for j_skim, skim2 in enumerate(skimList):
			union = np.logical_or(df_index['passes_%s'%skim], df_index['passes_%s'%skim2])
			union_matrix[i_skim, j_skim] = union.sum()
			intersection = np.logical_and(df_index['passes_%s'%skim], df_index['passes_%s'%skim2])
			intersection_matrix[i_skim, j_skim] = intersection.sum()
	np.save('%s/union_file%s.npy'%(outdir, index), union_matrix, allow_pickle=True)
	np.save('%s/intersection_file%s.npy'%(outdir, index), intersection_matrix, allow_pickle=True)
	print('Saved union and intersection events for file %s'%index)

	return


#get per-event skim multiplicity
def save_skim_multiplicity(rootdir, index, treeKey, skimList, outdir):

	df_index = loadFile(rootdir, index, treeKey, skimList)
	df_onlyskims = df_index.drop(columns=['__experiment__', '__run__', '__event__'])
	event_skim_multiplicity  = df_onlyskims.sum(axis=1)
	#Retain multiplicity upto 50
	multiplicity_vals = [*range(50)]
	multiplicity = np.zeros(50)
	for mult_val in multiplicity_vals:
		multiplicity[mult_val] = np.count_nonzero(event_skim_multiplicity == mult_val)	
	np.save('%s/skim_multiplicity_file%s.npy'%(outdir, index), multiplicity, allow_pickle=True)
	print('Saved skim-multiplicity for file-%s'%index)

	return


#get uniqueness of each skim
def save_unique_skim_events(rootdir, index, treeKey, skimList, outdir):

	df_index = loadFile(rootdir, index, treeKey, skimList)
	df_onlyskims = df_index.drop(columns=['__experiment__', '__run__', '__event__'])
	n_uniqueEvents_array = np.zeros((76))	
	for i_skim, skim in enumerate(skimList):
		column = 'passes_%s'%skim
		df_remainingSkims = df_onlyskims.drop(columns=[column])
		df_ifAnyNonZero = df_remainingSkims.any(axis=1)
		df_ifAllZeros = ~df_ifAnyNonZero
		unique_events = np.logical_and(df_index[column], df_ifAllZeros)
		n_unique = unique_events.sum()
		n_uniqueEvents_array[i_skim] = n_unique
	np.save('%s/skim_unique_events_file%s.npy'%(outdir, index), n_uniqueEvents_array, allow_pickle=True)
	print('Saved unique-skim events array for file-%s'%index)

	return


#get all events which passes at least one skim
def save_nonzero_events(rootdir, indexList, treeKey, skimList, outdir):

	df_all = pd.DataFrame()
	for index in indexList:
		df_index = loadFile(rootdir, index, treeKey, skimList)
		df_onlyskims = df_index.drop(columns=['__experiment__', '__run__', '__event__'])
		df_onlyskims_nonzero = df_onlyskims[df_onlyskims.any(axis=1)]
		df_all = df_all.append(df_onlyskims_nonzero)
		print('Appended non-zero events for file-%s'%index)
	np.save('%s/nonzero_skim_events.npy'%outdir, df_all, allow_pickle=True)
	print('Saved all nonzero skim events')

	return


#################################################################################################################
#                                           MAIN
#################################################################################################################


if __name__ == '__main__':

	#one time	
	#save_skim_order(skimList, outdir)
	save_nonzero_events(rootdir, indices, treeKey, skimList, outdir)
	'''
	#once per input file
	for index in indices:
		#save_ntot(rootdir, index, treeKey, skimList, outdir)
		#save_npass(rootdir, index, treeKey, skimList, outdir)
		#save_union_intersection(rootdir, index, treeKey, skimList, outdir)
		#save_skim_multiplicity(rootdir, index, treeKey, skimList, outdir)
		#save_unique_skim_events(rootdir, index, treeKey, skimList, outdir)
	'''








