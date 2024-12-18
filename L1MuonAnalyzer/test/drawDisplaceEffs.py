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
#from matplotlib import legend

print("asfdafafa")

gStyle.SetOptStat(0)
#gStyle.SetOptTitle(0);


inputFiles = []

canvases = []
hists = []

algoVersion = "t21a__Patterns_0x00012"
lineColor = kBlack

#old version, not good
#dir = "/home/kbunkow/CMSSW/CMSSW_12_1_0_pre3/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/"
#inputFile = TFile(dir + 'omtfAnalysis2_eff_SingleMu_tt10_displ_test_500files.root' )

#dir = "/home/kbunkow/CMSSW/CMSSW_12_1_0_pre5/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/"
#inputFile = TFile(dir + 'omtfAnalysis2_eff_SingleMu_tt15_displ_test_allfiles.root' )

#dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_12_x_x_official/CMSSW_12_6_0_pre4/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/"
#inputFile = TFile(dir + 'omtfAnalysis2_eff_SingleMu_tt14_extrapolSimpl_displ_allfiles.root' )
#inputFile = TFile(dir + 'omtfAnalysis2_eff_SingleMu_tExtraplMB1nadMB2SimplifiedFP_t17_v2.root' )

#dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_12_x_x_official/CMSSW_12_6_0_pre4/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/"
#inputFile = TFile(dir + 'omtfAnalysis2_eff_SingleMu_tt16_extrapolFul_displ.root' )

dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/"
#inputFile = TFile(dir + 'omtfAnalysis2_eff_SingleMu_tExtraplMB1nadMB2SimplifiedFP_t19_v16_test_bits_HTo2LongLivedTo2mu2jets_allFiles.root' )

#algoVersion = "t21a__Patterns_0x00012_EfeMC_HTo2LongLivedTo2mu2jets"
#lineColor = kBlack
#inputFile = TFile(dir + 'omtfAnalysis/omtfAnalysis2_eff__t21a__Patterns_0x00012__MH-1000_MFF-150_CTau-1000mm_allFiles.root' )

#algoVersion = "t21a__Extrapl_Patterns_t17_gpFinalize10_EfeMC_HTo2LongLivedTo2mu2jets"  small statistics!!!!!!!!
#lineColor = kGreen
#inputFile = TFile(dir + 'omtfAnalysis/omtfAnalysis2_eff__t21a__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3__MH-1000_MFF-150_CTau-1000mm_allFiles_gpFinalize10.root' )
# #
# algoVersion = "t21a__Extrapl_Patterns_t17_gpFinalize11"
# lineColor = kRed
# inputFile = TFile(dir + 'omtfAnalysis/omtfAnalysis2_eff__t21a__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3__MH-1000_MFF-150_CTau-1000mm_allFiles_gpFinalize11.root' )
#
# algoVersion = "t22__Extrapl_Patterns_t17_v0_gpFinalize10_EfeMC_HTo2LongLivedTo2mu2jets"
# lineColor = kMagenta
# inputFile = TFile(dir + 'omtfAnalysis/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_gpFinalize10__EfeMC_HTo2LongLivedTo2mu2jets.root' )
#
# algoVersion = "t22__Extrapl_Patterns_t17_gpFinalize10_EfeMC_HTo2LongLivedTo2mu2jets"
# lineColor = kGreen
# inputFile = TFile(dir + 'omtfAnalysis/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10__EfeMC_HTo2LongLivedTo2mu2jets.root' )


# algoVersion = "eff_t22__Extrapl_Patterns_t17_gpFinalize10_displMuGun"
# lineColor = kGreen
# inputFile = TFile(dir + 'omtfAnalysis/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10__Displaced_Dxy5m_pT0To1000_condRun3.root' )


# algoVersion = "phase2_t20__Extrapl_Dxy3m_pT0To1000"
# dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase2/test/expert/rootDump/"
# lineColor = kMagenta
# inputFile = TFile(dir + 'omtfAnalysis2_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_d1_DTQ0_SingleMu_effAna_rootDump_Displaced_Dxy3m_pT0To1000_condPhase2_realistic.root' )
#
#algoVersion = "phase2_t20__Extrapl_XTo2LLTo4Mu"
#lineColor = kBlue
#inputFile = TFile(dir + 'omtfAnalysis2_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t21b_DTQ0_effAna_rootDump_Displaced_cTau5m_XTo2LLTo4Mu.root' )

#dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase1/results/"

#algoVersion = "t27a__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__EfeMC_HTo2LongLivedTo2mu2jets"
#lineColor = kMagenta
#inputFile = TFile(dir + 'omtfAnalysis2_eff_t27a__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__EfeMC_HTo2LongLivedTo2mu2jets.root' )

dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_1_0_pre4/src/usercode/L1MuonAnalyzer/test/OMTF_phase1/"
algoVersion = "Phase1_2024__LLPGun_mH20_1000_cTau10_5000mm"
lineColor = kBlue
inputFile = TFile(dir + 'omtfAnalysis2_eff_t31__Phase1_2024__LLPGun_mH20_1000_cTau10_5000mm.root' )

dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_1_0_pre4/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/rootDump/"
#algoVersion = "DT_2_2_t30____DT_2_2_4_LLPGun_mH20_1000_cTau10_5000mm"
#lineColor = kMagenta
#inputFile = TFile(dir + 'omtfAnalysis2_ExtraplMB1nadMB2DTQualAndRFixedP__pats_DT_2_2_t30____DT_2_2_4_LLPGun_mH20_1000_cTau10_5000mm.root' )

#algoVersion = "DT_2_2_2_t31____DT_2_2_2_LLPGun_mH20_1000_cTau10_5000mm"
#lineColor = kGreen
#inputFile = TFile(dir + 'omtfAnalysis2_ExtraplMB1nadMB2DTQualAndRFixedP__pats_DT_2_2_2_t31____DT_2_2_2_LLPGun_mH20_1000_cTau10_5000mm.root' )

#algoVersion = "DT_2_2_2_t31____DT_2_2_2_t32_LLPGun_mH20_1000_cTau10_5000mm"
#lineColor = kBlue
#inputFile = TFile(dir + 'omtfAnalysis2_ExtraplMB1nadMB2DTQualAndRFixedP__pats_DT_2_2_2_t31____DT_2_2_2_t32_LLPGun_mH20_1000_cTau10_5000mm.root' )

#algoVersion = "DT_2_2_t30____DT_2_2_2_t33_LLPGun_mH20_1000_cTau10_5000mm"
#lineColor = kRed
#inputFile = TFile(dir + 'omtfAnalysis2_ExtraplMB1nadMB2DTQualAndRFixedP__pats_DT_2_2_t30____DT_2_2_2_t33_LLPGun_mH20_1000_cTau10_5000mm.root' )

dir = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/rootDump/"
algoVersion = "DT_2_2_2_t35____DT_2_2_2_t35_LLPGun_mH20_1000_cTau10_5000mm"
lineColor = kBlue
inputFile = TFile(dir + 'omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t35_LLPGun_mH20_1000_cTau10_5000mm.root' )

#algoVersion = "DT_2_2_2_t35____DT_2_2_2_t35_co1_LLPGun_mH20_1000_cTau10_5000mm"
#lineColor = kRed
#inputFile = TFile(dir + 'omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_co1_t35_LLPGun_mH20_1000_cTau10_5000mm.root' )

inputFiles.append(inputFile)
inputFile.ls()

efficiencyDir = inputFile.Get("L1MuonAnalyzerOmtf/efficiency")
#layersStatDirDispl.ls()

c1 = TCanvas('canvas_1' , 'canvas_1', 200, 10, 1200, 800)
c1.Divide(3, 2)
#c1.SetLeftMargin(0.13)
#c1.SetRightMargin(0.22)
canvases.append(c1)

c1.cd(1).SetGridx()
c1.cd(1).SetGridy()

ptL1Cut = "10"

qualityCut = "qualityCut_8"
q = "q8"

ptL1Cut = "22"
#ptL1Cut = "10"
#ptL1Cut = "5"
#ptL1Cut = "1"

qualityCut = "qualityCut_12"
q = "q12"

effHist = efficiencyDir.Get("omtf_" + q + "_effPtGenVsDxy_" + qualityCut + "_ptL1Cut_" + ptL1Cut)
effHist.GetXaxis().SetRangeUser(0, 100)
effHist.Draw("colz")
hists.append(effHist)

c1.cd(4).SetGridx()
c1.cd(4).SetGridy()

allCandsPtGenVsDxyProj = efficiencyDir.Get("omtf_" + q + "_allCandsPtGenVsDxy_" + qualityCut + "_ptL1Cut_" + ptL1Cut).ProjectionY()
aceptedCandsPtGenVsDxyProj = efficiencyDir.Get("omtf_" + q + "_aceptedCandsPtGenVsDxy_" + qualityCut + "_ptL1Cut_" + ptL1Cut).ProjectionY(algoVersion + "_" + qualityCut + "_ptL1Cut_" + ptL1Cut)
aceptedCandsPtGenVsDxyProj.Divide(allCandsPtGenVsDxyProj)
aceptedCandsPtGenVsDxyProj.SetName(qualityCut + " ptCut " + ptL1Cut +"GeV " + algoVersion)
#aceptedCandsPtGenVsDxyProj.GetXaxis().SetRangeUser(0, 100)
aceptedCandsPtGenVsDxyProj.SetLineColor(lineColor)
aceptedCandsPtGenVsDxyProj.GetYaxis().SetRangeUser(0, 1.0)
aceptedCandsPtGenVsDxyProj.Draw()
hists.append(aceptedCandsPtGenVsDxyProj)
histPt = aceptedCandsPtGenVsDxyProj

