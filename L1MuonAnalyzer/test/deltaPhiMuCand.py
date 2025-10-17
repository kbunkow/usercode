# author Wiktor Radoslaw Matyszkiewicz wmatyszk@cern.ch

import uproot
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

import warnings
warnings.filterwarnings("ignore", message="The value of the smallest subnormal for <class 'numpy.float64'> type is zero.")

###CONSTANTS###

CALCULATE = True
MAX_CUT = 0.998
MIN_CUT = 0.002
OUTPUT_FILE = "deltaPhi_cand_simMu.root"

#INPUT_FILE = "data_dump_21_02_2025.root"
prefix = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/rootDump/"
input_files = [
                prefix + "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t35_mcWaw2023_iPt2_04_04_2023.root",
                prefix + "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t35_mcWaw_2024_04_03_OneOverPt.root",
                ]

###UPLOADING ROOT FILES -> NUMPY ARRAYS
tree_path = "simOmtfPhase2Digis/OMTFHitsTree"

#data = np.array(["omtfPhi", "muonPt", "muonPhi", "muonCharge", "omtfProcessor"])

data = uproot.concatenate(input_files, expressions=["omtfPhi", "muonPt", "muonPhi", "muonCharge", "omtfProcessor"], library="np")

###DATA PROCESSING
print("full data len ", len(data["omtfProcessor"]),"\n", data)

processor = data["omtfProcessor"]
simPt = data["muonPt"]
mask = (processor != 10) & (simPt != 0)
processor = np.fabs(processor[mask])
simPt = simPt[mask]
omtfPhi = data["omtfPhi"][mask]
simPhi = data["muonPhi"][mask]
simCharge = data["muonCharge"][mask]

###CONVERSION MEASURED PHI TO RADIANS
#(simPhi already in radians)

phiUnit = 2*np.pi / 5400
phiProc = np.pi*2 / 3 * processor
phi15deg = np.pi/12

omtfPhi = omtfPhi * phiUnit + phiProc + phi15deg
omtfPhi [omtfPhi > 2*np.pi] -= 2*np.pi
omtfPhi [omtfPhi > np.pi] -= 2*np.pi
print("Minimum of radian OMTF: ", np.min(omtfPhi)/np.pi)
print("Maximum of radian OMTF: ", np.max(omtfPhi)/np.pi)

print("Minimum of simPhi: ", np.min(simPhi)/np.pi)
print("Maximum of simPhi: ", np.max(simPhi)/np.pi)

deltaPhi = (simPhi - omtfPhi) % (np.pi*2)
deltaPhi [deltaPhi > np.pi] -= 2*np.pi

output_name = OUTPUT_FILE # + f"_{sign}.root"

output_file = ROOT.TFile(output_name, "RECREATE")
if output_file.IsZombie():
    print(f"Error: Could not create file {output_name}")
    exit(1)    

def dynamic_bins(min_pt, max_pt, bin_widths):
    bins = [min_pt]
    current_pt = min_pt
    current_bin_width = bin_widths[0]

    while current_pt < max_pt:
        if current_pt / current_bin_width >= 10:
            current_bin_width = next((bw for bw in bin_widths if current_pt / bw < 10), bin_widths[-1])
        current_pt += current_bin_width
        bins.append(current_pt)

    return np.array(bins)

