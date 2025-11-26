from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TH1D, TEfficiency, TH2D, TDirectory
from ROOT import gROOT
from ROOT import gStyle

#from libPyROOT import TDirectory
import os
import sys

gStyle.SetOptStat(0)

def makeEfficiency(passed, total, title, lineColor):
    if TEfficiency.CheckConsistency(passed, total) :
        efficiency = TEfficiency(passed, total)
        #title = std::regex_replace(title, std::regex("\\muCandGenEtaMuons"), "tagging efficiency");
        efficiency.SetTitle( title );
        efficiency.SetStatisticOption(6  ); #TEfficiency.EStatOption.kBUniform
        efficiency.SetPosteriorMode();
        efficiency.SetLineColor(lineColor);
        return efficiency;
    else :
        print("makeEfficiency TEfficiency::CheckConsistency(*ptGenPtTTMuonNom, *ptGenPtTTMuonDenom) failed" )
        exit(1);
    

#version = "PU200_v2_t" + sys.argv[1] #PU200_mtd5_v2_t

#inputResults  = sys.argv[1] 
#version = inputResults[inputResults.find("_t") +1 : ]

#version = sys.argv[1] 
#inputResults = 'SingleNeutrino_' + version 

rootDirPostFix = ""
print("sys.argv.__len__", len(sys.argv) )
if len(sys.argv) >= 2 :
    rootDirPostFix = sys.argv[1] 

#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis_newerSAmple_v21_1_10Files_withMatching.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis_newerSAmple_v21_1.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis2_rate_v0006.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis2_v31.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_omtf_nn_MC_analysis_MuFlatPt_PU200_v2_t30/results/omtfAnalysis2.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_omtf_nn_MC_analysis_SingleNeutrino_PU200_' + version + '/results/omtfAnalysis2.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_omtf_nn_MC_analysis_' + inputResults + '/results/omtfAnalysis2.root' )

#if version < "MuFlatPt_PU200_v3_t73" :
#    histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/' + inputResults + '/results/omtfAnalysis2.root' )
#else :
#    histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_omtf_' + inputResults + '/results/omtfAnalysis2.root' )

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/omtfAnalysis/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10__NeutrinoGun_PU200_Alibordi.root' )
#version = "t22__with_extrapolation"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/omtfAnalysis/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10_DTQ_2_2__NeutrinoGun_PU200_Alibordi.root' )
#version = "t22__with_extrapolation__DTQ_2_2"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/omtfAnalysis/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2FullAlgo_t16_classProb17_recalib2_gpFinalize10__NeutrinoGun_PU200_Alibordi.root' )
#version = "t22__full_extrapolation"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/omtfAnalysis/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_gpFinalize10__NeutrinoGun_PU200_Alibordi.root' )
#version = "t22__with_extrapolation_patts0"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/omtfAnalysis/omtfAnalysis2_eff_t22__Patterns_0x00012__NeutrinoGun_PU200_Alibordi.root' )
#version = "t22__OMTF2023_DTQ_2_2"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/omtfAnalysis/omtfAnalysis2_eff_t22__Patterns_0x00012_DTQ_2_4__NeutrinoGun_PU200_Alibordi.root' )
#version = "t22__OMTF2023_DTQ_2_4"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_run3_ZeroBias_Run2023_t22/results/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10.root' )
#version = "t22__with_extrapolation_367883"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase2/test/expert/omtfAnalysis/omtfAnalysis2_rate_t22__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0__NeutrinoGun_PU200_Alibordi.root' )
#version = "t22_phase2_with_extrapolation"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t23__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0__MinBias_Phase2Spring23_PU140.root' )
#version = "t23_phase2_with_extrapolation_DTQ_2_2__MinBias_Phase2Spring23_PU140"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t23__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_NN_FP_v217__MinBias_Phase2Spring23_PU140.root' )
#version = "t23_phase2_with_extrapolation_NN_FP_v217_DTQ_2_2__MinBias_Phase2Spring23_PU140"


# histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t23__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_DTQ_2_4__MinBias_Phase2Spring23_PU140.root' )
# version = "t23_phase2_with_extrapolation_DTQ_2_4__MinBias_Phase2Spring23_PU140"
#
# histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t23__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_DTQ_2_4_NN_FP_v217__MinBias_Phase2Spring23_PU140.root' )
# version = "t23_phase2_with_extrapolation_NN_FP_v217_DTQ_2_4__MinBias_Phase2Spring23_PU140"
#
#
# histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t23__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_DTQ_0_2__MinBias_Phase2Spring23_PU140.root' )
# version = "t23_phase2_with_extrapolation_DTQ_0_2__MinBias_Phase2Spring23_PU140"
#
# #histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t23__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_DTQ_0_2_NN_FP_v217__MinBias_Phase2Spring23_PU140.root' )
# #version = "t23_phase2_with_extrapolation_NN_FP_v217_DTQ_0_2__MinBias_Phase2Spring23_PU140"
#
# histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t23a__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_DTQ_2_2_NN_FP_v217__MinBias_Phase2Spring23_PU140.root' )
# version = "t23a_phase2_with_extrapolation_NN_FP_v217_DTQ_2_2__MinBias_Phase2Spring23_PU140"
#
# #histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t23b__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_DTQ_2_2_NN_FP_v217__MinBias_Phase2Spring23_PU140.root' )
# #version = "t23b_phase2_with_extrapolation_NN_FP_v217_DTQ_2_2__MinBias_Phase2Spring23_PU140"
#
# histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t24b__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_DTQ_2_2_NN_FP_v217__MinBias_Phase2Spring23_PU140.root' )
# version = "t24b_phase2_with_extrapolation_NN_FP_v217_DTQ_2_2__MinBias_Phase2Spring23_PU140"
#
#
#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t24c__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_DTQ_2_2__MinBias_Phase2Spring23_PU200.root')
#version = "t24c_phase2_with_extrapolation_DTQ_2_2__MinBias_Phase2Spring23_PU200"

#histFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/results/omtfAnalysis2_eff_t24c__Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0_DTQ_2_2_NN_FP_v217__MinBias_Phase2Spring23_PU200.root' )
#version = "t24c_phase2_with_extrapolation_NN_FP_v217_DTQ_2_2__MinBias_Phase2Spring23_PU200"

#path = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase1/results/"
#histFile = TFile(path + "omtfAnalysis2_rate_t26__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10_DTQ_2_4__EphemeralZeroBias_Run370580.root")
#version = "t26_phase2_with_extrapolation_DTQ_2_4__EphemeralZeroBias_Run370580"

#histFile = TFile(path + "omtfAnalysis2_rate_t27__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10_DTQ_2_4__MinBias_Phase2Spring23_PU200.root")
#version = "t27_phase2_with_extrapolation_DTQ_2_4__MinBias_Phase2Spring23_PU200"

#histFile = TFile(path + "omtfAnalysis2_rate_t27a__Patterns_0x00020_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200.root")
#version = "t27a__Patterns_0x00020_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200"

#histFile = TFile(path + "omtfAnalysis2_rate_t27a__Patterns_0x00021_classProb20_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200.root")
#version = "t27a__Patterns_0x00021_classProb20_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200"

#histFile = TFile(path + "omtfAnalysis2_rate_t27a__Patterns_0x00020_classProb21_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200.root")
#version = "t27a__Patterns_0x00020_classProb21_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200"

#histFile = TFile(path + "omtfAnalysis2_rate_t27a__Patterns_0x00021_classProb21_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200.root")#
#version = "t27a__Patterns_0x00021_classProb21_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200"


#histFile = TFile(path + "omtfAnalysis2_rate_t27b__Patterns_0x00020_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200.root")
#version = "t27b__Patterns_0x00020_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200"

#histFile = TFile(path + "omtfAnalysis2_rate_t27b__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200.root")
#version = "t27b__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200"


#histFile = TFile(path + "omtfAnalysis2_rate_t27a__Patterns_0x00020_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200.root")
#version = "t27a__Patterns_0x00020_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200"

#histFile = TFile(path + "omtfAnalysis2_rate_t27a__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200.root")
#version = "t27a__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__MinBias_Phase2Spring23_PU200"

#path = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_run3_ZeroBias_Run2023_t26_0/results"
#histFile = TFile(path + "omtfAnalysis2_rate_t26__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10_DTQ_2_4__ZeroBiasRun370580.root")
#version = "t26__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10_DTQ_2_4__ZeroBiasRun370580"

#path = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_run3_ZeroBias_Run2023_367883_t27a_0/results/"
#histFile = TFile(path + "omtfAnalysis2_rate_t27a__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__ZeroBiasRun370580.root")
#version = "rate_t27a__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__ZeroBiasRun367883"

