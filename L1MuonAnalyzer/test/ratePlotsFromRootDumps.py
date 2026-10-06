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

from pathlib import Path
import json

warnings.filterwarnings("ignore", message="The value of the smallest subnormal for <class 'numpy.float64'> type is zero.")

###CONSTANTS###

CALCULATE = True
MAX_CUT = 0.998
MIN_CUT = 0.002

versions_to_comapre = []

#maybe this version is not good, there are much more muons there
dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_Phase2Spring24_MinBias__t36/results/"
fileNameLike = "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t35p_omtfPhiAtSt2__"
version = "Phase2Spring24_MinBias__t36"

dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_Phase2Spring24_MinBias__t37/results"
fileNameLike = "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t37__"
version = "Phase2Spring24_MinBias__t37"

if False :
    dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/usercode/L1MuonAnalyzer/test/crab/crab_OMTF_phase1_Phase2Spring24_MinBias__t40/results/"
    fileNameLike = "omtfAnalysis2_t40__Phase1_2024__"
    version = "OMTF_phase1_t40__Phase2Spring24_MinBias"   
    versions_to_comapre = [ { "version":"OMTF_phase2_t40__Phase2Spring24_MinBias_rate_plots", "file_name":"rate_at_omtfPt.json", "color":"magenta"},]
    label_prefix = "Phase1" 
        
if True :
    dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_Phase2Spring24_MinBias__t40/results/"
    fileNameLike = "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t40__"
    version = "OMTF_phase2_t40__Phase2Spring24_MinBias"
    versions_to_comapre = [ { "version":"OMTF_phase1_t40__Phase2Spring24_MinBias_rate_plots", "file_name":"rate_at_omtfPt.json", "color":"magenta"},]
    label_prefix = "Phase2"
    
if False :
    dir = "/home/kbunkow/projects/machine_learning/results/omtfRegression_displ_quant_t36_v435/"
    fileNameLike = "minBias_t40_Phase2Spring24_omtfNN_.root"
    version = "OMTF_phase2_t40_NNreg_v435__Phase2Spring24_MinBias"
    versions_to_comapre = [ { "version":"OMTF_phase2_t40__Phase2Spring24_MinBias_rate_plots", "file_name":"rate_at_omtfPt.json", "color":"magenta"},]
    label_prefix = "Phase2 NNreg v435" 
    
if False :
    dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/rootDump/"
    fileNameLike = "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t40_EphemeralZeroBias7_Run2025G.root"
    version = "t40_EphemeralZeroBias7_Run2025G"  
        
if False :
    dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/usercode/L1MuonAnalyzer/test/OMTF_phase1/rootDump/"
    fileNameLike = "omtfAnalysis2_t40__Phase1_2024_EphemeralZeroBias7_Run2025G.root"
    version = "OMTF_phase1_t40__EphemeralZeroBias7_Run2025G"    

output_dir = Path(version + "_rate_plots/")
output_dir.mkdir(parents=True, exist_ok=True)    

ptCut = 19
if "OMTF_phase1" in version :
    ptCut = 22

input_files = [os.path.join(dir, f) for f in os.listdir(dir) if (f.endswith('.root') and fileNameLike in f)]

print("input_files: ", input_files)

###UPLOADING ROOT FILES -> NUMPY ARRAYS
tree_path = "simOmtfPhase2Digis/OMTFHitsTree"

#data = np.array(["omtfPhi", "muonPt", "muonPhi", "muonCharge", "omtfProcessor"]) "omtfPhi", 

expressions=["eventNum", "muonPt", "muonPhi", "muonEta", "muonCharge", "muonDxy", "muonRho", 'omtfPt', 'omtfUPt', 'omtfEta', 'omtfQuality']
if "NNreg" in version :
    expressions = ["eventNum", "muonPt", "muonPhi", "muonEta", "muonCharge", "muonDxy", "muonRho", 'omtfPt', 'omtfUPt', 'omtfEta', 'omtfQuality', 'nnPt0', 'nnPt1', 'nnUpt',]


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

params = {  'font.size': 8,
            'legend.fontsize': 'large',
            'figure.figsize': (10, 7),
            'axes.labelsize': 'large',
            'axes.titlesize':'large',
            'axes.grid': True,
            'xtick.labelsize':'large',
            'ytick.labelsize':'large',
            'lines.linewidth': 3,
            'lines.markersize': 10,
            'xtick.direction': 'in',
            'ytick.direction': 'in',
            'xtick.major.size': 8,
            'xtick.minor.size': 4,
            'ytick.major.size': 8,
            'ytick.minor.size': 4,
            'xtick.minor.visible': True,
            'ytick.minor.visible': True,
            'xtick.top': True,
            'ytick.right': True
         }
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

fig2, axs2 = plt.subplots(2, 2, figsize=(12, 7))

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
lhcFillingRatio = 2448./3564 #  2025 ;;; 2345./3564.; #run 367883     2023C
lhcFreq = 40144896; #11264 * 3564

