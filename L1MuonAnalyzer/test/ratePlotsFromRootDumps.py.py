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

###CONSTANTS###

CALCULATE = True
MAX_CUT = 0.998
MIN_CUT = 0.002
OUTPUT_FILE = "deltaPhi_cand_simMu.root"

#version = "t35_mcWaw_2024_03_11"
#version = "t36_mcWaw_2024_03_11"
#version = "t35_mcWaw_2024_04_03"
version = "t36_mcWaw_2024_04_03"


#INPUT_FILE = "data_dump_21_02_2025.root"
#prefix = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/rootDump/omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_" + version
#input_files = [
                #prefix + "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_" + version + "_mcWaw2023_iPt2_04_04_2023.root",
#                prefix + "_OneOverPt.root",
                #prefix + "_mcWaw_2024_03_11_OneOverPt.root",
#                ]

#maybe this version is not good, there are much more muons there
dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_Phase2Spring24_MinBias__t36/results/"
fileNameLike = "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t35p_omtfPhiAtSt2__"
version = "Phase2Spring24_MinBias__t36"

dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_Phase2Spring24_MinBias__t37/results"
fileNameLike = "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t37__"
version = "Phase2Spring24_MinBias__t37"

if False :
    dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_Phase2Spring24_MinBias__t40/results/"
    fileNameLike = "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t40__"
    version = "Phase2Spring24_MinBias__t40"

if True :
    dir = "/home/kbunkow/projects/machine_learning/results/omtfRegression_displ_quant_t36_v435/"
    fileNameLike = "minBias_t40_Phase2Spring24_omtfNN_.root"
    version = "Phase2Spring24_MinBias__t40_NNreg_v435"
    
if True :
    dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/rootDump/"
    fileNameLike = "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t40_EphemeralZeroBias7_Run2025G.root"
    version = "t40_EphemeralZeroBias7_Run2025G"    

input_files = [os.path.join(dir, f) for f in os.listdir(dir) if (f.endswith('.root') and fileNameLike in f)]

print("input_files: ", input_files)

###UPLOADING ROOT FILES -> NUMPY ARRAYS
tree_path = "simOmtfPhase2Digis/OMTFHitsTree"

#data = np.array(["omtfPhi", "muonPt", "muonPhi", "muonCharge", "omtfProcessor"]) "omtfPhi", 

expressions=["muonPt", "muonPhi", "muonEta", "muonCharge", "muonDxy", "muonRho", 'omtfPt', 'omtfUPt', 'omtfEta', 'omtfQuality']
if "NNreg" in version :
    expressions = ["muonPt", "muonPhi", "muonEta", "muonCharge", "muonDxy", "muonRho", 'omtfPt', 'omtfUPt', 'omtfEta', 'omtfQuality', 'nnPt0', 'nnPt1', 'nnUpt',]


data = uproot.concatenate(input_files, expressions, library="pd")

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

###DATA PROCESSING
print("full data len ", len(data["muonPt"]),"\n")

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

fig1, axs = plt.subplots(2, 2, figsize=(20, 12))

# Histogram of muonDxy with 50 bins and range from -0.1 to 0.1
axs[0, 0].hist(data["muonDxy"], bins=50, range=(-0.1, 0.1), color='blue', alpha=0.7, edgecolor='black', log=True)
#axs[0, 0].set_title("muonDxy (Range: -0.1 to 0.1)")
axs[0, 0].set_xlabel("muonDxy")
axs[0, 0].set_ylabel("Frequency (log scale)")
axs[0, 0].set_ylim(bottom=0.1)
#axs[0, 0].grid(axis='y', alpha=0.75)

# Histogram of muonDxy with range from -100 to 100
axs[1, 0].hist(data["muonDxy"], bins=50, range=(-100, 100), color='green', alpha=0.7, edgecolor='black', log=True)
#axs[1, 0].set_title("muonDxy (Range: -100 to 100)")
axs[1, 0].set_xlabel("muonDxy")
axs[1, 0].set_ylabel("Frequency (log scale)")
axs[1, 0].set_ylim(bottom=0.1)
#axs[1, 0].grid(axis='y', alpha=0.75)

# Histogram of muonEta
axs[0, 1].hist(data["muonEta"], bins=50, range=(-2.0, 2.0), color='green', alpha=0.7, edgecolor='black', log=True)
#axs[0, 1].set_title("muonEta")
axs[0, 1].set_xlabel("muonEta")
axs[0, 1].set_ylabel("Frequency (log scale)")
axs[0, 1].xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
axs[0, 1].xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
axs[0, 1].set_ylim(bottom=0.1)
#axs[0, 1].grid(axis='y', alpha=0.75)

axs[1, 1].hist(data["muonRho"], bins=50, range=(-0.1, 0.1), color='blue', alpha=0.7, edgecolor='black', log=True)
#axs[1, 1].set_title("muonRho (Range: -0.1 to 0.1)")
axs[1, 1].set_xlabel("muonRho")
axs[1, 1].set_ylabel("Frequency (log scale)")
axs[1, 1].set_ylim(bottom=0.1)
#axs[1, 1].grid(axis='y', alpha=0.75)

# Add a title to the entire figure
fig1.suptitle(version, fontsize=16, fontweight='bold')
######################################################################

fig2, axs2 = plt.subplots(2, 2, figsize=(20, 12))

axs2[0, 0].hist(data.query('muonPt > 0')["muonPt"],                  label='all muons', bins=50, range=(0, 50), color='blue', alpha=0.7, edgecolor='black', histtype='step', log=True)
axs2[0, 0].hist(data.query('muonRho < 10 and muonPt > 0')["muonPt"], label='prompt muons', bins=50, range=(0, 50), color='blue', alpha=0.7, edgecolor='red', histtype='step', log=True)
axs2[0, 0].hist(data.query('muonRho > 10 and muonPt > 0')["muonPt"], label='non prompt', bins=50, range=(0, 50), color='blue', alpha=0.7, edgecolor='green', histtype='step', log=True)

