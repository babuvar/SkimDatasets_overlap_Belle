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

fullSkimDic = np.load('skim_dic.npy', allow_pickle=True).item()
fullSkimList = fullSkimDic.keys()


indices = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 38, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 73, 74, 76, 77, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 99, 100, 101, 102, 103, 104, 105, 106, 109, 110, 112, 113, 114, 115, 116, 117, 118]


result_dir = '/group/belle/users/varghese/skim_codes/SkimOverlapTools/1_Calculations/results'
conres_dir = '/group/belle/users/varghese/skim_codes/SkimOverlapTools/1_Calculations/consolidated_results'

#################################################################################################################
#                                           FUNCTION DEFINITIONS
#################################################################################################################


def split_prop(var):
	if isinstance(var, str):
		return (var, {})
	else:
		return var

#return the error on a fraction in %, considering the poissonian error on the numerator and denominator
def get_err_frac(num, den):

	e_num = np.sqrt(num)
	e_den = np.sqrt(den)
	e_frac = (np.sqrt((den*den*e_num*e_num) + (num*num*e_den*e_den)) * 100) / (den * den)

	return e_frac


def get_consolidated_retention(indices, result_dir, fullSkimList):

	skim_retentions = np.zeros(76)
	n_tot_all = 0
	npass_skim = np.zeros(76)

	for index in indices:
		ntot_file = '%s/ntot_file%s.npy'%(result_dir, index); ntot_index = np.load(ntot_file)
		npass_file = '%s/npass_file%s.npy'%(result_dir, index); npass_index = np.load(npass_file)

		n_tot_all = np.add(n_tot_all, ntot_index)
		npass_skim = np.add(npass_skim, npass_index)

	for i_skim, skim in enumerate(fullSkimList):
		skim_retentions[i_skim] = (npass_skim[i_skim]*100/n_tot_all) # Store retentions in percentage

	return skim_retentions, npass_skim, n_tot_all

def get_consolidated_overlaps(indices, result_dir, fullSkimList):

	skim_overlaps = np.zeros((76, 76))
	npass_skim = np.zeros(76)
	intersection_skim = np.zeros((76, 76))
	union_skim = np.zeros((76, 76))

	for index in indices:
		intersection_file = '%s/intersection_file%s.npy'%(result_dir, index); intersection_index = np.load(intersection_file)
		intersection_skim = np.add(intersection_skim, intersection_index)
		npass_file = '%s/npass_file%s.npy'%(result_dir, index); npass_index = np.load(npass_file)
		npass_skim = np.add(npass_skim, npass_index)		

	for i_skim, skim in enumerate(fullSkimList):
		for j_skim, skim2 in enumerate(fullSkimList):
			skim_overlaps[i_skim, j_skim] = (intersection_skim[i_skim, j_skim]*100) / min(npass_skim[i_skim], npass_skim[j_skim])
	
	return skim_overlaps


def get_consolidated_uniqueness(indices, result_dir, fullSkimList):

	npass_skim = np.zeros(76)
	nunique_skim = np.zeros(76)
	uniqueness_skim = np.zeros(76)

	for index in indices:
		unique_events_file = '%s/skim_unique_events_file%s.npy'%(result_dir, index); nunique_index = np.load(unique_events_file)
		nunique_skim = np.add(nunique_skim, nunique_index)
		npass_file = '%s/npass_file%s.npy'%(result_dir, index); npass_index = np.load(npass_file)
		npass_skim = np.add(npass_skim, npass_index)
	
	for i_skim, skim in enumerate(fullSkimList):
		uniqueness_skim[i_skim] = (nunique_skim[i_skim]*100)/npass_skim[i_skim]

	return uniqueness_skim


def get_consolidated_skim_multiplicity(indices, result_dir, fullSkimList):

	skim_multiplicity = np.zeros(50)#skim-multiplicity is calculated upto value 49
	n_tot_all = 0	

	for index in indices:
		multiplicity_file = '%s/skim_multiplicity_file%s.npy'%(result_dir, index); multiplicity_index = np.load(multiplicity_file)
		skim_multiplicity = np.add(skim_multiplicity, multiplicity_index)
		ntot_file = '%s/ntot_file%s.npy'%(result_dir, index); ntot_index = np.load(ntot_file)
		n_tot_all = np.add(n_tot_all, ntot_index)
	
	#Normalize and store as percentage
	for i in range(50):
		skim_multiplicity[i] = (skim_multiplicity[i]*100)/n_tot_all

	return skim_multiplicity
	
	

#################################################################################################################
#                                           MAIN
#################################################################################################################


if __name__ == '__main__':

	skim_retentions, npass_skim, n_tot_all = get_consolidated_retention(indices, result_dir, fullSkimList); #print(skim_retentions)
	skim_overlaps = get_consolidated_overlaps(indices, result_dir, fullSkimList); #print(skim_overlaps)
	uniqueness_skim = get_consolidated_uniqueness(indices, result_dir, fullSkimList); #print(uniqueness_skim)
	skim_multiplicity = get_consolidated_skim_multiplicity(indices, result_dir, fullSkimList); #print(skim_multiplicity)

	#Save consolidated results
	np.save('%s/skim_retentions.npy'%conres_dir, skim_retentions, allow_pickle=True)
	np.save('%s/npass_skim.npy'%conres_dir, npass_skim, allow_pickle=True)
	np.save('%s/ntot.npy'%conres_dir, n_tot_all, allow_pickle=True)
	np.save('%s/skim_overlaps.npy'%conres_dir, skim_overlaps, allow_pickle=True)
	np.save('%s/uniqueness_skim.npy'%conres_dir, uniqueness_skim, allow_pickle=True)
	np.save('%s/skim_multiplicity.npy'%conres_dir, skim_multiplicity, allow_pickle=True)













