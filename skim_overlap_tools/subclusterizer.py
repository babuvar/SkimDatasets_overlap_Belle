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
	# initialize cluster_index to be same as skimList-index
	for i in range(len(skimList)):
		cluster_index[i] = i

	#Overlap-finding loop
	changes = 99 # initialize with random non-zero number
	while changes != 0:
		changes = clusterFind(overlap_mat, cluster_index, overlap_Threshold, skimList)

	unique_cluster_indicess = np.unique(cluster_index)
	num_clusters = unique_cluster_indicess.size

	#get list of clusters, each cluster being a list of skims
	cluster_list = []
	for unq_idx in unique_cluster_indicess:
		cluster = []
		for i, cl_idx in enumerate(cluster_index) :
			if unq_idx == cl_idx:
				cluster.append(skimList[i])
		cluster_list.append(cluster)


	return num_clusters, cluster_list


def clusterFind(overlap_mat, cluster_index, overlap_Threshold, skimList):

	changes = 0

	for i in range(len(skimList)):
		for j in range(i+1, len(skimList)):
			#check if overlap-threshold is surpassed for the i-j skim combination
			if (overlap_mat[i,j] > overlap_Threshold) and (cluster_index[i] != cluster_index[j]):
				changes = changes + 1
				lower_cluster_index = min(cluster_index[i], cluster_index[j])
				cluster_index[i] = lower_cluster_index
				cluster_index[j] = lower_cluster_index

	return changes		
	







	
	

