#axs2[0, 0].set_title("muonDxy (Range: -0.1 to 0.1)")
axs2[0, 0].set_xlabel("muonPt")
axs2[0, 0].set_ylabel("Frequency")
axs2[0, 0].set_ylim(bottom=0.1, top=200000)
axs2[0, 0].legend()

###########################################################################3
#lhcFillingRatio = 2760./3564.;
lhcFillingRatio = 2345./3564.; #run 367883     2023C
lhcFreq = 40144896; #11264 * 3564

if "Phase2Spring24" in version :
    eventCntRate = 1999360 #TODO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
elif "Phase2Spring23" in version :    
    eventCntRate = 416000 + 700154 # Phase2Spring23_
elif 'EphemeralZeroBias7_Run2025G' in version :
    eventCntRate = 7685316 
scale = 1./eventCntRate * lhcFreq * lhcFillingRatio;
norm = 1. / scale

ptCuts = np.linspace(0, 100, 201)


def rate_plots(axs, data_omtf, omtfPt, qualityCut, ptCuts, norm):
# Select OMTF candidates using the variable column name for pt
    
    # Use pandas' query variable injection (@) to inject ptCut safely into the query string.
    # Inject the column name via f-string and enclose it in backticks so pandas.query treats it as a column identifier.
    omtf_pt_rate = np.array([data_omtf.query(f"`{omtfPt}` >= @ptCut").shape[0] / norm for ptCut in ptCuts])
    axs.hist(ptCuts, bins=ptCuts, weights=omtf_pt_rate, histtype='step', label='all candidates', color='black', log=True)
    
    omtf_pt_rate_prompt = np.array([data_omtf.query(f"`{omtfPt}` >= @ptCut and muonRho < 10 and muonPt > 0").shape[0] / norm for ptCut in ptCuts])
    axs.hist(ptCuts, bins=ptCuts, weights=omtf_pt_rate_prompt, histtype='step', label='matched to prompt', color='red', log=True)
    
    omtf_pt_rate_nonprompt = np.array([data_omtf.query(f"`{omtfPt}` >= @ptCut and muonRho >= 10 and muonPt > 0").shape[0] / norm for ptCut in ptCuts])
    axs.hist(ptCuts, bins=ptCuts, weights=omtf_pt_rate_nonprompt, histtype='step', label='matched to nonprompt', color='green', log=True)
    
    omtf_pt_rate_notmatched = np.array([data_omtf.query(f"`{omtfPt}` >= @ptCut and muonPt == 0").shape[0] / norm for ptCut in ptCuts])
    axs.hist(ptCuts, bins=ptCuts, weights=omtf_pt_rate_notmatched, histtype='step', label='not matched', color='blue', log=True)
    
    # Find the rate value at ptCut == 19 (or nearest available ptCut)
    try:
        # ptCuts might be a numpy array or a sequence; ensure numpy array
        pt_array = np.asarray(ptCuts)
        # find exact match first
        matches = np.where(np.isclose(pt_array, 19.0))[0]
        if matches.size > 0:
            idx = matches[0]
            pt_val = pt_array[idx]
        else:
            # if exact 19 not present, pick the nearest pt cutoff
            idx = int(np.argmin(np.abs(pt_array - 19.0)))
            pt_val = pt_array[idx]
        # Print the rates at this pt cut
        print(f"{omtfPt} Rates at ptCut = {pt_val} GeV (quality >= {qualityCut}, |omtfEta| < 1.24):")
        print(f"  all candidates:       {omtf_pt_rate[idx]:.6g} Hz")
        print(f"  matched to prompt:    {omtf_pt_rate_prompt[idx]:.6g} Hz")
        print(f"  matched nonprompt:    {omtf_pt_rate_nonprompt[idx]:.6g} Hz")
        print(f"  not matched:          {omtf_pt_rate_notmatched[idx]:.6g} Hz")
    except Exception as e:
        print('Warning: could not extract/print rates at ptCut 19:', e)
    
    axs.set_xlabel(omtfPt + " cut [GeV]")
    axs.set_ylabel("Rate [Hz]")
    axs.set_title("OMTF quality >= %i, |omtfEta| < 1.24" % qualityCut)
    axs.set_ylim(bottom=100, top=1e6)
    axs.legend()

    

qualityCut = 12

omtfPt = "omtfPt"

nnCut = ""
if "NNreg" in version :
    omtfPt = "nnPt0"
    #nnCut = " and nnPt1 > 5"

data_omtf = data.query(f'omtfQuality >= @qualityCut and abs(omtfEta) < 1.24 and `{omtfPt}` > 1' + nnCut)

if "NNreg" in version :
    omtfPt = "combPt"

#omtfPt = "omtfPt"    


rate_plots(axs2[1, 0], data_omtf, omtfPt, qualityCut, ptCuts, norm)
rate_plots(axs2[1, 1], data_omtf, "omtfUPt", qualityCut, ptCuts, norm)

fig2.suptitle(version, fontsize=16, fontweight='bold')
##################################################################################3
#axs[0, 0].grid(axis='y', alpha=0.75)
# Adjust layout and save each figure to its own file
output_dir = "./plots/"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

fig1.tight_layout()

postfix = version + '_' + omtfPt + '_' + str(qualityCut)

fig1.savefig(output_dir + 'muonDxy_' + postfix + '.png')

fig2.tight_layout()
fig2.savefig(output_dir + 'muonPt_' + postfix + '.png')

#plt.show()