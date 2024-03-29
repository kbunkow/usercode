from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TH1D, TEfficiency, TH2D,TDirectory
from ROOT import gROOT

import sys
    

#version = "v2_t" + sys.argv[0]
version = "v2_t78" 

#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis_newerSAmple_v21_1_10Files_withMatching.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis_newerSAmple_v21_1.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis2_rate_v0006.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/expert/omtf/omtfAnalysis2_v31.root' )
#histFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_omtf_nn_MC_analysis_MuFlatPt_PU200_v2_t30/results/omtfAnalysis2.root' )
#rateHistFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_1_patch2/src/L1Trigger/L1TMuonBayes/test/crab/crab_omtf_nn_MC_analysis_SingleNeutrino_PU250_'+ version + '/results/omtfAnalysis2.root' )
#rateHistFile = TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_omtf_nn_MC_analysis_SingleNeutrino_PU250_'+ version + '/results/omtfAnalysis2.root' )
#rateHistFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_run3_ZeroBias_Run2023_t22/results/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10.root' )
#rateHistFile = TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_run3_ZeroBias_Run2023_t22/results/omtfAnalysis2_eff_t22__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10.root' )


#version = "v2_t44" 
version = "v3_t78" 
#effHistFile =  TFile( '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/L1Trigger/L1TMuonOverlapPhase1/test/crab/crab_omtf_nn_MC_analysis_MuFlatPt_PU200_' + version + '/results/omtfAnalysis2.root' )
#effHistFile =  TFile('/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/omtfAnalysis/omtfAnalysis2_eff_t21a__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10__mcWaw2023_OneOverPt_and_iPt2.root')

path = "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/OMTF_phase1/results/"
rateHistFile = TFile(path + "omtfAnalysis2_rate_t26__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10_DTQ_2_4__EphemeralZeroBias_Run370580.root")
effHistFile =  TFile(path + "omtfAnalysis2_eff_t26__Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3_gpFinalize10_DTQ_2_4__mcWaw2023_OneOverPt_and_iPt2.root")
#histFile.ls()

print ("rateHistFile " + rateHistFile.GetName())
print ("effHistFile " + effHistFile.GetName())

#lhcFillingRatio = 2760./3564.;
lhcFillingRatio = 2345./3564.; #run 367883     2023C
lhcFreq = 40144896; #11264 * 3564

analyzerOmtfDirRate = rateHistFile.Get("L1MuonAnalyzerOmtf")
candPerEvent = analyzerOmtfDirRate.Get("candPerEvent")
print ("candPerEvent " + str(type(candPerEvent) ))

eventCnt = candPerEvent.Integral() 
scale = 1./eventCnt * lhcFreq * lhcFillingRatio;

print ("eventCnt " + str(eventCnt) );
print ("scale " + str(scale) );


firedLayersEventCntOmtfRate = analyzerOmtfDirRate.Get("firedLayersEventCntOmtf")
#firedLayersEventCntOmtfRate = analyzerOmtfDirRate.Get("firedLayersEventCntNN") #firedLayersEventCntNN firedPlanesEventCntNN

firedLayersEventCntOmtfEff = effHistFile.Get("L1MuonAnalyzerOmtf").Get("firedLayersEventCntOmtf")
#firedLayersEventCntOmtfEff = effHistFile.Get("L1MuonAnalyzerOmtf").Get("firedLayersEventCntNN") #firedLayersEventCntOmtf firedPlanesEventCntOmtf

print("rate hist " + firedLayersEventCntOmtfRate.GetName() )
print("eff  hist " + firedLayersEventCntOmtfEff.GetName() )



effNorm = firedLayersEventCntOmtfEff.Integral() 

firedLayersStat = []
firedLayersStatQuality_1 = []

fullRate = 0

quality_1 = [
    int("000000110000000011", 2),
    int("000000100000000011", 2),
    int("000000010000000011", 2),
    int("000000110000000001", 2),        
    int("000001000000001100", 2),
    int("000011000000001100", 2),
    int("000010000000001100", 2),
    int("000011000000000100", 2), 
    int("000000011000000001", 2),
    int("001000010000000001", 2),
    ]