c1.cd(2).SetGridx()
c1.cd(2).SetGridy()
effHist = efficiencyDir.Get("omtf_" + q + "_effPtGenVsDxy_" + qualityCut + "_uptL1Cut_" + ptL1Cut)
effHist.GetXaxis().SetRangeUser(0, 100)
effHist.Draw("colz")
hists.append(effHist)

c1.cd(5).SetGridx()
c1.cd(5).SetGridy()

allCandsPtGenVsDxyProj = efficiencyDir.Get("omtf_" + q + "_allCandsPtGenVsDxy_" + qualityCut + "_uptL1Cut_" + ptL1Cut).ProjectionY()
aceptedCandsPtGenVsDxyProj = efficiencyDir.Get("omtf_" + q + "_aceptedCandsPtGenVsDxy_" + qualityCut + "_uptL1Cut_" + ptL1Cut).ProjectionY(algoVersion + "_" + qualityCut + "_uptL1Cut_" + ptL1Cut)
aceptedCandsPtGenVsDxyProj.Divide(allCandsPtGenVsDxyProj)
aceptedCandsPtGenVsDxyProj.SetName(qualityCut + " uptCut " + ptL1Cut +"GeV " + algoVersion)
#aceptedCandsPtGenVsDxyProj.GetXaxis().SetRangeUser(0, 100)
aceptedCandsPtGenVsDxyProj.SetLineColor(lineColor)
aceptedCandsPtGenVsDxyProj.GetYaxis().SetRangeUser(0, 1.0)
aceptedCandsPtGenVsDxyProj.Draw("colz")
hists.append(aceptedCandsPtGenVsDxyProj)
histUPt = aceptedCandsPtGenVsDxyProj

c1.cd(3).SetGridx()
c1.cd(3).SetGridy()
effHist = efficiencyDir.Get("omtf_" + q + "_effPtGenVsDxy_ifPtBelowCut_" + qualityCut + "_uptL1Cut_" + ptL1Cut)
effHist.GetXaxis().SetRangeUser(0, 100)
effHist.Draw("colz")
hists.append(effHist)

c1.cd(6).SetGridx()
c1.cd(6).SetGridy()

allCandsPtGenVsDxyProj = efficiencyDir.Get("omtf_" + q + "_allCandsPtGenVsDxy_ifPtBelowCut_" + qualityCut + "_uptL1Cut_" + ptL1Cut).ProjectionY()
aceptedCandsPtGenVsDxyProj = efficiencyDir.Get("omtf_" + q + "_aceptedCandsPtGenVsDxy_ifPtBelowCut_" + qualityCut + "_uptL1Cut_" + ptL1Cut).ProjectionY(algoVersion + "_" + qualityCut + "_uptL1Cut_" + ptL1Cut + "_ifPtBelowCut")
aceptedCandsPtGenVsDxyProj.SetName(qualityCut + " uptCut " + ptL1Cut +"GeV " + algoVersion+ " ifPtBelowCut")
aceptedCandsPtGenVsDxyProj.Divide(allCandsPtGenVsDxyProj)
#aceptedCandsPtGenVsDxyProj.GetXaxis().SetRangeUser(0, 100)
aceptedCandsPtGenVsDxyProj.SetLineColor(lineColor)
aceptedCandsPtGenVsDxyProj.GetYaxis().SetRangeUser(0, 1.0)
aceptedCandsPtGenVsDxyProj.Draw("colz")
hists.append(aceptedCandsPtGenVsDxyProj)


#effHist.GetYaxis().SetTitle("#phi_{B2} - #phi_{B2extrpol}")
#effHist.GetXaxis().SetTitle("dXY")
#effHist.GetYaxis().SetTitle("efficiency")


c1.Modified()
c1.Update()

outFile = TFile(algoVersion + "_ptL1Cut_" + ptL1Cut + "_" + q + ".root", "RECREATE")
outFile.cd()
for hist in hists :
    hist.Write()

c2 = TCanvas('canvas_2' , 'canvas_2', 200, 10, 450, 450)
c2.cd()
c2.SetGridx()
c2.SetGridy()
histPt.SetLineStyle(2)
histPt.Draw()
histUPt.SetLineColor(lineColor)
histUPt.Draw("same")
legend = TLegend(0.5, 0.6, 0.8, 0.8)
legend.SetBorderSize(0)
legend.SetTextSize(0.027)
legend.AddEntry(histPt, "OMTF pT #geq " + str(ptL1Cut) + "GeV, " + q)
legend.AddEntry(histUPt, "OMTF upT #geq " + str(ptL1Cut) + "GeV, " + q)

legend.Draw()

c2.Modified()
c2.Update()



input("Press ENTER to exit")
 