#path = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_run3_ZeroBias_Run2024_379252_t27b_1/results/"
#histFile = TFile(path + "omtfAnalysis2_rate_t27b__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__ZeroBiasRun370580.root")
#version = "rate_t27b__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__ZeroBiasRun370580"


#path = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_run3_ZeroBias_Run2024_379252_t27a_0/results/"
#histFile = TFile(path + "omtfAnalysis2_rate_t27a__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__ZeroBiasRun370580.root")
#version = "rate_t27a__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__ZeroBiasRun370580"

#path = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_run3_ZeroBias_Run2024_379252_t27b_0/results/"
#histFile = TFile(path + "omtfAnalysis2_rate_t27b__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__ZeroBiasRun370580.root")
#version = "rate_t27b__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__ZeroBiasRun370580"

#path = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_Phase2Spring24_MinBias__t37/results/"
#histFile = TFile(path + "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t37.root")
#version = "rate_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t37_Phase2Spring24_MinBias"

path = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/rootDump/"
#histFile = TFile(path + "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t38_MinBias_Phase2Spring23_PU200.root")
#version = "DT_2_2_2_t38_MinBias_Phase2Spring23_PU200"

#histFile = TFile(path + "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t38_NN_MinBias_Phase2Spring23_PU200.root")
#version = "DT_2_2_2_t38_NN_MinBias_Phase2Spring23_PU200"

histFile = TFile(path + "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t39_MinBias_Phase2Spring23_PU200.root")
version = "DT_2_2_2_t39_MinBias_Phase2Spring23_PU200"

path = '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_Phase2Spring24_MinBias__t40/results/'

histFile = TFile(path + "omtfAnalysis2_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_2_2_2_t40.root")
version = "DT_2_2_2_t40_Phase2Spring24_MinBias_PU200"


inputResults = version

print (histFile)

#lhcFillingRatio = 2760./3564.
lhcFillingRatio = 2345./3564.; #run 367883     2023C
lhcFreq = 40144896; #11264 * 3564

rootDirStr = "L1MuonAnalyzerOmtf" + rootDirPostFix

analyzerOmtfDir = histFile.Get(rootDirStr)
candPerEvent = analyzerOmtfDir.Get("candPerEvent")
print ("candPerEvent " + str(type(candPerEvent) ))

eventCnt = candPerEvent.Integral() 
scale = 1./eventCnt * lhcFreq * lhcFillingRatio;

print ("eventCnt " + str(eventCnt) );
print ("scale " + str(scale) );


rateDir = histFile.Get(rootDirStr + "/rate")
rateDir.ls()

canvases = []
rateCumuls = []
efficienciesHist1 = []
efficienciesHist2 = []

rateCumul_withTEffs = []
paintedGraphs = []
#gStyle.SetOptStat(111111111)

outPath = inputResults 
if rootDirPostFix != "":
    inputResults = inputResults + "_" + rootDirPostFix
    
if not os.path.exists(outPath):
    os.mkdir(outPath)
    
outFile = TFile(outPath + "/ratePlots.root", "RECREATE")




def makeRatePlotWithEff(candPt_rateCumul_copy, lineColor, canvasRate1, canvasRate2) :
    allEventsHist = candPt_rateCumul_copy.Clone(candPt_rateCumul_copy.GetName() + "_allEventsHist");
    for iBin in range(0, allEventsHist.GetNbinsX() ) :
        allEventsHist.SetBinContent(iBin, eventCnt)
    
    candPt_rateCumul_copy.Sumw2(False);
    allEventsHist.Sumw2(False);
    
    title = ("; OMTF p_{T}^{cut} [GeV]; probability per BX");
    rateCumul_withTEff = makeEfficiency(candPt_rateCumul_copy, allEventsHist, title, lineColor)
    
    canvasRate1.cd()
    rateCumul_withTEff.Draw("APZ")
    canvasRate1.Update()
    rateCumul_withTEff.GetPaintedGraph().GetXaxis().SetRangeUser(0, 100)
    #rateCumul_withTEff.GetPaintedGraph().GetYaxis().SetRangeUser(1, 1000)
    
    paintedGraph = rateCumul_withTEff.GetPaintedGraph().Clone(rateCumul_withTEff.GetName() + "_copy" ) 
    
    #rateCumul_withTEff.GetPaintedGraph().SetTitle( "probability per BX")
    #canvasRate1.Update()
    
    scalekHz = 0.001
    for i in range(0, paintedGraph.GetN()) :
        paintedGraph.GetY()[i] *= lhcFreq * lhcFillingRatio * scalekHz
        paintedGraph.GetEYhigh()[i] *= lhcFreq * lhcFillingRatio * scalekHz
        paintedGraph.GetEYlow()[i] *= lhcFreq * lhcFillingRatio * scalekHz
          
    canvasRate2.cd()     
    canvasRate2.SetGridx()
    canvasRate2.SetGridy()   
    canvasRate2.SetLogy()
    paintedGraph.Draw("APZ")
    canvasRate2.Update();
    paintedGraph.GetXaxis().SetRangeUser(0, 60);
    #paintedGraph.GetYaxis().SetRangeUser(10 * scalekHz, 50000000 * scalekHz);
    paintedGraph.GetYaxis().SetRangeUser(1, 1000);
    
    paintedGraph.GetYaxis().SetTitle("rate [kHz]")
    canvasRate2.Update();     
          
    print ("createad rateCumul_withTEff "  + rateCumul_withTEff.GetName() )           
    print ("createad paintedGraph       "  + paintedGraph.GetName() )       
    return rateCumul_withTEff , paintedGraph