if "Phase2Spring24" in version :
    eventCntRate = 1999360 #TODO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
elif "Phase2Spring23" in version :    
    eventCntRate = 416000 + 700154 # Phase2Spring23_
elif 'EphemeralZeroBias7_Run2025G' in version :
    eventCntRate = 7685316 
scale = 1./eventCntRate * lhcFreq * lhcFillingRatio;
norm = 1. / scale

ptCutBins = np.linspace(0, 100, 201)


def print_matching_rows(df, omtfPt_col, ptCut_val, qualityCut_val, max_rows=200):
    """Print rows from df where `omtfPt_col` >= ptCut_val and omtfQuality >= qualityCut_val.
    Caps output to max_rows rows to avoid flooding the terminal.
    """
    try:
        # build a safe query string; use backticks for column identifier
        query_str = f"`{omtfPt_col}` >= @ptCut_val and omtfQuality >= @qualityCut_val"
        matched = df.query(query_str)
        cnt = matched.shape[0]
        print(f"\nFound {cnt} rows with `{omtfPt_col}` >= {ptCut_val} and omtfQuality >= {qualityCut_val}\n")
        if cnt == 0:
            return
        # if too many rows, show only the first max_rows
        if cnt <= max_rows:
            print(matched.to_string(index=False))
        else:
            print(matched.head(max_rows).to_string(index=False))
            print(f"... (showing first {max_rows} of {cnt} rows)")
    except Exception as e:
        print('Error while printing matching rows:', e)


def rate_plots(axs, data_omtf, omtfPt, qualityCut, ptCutBins, norm, axs_stack):
# Select OMTF candidates using the variable column name for pt
    
    # Use pandas' query variable injection (@) to inject ptCut safely into the query string.
    # Inject the column name via f-string and enclose it in backticks so pandas.query treats it as a column identifier.
    omtf_pt_rate = np.array([data_omtf.query(f"`{omtfPt}` >= @ptCut").shape[0] / norm for ptCut in ptCutBins])
    axs.hist(ptCutBins, bins=ptCutBins, weights=omtf_pt_rate, histtype='step', label='all candidates', color='black', log=True)
    
    omtf_pt_rate_prompt = np.array([data_omtf.query(f"`{omtfPt}` >= @ptCut and muonRho < 10 and muonPt > 0").shape[0] / norm for ptCut in ptCutBins])
    axs.hist(ptCutBins, bins=ptCutBins, weights=omtf_pt_rate_prompt, histtype='step', label='matched to prompt', color='red', log=True)
    
    omtf_pt_rate_nonprompt = np.array([data_omtf.query(f"`{omtfPt}` >= @ptCut and muonRho >= 10 and muonPt > 0").shape[0] / norm for ptCut in ptCutBins])
    axs.hist(ptCutBins, bins=ptCutBins, weights=omtf_pt_rate_nonprompt, histtype='step', label='matched to nonprompt', color='green', log=True)
    
    omtf_pt_rate_notmatched = np.array([data_omtf.query(f"`{omtfPt}` >= @ptCut and muonPt == 0").shape[0] / norm for ptCut in ptCutBins])
    axs.hist(ptCutBins, bins=ptCutBins, weights=omtf_pt_rate_notmatched, histtype='step', label='not matched', color='blue', log=True)
    
    axs.set_xlabel(omtfPt + " cut [GeV]")
    axs.set_ylabel("Rate [Hz]")
    axs.set_title(version + "\n" + nnCut + " qual >= %i, |omtfEta| < 1.24" % qualityCut )
    axs.set_ylim(bottom=100, top=1e6)
    axs.set_xlim(0, 30)
    
    # Add secondary/minor ticks on the x-axis for finer resolution (0.5 GeV)

    # place minor ticks every 0.5 GeV
    axs.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(0.5))
    # ensure minor ticks are drawn and styled
    axs.tick_params(axis='x', which='minor', length=6)
    axs.tick_params(axis='x', which='major', length=8)
    # optional: show a subtle minor-grid for readability
    axs.grid(which='minor', axis='x', linestyle=':', alpha=0.6)
    axs.grid(which='minor', axis='y', linestyle=':', alpha=0.6)
    axs.legend()

    # Find the rate value at ptCut == 19 (or nearest available ptCut)

    # ptCutBins might be a numpy array or a sequence; ensure numpy array
    pt_array = np.asarray(ptCutBins)
    # find exact match first
    matches = np.where(np.isclose(pt_array, ptCut))[0]
    if matches.size > 0:
        idx = matches[0]
        pt_val = pt_array[idx]
    else:
        # if exact 19 not present, pick the nearest pt cutoff
        idx = int(np.argmin(np.abs(pt_array - ptCut)))
        pt_val = pt_array[idx]
    # Print the rates at this pt cut
    print(f"{omtfPt} Rates at ptCut = {pt_val} GeV (quality >= {qualityCut}):")
    print(f"  all candidates:       {omtf_pt_rate[idx]:.6g} Hz")
    print(f"  matched to prompt:    {omtf_pt_rate_prompt[idx]:.6g} Hz")
    print(f"  matched nonprompt:    {omtf_pt_rate_nonprompt[idx]:.6g} Hz")
    print(f"  not matched:          {omtf_pt_rate_notmatched[idx]:.6g} Hz")

    if axs_stack is not None:
        # Stack plot for cumulative rates
        bottom = np.zeros(1)
        bins = [label_prefix + " " + omtfPt + ' ptCut = ' + str(pt_val)]
        rates = {
       # { "vals" : [omtf_pt_rate[idx]], "bottom":bottom, "label":'all candidates', "color":'black'},
        "prompt":{ "vals" : [omtf_pt_rate_prompt[idx]], "bottom":bottom.tolist(), "label":'matched to prompt muons', "color":'red'},
        "non_prompt":{ "vals" : [omtf_pt_rate_nonprompt[idx]], "bottom":[omtf_pt_rate_prompt[idx]], "label":'matched to nonprompt', "color":'green'},
        "not_matched":{ "vals" : [omtf_pt_rate_notmatched[idx]], "bottom":( np.array([omtf_pt_rate_prompt[idx]]) +  np.array([omtf_pt_rate_nonprompt[idx]])).tolist(), "label":'not matched', "color":'blue'},
         }            
        
        hist_data = {    
            "omtfPt": omtfPt,
            "ptCut": pt_val,
            "qualityCut": qualityCut,
            "rates": rates,
            "bins": bins
        }
        
        with open(output_dir / ("rate_at_" + omtfPt + ".json"), "w") as f:
            json.dump(hist_data, f)                    

        for ver in versions_to_comapre:
            print("versions_to_comapre ver:", ver)
            if "rate_at_" in ver["file_name"]:
                filename = ver["version"] + "/" + ver["file_name"]
                with open(filename, "r") as f:
                    hist_data = json.load(f)
                    rates["prompt"]["vals"].append(hist_data["rates"]["prompt"]["vals"][0])
                    rates["non_prompt"]["vals"].append(hist_data["rates"]["non_prompt"]["vals"][0])
                    rates["not_matched"]["vals"].append(hist_data["rates"]["not_matched"]["vals"][0])
                    
                    rates["non_prompt"]["bottom"].append( hist_data["rates"]["non_prompt"]["bottom"][0] )
                    rates["not_matched"]["bottom"].append( hist_data["rates"]["not_matched"]["bottom"][0] )
                    
            bins.append(hist_data["bins"][0])    
               

        for key, rate_info in rates.items() :
            print ("stacking: ", rate_info)
            axs_stack.bar(bins, rate_info["vals"], bottom=rate_info["bottom"], label=rate_info["label"], color=rate_info["color"])
        
        axs_stack.legend()
        axs_stack.set_ylabel("Rate [Hz]")  
        axs_stack.set_ylim(0, 10000)  
        
