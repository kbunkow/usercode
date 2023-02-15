/*
 * MuCorrelatorAnalyzerPlots2.cc
 *
 *  Created on: Nov 9, 2018
 *      Author: kbunkow
 */


#include "TROOT.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "TLegend.h"
#include "TEfficiency.h"
#include "THStack.h"


#include "PlottingTemplate-master/PlotTemplate.C"

#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <regex>

#include <sys/stat.h>

using namespace std;



void makeEfficiencyPlots(TDirectory* omtfTTAnalyzerDir, const char* nameLegend, string label, int color, int ptCut);
void makeCandidatesMatchingPlots(TDirectory* omtfTTAnalyzerDir, const char* nameLegend, double eventsCnt);
void makeEffVsBeta(TDirectory* omtfTTAnalyzerDir, const char* nameLegend);
void makeRatePlots(TDirectory* omtfTTAnalyzerDir, const char* nameLegend, int color, int ptCut);
TEfficiency* makeEfficiency(const TH1& passed, const TH1& total, std::string title, Color_t lineColor);

void makePlots(const char* name, string label, int color, int ptCut, const char* rootFileName);

int alogNumToCompare1 = 2; //1; //4;
int alogNumToCompare2 = 5;

float ptMaxRange = 50; //for the rate plots

TCanvas* canvasCompare = new TCanvas("canvasCompare", "canvasCompare", 1200, 800);
TLegend* legendCompare = new TLegend(0.5, 0.18, 0.88, 0.4);
int colorCompare =  2;

bool compareFirst = true;

double lhcFillingRatio = 2760./3564.;
double lhcFreq = 40144896; //11264 * 3564

double eventsCnt = 0;

bool rebinTurnOn = false; //TODO
bool rebinEtaEff = true; //TODO

int MuCorrelatorAnalyzerPlots2() {
  gStyle->SetOptStat(0);


  canvasCompare->Divide(2, 2);

  //leg->SetHeader("#left|#eta^{gen}#right| < 2.4, L1 p_{T} #geq 20 GeV"); //TODO change according to the plot
  //leg->SetBorderSize(0);
  //legendCompare->SetFillStyle(0);
  legendCompare->SetBorderSize(1);
  legendCompare->SetTextSize(0.03);
  legendCompare->SetMargin(0.2);

  canvasCompare->cd(1);
  canvasCompare->cd(1)->SetGridx();
  canvasCompare->cd(1)->SetGridy();

  canvasCompare->cd(2);
  canvasCompare->cd(2)->SetGridx();
  canvasCompare->cd(2)->SetGridy();

  //legendCompare->Draw();

  canvasCompare->cd(4);
  canvasCompare->cd(4)->SetGridx();
  canvasCompare->cd(4)->SetGridy();


  //canvasCompare->cd(2);
  //legendCompare->Draw();

  int ptCut = 1;

  //ptCut = 18+1;
  //ptCut = 1+1;
  //ptCut = 10 +1;

  ostringstream ostr;

  //makePlots("hscp",    kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_5_0_pre1/src/L1Trigger/L1TMuonBayes/test/muCorrelatorTTAnalysis1HSCP_100Files.root");
  //makePlots("hscp",    kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_5_0_pre1/src/L1Trigger/L1TMuonBayes/test/muCorrelatorTTAnalysis1HSCP.root");
  //makePlots("hscp CMSSW_10_5_0_pre1",    kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_5_0_pre1/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1HSCP_100FilesUpdatedCuts.root");

  //makePlots("hscp_noiRPC",    kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_5_0_pre1/src/L1Trigger/L1TMuonBayes/test/muCorrelatorTTAnalysis1HSCP_noiRPC.root");

  //makePlots("hscp CMSSW_10_6_0_pre4", "stau", kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_0_pre4/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1HSCP.root");


  //makePlots("singleMu",    kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_5_0_pre1/src/L1Trigger/L1TMuonBayes/test/muCorrelatorTTAnalysis1.root");

  //makePlots("singleNeutrinoPU200 without_iRPC",    kGreen,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_1_7/src/L1Trigger/L1TMuonBayes/test/crab/without_iRPC/crab_muCorr_MC_analysis_SingleNeutrino_PU200_600Files/results/muCorrelatorTTAnalysis1.root");
  //makePlots("singleNeutrinoPU300_noChi2DofCut",    kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_1_7/src/L1Trigger/L1TMuonBayes/test/crab/without_iRPC/crab_muCorr_MC_analysis_SingleNeutrinoPU300_noChi2DofCut/results/muCorrelatorTTAnalysis1.root");
  //makePlots("singleNeutrinoPU300",    kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_1_7/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrinoPU300/results/muCorrelatorTTAnalysis1.root");


  //makePlots("singleNeutrinoPU200 CMSSW_10_1_7",  kBlue,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_1_7/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200_600Files/results/muCorrelatorTTAnalysis1.root");

  //makePlots("singleNeutrinoPU300",  kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_1_7/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU300/results/muCorrelatorTTAnalysis1.root");

  //makePlots("singleNeutrinoPU200 CMSSW_10_6_0_pre4",  kBlue,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_0_pre4//src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200/results/muCorrelatorTTAnalysis1.root");

  //makePlots("singleNeutrinoPU300 CMSSW_10_6_0_pre4",  kBlue,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_0_pre4//src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200/results/muCorrelatorTTAnalysis1.root");


  //makePlots("SingleMu_PU200",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_1_7/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleMu_PU200/results/muCorrelatorTTAnalysis1.root");

  //makePlots("SingleMu_PU200 CMSSW_10_6_0_pre4",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_0_pre4/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleMu_PU200_v0/results/muCorrelatorTTAnalysis1.root");

  //makePlots("HToZZTo4L CMSSW_10_6_0_pre4 gb2Stub",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_0_pre4/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_HToZZTo4L_v0_gb2Stub/results/muCorrelatorTTAnalysis1.root");
  //makePlots("HToZZTo4L CMSSW_10_6_0_pre4 gb1Stub",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_0_pre4/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_HToZZTo4L_v-3_gb1Stub/results/muCorrelatorTTAnalysis1.root");

  //makePlots("SingleMu_PU200_without_iRPC",    kRed,   ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_1_7/src/L1Trigger/L1TMuonBayes/test/crab/without_iRPC/crab_muCorr_MC_analysis_SingleMu_PU200/results/muCorrelatorTTAnalysis1.root");

  //makePlots("GluGluHToZZTo4L_noPu",  "GluGluHToZZTo4L",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_GluGluHToZZTo4L_NoPU.root");

  //makePlots("singleMu500Ev",  "singleMu500Ev",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_singleMu.root");


  //makePlots("SingleNeutrino_PU200_t5", "singleNu",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200_v1_t5/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU200_t7", "singleNu", kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200_v1_t7/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU200_t9",  "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200_v1_t9/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU200_t10", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200_v1_t10/results/muCorrelatorTTAnalysis1.root");

  //makePlots("SingleNeutrino_PU200_mtd5_t11", "singleNu", kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200_mtd5_v1_t11/results/muCorrelatorTTAnalysis1.root");

  //makePlots("DYToLL_mtd5_t11_1",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_DYToLL_mtd5_v1_t11_1/results/muCorrelatorTTAnalysis1.root");


  //makePlots("TTTo2L2Nu_PU200_t6",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_TTTo2L2Nu_v1_t6/results/muCorrelatorTTAnalysis1.root");
  //makePlots("TTTo2L2Nu_PU200_t7_1", "tt #rightarrow ll#nu#nu",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_TTTo2L2Nu_v1_t7_1/results/muCorrelatorTTAnalysis1.root");
  //makePlots("DYToMuMuorEleEle",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_DYToMuMuorEleEle_v1_t6/results/muCorrelatorTTAnalysis1.root");
  //makePlots("DYToMuMuorEleEle_t18", "DY #rightarrow #mu#mu/ee",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_DYToMuMuorEleEle_v1_t18/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MuFlatPt_PU200_t6",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t6/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MuFlatPt_PU200_t7",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t7/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MuFlatPt_PU200_t9",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t9/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MuFlatPt_PU200_t10", "#mu 0-100 GeV",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t10/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_Pt0to100_PU200_t6", "J/#psi #rightarrow #mu#mu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_JPsiToMuMu_Pt0to100_PU200_v1_t6/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_Pt0to100_PU200_t9",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_JPsiToMuMu_Pt0to100_PU200_v1_t9/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_Pt0to100_PU200_t7_1", "J/#psi #rightarrow #mu#mu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_JPsiToMuMu_Pt0to100_PU200_v1_t7_1/results/muCorrelatorTTAnalysis1.root");
  //makePlots("TauTo3Mu_PU200_v1_t11", "#tau #rightarrow 3#mu",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_TauTo3Mu_PU200_v1_t11/results/muCorrelatorTTAnalysis1.root");
  //makePlots("BsToMuMu_PU200_v1_t11", "Bs #rightarrow #mu#mu",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_BsToMuMu_PU200_v1_t11/results/muCorrelatorTTAnalysis1.root");

  //makePlots("MuFlatPt_PU200_t21", "#mu 0-100 GeV",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t21/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MuFlatPt_PU200_t12", "#mu 0-100 GeV",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t12/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU200_t17", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200_v1_t17/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU140_t13", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU140_v1_t13/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU250_t13", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU250_v1_t13/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU300_t23", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU300_v1_t23/results/muCorrelatorTTAnalysis1.root");


  //makePlots("HSCPppstau_M_200_PU200_t21", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_HSCPppstau_M_200_PU200_v1_t21/results/muCorrelatorTTAnalysis1.root");
  //makePlots("HSCPppstau_M_871_PU200_t25", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_HSCPppstau_M_871_PU200_v1_t25/results/muCorrelatorTTAnalysis1.root");

  //makePlots("MuFlatPt_PU200_v1_t21_bayesOMTF_L1TkMuons", "#mu 0-100 GeV",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t21_bayesOMTF_L1TkMuons_v2_36_4/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MuFlatPt_PU200_v1_t15_bayesOMTFonly", "#mu 0-100 GeV",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t15_bayesOMTFonly/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MuFlatPt_PU200_v1_t17_bayesOMTFonly_L1TkMuonsTP", "#mu 0-100 GeV",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t17_bayesOMTFonly_L1TkMuonsTP/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MuFlatPt_PU200_v1_t17_bayesOMTFonly_L1TkMuonsTP_withPR807", "#mu 0-100 GeV",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t17_bayesOMTFonly_L1TkMuonsTP_withPR807/results/muCorrelatorTTAnalysis1.root");

  //makePlots("SingleNeutrino_PU140_v1_t19_bayesOMTF_L1TkMuons_v2_36_4", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU140_v1_t19_bayesOMTF_L1TkMuons_v2_36_4/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU250_v1_t19_bayesOMTF_L1TkMuons_v2_36_4", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU250_v1_t19_bayesOMTF_L1TkMuons_v2_36_4/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU200_v1_t19_bayesOMTF_L1TkMuons_v2_36_4", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU200_v1_t19_bayesOMTF_L1TkMuons_v2_36_4/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleNeutrino_PU300_v1_t23_bayesOMTF_L1TkMuons_v2_36_4", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_SingleNeutrino_PU300_v1_t23_bayesOMTF_L1TkMuons_v2_36_4/results/muCorrelatorTTAnalysis1.root");



  //>>makePlots("MuFlatPt_PU200_v1_t19_L1TkMuons_pr832", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_muCorr_MC_analysis_MuFlatPt_PU200_v1_t19_bayesOMTFonly_L1TkMuons_pr832/results/muCorrelatorTTAnalysis1.root");


  //makePlots("GluGluHToZZTo4L_NoPU gb4",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_GluGluHToZZTo4L_NoPU_gb4.root");
  //makePlots("singleMu_sigma_2p8",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_singleMu_sigma_2p8.root");
  //makePlots("singleMu_sigma_1p4",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_singleMu_sigma_1p4.root");

  //makePlots("HSCPppstau_M_200_NoPU",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_HSCPppstau_M_200_NoPU.root");
  //makePlots("JPsiToMuMu_Pt0to100_NoPU gb4",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_JPsiToMuMu_Pt0to100_NoPU_gb4.root");
  //makePlots("JPsiToMuMu_Pt0to100_NoPU",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_JPsiToMuMu_Pt0to100_NoPU.root");
  //makePlots("JPsiToMuMu_Pt0to100_NoPU",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_JPsiToMuMu_Pt0to100_NoPU_v1.root");

  //makePlots("JPsiToMuMu_Pt0to100_NoPU gb3",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_JPsiToMuMu_Pt0to100_NoPU_gb3.root");

  //makePlots("mtd5_BsToMuMu",    kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_mtd5_BsToMuMu_SoftQCDnonD_NoPU.root");

  //makePlots("HSCP",  "HSCP",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1HSCP.root");
  //makePlots("MuFlatPt_PU200_v1_t15_bayesOMTFonly", "#mu 0-100 GeV",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/muCorrelatorTTAnalysis1.root");
  //makePlots("HSCP",  "HSCP",  kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/muCorrelator/muCorrelatorTTAnalysis1_HSCPppstau_M_200_PU200.root");

  //makePlots("DoubleMuon_gun_test", "singleNu",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TkMuonBayes/test/expert/muCorrelatorTTAnalysis1.root");
  //makePlots("DoubleMuon_gun_test", "doubleMuon_gun",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_L1TkMuonBayes_MC_analysis_DoubleMuon_gun_FlatPt-1To100_NoPU_t112/results/muCorrelatorTTAnalysis1.root");
 //makePlots("DoubleMuon_gun_test", "doubleMuon_gun",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TkMuonBayes/test/expert/muCorrelatorTTAnalysis1_DoubleMuon_gun.root");
  //makePlots("DoubleMuon_gun_test", "doubleMuon_gun",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_L1TkMuonBayes_MC_analysis_DoubleMuon_gun_FlatPt-1To100_PU200_t112/results/muCorrelatorTTAnalysis1.root");
  //makePlots("minBias_PU200_t112", "minBias PU200",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_L1TkMuonBayes_MC_analysis_MinBias_Summer20_PU200_t112/results/muCorrelatorTTAnalysis1.root");
  //makePlots("DoubleMuon_gun_test", "Summer20",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_L1TkMuonBayes_MC_analysis_DoubleMuon_gun_Summer20_PU200_t112/results/muCorrelatorTTAnalysis1.root");
  //makePlots("DYToLL_t114", "Summer20",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_L1TkMuonBayes_MC_analysis_DYToLL_M-50_Summer20_PU200_t114/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_t113", "Summer20",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_L1TkMuonBayes_MC_analysis_JPsiToMuMu_Summer20_PU200_t113/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_t114", "JPsiToMuMu PU200 t114 L1TkMuonBayes",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_L1TkMuonBayes_MC_analysis_JPsiToMuMu_Summer20_PU200_t114/results/muCorrelatorTTAnalysis1.root");
  //makePlots("minBias_PU200_t114", "minBias PU200",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_L1TkMuonBayes_MC_analysis_MinBias_Summer20_PU200_t114/results/muCorrelatorTTAnalysis1.root");

  //makePlots("DYToLL", "DYToLL",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/L1Trigger/Phase2L1GMT/test/muCorrelatorTTAnalysis1_Test.root");

  //makePlots("DYToLL_PU200_t200", "DYToLL PU200 t200",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_DYToLL_M-50_Summer20_PU200_t200/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_PU200_t200", "JPsiToMuMu PU200 t200",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org__MC_analysis_JPsiToMuMu_Summer20_PU200_t200/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MinBias_PU200_t200", "MinBias PU200 t200",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_MinBias_Summer20_PU200_t200/results/muCorrelatorTTAnalysis1.root");

  //makePlots("DYToLL_PU200_t201", "DYToLL PU200 t201",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_DYToLL_M-50_Summer20_PU200_t201/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_PU200_t201", "JPsiToMuMu PU200 t201",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org__MC_analysis_JPsiToMuMu_Summer20_PU200_t201/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MinBias_PU200_t201", "MinBias PU200 t201",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_MinBias_Summer20_PU200_t201/results/muCorrelatorTTAnalysis1.root");

  //makePlots("DYToLL_PU200_t202", "DYToLL PU200 t202",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_DYToLL_M-50_Summer20_PU200_t202/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_PU200_t202", "JPsiToMuMu PU200 t202",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org__MC_analysis_JPsiToMuMu_Summer20_PU200_t202/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MinBias_PU200_t202", "MinBias PU200 t202",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_MinBias_Summer20_PU200_t202/results/muCorrelatorTTAnalysis1.root");
  //makePlots("TauTo3Mu_PU200_t202", "TauTo3Mu PU200 t202",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/orginal_gmt/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_MC_analysis_TauTo3Mu_Summer20_PU200_withNewMB_t202/results/muCorrelatorTTAnalysis1.root");

  //makePlots("DYToLL_PU200_t203", "DYToLL PU200 t203",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_DYToLL_M-50_Summer20_PU200_t202/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_PU200_t203", "JPsiToMuMu PU200 t203",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org__MC_analysis_JPsiToMuMu_Summer20_PU200_t203/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MinBias_PU200_t203", "MinBias PU200 t203",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_MinBias_Summer20_PU200_t202/results/muCorrelatorTTAnalysis1.root");

  //makePlots("DYToLL_PU200_t204", "DYToLL PU200 t204",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_DYToLL_M-50_Summer20_PU200_t204/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_PU200_t204", "JPsiToMuMu PU200 t204",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org__MC_analysis_JPsiToMuMu_Summer20_PU200_t204/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MinBias_PU200_t204", "MinBias PU200 t204",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_MinBias_Summer20_PU200_t204/results/muCorrelatorTTAnalysis1.root");

  //makePlots("DYToLL_PU200_t205", "DYToLL PU200 t205",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_DYToLL_M-50_Summer20_PU200_t205/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_PU200_t205", "JPsiToMuMu PU200 t205",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org__MC_analysis_JPsiToMuMu_Summer20_PU200_t205/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MinBias_PU200_t205", "MinBias PU200 t205",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_MinBias_Summer20_PU200_t205/results/muCorrelatorTTAnalysis1.root");

  //makePlots("TauTo3Mu_PU140_t206", "TauTo3Mu PU200 t206",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_MC_analysis_TauTo3Mu_Summer20_PU140_withNewMB_t206/results/muCorrelatorTTAnalysis1.root");
  //makePlots("TauTo3Mu_PU200_t206", "TauTo3Mu PU200 t206",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_MC_analysis_TauTo3Mu_Summer20_PU200_withNewMB_t206/results/muCorrelatorTTAnalysis1.root");

  //makePlots("DYToLL_PU200_t207", "DYToLL PU200 t207",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org_MC_analysis_DYToLL_M-50_Summer20_PU200_t207/results/muCorrelatorTTAnalysis1.root");
  //makePlots("JPsiToMuMu_PU200_t207", "JPsiToMuMu PU200 t207",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_org__MC_analysis_JPsiToMuMu_Summer20_PU200_t207/results/muCorrelatorTTAnalysis1.root");
  //makePlots("MinBias_PU200_t207", "MinBias PU200 t207",   kRed,       ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_MC_analysis_MinBias_Summer20_PU200_t207/results/muCorrelatorTTAnalysis1.root");
  //makePlots("TauTo3Mu_PU200_t207", "TauTo3Mu PU200 t207",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/usercode/MuCorrelatorAnalyzer/crab/crab_Phase2L1GMT_MC_analysis_TauTo3Mu_Summer20_PU200_withNewMB_t207/results/muCorrelatorTTAnalysis1.root");
  //makePlots("SingleMu_OneOverPt_pilot", "SingleMu_OneOverPt_pilot",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_12_x_x_l1tOfflinePhase2/CMSSW_12_3_0_pre4/src/usercode/MuCorrelatorAnalyzer/crab/muCorrelatorTTAnalysis1_sample2023_pilot.root");

  makePlots("sample_14_02_2023_2", "sample_14_02_2023_2",   kRed, ptCut,  "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_12_x_x_official/CMSSW_12_6_3/src/usercode/MuCorrelatorAnalyzer/crab/muCorrelatorTTAnalysis1_sample_14_02_2023_2.root");


/*
  c0->cd();
  legend->Draw();
  c1->cd();
  legend->Draw();
*/
  canvasCompare->cd(2);
  legendCompare->Draw();

  return 0;

}