def makeRatePlots(algoDir, rateType, lineColor) :
    print (algoDir.GetName())
    algoDir.ls()
    
    c1 = TCanvas('canvas_' + algoDir.GetName() + "_" + rateType, algoDir.GetName().replace("_", " ") + " " + rateType, 200, 10, 900, 900)
    c1.Divide(2, 2)
    c1.cd(1).SetGridx()
    c1.cd(1).SetGridy()
    print ('created canvas ' + c1.GetName())

    ##########################
    
    candPtKey = "candPt"
    if rateType == "UPt" :
        candPtKey = "candUPt"
    for obj in algoDir.GetListOfKeys():
        if candPtKey in obj.GetName() :
            candPt = obj.ReadObj()
            candPt.SetLineColor(lineColor)
            candPt.Draw("")


            candPt.Sumw2(False);
            candPt_rateCumul = candPt.GetCumulative(False, "_");
            
#             trying to ge agreement woth Carlos plot, but it is not so easy, the last bin contains both pt 100 GeV and overflows, 
#             corr = candPt.GetBinContent(200)
#             print ("corr " + str(corr))
#             for iBin in range(0, candPt_rateCumul.GetNbinsX(), 1) : 
#                 candPt_rateCumul.AddBinContent(iBin, -corr)
            
            candPt_rateCumul.SetName(algoDir.GetName() + "_" + candPt_rateCumul.GetName().replace(candPtKey, "rate_" + rateType) ) #+ "_" + version
            candPt_rateCumul.SetTitle(algoDir.GetName().replace("_", " ") + ", " + version + " " + rootDirPostFix)
            
            
            c1.cd(3).SetGridx()
            c1.cd(3).SetGridy()   
            c1.cd(3).SetLogy()
            
            rateCumul_withTEff, paintedGraph = makeRatePlotWithEff(candPt_rateCumul.Clone(candPt_rateCumul.GetName() + "_copy"), lineColor, c1.cd(3), c1.cd(4))
            rateCumul_withTEffs.append(rateCumul_withTEff)
            paintedGraphs.append(paintedGraph)
            
            candPt_rateCumul.Scale(0.001)
            candPt_rateCumul.GetYaxis().SetTitle("rate [kHz]")
            
            print(candPtKey + ": " + obj.GetName() + " candPt_rateCumul " + candPt_rateCumul.GetName() + " " + candPt_rateCumul.GetTitle() )
            candPt_rateCumul.SetBinContent(1, 0);
            #candPt_rateCumul.Sumw2(False);
            candPt_rateCumul.Scale(scale) #TODO maybe it should be before Sumw2
            candPt_rateCumul.Sumw2(False);
    
            c1.cd(2).SetGridx()
            c1.cd(2).SetGridy()   
            candPt_rateCumul.SetLineColor(lineColor)
            candPt_rateCumul.Draw("")
            
            rateCumuls.append(candPt_rateCumul)
            print ("created rate plot " + candPt_rateCumul.GetName() + " name: " + candPt_rateCumul.GetTitle() )
     
    c1.Update()   
    canvases.append(c1) 
# makeRatePlots #######################################################################       

