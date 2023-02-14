from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TH1D, TEfficiency, TH2D
from ROOT import gROOT
from ROOT import gStyle
from ROOT import TLegend
from ROOT import kBlack, kBlue, kRed, kGreen, kMagenta, kCyan
from array import array

#from libPyROOT import TDirectory
from ROOT import TDirectory
import os
import sys
from matplotlib import legend

gStyle.SetOptStat(0)
#gStyle.SetOptTitle(0);


inputFiles = []
canvases = []
hists = []

#old version, not good
#dir = "/home/kbunkow/CMSSW/CMSSW_12_1_0_pre3/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/"
#inputFile = TFile(dir + 'omtfAnalysis2_eff_SingleMu_tt10_displ_test_500files.root' )

dir = "/home/kbunkow/CMSSW/CMSSW_12_1_0_pre5/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/"
inputFile = TFile(dir + 'omtfAnalysis2_eff_SingleMu_tt15_displ_test_allfiles.root' )

#dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_12_x_x_official/CMSSW_12_6_0_pre4/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/"
#inputFile = TFile(dir + 'omtfAnalysis2_eff_SingleMu_tt14_extrapolSimpl_displ_allfiles.root' )


inputFiles.append(inputFile)
inputFile.ls()

efficiencyDir = inputFile.Get("L1MuonAnalyzerOmtf/efficiency")
#layersStatDirDispl.ls()

c1 = TCanvas('canvas_1' , 'canvas_1', 200, 10, 1200, 1000)
c1.Divide(3, 2)
#c1.SetLeftMargin(0.13)
#c1.SetRightMargin(0.22)
canvases.append(c1)

c1.cd(1).SetGridx()
c1.cd(1).SetGridy()

ptL1Cut = "12"

effHist = efficiencyDir.Get("omtf_q12_effPtGenVsDxy_qualityCut_12_ptL1Cut_" + ptL1Cut)
effHist.GetXaxis().SetRangeUser(0, 100)
effHist.Draw("colz")
hists.append(effHist)

c1.cd(2).SetGridx()
c1.cd(2).SetGridy()

effHist = efficiencyDir.Get("omtf_q12_effPtGenVsDxy_qualityCut_12_uptL1Cut_" + ptL1Cut)
effHist.GetXaxis().SetRangeUser(0, 100)
effHist.Draw("colz")
hists.append(effHist)

c1.cd(3).SetGridx()
c1.cd(3).SetGridy()
effHist = efficiencyDir.Get("omtf_q12_effPtGenVsDxy_ifPtBelowCut_qualityCut_12_uptL1Cut_" + ptL1Cut)
effHist.GetXaxis().SetRangeUser(0, 100)
effHist.Draw("colz")
hists.append(effHist)


#effHist.GetYaxis().SetTitle("#phi_{B2} - #phi_{B2extrpol}")
#effHist.GetXaxis().SetTitle("dXY")
#effHist.GetYaxis().SetTitle("efficiency")






c1.Modified()
c1.Update()

input("Press ENTER to exit")
 