quality_1_rate = 0;
qulaity_1_eff = 0

for firedLayers in range(0, firedLayersEventCntOmtfRate.GetNbinsX(), 1) : 
    rate = firedLayersEventCntOmtfRate.GetBinContent(firedLayers +1) * scale
    eff = firedLayersEventCntOmtfEff.GetBinContent(firedLayers +1) / effNorm
    
    fullRate += rate
    eff_rate = 10000000
    if rate > 0 :
        eff_rate = eff/(rate ) #* rate

    #if eff > 0 :
    #    eff_rate = rate/eff #eff/rate

    if rate > 0 or eff > 0:
        if firedLayers in quality_1 :
            quality_1_rate += rate;
            qulaity_1_eff += eff
            
            if rate == 0:
                eff_rate = 0
                
            firedLayersStatQuality_1.append( (firedLayers, rate, eff, eff_rate) )
        else :
            #if rate >= 20: #<<<<<<<<<<<<<<<<,todo tune depanding on the statistics
            if firedLayersEventCntOmtfRate.GetBinContent(firedLayers +1) >= 2 :
                firedLayersStat.append( (firedLayers, rate, eff, eff_rate) )
                #print("%8i %018i %f" % (firedLayers, firedLayers,  rate) ) 
                #print("%8i %s rate: %8.1f eff: %.5f ratio %f" % (firedLayers, format(firedLayers, '018b'), rate, eff, eff_rate) ) 

print("fullRate", fullRate)
print("quality_1_rate", quality_1_rate)
print("qulaity_1_eff", qulaity_1_eff)

print("\nselected\n")
firedLayersStat.sort(key = lambda x: x[3], reverse = False)  

totalRateDrop = 0
totalEff = 0

totalEff10 = 0

for firedLayerStat in firedLayersStatQuality_1 :
    totalRateDrop += firedLayerStat[1]
    totalEff  += firedLayerStat[2]
    print("%8i %s rate: %8.1f eff: %.5f ratio %f totalEff %f totalRateDrop %f fullRate %f " % (firedLayerStat[0], format(firedLayerStat[0], '018b'),  firedLayerStat[1], firedLayerStat[2], firedLayerStat[3], totalEff, totalRateDrop, fullRate - totalRateDrop) ) 

print()

for firedLayerStat in firedLayersStat :
    #print (format(firedLayerStat[0], '018b'), firedLayerStat)
    if (firedLayerStat[1] > -1 and firedLayerStat[2] < 0.003) :
    #if (firedLayerStat[1] > 150) or (firedLayerStat[2] < 0.0001 and firedLayerStat[1] > 100): #rate > 100
        totalRateDrop += firedLayerStat[1]
        totalEff  += firedLayerStat[2]
        if firedLayerStat[1]: #if rate not 0
            print("%8i %s rate: %8.1f eff: %.5f ratio %f totalEff %f totalRateDrop %f fullRate %f " % (firedLayerStat[0], format(firedLayerStat[0], '018b'),  firedLayerStat[1], firedLayerStat[2], firedLayerStat[3], totalEff, totalRateDrop, fullRate - totalRateDrop) ) 
        #print("%s" % (format(firedLayerStat[0], '018b')) ) 
#         if ((firedLayerStat[0] & 0x3) ^ 0x2 ) == 0:
#             print("aaaaaaaaaaaaaaaaaaaaa")
#             totalEff10 += firedLayerStat[2]
# 
#         if ((firedLayerStat[0] & 0b1100) ^ 0b1000 ) == 0:
#             print("aaaaaaaaaaaaaaaaaaaaa")
#             totalEff10 += firedLayerStat[2]
#             
#         if ((firedLayerStat[0] & 0b110000) ^ 0b100000 ) == 0:
#             print("aaaaaaaaaaaaaaaaaaaaa")
#             totalEff10 += firedLayerStat[2]

print ("totalEff10 " , totalEff10) 
#execfile('ratePlots.py')
