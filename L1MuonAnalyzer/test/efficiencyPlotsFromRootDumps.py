# author Wiktor Radoslaw Matyszkiewicz wmatyszk@cern.ch

import uproot
import ROOT
import numpy as np
import matplotlib.ticker
import matplotlib.pyplot as plt
import pandas as pd
import math

import warnings
import os
warnings.filterwarnings("ignore", message="The value of the smallest subnormal for <class 'numpy.float64'> type is zero.")


def read_root_files(dir, fileNameLike):
    input_files = [os.path.join(dir, f) for f in os.listdir(dir) if (f.endswith('.root') and fileNameLike in f)]
    
    print("input_files: ", input_files)
    
    ###UPLOADING ROOT FILES -> NUMPY ARRAYS
    tree_path = "simOmtfPhase2Digis/OMTFHitsTree"
    
    #data = np.array(["omtfPhi", "muonPt", "muonPhi", "muonCharge", "omtfProcessor"]) "omtfPhi", 
    
    expressions=["muonPt", "muonPhi", "muonEta", "muonCharge", "muonDxy", "muonRho", 'omtfPt', 'omtfUPt', 'omtfEta', 'omtfQuality']
    if "NNreg" in version :
        expressions = ["muonPt", "muonPhi", "muonEta", "muonCharge", "muonDxy", "muonRho", 'omtfPt', 'omtfUPt', 'omtfEta', 'omtfQuality', 'nnPt0', 'nnPt1', 'nnUpt',]
    
    
    data = uproot.concatenate(input_files, expressions, library="pd")
    print("full data len ", len(data["muonPt"]),"\n")   
    return data

def add_combPt(data):
    try:
        if 'omtfPt' in data.columns:
            if 'nnPt0' in data.columns:
                nn_present = data['nnPt0'].notna() #and data['nnPt0'] > 2.5
                data['combPt'] = np.where(~nn_present,
                                          data['omtfPt'],
                                          np.where(data['omtfPt'] < 0.75 * data['nnPt0'], data['omtfPt'], data['nnPt0']))
            else:
                data['combPt'] = data['omtfPt']
        else:
            # fallback: create combPt as zeros if omtfPt doesn't exist
            data['combPt'] = 0.0
    except Exception as e:
        print('Warning: could not create combPt column on data:', e)



#Increase plots font size
params = {'font.size': 12,
        'legend.fontsize': 'large',
          'figure.figsize': (10, 7),
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'axes.grid': True,
         'xtick.labelsize':'large',
         'ytick.labelsize':'large',
         'lines.linewidth': 3,
         'lines.markersize': 10,}
plt.rcParams.update(params)

#ptBins = np.linspace(0, 800, 2*800+1)
# create variable-width bins: 0-100 GeV in 0.5 GeV steps, then 100-800 GeV in 100 GeV steps
ptBins_fine = np.arange(0.0, 100.0 + 0.5, 0.5)  # 0, 0.5, ..., 100.0
ptBins_coarse = np.arange(100.0, 1000.0 + 100.0, 100.0)  # 100, 200, ..., 800
ptBins = np.concatenate((ptBins_fine, ptBins_coarse[1:]))  # drop duplicate 100

print('ptBins:', ptBins)

def efficiency_vs_pt_plots(axs, data, version, omtfPt, qualityCut, ptCut, color, ptBins):
    data_events_with_mu = data.query('abs(muonEta) > 0.84 and abs(muonEta) < 1.24 and muonPt > 0')
    
    total_counts, _ = np.histogram(data_events_with_mu["muonPt"], bins=ptBins)
    passed_counts, _ = np.histogram(data_events_with_mu.query(f'{omtfPt} >= {ptCut} and omtfQuality >= {qualityCut}')["muonPt"], bins=ptBins)

    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        efficiency = np.true_divide(passed_counts, total_counts)
        efficiency[total_counts == 0] = 0  # Set efficiency to 0 where total counts are 0

    # Clip efficiencies to a small positive floor so the lines can be shown on log scales later
    eps_floor = 1e-7
    efficiency = np.clip(efficiency, eps_floor, 1.0)

    #bin_centers = (ptBins[:-1] + ptBins[1:]) / 2
    axs.step(ptBins[:-1], efficiency, label=omtfPt, linestyle='-', where='post', color=color, linewidth=1.5) #marker='o', 
    axs.set_xlabel('muonPt')
    axs.set_ylabel('Efficiency')    
    # For the linear plot keep 0 as lower bound so the top plot looks natural
    #axs.set_xlim(0, ptBins[-1])
    axs.set_ylim(0.0, 1.0)
    axs.legend()