string plotsDir = "";

void makePlots(const char* name, string label, int color, int ptCut, const char* rootFileName) {

  TFile* file = new TFile(rootFileName);
  file->ls();

  TDirectory* omtfTTAnalyzerDir = file;
  file->cd("muCorrelatorAnalyzer");
  file->ls();

  omtfTTAnalyzerDir = (TDirectory*)file->Get("muCorrelatorAnalyzer"); //omtfTTAnalyzer

  TH1D* gpPerEvent = (TH1D*)omtfTTAnalyzerDir->Get("gpPerEvent");
  eventsCnt = gpPerEvent->GetEntries();

  plotsDir = string("plots_") + name;
  mkdir( plotsDir.c_str(), 0777);

  //makeEffVsBeta(omtfTTAnalyzerDir, name);

  //makeCandidatesMatchingPlots(omtfTTAnalyzerDir, name, eventsCnt);

  makeEfficiencyPlots(omtfTTAnalyzerDir, name, label, color, ptCut);

  //makeEfficiencyPlots(omtfTTAnalyzerDir, name, label, color, 2);
  //makeEfficiencyPlots(omtfTTAnalyzerDir, name, label, color, 10);
  //makeEfficiencyPlots(omtfTTAnalyzerDir, name, label, color, 20);

  //makeRatePlots(omtfTTAnalyzerDir, name, color, ptCut);
}

