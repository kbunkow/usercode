from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TH1D, TEfficiency, TH2D
from ROOT import gROOT
from libPyROOT import TDirectory
import sys
    

#version = "v2_t" + sys.argv[0]
version = "v2_t38" 

#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis_newerSAmple_v21_1_10Files_withMatching.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis_newerSAmple_v21_1.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis2_rate_v0006.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis2_v31.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_omtf_nn_MC_analysis_MuFlatPt_PU200_v2_t30/results/omtfAnalysis2.root' )
rateHistFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_omtf_nn_MC_analysis_SingleNeutrino_PU200_' + version + '/results/omtfAnalysis2.root' )
effHistFile =  TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_omtf_nn_MC_analysis_MuFlatPt_PU200_' + version + '/results/omtfAnalysis2.root' )


#histFile.ls()

print (rateHistFile)

lhcFillingRatio = 2760./3564.;
lhcFreq = 40144896; #11264 * 3564

analyzerOmtfDirRate = rateHistFile.Get("L1MuonAnalyzerOmtf")
candPerEvent = analyzerOmtfDirRate.Get("candPerEvent")
print ("candPerEvent " + str(type(candPerEvent) ))

eventCnt = candPerEvent.Integral() 
scale = 1./eventCnt * lhcFreq * lhcFillingRatio;

print ("eventCnt " + str(eventCnt) );
print ("scale " + str(scale) );


#firedLayersEventCntOmtfRate = analyzerOmtfDirRate.Get("firedLayersEventCntOmtf")
firedLayersEventCntOmtfRate = analyzerOmtfDirRate.Get("firedLayersEventCntNN") #firedLayersEventCntNN firedPlanesEventCntNN

firedLayersEventCntOmtfEff = effHistFile.Get("L1MuonAnalyzerOmtf").Get("firedLayersEventCntOmtf") #firedLayersEventCntOmtf firedPlanesEventCntOmtf
effNorm = firedLayersEventCntOmtfEff.Integral() 

firedLayersStat = []

fullRate = 0
for firedLayers in range(0, firedLayersEventCntOmtfRate.GetNbinsX(), 1) : 
    rate = firedLayersEventCntOmtfRate.GetBinContent(firedLayers +1) * scale
    eff = firedLayersEventCntOmtfEff.GetBinContent(firedLayers +1) / effNorm
    
    fullRate += rate
    eff_rate = 10000000
    if rate > 0 :
        eff_rate = eff/rate

    #if eff > 0 :
    #    eff_rate = rate/eff #eff/rate

    if rate > 0 or eff > 0:
        #if rate > 100:
            firedLayersStat.append( (firedLayers, rate, eff, eff_rate) )
            #print("%8i %018i %f" % (firedLayers, firedLayers,  rate) ) 
            print("%8i %s rate: %8.1f eff: %.5f ratio %f" % (firedLayers, format(firedLayers, '018b'), rate, rate, eff_rate) ) 

print("\nselected\n")
firedLayersStat.sort(key = lambda x: x[3], reverse = False)  

totalRateDrop = 0
totalEff = 0
for firedLayerStat in firedLayersStat :
    #print (format(firedLayerStat[0], '018b'), firedLayerStat)
    totalRateDrop += firedLayerStat[1]
    totalEff  += firedLayerStat[2]
    if firedLayerStat[1] > 60: #rate > 100
        print("%8i %s rate: %8.1f eff: %.5f ratio %f totalEff %f totalRateDrop %f fullRate %f " % (firedLayerStat[0], format(firedLayerStat[0], '018b'),  firedLayerStat[1], firedLayerStat[2], firedLayerStat[3], totalEff, totalRateDrop, fullRate - totalRateDrop) ) 
        #print("%s" % (format(firedLayerStat[0], '018b')) ) 

#execfile('ratePlots.py')