def efficiency_vs_eta_plots(axs, data, version, omtfPt, qualityCut, muPtCut, omtfPtCut, color, etaBins):
    # filter events with muonPt greater than the provided cut
    data_events_with_mu = data.query(f'muonPt > {muPtCut}')
    
    # histogram total and passed counts over etaBins
    total_counts, _ = np.histogram(data_events_with_mu["muonEta"], bins=etaBins)
    passed_counts, _ = np.histogram(data_events_with_mu.query(f'{omtfPt} >= {omtfPtCut} and omtfQuality >= {qualityCut}')["muonEta"], bins=etaBins)

    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        efficiency = np.true_divide(passed_counts, total_counts)
        efficiency[total_counts == 0] = 0  # Set efficiency to 0 where total counts are 0

    # Clip efficiencies to a small positive floor so the lines can be shown on log scales later
    eps_floor = 1e-7
    efficiency = np.clip(efficiency, eps_floor, 1.0)

    # plot efficiency on the left y-axis
    axs.step(etaBins[:-1], efficiency, label=omtfPt, linestyle='-', where='post', color=color, linewidth=1.5)
    axs.set_xlabel('muonEta')
    axs.set_ylabel('Efficiency')
    axs.set_ylim(0, 1.05)

    # draw total counts as a light-grey filled histogram on the right y-axis
    ax_counts = axs.twinx()
    widths = np.diff(etaBins)
    # bar aligned to the left edge of each bin
    ax_counts.bar(etaBins[:-1], total_counts, width=widths, align='edge', color='lightgrey', alpha=0.5, label='Total counts', zorder=0)
    ax_counts.set_ylabel('Total counts', color='gray')
    ax_counts.tick_params(axis='y', labelcolor='gray')
    # set a sensible ylim for counts (allow space above highest bar)
    maxc = total_counts.max() if len(total_counts) > 0 else 0
    if maxc > 0:
        ax_counts.set_ylim(0, maxc * 2.0)
    else:
        ax_counts.set_ylim(0, 1)

    # combine legends from both axes
    lines, labels = axs.get_legend_handles_labels()
    lines2, labels2 = ax_counts.get_legend_handles_labels()
    # prefer placing the legend on the left axis (efficiency lines) unless crowded
    axs.legend(lines + lines2, labels + labels2, loc='best')
    
    return

fig1, axs1 = plt.subplots(2, 2, figsize=(20, 12))

data_file_dir  = '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/rootDump/'        
fileNameLike = "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t40_mcWaw_2024_01_03_OneOverPt_iPt2.root"  
version = "DT_2_2_2_t40"   

#data = read_root_files(data_file_dir, fileNameLike)

qualityCut = 12

ptCut = 19
axs1[0, 0].set_title(f'Efficiency vs muonPt (omtfQuality >= {qualityCut}, ptCut {ptCut} GeV)')
#efficiency_vs_pt_plots(axs1[0, 0], data, version, 'omtfPt', qualityCut, ptCut, "blue", ptBins)

data_file_dir = "/home/kbunkow/projects/machine_learning/results/omtfRegression_displ_quant_t36_v435/"
fileNameLike = "t40_NNReg_mcWaw_2024_01_03_OneOverPt_iPt2.root"
version = "t40_NNreg_v435"
data = read_root_files(data_file_dir, fileNameLike)
add_combPt(data)
efficiency_vs_pt_plots(axs1[0, 0], data, version, 'omtfPt', qualityCut, ptCut, "blue", ptBins)
efficiency_vs_pt_plots(axs1[0, 0], data, version, 'nnPt0', qualityCut, ptCut, "green", ptBins)
efficiency_vs_pt_plots(axs1[0, 0], data, version, 'combPt', qualityCut, ptCut, "red", ptBins)

# Copy the plotted lines from axs1[0,0] to axs1[1,0] and set the y-axis to log scale.
# The efficiencies are clipped to a small positive floor inside efficiency_vs_pt_plots, so zeros are avoided.
def draw_copy(source_ax, target_ax, log_scale_y=True, x_min=None, x_max=None):
    for line in source_ax.get_lines():
        target_ax.step(line.get_xdata(), line.get_ydata(), label=line.get_label(),
                        linestyle=line.get_linestyle(), where='post', color=line.get_color(), linewidth=1.5)
    target_ax.set_xlabel(source_ax.get_xlabel())
    target_ax.set_ylabel(source_ax.get_ylabel())
    target_ax.set_title(source_ax.get_title())
    target_ax.legend()
    if log_scale_y:
        target_ax.set_yscale('log')
        target_ax.set_ylim(1e-7, 1.05)
    if x_min is not None and x_max is not None:
        target_ax.set_xlim(x_min, x_max)

draw_copy(axs1[0, 0], axs1[1, 0], log_scale_y=True, x_min=0, x_max=40)
draw_copy(axs1[0, 0], axs1[0, 1], log_scale_y=False, x_min=0, x_max=100)

etaBins = np.linspace(-2., 2., 51) 
print('etaBins:', etaBins)
omtfPtCut = 19
muPtCut = 25
efficiency_vs_eta_plots(axs1[1, 1], data, version, 'omtfPt', qualityCut, muPtCut, omtfPtCut, "blue", etaBins)
efficiency_vs_eta_plots(axs1[1, 1], data, version, 'nnPt0', qualityCut, muPtCut, ptCut, "green", etaBins)
efficiency_vs_eta_plots(axs1[1, 1], data, version, 'combPt', qualityCut, muPtCut, ptCut, "red", etaBins)

##################################################################################3
#axs[0, 0].grid(axis='y', alpha=0.75)
# Adjust layout and save each figure to its own file
output_dir = "./plots/"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

fig1.tight_layout()

postfix = version + '_' + str(qualityCut)

fig1.savefig(output_dir + postfix + '.png')

#fig2.tight_layout()
#fig2.savefig(output_dir + 'muonPt_' + postfix + '.png')

#plt.show()