void savePlot(string name, TVirtualPad* orgianlPad) {
  if(name.find("SingleMuAlgo20") == string::npos &&
     name.find("RateAnalyzer_HscpAlgoSoftCuts20") == string::npos &&
     name.find("SingleMuAlgo5") == string::npos
     )
    return;

  orgianlPad->SaveAs("test.png");
  TVirtualPad* padCopy = (TVirtualPad*)orgianlPad->Clone((orgianlPad->GetName() + string("_copy")).c_str());
  //padCopy = orgianlPad;
  TCanvas* canvas = CreateCanvas(name, false, true);
  canvas->cd();
  //padCopy->SetBorderSize(3);

  padCopy->SetPad(0,0,1,1);
  TPaveText* titlePave = dynamic_cast<TPaveText*>(padCopy->FindObject("title"));
  if(titlePave)
    titlePave->SetTextColor(kWhite);
  padCopy->Draw();

/*
  padCopy->ls();
  cout<<"orgianlPad->FindObject(efficiency)  "<<orgianlPad->FindObject("efficiency")<<endl;
  TEfficiency* orgGraph = dynamic_cast<TEfficiency*> (orgianlPad->FindObject("efficiency") );
  if( orgGraph) {
    cout<<"eeeeeeeee"<<endl;
    TEfficiency* copyGraph = dynamic_cast<TEfficiency*> (padCopy->FindObject("efficiency") );
    copyGraph->GetPaintedGraph()->GetXaxis()->SetRange(orgGraph->GetPaintedGraph()->GetXaxis()->GetFirst(), orgGraph->GetPaintedGraph()->GetXaxis()->GetLast());
    copyGraph->GetPaintedGraph()->GetYaxis()->SetRange(orgGraph->GetPaintedGraph()->GetYaxis()->GetFirst(), orgGraph->GetPaintedGraph()->GetYaxis()->GetLast());
  }
*/

  //DrawPrelimLabel(canvas);
  //DrawLumiLabel(canvas, Lumi);
  DrawCmsSimulationLabel(padCopy);
  DrawPuLabel(padCopy);

  SaveCanvas(canvas, plotsDir, name);
  cout<<__FUNCTION__<<":"<<__LINE__<<endl;

  canvas->Close();
}

TH1D* makeAbs(TH1D* orgHist) {
  TH1D* absHist = new TH1D( (orgHist->GetName() + string("_abs")).c_str(), orgHist->GetTitle(), orgHist->GetNbinsX()/2., 0, orgHist->GetXaxis()->GetXmax());
  for(unsigned int iBin = 0; iBin <= orgHist->GetNbinsX(); iBin++) {
    absHist->Fill( fabs( orgHist->GetBinCenter(iBin)), orgHist->GetBinContent(iBin));
  }

  absHist->Sumw2(false);
  return absHist;
}

void makeEffVsBeta(TDirectory* omtfTTAnalyzerDir, const char* nameLegend) {
  string canvasName = string("canvas_") + nameLegend + string("_beta");
  TCanvas* canvasBetaPlost = new TCanvas(canvasName.c_str(), canvasName.c_str(), 1200, 800);
  canvasBetaPlost->cd();
  canvasBetaPlost->Divide(2, 2);
  canvasBetaPlost->cd(1);
  canvasBetaPlost->cd(1)->SetGridx();
  canvasBetaPlost->cd(1)->SetGridy();
  TLegend* legend = new TLegend(0.3,0.3,0.9,0.6);

  TIter next(omtfTTAnalyzerDir->GetListOfKeys());
  TKey* key;
  bool first = true;
  int color = 1;

  TH1D* l1MuVsBetaGenSingleMu = nullptr;

  string singleMuAlgoName = "EfficiencyAnalyser_SingleMuAlgo20_ptGenFrom_25_ptGenTo_10000";

  while ((key = (TKey*)next())) {
    if (key->IsFolder()) {
      omtfTTAnalyzerDir->cd(key->GetName());
      string dirName = key->GetName();
      if(dirName.find("EfficiencyAnalyser_") != string::npos) {
        TDirectory* subdir = gDirectory;
        cout<<"making beta  plots for "<<dirName<<" color "<<color<<endl;

        TH2I* betaGenBetaL1Mu = (TH2I*)subdir->Get("betaGenBetaL1Mu");

        int bin0 = betaGenBetaL1Mu->GetYaxis()->FindBin(0.);
        TH1* l1MuVsBetaGen = betaGenBetaL1Mu->ProjectionX( ( string("l1MuVsBetaGen_") + to_string(color) ).c_str(), bin0, -1);
        TH1* allVsBetaGen = betaGenBetaL1Mu->ProjectionX("allVsBetaGen", -1, -1);

        if(dirName == singleMuAlgoName) {
          l1MuVsBetaGenSingleMu = (TH1D*)l1MuVsBetaGen->Clone("l1MuVsBetaGenSingleMu");
        }

        l1MuVsBetaGen->Sumw2(false);
        allVsBetaGen->Sumw2(false);
        std::string title = ("HSCP efficiency; generated #beta; efficiency");
        TEfficiency* effVsBeta = makeEfficiency(*l1MuVsBetaGen, *allVsBetaGen, title, color);

        canvasBetaPlost->cd(1);

        if(first) {
          effVsBeta->Draw("APZ");
          canvasBetaPlost->cd(1)->Update();
        }
        else {
          effVsBeta->Draw("same PZ");
          canvasBetaPlost->cd(1)->Update();
        }

        string fileName1 = (plotsDir + "/" + dirName + "_" + effVsBeta->GetName()  + "_algoEff_"+ string(".root"));
        effVsBeta->SaveAs(fileName1.c_str() );

        cout<<"l1MuVsBetaGen->GetName() "<<l1MuVsBetaGen->GetName()<<endl;

        legend->AddEntry(effVsBeta, dirName.erase(0, 19).c_str());

        first = false;
        color++;
        if(color == 5 || color == 10)
          color++;
      }
    }
  }

  if(l1MuVsBetaGenSingleMu == nullptr) {
    cout<<"l1MuVsBetaGenSingleMu == nullptr"<<endl;
  }

  canvasBetaPlost->cd(2);
  legend->Draw();

  canvasBetaPlost->cd(3)->SetGridx();
  canvasBetaPlost->cd(3)->SetGridy();
  first = true;
  next.Reset();
  color = 1;

  while ((key = (TKey*)next())) {
    if (key->IsFolder()) {
      omtfTTAnalyzerDir->cd(key->GetName());
      string dirName = key->GetName();
      if(dirName.find("EfficiencyAnalyser_") != string::npos) {
        TDirectory* subdir = gDirectory;
        cout<<"making sum beta  plots for "<<dirName<<endl;

        TH2I* betaGenBetaL1Mu = (TH2I*)subdir->Get("betaGenBetaL1Mu");

        int bin0 = betaGenBetaL1Mu->GetYaxis()->FindBin(0.);
        TH1D* l1MuVsBetaGen = betaGenBetaL1Mu->ProjectionX("l1MuVsBetaGen2", bin0, -1);
        TH1D* allVsBetaGen = betaGenBetaL1Mu->ProjectionX("allVsBetaGen2", -1, -1);

        if(dirName.find("Hscp")  != string::npos ) {
          cout<<"dirName "<<dirName<<endl;
          TH1D* l1MuVsBetaGenSum = (TH1D*)l1MuVsBetaGen->Clone("l1MuVsBetaGenSum");
          TH1D* allVsBetaGenSum = (TH1D*)allVsBetaGen->Clone("allVsBetaGenSum");

          l1MuVsBetaGenSum->Add(l1MuVsBetaGenSingleMu);

          l1MuVsBetaGenSum->Sumw2(false);
          allVsBetaGenSum->Sumw2(false);

          l1MuVsBetaGenSum->SetLineColor(color);
          allVsBetaGenSum->SetLineColor(color);
          allVsBetaGenSum->SetFillColor(color);

          std::string title = ("HSCP efficiency; generated #beta; efficiency");
          TEfficiency* effVsBeta = makeEfficiency(*l1MuVsBetaGenSum, *allVsBetaGenSum, title, color);

          canvasBetaPlost->cd(3);

          if(first) {
            effVsBeta->Draw("APZ");
          }
          else {
            effVsBeta->Draw("same PZ");
          }
          canvasBetaPlost->cd(3)->Update();

          string fileName1 = (plotsDir + "/" + dirName + "_" + effVsBeta->GetName()  + "_totalEff_"+ string(".root"));
          effVsBeta->SaveAs(fileName1.c_str() );

          first = false;

          /*if(color == 7) {
            canvasCompare->cd(3);
            if(compareFirst)
              l1MuVsBetaGenSum->Draw("hist");
            else
              l1MuVsBetaGenSum->Draw("histsame");
          }*/

        }

        color++;
        if(color == 5 || color == 10)
          color++;
      }
    }
  }
}


TEfficiency* makeEfficiency(const TH1& passed, const TH1& total, std::string title, Color_t lineColor) {
  if(TEfficiency::CheckConsistency(passed, total) ) {
    TEfficiency* efficiency = new TEfficiency(passed, total);
    //title = std::regex_replace(title, std::regex("\\muCandGenEtaMuons"), "tagging efficiency");
    efficiency->SetTitle( (title).c_str());
    efficiency->SetStatisticOption(TEfficiency::EStatOption::kBUniform );
    efficiency->SetPosteriorMode();
    efficiency->SetLineColor(lineColor);
    return efficiency;
  }
  else  {
    std::cout<<"line "<<__LINE__<<"TEfficiency::CheckConsistency(*ptGenPtTTMuonNom, *ptGenPtTTMuonDenom) failed"<<std::endl;
    exit(1);
  }
  return nullptr;
}