for iAlgo, obj in enumerate(rateDir.GetListOfKeys() ) :
    algoDir = obj.ReadObj()
    if isinstance(algoDir, TDirectory):
        #makeRatePlots(5)
        lineColor = 2
        if iAlgo ==  0:
            lineColor = 1
        if iAlgo == 1:
            lineColor = 4
        makeRatePlots(algoDir, "Pt", lineColor)
        makeRatePlots(algoDir, "UPt", lineColor)
        
        
ratesOnThreshHist = TH1D("ratesOnThreshHist", inputResults.replace("_", " "), rateCumuls.__len__(), 0, rateCumuls.__len__()) 
relativeRatesOnThreshHist = TH1D("relativeRatesOnThreshHist", "relativeRatesOnThreshHist", rateCumuls.__len__(), 0, rateCumuls.__len__()) 
ratesOnThreshHist.GetYaxis().SetTitle("rate [kHz]")
relativeRatesOnThreshHist.GetYaxis().SetTitle("rate [kHz]")

referenceRate = 13.679002  #omtf q12, PU200_v2_t35

print(histFile)

for iAlgo, canvas in enumerate(canvases ) :
    if iAlgo >= 1 :
        canvas.cd(2)
        rateCumuls[0].DrawCopy("same hist")
        canvas.cd(2).Modified()
        canvas.Update()
    
    ptCutGev = 21.5
        
    if rateCumuls[iAlgo].GetName().find("nn_omtf") >= 0:
        ptCutGev = 22
    elif version.find("t58") >= 0 or version.find("t65") >= 0 or version.find("t74") >= 0 or version.find("t78") >= 0 or version.find("t80") >= 0 or version.find("t82") >= 0 or version.find("t98") >= 0:
        ptCutGev = 18
    else :
        lineColor = 1
        ptCutGev = 20    
    
    ptCutGev = 18 #<<<<<<!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
    
    ptCutBin = rateCumuls[iAlgo].GetXaxis().FindBin(ptCutGev)        
    rateOnThresh = rateCumuls[iAlgo].GetBinContent(ptCutBin)   
    ratesOnThreshHist.Fill( iAlgo, rateOnThresh)
    ratesOnThreshHist.GetXaxis().SetBinLabel(iAlgo +1, canvases[iAlgo].GetTitle() + " ptCut " + str(ptCutGev) + "GeV" )   
    

    relativeRatesOnThresh = rateOnThresh / referenceRate

    print("%s rate %f realitve rate %f " % (ratesOnThreshHist.GetXaxis().GetBinLabel(iAlgo +1), rateOnThresh, relativeRatesOnThresh) )

    relativeRatesOnThreshHist.Fill( iAlgo, relativeRatesOnThresh)
    relativeRatesOnThreshHist.GetXaxis().SetBinLabel(iAlgo +1, canvases[iAlgo].GetTitle() + " ptCut " + str(ptCutGev) + "GeV")    
        
    outFile.cd()
    rateCumuls[iAlgo].Write()
    rateCumul_withTEffs[iAlgo].Write()
    paintedGraphs[iAlgo].Write()
    canvas.Write()

canvasComapre = TCanvas('canvasComapre' , "compare_ " + inputResults, 200, 10, 1400, 700)    
canvasComapre.Divide(2, 1)

canvasComapre.cd(1)
   
canvasComapre.cd(1).SetLeftMargin(0.4)
canvasComapre.cd(1).SetGridx()
canvasComapre.cd(1).SetGridy()
ratesOnThreshHist.GetYaxis().SetRangeUser(4, 20)
ratesOnThreshHist.GetYaxis().SetLabelSize(0.02)
ratesOnThreshHist.SetFillColor(0)
ratesOnThreshHist.SetFillStyle(3001)
ratesOnThreshHist.Draw("HBAR")

canvasComapre.cd(2)
   
canvasComapre.cd(2).SetLeftMargin(0.4)
canvasComapre.cd(2).SetGridx()
canvasComapre.cd(2).SetGridy()
relativeRatesOnThreshHist.GetYaxis().SetRangeUser(0.5, 1)
relativeRatesOnThreshHist.GetYaxis().SetLabelSize(0.02)
relativeRatesOnThreshHist.SetFillColor(0)
relativeRatesOnThreshHist.SetFillStyle(3001)
relativeRatesOnThreshHist.Draw("HBAR")

outFile.cd()
ratesOnThreshHist.Write()
canvasComapre.Write()
#%jsroot on
#from ROOT import gROOT 
gROOT.GetListOfCanvases().Draw()

#outFile.Close()

input("Press ENTER to exit")

#execfile('ratePlots.py')
