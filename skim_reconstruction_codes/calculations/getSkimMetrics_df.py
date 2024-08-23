import uproot
import pandas as pd
from ROOT import TFile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def plot_overlap(overlap_matrix, row_l, row_h, col_l, col_h, dim, name):

	fig = plt.figure(figsize=(20, 16))
	ax = fig.add_subplot(111)
	cax = ax.matshow(overlap_matrix[row_l:row_h, col_l:col_h], cmap=plt.get_cmap('Greys'), norm=LogNorm(vmin=0.01, vmax=100))
	for (i, j), z in np.ndenumerate(overlap_matrix[row_l:row_h, col_l:col_h]):
		ax.text(j, i, '{:0.2f}'.format(z), ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white', edgecolor='white'))
	plt.title('Overlap matrix of various skims (%)')
	fig.colorbar(cax)
	tick_marks = np.arange(dim)
	plt.xticks(tick_marks, skimList[col_l:col_h], rotation=45, ha='left')
	plt.yticks(tick_marks, skimList[row_l:row_h])
	plt.tight_layout()
	plt.savefig('plots/%s_row%s_%s_col%s_%s.png'%(name, row_l, row_h, col_l, col_h))
	plt.close(fig)


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




skimList = ['Random', 'SystematicsTracking', 'Resonance', 'SystematicsRadMuMu', 'SystematicsEELL', 'SystematicsRadEE', 'SystematicsLambda', 'SystematicsPhiGamma', 'SystematicsFourLeptonFromHLTFlag', 'SystematicsRadMuMuFromHLTFlag', 'SystematicsJpsi', 'SystematicsKshort', 'SystematicsBhabha', 'SystematicsDstar', 'PRsemileptonicUntagged', 'LeptonicUntagged', 'dilepton', 'SLUntagged', 'B0toDstarl_Kpi_Kpipi0_Kpipipi', 'BtoXgamma', 'BtoXll', 'BtoXll_LFV', 'inclusiveBplusToKplusNuNu', 'TDCPV_ccs', 'TDCPV_qqs', 'BtoD0h_Kspi0', 'BtoD0h_Kspipipi0', 'B0toDpi_Kpipi', 'B0toDpi_Kspi', 'B0toDstarPi_D0pi_Kpi', 'B0toDstarPi_D0pi_Kpipipi_Kpipi0', 'B0toDrho_Kpipi', 'B0toDrho_Kspi', 'B0toDstarRho_D0pi_Kpi', 'B0toDstarRho_D0pi_Kpipipi_Kpipi0', 'BtoD0h_hh', 'BtoD0h_Kpi', 'BtoD0h_Kpipipi_Kpipi0', 'BtoD0h_Kshh', 'BtoD0rho_Kpi', 'BtoD0rho_Kpipipi_Kpipi0', 'B0toDD_Kpipi_Kspi', 'B0toDstarD', 'InclusiveLambda', 'BottomoniumEtabExclusive', 'BottomoniumUpsilon', 'CharmoniumPsi', 'XToD0_D0ToHpJm', 'XToD0_D0ToNeutrals', 'DstToD0Pi_D0ToRare', 'XToDp_DpToKsHp', 'XToDp_DpToHpHmJp', 'LambdacTopHpJm', 'DstToD0Pi_D0ToHpJm', 'DstToD0Pi_D0ToHpJmPi0', 'DstToD0Pi_D0ToHpHmPi0', 'DstToD0Pi_D0ToKsOmega', 'DstToD0Pi_D0ToHpJmEta', 'DstToD0Pi_D0ToNeutrals', 'DstToD0Pi_D0ToHpJmKs', 'EarlyData_DstToD0Pi_D0ToHpJmPi0', 'EarlyData_DstToD0Pi_D0ToHpHmPi0', 'DstToDpPi0_DpToHpPi0', 'DstToD0Pi_D0ToHpHmHpJm', 'SinglePhotonDark', 'GammaGammaControlKLMDark', 'ALP3Gamma', 'EGammaControlDark', 'InelasticDarkMatter', 'RadBhabhaV0Control', 'TauLFV', 'DimuonPlusMissingEnergy', 'ElectronMuonPlusMissingEnergy', 'DielectronPlusMissingEnergy', 'LFVZpVisible', 'TauGeneric', 'TauThrust', 'TwoTrackLeptonsForLuminosity', 'LowMassTwoTrack', 'SingleTagPseudoScalar', 'BtoPi0Pi0', 'BtoHadTracks', 'BtoHad1Pi0', 'BtoHad3Tracks1Pi0', 'BtoRhopRhom', 'SystematicsLambda']
skimList.remove('DstToD0Pi_D0ToRare')
skimList.remove('SystematicsLambda')

rootdir = 'skimFlag_rootFiles'
merged_file = 'merged_skimFkags.root'
merged_file_pkl = 'merged_skimFkags.pkl'
treeKey = 'variables'

all_vars = ['__experiment__', '__run__', '__event__']
for skim in skimList:
	all_vars.append('passes_%s'%skim)
	#Define N_pass variables for each skim
	exec('Npass_%s = 0'%skim)
	#Define N_A∩B and N_A∪B variables for each A, B
	for skim1 in skimList:
		exec('N_%s_n_%s = 0'%(skim, skim1))#intersection
		exec('N_%s_u_%s = 0'%(skim, skim1))#union


df_all = uproot.open('%s/%s'%(rootdir, merged_file))[treeKey].arrays([split_prop(i)[0] for i in all_vars], library='pd')

#df_all = pd.read_pickle('skimFlag_rootFiles/merged_skimFkags.pkl')

#print(df_all.shape)
#print(len(skimList))
#print(df_all['passes_Random'])
ntot = df_all.shape[0]
e_ntot = np.sqrt(ntot)
print('total number of events = ',ntot)

overlap_matrix = np.zeros((84, 84))  # N_A∩B / N_A∪B
overlap_matrix2 = np.zeros((84, 84)) # N_A∩B / min(N_A, N_B)
overlap_matrix3 = np.zeros((84, 84)) # N_A∩B / N_B
e_overlap_matrix2 = np.zeros((84, 84)) #error on overlap matrix-2

for i_skim, skim in enumerate(skimList):
	column = 'passes_%s'%skim
	npass = df_all[column].sum()
	e_npass = np.sqrt(npass)
	retrate = npass *100 / ntot
	e_retrate = (np.sqrt((ntot*ntot*e_npass*e_npass) + (npass*npass*e_ntot*e_ntot)) * 100) / (ntot * ntot)
	#print(skim, '  &  ', int(npass), '  &  ', '{:.2e}'.format(retrate), '  &  ', '{:.1e}'.format(e_retrate),'\\\\') 

	#loop for calculating overlaps
	for j_skim, skim2 in enumerate(skimList):
		column2 = 'passes_%s'%skim2
		union = np.logical_or(df_all[column], df_all[column2])
		intersection = np.logical_and(df_all[column], df_all[column2])
		overlap_matrix[i_skim, j_skim] = intersection.sum()*100/union.sum() #defined as intersection/union
		#print(skim, skim2, overlap_matrix[i_skim, j_skim])
		npass2 = df_all[column2].sum()
		nintersection = intersection.sum()
		overlap1 = nintersection*100 / npass #defined as intersection / 1st set
		overlap2 = nintersection*100 / npass2 #defined as intersection / 2nd set
		overlap_matrix2[i_skim, j_skim] = max(overlap1, overlap2)
		overlap_matrix3[i_skim, j_skim] = overlap2
		e_overlap_matrix2[i_skim, j_skim] = get_err_frac(nintersection, min(npass,npass2))


#plot_overlaps
plotname = 'overlap'
plotname2 = 'overlap2'
plotname3 = 'overlap3'
plotname4 = 'e_overlap2'
dim = 21
for row_l in [0, 21, 42, 63]:
	row_h = row_l + dim 	
	for col_l in [0, 21, 42, 63]:
		col_h = col_l +dim
		#plot_overlap(overlap_matrix, row_l, row_h, col_l, col_h, dim, plotname)
		#plot_overlap(overlap_matrix2, row_l, row_h, col_l, col_h, dim, plotname2)
		#plot_overlap(overlap_matrix3, row_l, row_h, col_l, col_h, dim, plotname3)	
		plot_overlap(e_overlap_matrix2, row_l, row_h, col_l, col_h, dim, plotname4)			

#Save overlap matrix into numpy file
#np.save('overlap2.npy', overlap_matrix2, allow_pickle=True)
