void makeEfficiencyPlots(TDirectory* omtfTTAnalyzerDir, const char* nameLegend, string label, int color, int ptCut)
{
  string canvasName = string("canvas_") + nameLegend + string("_controlPlost");
  TCanvas* canvasControlPlost = new TCanvas(canvasName.c_str(), canvasName.c_str(), 1200, 800);
  canvasControlPlost->Divide(2, 2);
  canvasControlPlost->SetGrid();

  TH1* ttTracksPt  = (TH1*)omtfTTAnalyzerDir->Get("ttTracksPt");
  TH1D* gpMuonPt   = (TH1D*)(omtfTTAnalyzerDir->Get("gpMuonPt"));
  TH1D* gpMuonEta  = (TH1D*)omtfTTAnalyzerDir->Get("gpMuonEta");
  //TH1D* gpMuonEta_ptGen20GeV  = (TH1D*)omtfTTAnalyzerDir->Get("gpMuonEta_ptGen20GeV");
  TH1D* gpMuonPhi  = (TH1D*)omtfTTAnalyzerDir->Get("gpMuonPhi");

  TH1D* ttMuonPt  = (TH1D*)omtfTTAnalyzerDir->Get("ttMuonPt");
  TH1D* ttMuonEta = (TH1D*)omtfTTAnalyzerDir->Get("ttMuonEta");
  //TH1D* ttMuonEta_ptGen20GeV_ptTT18Gev = (TH1D*)omtfTTAnalyzerDir->Get("ttMuonEta_ptGen20GeV_ptTT18Gev");
  TH1D* ttMuonPhi = (TH1D*)omtfTTAnalyzerDir->Get("ttMuonPhi");

  //#####################################################################################
  canvasControlPlost->cd(1);
  canvasControlPlost->cd(1)->SetLogy();

  TLegend* legend1 = new TLegend(0.55, 0.5,0.95,0.85);
  //leg->SetHeader("#left|#eta^{gen}#right| < 2.4, L1 p_{T} #geq 20 GeV"); //TODO change according to the plot
  //leg->SetBorderSize(0);
  legend1->SetFillStyle(0);
  legend1->SetBorderSize(0);
  legend1->SetTextSize(0.03);
  legend1->SetMargin(0.2);

  ttTracksPt->SetLineColor(kBlack);
  ttTracksPt->Draw("hist");

  gpMuonPt->SetLineColor(kBlue);
  gpMuonPt->Draw("histsame");

  ttMuonPt->SetLineColor(kRed);
  ttMuonPt->Draw("histsame");

  gpMuonPt->GetXaxis()->SetRangeUser(0, ptMaxRange);

  legend1->AddEntry(ttTracksPt , "ttTracksPt", "lep");
  legend1->AddEntry(gpMuonPt , "gpMuonPt", "lep");
  legend1->AddEntry(ttMuonPt , "ttMuonPt", "lep");
  legend1->Draw();
  //---------------------------------------------------------------------

  canvasControlPlost->cd(2);
  canvasControlPlost->cd(2)->SetLogy();

  cout<<"eventsCnt: "<<eventsCnt<<endl;

  TH1D* gpPerEvent = (TH1D*)omtfTTAnalyzerDir->Get("gpPerEvent");
  gpPerEvent->Draw("hist");

  //////////////////////////////////////////////////
  canvasControlPlost->cd(3);
  TH2F* ttTrackEta_Pt = (TH2F*)omtfTTAnalyzerDir->Get("ttTrackEta_Pt");
  TH2F* ttMuonEta_Pt = (TH2F*)omtfTTAnalyzerDir->Get("ttMuonEta_Pt");
  ttMuonEta_Pt->Divide(ttTrackEta_Pt);
  ttMuonEta_Pt->SetTitle("ttMuonEta_Pt / ttTrackEta_Pt");
  ttMuonEta_Pt->Draw("colz");

  //_######################################################################################################

//*************************************************** efficiency ********************************************
  //tracking trigger efficiency, reference for all algos

  TH2I* ptGenPtTTMuonEv0= (TH2I*)omtfTTAnalyzerDir->Get("ptGenPtTTMuonEv0");

  TH1* ptGenPtTTMuonNomEv0 = ptGenPtTTMuonEv0->ProjectionX("ptGenPtTTMuonNomEv0", ptGenPtTTMuonEv0->GetYaxis()->FindBin(ptCut), -1);
  TH1* ptGenPtTTMuonDenomEv0 = ptGenPtTTMuonEv0->ProjectionX("ptGenPtTTMuonDenomEv0", 0, -1);

  int binNum = ptGenPtTTMuonEv0->GetYaxis()->FindBin(ptCut);
  cout<<"ptGenPtTTMuonEv0 FindBin("<<ptCut<<") = "<<binNum<<" GetBinLowEdge "<<ptGenPtTTMuonEv0->GetYaxis()->GetBinLowEdge(binNum)<<"  "<<ptGenPtTTMuonEv0->GetYaxis()->GetBinUpEdge(binNum)<<endl;
/*  ptGenPtTTMuonNomEv0->SetTitle( ("ttTrack efficiency, Event 0, pT cut = " + to_string(ptCut -1) + " GeV").c_str() );
  ptGenPtTTMuonNomEv0->Divide(ptGenPtTTMuonDenomEv0);
  ptGenPtTTMuonNomEv0->GetYaxis()->SetTitle("efficiency");
  ptGenPtTTMuonNomEv0->SetLineColor(kBlue);*/

  if(rebinTurnOn) {
    ptGenPtTTMuonNomEv0 = ptGenPtTTMuonNomEv0->Rebin(2, (string(ptGenPtTTMuonNomEv0->GetName() )+ "_rebin2").c_str() );
    ptGenPtTTMuonDenomEv0 = ptGenPtTTMuonDenomEv0->Rebin(2, (string(ptGenPtTTMuonDenomEv0->GetName() )+ "_rebin2").c_str() );
  }

  std::string title = ("ttTrack efficiency, Event 0, pT cut = " + to_string(ptCut) + " GeV" + "; generated p_{T} [GeV]; efficiency");
  TEfficiency* ttMuon_vs_ptGen_Ev0_Eff = makeEfficiency(*ptGenPtTTMuonNomEv0, *ptGenPtTTMuonDenomEv0, title, kBlue);
  ttMuon_vs_ptGen_Ev0_Eff->SetName("efficiency");

  TH2I* ptGenPtTTMuonEvPu= (TH2I*)omtfTTAnalyzerDir->Get("ptGenPtTTMuonEvPu");

  TH1D* ptGenPtTTMuonNomEvPu = ptGenPtTTMuonEvPu->ProjectionX("ptGenPtTTMuonNomEvPu", ptGenPtTTMuonEvPu->GetYaxis()->FindBin(ptCut), -1);
  TH1D* ptGenPtTTMuonDenomEvPu = ptGenPtTTMuonEvPu->ProjectionX("ptGenPtTTMuonDenomEvPu", 0, -1);

  ptGenPtTTMuonNomEvPu->SetTitle( ("ttTrack efficiency, PU Events, pT cut = " + to_string(ptCut) + " GeV").c_str() );
  ptGenPtTTMuonNomEvPu->Divide(ptGenPtTTMuonDenomEvPu);
  ptGenPtTTMuonNomEvPu->GetYaxis()->SetTitle("efficiency");
  ptGenPtTTMuonNomEvPu->SetLineColor(kBlue);


  TH1D* ttMuonEtaEff = (TH1D*)ttMuonEta->Clone("ttMuonEtaEff");
  ttMuonEtaEff->Divide(gpMuonEta);

  //TDirectory* currentDir = gDirectory;
  TIter next(omtfTTAnalyzerDir->GetListOfKeys());
  TKey* key;
  int algoNum = 0;
  colorCompare++;
  if(colorCompare == 4)
    colorCompare+=2;

  while ((key = (TKey*)next())) {
    if (key->IsFolder()) {
      omtfTTAnalyzerDir->cd(key->GetName());
      string dirName = key->GetName();

      if(dirName.find("EfficiencyAnalyser_") != string::npos) {
        algoNum++;

        TDirectory* subdir = gDirectory;
        cout<<"making plots for "<<dirName<<endl;
        canvasName = string("canvas_") + nameLegend + "_" + dirName;
        TCanvas* canvas1Eff = new TCanvas(canvasName.c_str(), canvasName.c_str(), 1500, 1200);
        canvas1Eff->Divide(2, 2);

        canvas1Eff->cd(1);
        canvas1Eff->cd(1)->SetGridx();
        canvas1Eff->cd(1)->SetGridy();


        canvas1Eff->cd(1)->Update();


        canvas1Eff->Update();

        //--------------------------------------------

        canvas1Eff->cd(2);
        canvas1Eff->cd(2)->SetGridx();
        canvas1Eff->cd(2)->SetGridy();
        canvas1Eff->cd(2)->SetLeftMargin(0.12);
        ttMuon_vs_ptGen_Ev0_Eff->SetMarkerStyle(22);
        ttMuon_vs_ptGen_Ev0_Eff->SetMarkerColor(kBlue);
        ttMuon_vs_ptGen_Ev0_Eff->SetMarkerSize(0.8);

        ttMuon_vs_ptGen_Ev0_Eff->Draw("APZ");
        canvas1Eff->cd(2)->Update();
        ttMuon_vs_ptGen_Ev0_Eff->GetPaintedGraph()->GetYaxis()->SetRangeUser(0.8, 1.01);
        ttMuon_vs_ptGen_Ev0_Eff->GetPaintedGraph()->GetXaxis()->SetRangeUser(0, 100);
        cout<<"ttMuon_vs_ptGen_Ev0_Eff->GetPaintedGraph()->GetName() "<<ttMuon_vs_ptGen_Ev0_Eff->GetPaintedGraph()->GetName()<<endl;
        canvas1Eff->cd(2)->Update();
        TH2I* ptGenPtMuCandMuonsEv0 = (TH2I*)subdir->Get("ptGenPtMuCandMuonsEv0;1");

        TH1* ptGenPtMuCandMuonsEv0Nom = ptGenPtMuCandMuonsEv0->ProjectionX("ptGenPtMuCandMuonsEv0Nom", ptGenPtMuCandMuonsEv0->GetYaxis()->FindBin(ptCut), -1);
        TH1* ptGenPtMuCandMuonsEv0Denom = ptGenPtMuCandMuonsEv0->ProjectionX("ptGenPtMuCandMuonsEv0Denom", 0, -1);

        if(rebinTurnOn) {
          ptGenPtMuCandMuonsEv0Nom = ptGenPtMuCandMuonsEv0Nom->Rebin(2, (string(ptGenPtMuCandMuonsEv0Nom->GetName() ) + " "+ nameLegend + "_rebin2").c_str() );
          ptGenPtMuCandMuonsEv0Denom = ptGenPtMuCandMuonsEv0Denom->Rebin(2, (string(ptGenPtMuCandMuonsEv0Denom->GetName() ) + " "+ nameLegend + "_rebin2").c_str() );
        }

        //ptGenPtOMtfMuonNom->Divide(ptGenPtOMtfMuonDenom); //TODO!!!! in principle ptGenPtOMtfMuonDenom and ptGenPtTTMuonDenom should be the same
/*
        ptGenPtMuCandMuonsEv0Nom->Divide(ptGenPtTTMuonDenomEv0);
        ptGenPtMuCandMuonsEv0Nom->SetTitle( ("ttTrack and OMTF efficiency, Event 0, pT cut = " + to_string(ptCut -1 ) + " GeV").c_str() );
        ptGenPtMuCandMuonsEv0Nom->SetLineColor(kRed);
        ptGenPtMuCandMuonsEv0Nom->Draw("samehist");
*/

        title = ("muCand efficiency, Event 0, pT cut = " + to_string(ptCut) + " GeV" + "; generated p_{T} [GeV]; efficiency");
        TEfficiency* muCand_vs_ptGen_Ev0_Eff = makeEfficiency(*ptGenPtMuCandMuonsEv0Nom, *ptGenPtMuCandMuonsEv0Denom, title, kRed);

        muCand_vs_ptGen_Ev0_Eff->SetMarkerStyle(23);
        muCand_vs_ptGen_Ev0_Eff->SetMarkerSize(0.7);
        muCand_vs_ptGen_Ev0_Eff->SetMarkerColor(colorCompare);
        muCand_vs_ptGen_Ev0_Eff->SetLineColor(colorCompare);
        muCand_vs_ptGen_Ev0_Eff->Draw("same PZ");

        //DrawLabel(canvas1Eff->cd(2), label);

        {
          TLegend* leg = new TLegend(0.33, 0.13,0.77,0.38);
          //leg->SetHeader("#left|#eta^{gen}#right| < 2.4, L1 p_{T} #geq 20 GeV"); //TODO change according to the plot
          //leg->SetBorderSize(0);
          leg->SetFillStyle(0);
          leg->SetBorderSize(0);
          leg->SetTextSize(0.03);
          leg->SetMargin(0.2);

          leg->AddEntry(ttMuon_vs_ptGen_Ev0_Eff , "Tracking Trigger Track", "lep");
          leg->AddEntry(muCand_vs_ptGen_Ev0_Eff , "Track + Stubs", "lep");

          leg->Draw("same");
        }

        canvasCompare->cd(2);

        if( (algoNum == alogNumToCompare1) && compareFirst)  {
          ttMuon_vs_ptGen_Ev0_Eff->Draw("APZ");
          legendCompare->AddEntry(ttMuon_vs_ptGen_Ev0_Eff , "Tracking Trigger Track", "lep");
        }

        if(algoNum == alogNumToCompare1 || algoNum == alogNumToCompare2)
        {
          //muCand_vs_ptGen_Ev0_Eff->SetMarkerColor(colorCompare);
          muCand_vs_ptGen_Ev0_Eff->Draw("same PZ");
          legendCompare->AddEntry(muCand_vs_ptGen_Ev0_Eff , (string("Track + Stubs ") + label).c_str(), "lep");
          //colorCompare++;
        }

        savePlot(canvasName + "_effVsPt_ttTrack_and_corr", canvas1Eff->cd(2) );

        //-----------------------------------------------------------------------------------------------------------
        canvas1Eff->cd(1);
        canvas1Eff->cd(1)->SetGridx();
        canvas1Eff->cd(1)->SetGridy();

        ptGenPtTTMuonNomEvPu->Draw("hist");


        TH2I* ptGenPtMuCandMuonsPu = (TH2I*)subdir->Get("ptGenPtMuCandMuonsPu;1");
        TH1D* ptGenPtMuCandMuonsPuNom = ptGenPtMuCandMuonsPu->ProjectionX("ptGenPtMuCandMuonsPuNom", ptGenPtMuCandMuonsPu->GetYaxis()->FindBin(ptCut), -1);
        TH1D* ptGenPtMuCandMuonsPuDenom = ptGenPtMuCandMuonsPu->ProjectionX("ptGenPtMuCandMuonsPuDenom", 0, -1);

        //ptGenPtOMtfMuonNom->Divide(ptGenPtOMtfMuonDenom); //TODO!!!! in principle ptGenPtOMtfMuonDenom and ptGenPtTTMuonDenom should be the same
        ptGenPtMuCandMuonsPuNom->Divide(ptGenPtMuCandMuonsPuDenom);
        ptGenPtMuCandMuonsPuNom->SetTitle( ("ttTrack and OMTF efficiency, PU Events, pT cut = " + to_string(ptCut) + " GeV").c_str() );
        ptGenPtMuCandMuonsPuNom->SetLineColor(kRed);
        ptGenPtMuCandMuonsPuNom->Draw("samehist");

        //--------------------------------
        canvas1Eff->cd(3);
        canvas1Eff->cd(3)->SetGridx();
        canvas1Eff->cd(3)->SetGridy();

        std::string region = "Endcap";
        TH2I* ptGenPtMuCandMuonsEv0Overlap = (TH2I*)subdir->Get( ("ptGenPtMuCandMuonsEv0" + region + ";1").c_str() );
        TH1* ptGenPtMuCandMuonsEv0OverlapNom = ptGenPtMuCandMuonsEv0Overlap->ProjectionX(("ptGenPtMuCandMuonsEv0" + region + "Nom").c_str(), ptGenPtMuCandMuonsEv0Overlap->GetYaxis()->FindBin(ptCut), -1);
        TH1* ptGenPtMuCandMuonsEv0OverlapDenom = ptGenPtMuCandMuonsEv0Overlap->ProjectionX(("ptGenPtMuCandMuonsEv0" + region + "pDenom").c_str(), 0, -1);

        if(rebinTurnOn) {
          ptGenPtMuCandMuonsEv0OverlapNom = ptGenPtMuCandMuonsEv0OverlapNom->Rebin(2, (string(ptGenPtMuCandMuonsEv0OverlapNom->GetName() )+ "_rebin2").c_str() );
          ptGenPtMuCandMuonsEv0OverlapDenom = ptGenPtMuCandMuonsEv0OverlapDenom->Rebin(2, (string(ptGenPtMuCandMuonsEv0OverlapDenom->GetName() )+ "_rebin2").c_str() );
        }

        title = ("muCand efficiency " + region + " region, Event 0, pT cut = " + to_string(ptCut) + " GeV" + "; generated p_{T} [GeV]; efficiency");
        TEfficiency* muCandEv0Overlap_EffVsPtGen = makeEfficiency(*ptGenPtMuCandMuonsEv0OverlapNom, *ptGenPtMuCandMuonsEv0OverlapDenom, title, kRed);

        muCandEv0Overlap_EffVsPtGen->SetMarkerStyle(23);
        muCandEv0Overlap_EffVsPtGen->SetMarkerSize(0.7);
        muCandEv0Overlap_EffVsPtGen->SetMarkerColor(colorCompare);
        muCandEv0Overlap_EffVsPtGen->SetLineColor(colorCompare);
        muCandEv0Overlap_EffVsPtGen->Draw("same PZ");

        DrawLabel(canvas1Eff->cd(3), label);
        savePlot(canvasName + "_effVsPt", canvas1Eff->cd(3) );


        string fileName1 = (plotsDir + "/" + dirName + "_" + muCandEv0Overlap_EffVsPtGen->GetName() + "_ptCut_" + to_string(ptCut) + string(".root"));
        cout<<"saving hist as "<<fileName1<<endl;
        muCandEv0Overlap_EffVsPtGen->SaveAs(fileName1.c_str() );

        if(algoNum == alogNumToCompare1 || algoNum == alogNumToCompare2)
        {
          canvasCompare->cd(1);
          if(compareFirst)
            muCandEv0Overlap_EffVsPtGen->Draw("APZ");
          else
            muCandEv0Overlap_EffVsPtGen->Draw("same PZ");
        }

        //--------------------------------

        double meanEff = 0;
        int binCnt = 0; //TODO

        TH1* gpMuonGenEtaMuons_withPtCuts = (TH1D*)subdir->Get("gpMuonGenEtaMuons_withPtCuts;1");
        TH1* ttMuonGenEtaMuons_withPtCuts = (TH1D*)subdir->Get("ttMuonGenEtaMuons_withPtCuts;1");
        TH1* muCandGenEtaMuons_withPtCuts = (TH1D*)subdir->Get("muCandGenEtaMuons_withPtCuts;1");

        double ttMuonEff = ttMuonGenEtaMuons_withPtCuts->Integral() / gpMuonGenEtaMuons_withPtCuts->Integral();
        double muCadnEffEff = muCandGenEtaMuons_withPtCuts->Integral() / gpMuonGenEtaMuons_withPtCuts->Integral();
        double taggingEff = muCandGenEtaMuons_withPtCuts->Integral() / ttMuonGenEtaMuons_withPtCuts->Integral();

        cout<<"ttMuonEff    "<<ttMuonEff<<endl;
        cout<<"muCadnEffEff "<<muCadnEffEff<<endl;
        cout<<"taggingEff   "<<taggingEff<<endl<<endl;

        //------------------------

        canvas1Eff->cd(4);
        canvas1Eff->cd(4)->SetGridx();
        canvas1Eff->cd(4)->SetGridy();
        canvas1Eff->cd(4)->SetLeftMargin(0.12);
        {
          TLegend* leg = new TLegend(0.33, 0.13,0.77,0.38);
          leg->SetHeader("p_{T}^{gen} > 25 GeV, L1 p_{T} #geq 20 GeV"); //TODO change according to the plot
          //leg->SetBorderSize(0);
          leg->SetFillStyle(0);
          leg->SetBorderSize(0);
          leg->SetTextSize(0.03);
          leg->SetMargin(0.2);

          if(rebinEtaEff) {
            ttMuonGenEtaMuons_withPtCuts = ttMuonGenEtaMuons_withPtCuts->Rebin(4, (string(ttMuonGenEtaMuons_withPtCuts->GetName() )+ "_rebin2").c_str() );
            gpMuonGenEtaMuons_withPtCuts = gpMuonGenEtaMuons_withPtCuts->Rebin(4, (string(gpMuonGenEtaMuons_withPtCuts->GetName() )+ "_rebin2").c_str() );
            muCandGenEtaMuons_withPtCuts = muCandGenEtaMuons_withPtCuts->Rebin(4, (string(muCandGenEtaMuons_withPtCuts->GetName() )+ "_rebin2").c_str() );
          }

          if(TEfficiency::CheckConsistency(*ttMuonGenEtaMuons_withPtCuts, *gpMuonGenEtaMuons_withPtCuts) )
          {
            TEfficiency* ttMuonEta_ptCut_Eff = makeEfficiency(*ttMuonGenEtaMuons_withPtCuts, *gpMuonGenEtaMuons_withPtCuts, title, kBlue);

            std::string title = ttMuonGenEtaMuons_withPtCuts->GetTitle();
            //title = std::regex_replace(title, std::regex("\\muCandGenEtaMuons"), "tagging efficiency");


            ttMuonEta_ptCut_Eff->SetMarkerStyle(22);
            ttMuonEta_ptCut_Eff->SetMarkerColor(kBlue);
            ttMuonEta_ptCut_Eff->SetMarkerSize(0.8);

            ttMuonEta_ptCut_Eff->Draw("APZ");
            ttMuonEta_ptCut_Eff->SetTitle((title + "; generated #eta; efficiency").c_str());
            canvas1Eff->Update();

            if(alogNumToCompare1 == 1 || alogNumToCompare1 == 4)
              ttMuonEta_ptCut_Eff->GetPaintedGraph()->GetYaxis()->SetRangeUser(0.8, 1.05);
            else
              ttMuonEta_ptCut_Eff->GetPaintedGraph()->GetYaxis()->SetRangeUser(0.0, 1.05);

            //ttMuonEta_ptCut_Eff->GetPaintedGraph()->GetYaxis()->SetRangeUser(0.8, 1.05);
            ttMuonEta_ptCut_Eff->GetPaintedGraph()->GetXaxis()->SetRangeUser(-2.4, 2.4);

            leg->AddEntry(ttMuonEta_ptCut_Eff , "Tracking Trigger Track", "lep");

            if( (algoNum == alogNumToCompare1 || algoNum == alogNumToCompare2) && compareFirst) {
              canvasCompare->cd(4);
              ttMuonEta_ptCut_Eff->Draw("APZ");
              //legendCompare->AddEntry(ttMuonEta_ptCut_Eff , "Tracking Trigger Track", "lep");
              compareFirst = false;
            }
          }

          canvas1Eff->cd(4);
          if(TEfficiency::CheckConsistency(*muCandGenEtaMuons_withPtCuts, *gpMuonGenEtaMuons_withPtCuts) )
          {
            std::string title = " ";
            TEfficiency* muCandGenEtaMuons_ptCut_Eff = makeEfficiency(*muCandGenEtaMuons_withPtCuts, *gpMuonGenEtaMuons_withPtCuts , title, kRed);
            muCandGenEtaMuons_ptCut_Eff->SetMarkerStyle(23);
            muCandGenEtaMuons_ptCut_Eff->SetMarkerSize(0.7);
            muCandGenEtaMuons_ptCut_Eff->SetMarkerColor(colorCompare);
            muCandGenEtaMuons_ptCut_Eff->SetLineColor(colorCompare);
            muCandGenEtaMuons_ptCut_Eff->Draw("same PZ");

            leg->AddEntry(muCandGenEtaMuons_ptCut_Eff , "Track + Stubs", "lep");

            string fileName1 = (plotsDir + "/" + dirName + "_" + muCandGenEtaMuons_ptCut_Eff->GetName() + string(".root"));
            cout<<"saving hist as "<<fileName1<<endl;
            muCandGenEtaMuons_ptCut_Eff->SaveAs(fileName1.c_str() );

            if(algoNum == alogNumToCompare1 || algoNum == alogNumToCompare2) {
              canvasCompare->cd(4);
              muCandGenEtaMuons_ptCut_Eff->Draw("same PZ");
              //legendCompare->AddEntry(muCandGenEtaMuons_ptCut_Eff , (string("Track + Stubs ") + label).c_str(), "lep");

              colorCompare++;
              if(colorCompare == 4)
                colorCompare+=2;
            }

            {
              TH1D* muCandGenEtaMuons_withPtCuts_overlap = (TH1D*)muCandGenEtaMuons_withPtCuts->Clone( (muCandGenEtaMuons_withPtCuts->GetName() + string("_overlap")).c_str() );
              TH1D* gpMuonGenEtaMuons_withPtCuts_overlap = (TH1D*)gpMuonGenEtaMuons_withPtCuts->Clone( (gpMuonGenEtaMuons_withPtCuts->GetName() + string("_overlap")).c_str() );

              for(int iBin = 1; iBin <= gpMuonGenEtaMuons_withPtCuts_overlap->GetNbinsX(); iBin++) {
                if( fabs(gpMuonGenEtaMuons_withPtCuts_overlap->GetBinCenter(iBin)) < 0.8 || fabs(gpMuonGenEtaMuons_withPtCuts_overlap->GetBinCenter(iBin)) > 1.3) {
                  gpMuonGenEtaMuons_withPtCuts_overlap->SetBinContent(iBin, 0);
                  muCandGenEtaMuons_withPtCuts_overlap->SetBinContent(iBin, 0);
                }
              }

              TEfficiency* muCandGenEtaMuons_ptCut_Eff_overlap  = makeEfficiency(*muCandGenEtaMuons_withPtCuts_overlap , *gpMuonGenEtaMuons_withPtCuts_overlap , title, kRed);
              //muCandGenEtaMuons_ptCut_Eff_overlap->Draw("APZ");

              string fileName1 = (plotsDir + "/" + dirName + "_" + muCandGenEtaMuons_ptCut_Eff_overlap->GetName() + string(".root"));
              cout<<"!!!!!!! saving hist as "<<fileName1<<endl;
              muCandGenEtaMuons_ptCut_Eff_overlap->SaveAs(fileName1.c_str() );


              TH1* muCandGenEtaMuons_withPtCuts_overlap_abs = makeAbs(muCandGenEtaMuons_withPtCuts_overlap);
              TH1* gpMuonGenEtaMuons_withPtCuts_overlap_abs = makeAbs(gpMuonGenEtaMuons_withPtCuts_overlap);


              TEfficiency* muCandGenEtaMuons_ptCut_Eff_overlap_abs  = makeEfficiency(*muCandGenEtaMuons_withPtCuts_overlap_abs , *gpMuonGenEtaMuons_withPtCuts_overlap_abs , title, kRed);
              //muCandGenEtaMuons_ptCut_Eff_overlap->Draw("APZ");

              fileName1 = (plotsDir + "/" + dirName + "_" + muCandGenEtaMuons_ptCut_Eff_overlap_abs->GetName() + string(".root"));
              muCandGenEtaMuons_ptCut_Eff_overlap_abs->SaveAs(fileName1.c_str() );
              //muCandGenEtaMuons_withPtCuts_overlap_abs->SaveAs(fileName1.c_str() );
              //gpMuonGenEtaMuons_withPtCuts_overlap_abs->SaveAs(fileName1.c_str() );
            }
          }

          //leg->Draw("same");
        }


        //DrawLabel(canvas1Eff->cd(4), label);
        savePlot(canvasName + "_effVsEta", canvas1Eff->cd(4) );
      //------------------------
        //nominator
/*        TH1D* muCandGenEtaMuons = (TH1D*)subdir->Get("muCandGenEtaMuons");
        TH1D* muCandGenPhiMuons = (TH1D*)subdir->Get("muCandGenPhiMuons");

        TH1D* lostTtMuonPt  = (TH1D*)subdir->Get("lostTtMuonPt");
        TH1D* lostTtMuonEta = (TH1D*)subdir->Get("lostTtMuonEta");
        TH1D* lostTtMuonPhi = (TH1D*)subdir->Get("lostTtMuonPhi");

        canvas1Eff->cd(5);
        canvas1Eff->cd(5)->SetGridx();
        canvas1Eff->cd(5)->SetGridy();


        ttMuonEtaEff->Draw("hist");
        ttMuonEtaEff->GetYaxis()->SetRangeUser(0.8, 1.0);

        TH1D* muCandGenEtaMuonsEff = (TH1D*)muCandGenEtaMuons->Clone("muCandGenEtaMuonsEff");
        muCandGenEtaMuonsEff->Divide(gpMuonEta);
        muCandGenEtaMuonsEff->SetLineColor(kRed);
        muCandGenEtaMuonsEff->Draw("histsame");*/

        //------------------------------------------------------------------------
/*        canvas1Eff->cd(6);
        canvas1Eff->cd(6)->SetGridx();
        canvas1Eff->cd(6)->SetGridy();
        TH2I* betaGenBetaL1Mu = (TH2I*)subdir->Get("betaGenBetaL1Mu");
        //betaGenBetaL1Mu->Draw("colz");
        int bin0 = betaGenBetaL1Mu->GetYaxis()->FindBin(0.);
        TH1D* l1MuVsBetaGen = betaGenBetaL1Mu->ProjectionX("l1MuVsBetaGen", bin0, -1);
        TH1D* allVsBetaGen = betaGenBetaL1Mu->ProjectionX("allVsBetaGen", -1, -1);
        l1MuVsBetaGen->Divide(allVsBetaGen);
        l1MuVsBetaGen->SetTitle("efficiency vs beta gen");
        l1MuVsBetaGen->Draw("hist");*/

        canvas1Eff->Update();
      }

      //if(compareFirst)
        //compareFirst = false;

      omtfTTAnalyzerDir->cd();
    }
  }

}