def deltaPhiMuCand(charge):

    mask2 = (simCharge == charge)
    deltaPhi_inner = deltaPhi[mask2]
    simPt_inner = simPt[mask2]
    print("Liczba eventów: ", simPt_inner.shape)

    ###DIVISION INTO BINS

    min_pt = np.min(simPt_inner)
    min_pt = 0 #math.floor(min_pt *2) / 2
    max_pt = np.max(simPt_inner)
    max_pt = math.ceil(max_pt)
    bin_widths = [0.5, 1, 2, 5, 10, 20, 50, 100]
    #bin_widths = [0.5, 1, 5, 10, 50, 100]
    
    bins = dynamic_bins(min_pt, max_pt, bin_widths)
    bins = np.unique(bins)
    print("BINS: ", bins)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_indices = np.digitize(simPt_inner, bins) - 1

    deltaPhi_by_pt = {}
    pt_by_pt = {}

    for i, center in enumerate(bin_centers):
        mask = (bin_indices == i)
        deltaPhi_by_pt[center] = deltaPhi_inner[mask]
        pt_by_pt[center] = simPt_inner[mask]


        
    if CALCULATE:
        minDelta_by_pt = {}
        maxDelta_by_pt = {}
        median_by_pt = {}
        deltaPhi_by_pt_filtered = {}

        for center in bin_centers:
            sorted_values = deltaPhi_by_pt[center] #np.sort(deltaPhi_by_pt[center])

            if len(sorted_values) == 0:
                continue

            minDelta_by_pt[center] = np.quantile(sorted_values, MIN_CUT)
            maxDelta_by_pt[center] = np.quantile(sorted_values, MAX_CUT)
            median_by_pt[center] = np.median(sorted_values)

            deltaPhi_by_pt_filtered[center] = sorted_values[(sorted_values > minDelta_by_pt[center]) & (sorted_values < maxDelta_by_pt[center])]

        ###SAVING TO ROOT FILE

        bin_edges = bins
        #if len(bin_edges) > 1:
        #    bin_edges = np.append(bin_edges, bin_edges[-1] + (bin_edges[-1] - bin_edges[-2]))
        #else:
        #    print("Error: Not enough bin edges to create histogram.")
        #    exit(1)

        pt_values = (bin_edges[:-1] + bin_edges[1:]) / 2

        sign = "pos" if charge == 1 else "neg"

        hist_min = ROOT.TH1F("minDelta_" + sign, "Minimum delta_phi, quatile " + str(MIN_CUT) + ", " + sign + "; pT; minDelta", len(bin_edges) -1, bin_edges)
        hist_max = ROOT.TH1F("maxDelta_" + sign, "Maximum , quatile " + str(MAX_CUT) + ", " + sign + "; pT; maxDelta", len(bin_edges) -1, bin_edges)
        hist_median = ROOT.TH1F("medianDelta_" + sign, "Median Delta Phi - " + sign + "; pT; medianDelta", len(bin_edges)-1, bin_edges)

        for i, pt in enumerate(pt_values):
            hist_min.SetBinContent(i + 1, minDelta_by_pt.get(pt, 0))
            hist_max.SetBinContent(i + 1, maxDelta_by_pt.get(pt, 0))
            hist_median.SetBinContent(i + 1, median_by_pt.get(pt, 0))
            
            
        hist_deltaphi_vs_pt = ROOT.TH2F("deltaphi_vs_pt_" + sign, "Delta Phi vs pt - " + sign + "; pT; delta phi", len(pt_values), bin_edges, 100, -3, 3)
        hist_deltaphi_vs_pt_filtered = ROOT.TH2F("deltaphi_vs_pt_filtered_" + sign, "Delta Phi vs pt (filtered) - " + sign + "; pT; delta phi", len(pt_values), bin_edges, 100, -3, 3)

        for i, pt in enumerate(pt_values):
            for delta_phi in deltaPhi_by_pt.get(pt, []):
                hist_deltaphi_vs_pt.Fill(pt, delta_phi)

        for i, pt in enumerate(pt_values):
            for delta_phi in deltaPhi_by_pt_filtered.get(pt, []):
                hist_deltaphi_vs_pt_filtered.Fill(pt, delta_phi)

        hist_min.Write()
        hist_max.Write()
        hist_median.Write()
        hist_deltaphi_vs_pt.Write()
        hist_deltaphi_vs_pt_filtered.Write()
 
deltaPhiMuCand(1)
deltaPhiMuCand(-1)

output_file.Close()