qualityCut = 12

omtfPt = "omtfPt"

nnCut = ""
if "NNreg" in version :
    omtfPt = "nnPt0"
    #nnCut = " and nnPt1 > 5"

data_omtf = data.query(f'omtfQuality >= @qualityCut and abs(omtfEta) < 1.24 and `{omtfPt}` > 1' + nnCut)
#data_omtf = data.query(f'omtfQuality >= @qualityCut and `{omtfPt}` > 1' + nnCut)

# Print matching rows from the already-filtered `data_omtf` where `{omtfPt}` >= ptCut
# and `omtfQuality` >= qualityCut. Limit output to avoid flooding the terminal.
#print_matching_rows(data_omtf, omtfPt, ptCut, qualityCut)

if "NNreg" in version :
    omtfPt = "combPt"
    #omtfPt = "nnPt0"

#omtfPt = "omtfPt"    

print(version, " using omtfPt = ", omtfPt)
rate_plots(axs2[1, 0], data_omtf, omtfPt, qualityCut, ptCutBins, norm, axs2[0, 1])
rate_plots(axs2[1, 1], data_omtf, "omtfUPt", qualityCut, ptCutBins, norm, None)

fig2.suptitle(version, fontsize=16, fontweight='bold')
##################################################################################3
#axs[0, 0].grid(axis='y', alpha=0.75)
# Adjust layout and save each figure to its own file
plots_dir = "./plots/"

# Ensure the output directory exists
os.makedirs(plots_dir, exist_ok=True)

fig1.tight_layout()

postfix = version + '_' + omtfPt + '_' + str(qualityCut)

fig1.savefig(plots_dir + 'controlPlots' + postfix + '.png')

fig2.tight_layout()
fig2.savefig(plots_dir + 'rates_' + postfix + '.png')

#plt.show()