//*************************************************** rate ********************************************
void makeRatePlots(TDirectory* omtfTTAnalyzerDir, const char* nameLegend, int color, int ptCut) {
  cout<<"lhcFillingRatio "<<lhcFillingRatio<<endl;

  TH2I* etaGenPtGenBx1 = (TH2I*)omtfTTAnalyzerDir->Get("etaGenPtGenBx1");
  TH1D* ptGenBx1 = etaGenPtGenBx1->ProjectionY("ptGenBx1");

  TH2I* etaGenPtGenBx2 = (TH2I*)omtfTTAnalyzerDir->Get("etaGenPtGenBx2");
  TH1D* ptGenBx2 = etaGenPtGenBx2->ProjectionY("ptGenBx2");

  TIter next(omtfTTAnalyzerDir->GetListOfKeys());
  TKey* key;

  next.Reset();
  while ((key = (TKey*)next())) {
    if (key->IsFolder()) {
      omtfTTAnalyzerDir->cd(key->GetName());
      string dirName = key->GetName();

      if(dirName.find("RateAnalyzer_") != string::npos) {
        TDirectory *subdir = gDirectory;
        cout<<"\nmaking plots for "<<dirName<<endl;
        string canvasName = string(nameLegend)  + "_" + dirName;
        TCanvas* canvasRate1 = new TCanvas((string("canvas_") + canvasName).c_str(), canvasName.c_str(), 1500, 1200);
        canvasRate1->Divide(2, 2);

        canvasRate1->cd(1);

        canvasRate1->cd(1)->SetLogy();
        canvasRate1->cd(1)->SetGridx();
        canvasRate1->cd(1)->SetGridy();

        TH1D* muCandPt = (TH1D*)subdir->Get("muCandPt");
        muCandPt->SetLineColor(kBlack);
        muCandPt->Draw("hist");
        muCandPt->GetXaxis()->SetRangeUser(0, ptMaxRange);
        muCandPt->GetYaxis()->SetRangeUser(0.1, 10000);

        TH1D* muCandPtMuons = (TH1D*)subdir->Get("muCandPtMuons");
        muCandPtMuons->SetLineColor(kBlue);
        muCandPtMuons->Draw("histsame");

        TH1D* muCandPtFakes = (TH1D*)subdir->Get("muCandPtFakes");
        muCandPtFakes->SetLineColor(kMagenta);
        //muCandPtFakes->SetFillColor(kMagenta);
        muCandPtFakes->Draw("histsame");

        TH1D* muCandPtWrongTag = (TH1D*)subdir->Get("muCandPtWrongTag");
        muCandPtWrongTag->SetLineColor(kGreen);
        muCandPtWrongTag->Draw("histsame");


        ///////
        canvasRate1->cd(2);
        canvasRate1->cd(2)->SetLogy();
        canvasRate1->cd(2)->SetGridx();
        canvasRate1->cd(2)->SetGridy();

        cout<<"eventsCnt "<<eventsCnt<<endl;
        double scale = 1./eventsCnt * lhcFreq * lhcFillingRatio;
        muCandPt->Sumw2(false);
        TH1* muCandPt_rateCumul = muCandPt->GetCumulative(false, "_rate");
        muCandPt_rateCumul->Sumw2(false);
        if(1) {
          TH1* muCandPt_rateCumul_copy = (TH1*)muCandPt_rateCumul->Clone( (muCandPt_rateCumul->GetName() + string("_copy")).c_str() );
          TH1* allEventsHist = (TH1*)muCandPt_rateCumul_copy->Clone("allEventsHist");
          for(int iBin = 0; iBin < allEventsHist->GetNbinsX(); iBin++) {
            allEventsHist->SetBinContent(iBin, eventsCnt);
          }
          muCandPt_rateCumul_copy->Sumw2(false);
          allEventsHist->Sumw2(false);

          canvasRate1->cd(3);
          canvasRate1->cd(3)->SetLogy();
          canvasRate1->cd(3)->SetGridx();
          canvasRate1->cd(3)->SetGridy();
          string title = ("; ttTrack p_{T} [GeV]; rate [Hz]");
          TEfficiency* muCandPt_rateCumul_withTEff = makeEfficiency(*muCandPt_rateCumul_copy, *allEventsHist, title, kRed );

          muCandPt_rateCumul_withTEff->Draw("APZ");
          canvasRate1->cd(3)->Update();
          muCandPt_rateCumul_withTEff->GetPaintedGraph()->GetXaxis()->SetRangeUser(0, ptMaxRange);
          //muCandPt_rateCumul_withTEff->GetPaintedGraph()->GetYaxis()->SetRangeUser(100, 50000000);

          TGraphAsymmErrors* paintedGraph = (TGraphAsymmErrors*) (muCandPt_rateCumul_withTEff->GetPaintedGraph()->Clone( (muCandPt_rateCumul_withTEff->GetName() + string("_copy")).c_str()  ) );

          for (int i=0;i < paintedGraph->GetN();i++) {
            paintedGraph->GetY()[i] *= lhcFreq * lhcFillingRatio;
            paintedGraph->GetEYhigh()[i] *= lhcFreq * lhcFillingRatio;
            paintedGraph->GetEYlow()[i] *= lhcFreq * lhcFillingRatio;

            if(paintedGraph->GetX()[i] == 20.25)
            {
              cout<<" rate at pt_cut "<< paintedGraph->GetX()[i] << "GeV "<<paintedGraph->GetY()[i] <<" error "<<paintedGraph->GetEYhigh()[i]<<endl;
            }
          }

          canvasRate1->cd(4);
          canvasRate1->cd(4)->SetLogy();
          canvasRate1->cd(4)->SetGridx();
          canvasRate1->cd(4)->SetGridy();
          paintedGraph->Draw("APZ");
          canvasRate1->cd(4)->Update();
          paintedGraph->GetXaxis()->SetRangeUser(0, ptMaxRange);
          paintedGraph->GetYaxis()->SetRangeUser(100, 50000000);
          canvasRate1->cd(4)->Update();
        }


        canvasRate1->cd(2);
        muCandPt_rateCumul->SetTitle(canvasRate1->GetTitle());
        muCandPt_rateCumul->Sumw2(false);
        muCandPt_rateCumul->Scale(scale);
        muCandPt_rateCumul->GetXaxis()->SetTitle("ttTrack p_{T} treshold [GeV]");
        muCandPt_rateCumul->GetXaxis()->SetTitleOffset(1.2);
        muCandPt_rateCumul->GetYaxis()->SetTitle("Event rate [Hz]");
        muCandPt_rateCumul->SetLineColor(kBlack);
        muCandPt_rateCumul->Draw("L");
        muCandPt_rateCumul->GetXaxis()->SetRangeUser(0, ptMaxRange);
        muCandPt_rateCumul->GetYaxis()->SetRangeUser(100, 50000000);

        cout<<" rate at pt_cut 20GeV "<<muCandPt_rateCumul->GetBinContent(muCandPt_rateCumul->FindBin(20))<<" error "<<muCandPt_rateCumul->GetBinError(muCandPt_rateCumul->FindBin(20))<<endl; //TODO <<<<<<<<<<<<<
        cout<<" rate at pt_cut 25GeV "<<muCandPt_rateCumul->GetBinContent(muCandPt_rateCumul->FindBin(25))<<" error "<<muCandPt_rateCumul->GetBinError(muCandPt_rateCumul->FindBin(25))<<endl<<endl; //TODO <<<<<<<<<<<<<


        TH1* muCandPtFakes_rateCumul = muCandPtFakes->GetCumulative(false, "_rate");
        muCandPtFakes_rateCumul->Sumw2(false);
        muCandPtFakes_rateCumul->Scale(scale);
        muCandPtFakes_rateCumul->SetLineColor(kMagenta);
        //muCandPtFakes_rateCumul->SetFillColor(kMagenta);
        muCandPtFakes_rateCumul->Draw("Lsame");

        TH1* muCandPtWrongTag_rateCumul = muCandPtWrongTag->GetCumulative(false, "_rate");
        muCandPtWrongTag_rateCumul->Sumw2(false);
        muCandPtWrongTag_rateCumul->Scale(scale);
        muCandPtWrongTag_rateCumul->SetLineColor(kGreen);
        muCandPtWrongTag_rateCumul->Draw("Lsame");


        TH1* muCandPtMuons_rateCumul = muCandPtMuons->GetCumulative(false, "_rate");
        muCandPtMuons_rateCumul->Sumw2(false);
        muCandPtMuons_rateCumul->Scale(scale);
        muCandPtMuons_rateCumul->SetLineColor(kBlue);
        muCandPtMuons_rateCumul->Draw("Lsame");
        //canvas1->cd(6)->SetLogy();

        savePlot(canvasName + "_EventsRate", canvasRate1->cd(2) );

        string fileName1 = (plotsDir + "/" + dirName + "_" + muCandPt_rateCumul->GetName()  + string(".root"));
        cout<<"saving hist as "<<fileName1<<endl;
        muCandPt_rateCumul->SaveAs(fileName1.c_str() );

/*        ////////////////////////////////
        canvasRate1->cd(3);
        canvasRate1->cd(3)->SetLogy();
        canvasRate1->cd(3)->SetGridx();
        canvasRate1->cd(3)->SetGridy();

        TH2I* etaGenPtGenLostBx1 = (TH2I*)subdir->Get("etaGenPtGenLostBx1");
        TH1D* ptGenLostBx1 = etaGenPtGenLostBx1->ProjectionY("ptGenLostBx1");
        ptGenLostBx1->SetLineColor(kRed);
        ptGenBx1->Draw("hist");
        //ptGenBx1->GetXaxis()->Set
        ptGenLostBx1->Draw("Lsame");

        int ptGenBx1Pt20 = ptGenBx1->Integral(ptGenBx1->FindBin(20), -1);
        int ptGenLostBx1Pt20 = ptGenLostBx1->Integral(ptGenBx1->FindBin(20), -1);
        cout<<" ptGenBx1Pt20 "<<ptGenBx1Pt20<<" ptGenLostBx1Pt20 "<<ptGenLostBx1Pt20<<" eff lost "<<ptGenLostBx1Pt20/(double)ptGenBx1Pt20<<endl;;

        ////////////////////////////////
        canvasRate1->cd(4);
        canvasRate1->cd(4)->SetLogy();
        canvasRate1->cd(4)->SetGridx();
        canvasRate1->cd(4)->SetGridy();

        TH2I* etaGenPtGenLostBx2 = (TH2I*)subdir->Get("etaGenPtGenLostBx2");
        TH1D* ptGenLostBx2 = etaGenPtGenLostBx2->ProjectionY("ptGenLostBx2");
        ptGenLostBx2->SetLineColor(kRed);
        ptGenBx2->Draw("hist");
        //ptGenBx2->GetXaxis()->Set
        ptGenLostBx2->Draw("histsame");

        int ptGenBx2Pt20 = ptGenBx2->Integral(ptGenBx2->FindBin(20), -1);
        int ptGenLostBx2Pt20 = ptGenLostBx2->Integral(ptGenBx2->FindBin(20), -1);
        cout<<" ptGenBx2Pt20 "<<ptGenBx2Pt20<<" ptGenLostBx2Pt20 "<<ptGenLostBx2Pt20<<" eff lost "<<ptGenLostBx2Pt20/(double)ptGenBx2Pt20<<endl;;*/

      }
    }
  }

  compareFirst = false;
}




void makeCandidatesMatchingPlots(TDirectory* omtfTTAnalyzerDir, const char* nameLegend, double eventsCnt) {
  bool cumulative = true;

  vector< std::pair<std::string, Color_t> > categoryNames;
  //categoryNames.emplace_back("all candidates", kBlack); //0

  categoryNames.emplace_back("muons", kBlue ); //1
  categoryNames.emplace_back("veryLooseMuons", kBlue -2); //2
  //categoryNames.emplace_back("pions", kGreen) ; //3
  categoryNames.emplace_back("pionsDecayedToMu", kGreen); //4
  categoryNames.emplace_back("kaonsDecayedToMu", kCyan + 1); //7

  categoryNames.emplace_back("pionsNotDecayedToMu", kGreen +1); //5
  //categoryNames.emplace_back("kaons", kCyan); //6
  categoryNames.emplace_back("kaonsNotDecayedToMu",kCyan + 2); //8
  categoryNames.emplace_back("otherParts", kGray ); //9
  categoryNames.emplace_back("fakes", kMagenta); //10


  TIter next(omtfTTAnalyzerDir->GetListOfKeys());
  TKey* key;


  TDirectory* subdirAllTTTrack;
  while ((key = (TKey*)next())) {
    if (key->IsFolder()) {
      omtfTTAnalyzerDir->cd(key->GetName());
      string dirName = key->GetName();
      if(dirName.find("MuCandsMatchingAnalyzer_AllTTTRacks10") != string::npos) {
        subdirAllTTTrack = gDirectory;
      }
    }
  }

  next.Reset();

  double scale = 1./eventsCnt * lhcFreq * lhcFillingRatio;

  while ((key = (TKey*)next())) {
    if (key->IsFolder()) {
      omtfTTAnalyzerDir->cd(key->GetName());
      string dirName = key->GetName();
      if(dirName.find("MuCandsMatchingAnalyzer_") != string::npos) {
        TDirectory* subdir = gDirectory;
        cout<<"making purity  plots for "<<dirName<<endl;

        string canvasName = string("canvas__PurityPlots_") + nameLegend  + "_" + dirName;
        TCanvas* canvasPurityPlots = new TCanvas(canvasName.c_str(), canvasName.c_str(), 1200, 800);
        canvasPurityPlots->cd();
        canvasPurityPlots->Divide(2, 2);

        canvasPurityPlots->cd(1);
        canvasPurityPlots->cd(1)->SetGridx();
        canvasPurityPlots->cd(1)->SetGridy();
        canvasPurityPlots->cd(1)->SetLogy();

        TLegend* legend = new TLegend(0.65, 0.55, 0.9, 0.9);

        canvasPurityPlots->cd(1);
        TH1D* allCandPt = (TH1D*)subdir->Get("candPt");
        allCandPt->SetLineColor(kBlack);
        canvasPurityPlots->cd(1);

        TH1* allCandPtCumul = allCandPt->GetCumulative(false, "_cumul");

        if(!cumulative) {
          allCandPt->Draw("L");
          allCandPt->GetXaxis()->SetRangeUser(0, ptMaxRange);
          allCandPt->GetYaxis()->SetRangeUser(0.5, 100000000);
          allCandPt->GetXaxis()->SetTitle("ttTrack p_{T} [GeV]");
        }
        else {
          TH1* allCandPtCumulCopy = (TH1*)allCandPtCumul->Clone( (allCandPtCumul->GetName() + string("copy")).c_str());
          allCandPtCumulCopy->Sumw2(false);
          allCandPtCumulCopy->Scale(scale);
          allCandPtCumulCopy->Draw("LE"); //"C"
          allCandPtCumulCopy->GetXaxis()->SetRangeUser(0, ptMaxRange);
          allCandPtCumulCopy->GetYaxis()->SetRangeUser(100, 100000000);
          allCandPtCumulCopy->GetXaxis()->SetTitle("ttTrack p_{T} threshold [GeV]");

          if(dirName.find("AllTTTRacks") != string::npos)
            allCandPtCumulCopy->GetYaxis()->SetTitle("ttTrack rate [Hz]");
          else
            allCandPtCumulCopy->GetYaxis()->SetTitle("muon candidate rate [Hz]");

        }

        legend->AddEntry(allCandPt, "all candidates", "f");

        //////////////////////////////////////// efficiency /////////
        {
          canvasPurityPlots->cd(2);
          canvasPurityPlots->cd(2)->SetLogy();
          canvasPurityPlots->cd(2)->SetGridx();
          canvasPurityPlots->cd(2)->SetGridy();

          TH1D* candPtAllTTTracks = (TH1D*)subdirAllTTTrack->Get("candPt");

          if(!cumulative) {
            /*TH1* allCandPtEff = (TH1D*)allCandPt->Clone( (allCandPtCumul->GetName() + std::string("_eff")).c_str() );
            allCandPtEff->Divide(candPtAllTTTracks);
            allCandPtEff->Draw("hist");
            allCandPtEff->GetXaxis()->SetTitle("ttTrack p_{T} [GeV]");
            allCandPtEff->GetYaxis()->SetRangeUser(0.00001, 1.1);
            allCandPtEff->GetYaxis()->SetTitle("efficiency");*/

            string title = ("; ttTrack p_{T} [GeV]; efficiency");
            TEfficiency* allCandPtEff = makeEfficiency(*allCandPt, *candPtAllTTTracks, title, allCandPt->GetLineColor() );
            allCandPtEff->Draw("APZ");
            canvasPurityPlots->cd(2)->Update();
            allCandPtEff->GetPaintedGraph()->GetXaxis()->SetRangeUser(0, ptMaxRange);
            allCandPtEff->GetPaintedGraph()->GetYaxis()->SetRangeUser(0.00001, 1.1);

          }
          else {
            TH1* candPtAllTTTracksCumul = candPtAllTTTracks->GetCumulative(false, "_cumul");
            TH1* candPtEffCumul = (TH1D*)allCandPtCumul->Clone( (allCandPtCumul->GetName() + std::string("_eff")).c_str() );
            candPtEffCumul->Divide(candPtAllTTTracksCumul);
            candPtEffCumul->SetTitle("efficiency - probability of tagging a ttTrack as muon");
            candPtEffCumul->Draw("hist");
            candPtEffCumul->GetXaxis()->SetTitle("ttTrack p_{T} threshold [GeV]");
            candPtEffCumul->GetXaxis()->SetRangeUser(0., ptMaxRange);
            candPtEffCumul->GetYaxis()->SetRangeUser(0.00001, 1.1);
            candPtEffCumul->GetYaxis()->SetTitle("efficiency");
          }
        }

        THStack * hsPurity = new THStack("hsPurity"," purity - probability that the muon candidate is matched to a given category of tracking particle");
        THStack * hsPurityCumul = new THStack("hsPurity"," hsPurityCumul");

        THStack * hsRateVsEta = new THStack("hsRateVsEta", "hsRateVsEta");
        if(dirName.find("10") != string::npos)
          hsRateVsEta->SetTitle("ttTracks p_{T} > 10 GeV");
        else if(dirName.find("20") != string::npos)
          hsRateVsEta->SetTitle("ttTracks p_{T} > 20 GeV");

        double totalRate = 0;

        TH1* sumHistRateVsEta = nullptr;

        for(auto& categoryName : categoryNames) {
          std::string histName = "candPt_" + categoryName.first;

          TH1D* candPt = (TH1D*)subdir->Get(histName.c_str());
          if(candPt) {

            TH1* candPt_rebined = candPt->Rebin(2, (histName + "_rebined").c_str() );
            candPt_rebined->SetLineColor(kGreen); //needed only for debug

            candPt->SetLineColor(categoryName.second);
            candPt->SetMarkerColor(categoryName.second);
            /*if(categoryName.first == "veryLooseMuons")*/
            //candPt->SetFillColor(categoryName.second);

            canvasPurityPlots->cd(1);//events count vs pt for every category of candidates

            if(!cumulative) {
              candPt->Draw("Lsame");
              cout<<"error "<<candPt->GetBinError(15)<<endl;
            }
            else {
              TH1* candPtCumul = candPt->GetCumulative(false, "_cumul");
              //GetCumulative cloens the original histogram to create the output one, then resets it - which reset the errors
              //then fills the output hist with cumulative values, but the errors are not filled therefore this magic with sumw2 is needed
              candPtCumul->Sumw2(false); //this just deletes the sumw2
              //it is then recreate in Scale (Sumw2 is called there, Sumw2 just copies the bin content to the fSumw2.fArray, the errors are calculate as sqrt of  sumw2)
              TH1* candPtCumulCopy = (TH1*)candPtCumul->Clone( (candPtCumul->GetName() + string("copy")).c_str());
              candPtCumulCopy->Scale(scale);
              candPtCumulCopy->Draw("LEsame");

              //cout<<"candPtCumul error "<<candPtCumul->GetBinError(15)<<endl;
              //cout<<"candPtCumulCopy error"<<candPtCumulCopy->GetBinError(15)<<endl;
            }

            ////////////////////////////////////////
            //efficiency, i.e. probability to tag as a muon the ttTrack of a given matchin category
            canvasPurityPlots->cd(2);

            //TH1D* candPtEff = (TH1D*)candPt->Clone((candPt->GetName() + std::string("_eff") ).c_str());

            TH1D* candPtAllTTTracks = (TH1D*)subdirAllTTTrack->Get(histName.c_str());
            //candPtAllTTTracks = (TH1D*)candPtAllTTTracks->Clone((candPtAllTTTracks->GetName() + std::string("_denom") ).c_str());
            if(!cumulative) {
              /*candPtEff->Divide(candPtAllTTTracks);
              candPtEff->SetMarkerStyle(22);
              candPtEff->SetMarkerSize(0.7);
              candPtEff->Draw("P hist same");*/

              string title = ("; ttTrack p_{T} [GeV]; efficiency");
              TEfficiency* candPtEff = makeEfficiency(*candPt, *candPtAllTTTracks, title, candPt->GetLineColor() );
              candPtEff->Draw("PZ same");
            }
            else {
              //efficiency cumulative
              TH1* candPtEffCumul = candPt->GetCumulative(false, "_eff_cumul");
              TH1* candPtAllTTTracksCumul = candPtAllTTTracks->GetCumulative(false, "_cumul");
              candPtEffCumul->Divide(candPtAllTTTracksCumul);
              candPtEffCumul->Draw("histsame");
            }

            /////////////////////////////////////////purity
            TH1D* candPtPurity = (TH1D*)candPt->Clone( (candPt->GetName() + std::string("_purity") ).c_str() );
            candPtPurity->Divide(allCandPt);
            candPtPurity->SetFillColor(categoryName.second);
            hsPurity->Add(candPtPurity);

            /////////////////////////////////////////// purity cumulative
            TH1* candPtCumul = candPt->GetCumulative(false, "_cumul");
            candPtCumul->Divide(allCandPtCumul);
            candPtCumul->SetFillColor(categoryName.second);
            hsPurityCumul->Add(candPtCumul);

            //////////////////////////////////////////////////////////////////////////
            histName = "candEta_" + categoryName.first;
            TH1D* candEta = (TH1D*)subdir->Get(histName.c_str());
            if(dirName.find("AllTTTRacks") == string::npos)
              candEta->Rebin(4);
            candEta->Scale(scale);
            candEta->SetFillColor(categoryName.second);
            hsRateVsEta->Add(candEta);
            totalRate += candEta->Integral();

            legend->AddEntry(candEta, categoryName.first.c_str(), "f");

            if(sumHistRateVsEta == nullptr)
              sumHistRateVsEta = (TH1*)candEta->Clone("sumHistRateVsEta");
            else
              sumHistRateVsEta->Add(candEta);
          }
          else {
            cout<<"no hist "<<histName<<endl;
          }
        }

        canvasPurityPlots->cd(1);
        legend->Draw();


        canvasPurityPlots->cd(4);
        if(!cumulative) {
          if(dirName.find("AllTTTRacks") != string::npos) {
            hsPurity->SetTitle("purity - fraction of ttTracks of a given category");
          }
          else {
            hsPurity->SetTitle("purity - fraction of muon candidates of a given category");
          }
          hsPurity->Draw("hist");
          canvasPurityPlots->cd(4)->Update();
          hsPurity->GetXaxis()->SetTitle("ttTrack pt [GeV]");
          hsPurity->GetXaxis()->SetRangeUser(0, ptMaxRange);

          hsPurity->GetYaxis()->SetTitle("purity");
        }
        else {
          hsPurityCumul->Draw("hist");
          if(dirName.find("AllTTTRacks") != string::npos)
            hsPurityCumul->SetTitle("cumulative purity - fraction of ttTracks of a given category");
          else
            hsPurityCumul->SetTitle("purity - fraction of muon candidates of a given category");
          hsPurityCumul->GetXaxis()->SetRangeUser(0, ptMaxRange);
          hsPurityCumul->GetXaxis()->SetTitle("ttTrack pt threshold [GeV]");
          hsPurityCumul->GetYaxis()->SetTitle("purity");
        }

        canvasPurityPlots->cd(3);
        hsRateVsEta->Draw("hist");
        canvasPurityPlots->cd(3)->Update();
        //hsRateVsEta->GetXaxis()->SetRangeUser(0, ptMaxRange);

        hsRateVsEta->GetXaxis()->SetTitle("ttTrack #eta");

        if(dirName.find("AllTTTRacks") != string::npos) {
          hsRateVsEta->GetYaxis()->SetTitle("ttTrack rate [Hz]");
          hsRateVsEta->SetMaximum(900000);
          hsRateVsEta->GetYaxis()->SetRangeUser(0, 900000);
        }
        else if(dirName.find("10") != string::npos) {
          hsRateVsEta->GetYaxis()->SetTitle("muon candidate rate [Hz]");
          hsRateVsEta->SetMaximum(9000);
          hsRateVsEta->GetYaxis()->SetRangeUser(0, 9000);
        }
        else if(dirName.find("20") != string::npos) {
          hsRateVsEta->GetYaxis()->SetTitle("muon candidate rate [Hz]");
          ///hsRateVsEta->SetMaximum(2*5000);
          hsRateVsEta->GetYaxis()->SetRangeUser(0, 1500);
        }
        else {
          hsRateVsEta->GetYaxis()->SetTitle("muon candidate rate [Hz]");
        }

        /*TH1* sumHistRateVsEta = (TH1*)hsRateVsEta->GetHistogram()->Clone();
        sumHistRateVsEta->Reset();
        sumHistRateVsEta->Sumw2(false);
        for(auto hist : *(hsRateVsEta->GetHists() ) ) {
          sumHistRateVsEta->Add((TH1*)hist);
        }*/
        sumHistRateVsEta->Draw("same");

        canvasPurityPlots->cd(3)->SetGridx();
        canvasPurityPlots->cd(3)->SetGridy();
        cout<<"totalRate "<<totalRate<<endl;

        canvasPurityPlots->cd(1)->Update();
        canvasPurityPlots->cd(2)->Update();
        canvasPurityPlots->cd(3)->Update();
        canvasPurityPlots->cd(4)->Update();
        canvasPurityPlots->Update();

        savePlot(canvasName + "_matcher_CandRateVsPt", canvasPurityPlots->cd(1) );
        savePlot(canvasName + "_matcher_effVsPt", canvasPurityPlots->cd(2) );
        savePlot(canvasName + "_matcher_CandRateVsEta", canvasPurityPlots->cd(3) );
        savePlot(canvasName + "_matcher_PurityVsPt", canvasPurityPlots->cd(4) );
      }
    }
  }
}

