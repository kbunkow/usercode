# -*- coding: utf-8 -*-
import FWCore.ParameterSet.Config as cms
process = cms.Process("L1TMuonEmulation")
import os
import sys
import re
from os import listdir
from os.path import isfile, join
import fnmatch


process.load("FWCore.MessageLogger.MessageLogger_cfi")

verbose = True

useExtraploationAlgo = True

version = 't30__'

if useExtraploationAlgo :
    #version = version + 'Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27'
    version = version + 'Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_gpFinalize10'
    #version = version + 'Patterns_ExtraplMB1nadMB2FullAlgo_t16_classProb17_recalib2_gpFinalize10'
else :
    version = version + 'Patterns_0x00012'

customize_omtf = False

runDebug = "DEBUG" # or "INFO" DEBUG
#useExtraploationAlgo = True


analysisType = "efficiency" # or rate
  
for a in sys.argv :
    if a == "efficiency" or a ==  "rate" or a == "withTrackPart" :
        analysisType = a
        break;
    
filesNameLike = sys.argv[1]
    
outFilesName = 'omtfAnalysis2_' 
if analysisType == "efficiency" :
    outFilesName = outFilesName + "eff_"
elif analysisType == "rate" :
    outFilesName = outFilesName + "rate_"    
    
if ("NeutrinoGun" in filesNameLike) or ("MinBias" in filesNameLike): 
    outFilesName = 'omtfAnalysis2_'  + "rate_"
    
outFilesName = outFilesName + version + "__" + filesNameLike

if(runDebug == "DEBUG") :
    outFilesName = outFilesName + "_test10b"

if verbose: 
    process.MessageLogger = cms.Service("MessageLogger",
       #suppressInfo       = cms.untracked.vstring('AfterSource', 'PostModule'),
       destinations   = cms.untracked.vstring(
                                               #'detailedInfo',
                                               #'critical',
                                               #'cout',
                                               #'cerr',
                                               'omtfEventPrint'
                    ),
       categories        = cms.untracked.vstring( 'OMTFReconstruction', 'l1tOmtfEventPrint', 'l1MuonAnalyzerOmtf'), #'l1tOmtfEventPrint', 'l1MuonAnalyzerOmtf'
       omtfEventPrint = cms.untracked.PSet(    
                         filename  = cms.untracked.string(outFilesName),
                         extension = cms.untracked.string('.txt'),                
                         threshold = cms.untracked.string("INFO"), #DEBUG
                         default = cms.untracked.PSet( limit = cms.untracked.int32(0) ), 
                         #INFO   =  cms.untracked.int32(0),
                         #DEBUG   = cms.untracked.int32(0),
                         l1tOmtfEventPrint = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                         OMTFReconstruction = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                         l1MuonAnalyzerOmtf = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                       ),
       debugModules = cms.untracked.vstring('L1MuonAnalyzerOmtf', 'simOmtfDigis', 'omtfParamsSource', 'omtfParams', "esProd", 'L1TMuonOverlapPhase1ParamsESProducer') #'L1MuonAnalyzerOmtf',
       #debugModules = cms.untracked.vstring('*')
    )

    #process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
if not verbose:
    process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False), 
                                         #SkipEvent = cms.untracked.vstring('ProductNotFound') 
                                     )
    
    
process.load('Configuration.Geometry.GeometryExtended2023Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023_cff')
############################
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')    
    
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
#process.load('Configuration.Geometry.GeometryExtended2026D41Reco_cff')
#process.load('Configuration.Geometry.GeometryExtended2026D41_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
#process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgradePLS3', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '103X_upgrade2023_realistic_v2', '') 
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_mc_FULL', '') 

chosenFiles = []

fileCnt = 100000 #1000 

 
       
if filesNameLike == "SingleMu_9_3_14_FullEta_v2" :    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cscBx = 6
    matchUsingPropagation  = False 
    paths = [
        '/eos/user/a/akalinow/Data/SingleMu/9_3_14_FullEta_v2/'
        ]  
    # fileCnt = 10 #<<<<<<!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if filesNameLike == 'mcWaw_2024_01_03_OneOverPt' :
    cscBx = 8
    matchUsingPropagation  = False 
    paths = [    
             {"path": "/eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_03_01_2024/", "fileCnt" : 500}, #1000 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_03_01_2024/", "fileCnt" : 500} #1000 files
             ]
    #fileCnt = 10 #<<<<<<!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if filesNameLike == 'mcWaw2023_OneOverPt_and_iPt2':
    cscBx = 8
    matchUsingPropagation  = False 
    paths = [
             # {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_20_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_20_04_2023/", "fileCnt" : 500}, #500 files only negative eta
             # {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_20_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_20_04_2023/", "fileCnt" : 500}, #500 files
             # #
             # {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_14_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_14_04_2023/", "fileCnt" : 500}, #500 files
             # {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_14_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_14_04_2023/", "fileCnt" : 500}, #500 files
             # #
             # {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_04_04_2023/", "fileCnt" : 500}, #500 files
             # {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_04_04_2023/", "fileCnt" : 500}, #500 files
             #
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_22_02_2023/", "fileCnt" : 500}, #200 files full eta
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_22_02_2023/", "fileCnt" : 500}, #200 files
             #
             #{"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_15_02_2023/", "fileCnt" : 500}, ##100 files
             #{"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_15_02_2023/", "fileCnt" : 500}, ##100 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt2_12_5_2_p1_04_04_2023/", "fileCnt" : 200}, #500 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_iPt2_12_5_2_p1_04_04_2023/", "fileCnt" : 200}, #500 files
             ]

if filesNameLike == "DYToLL_Phase2Spring23_PU200" :
    cscBx = 8
    matchUsingPropagation  = True 
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/DYToLL_M-50_TuneCP5_14TeV-pythia8/crab_DYToLL_M-50_TuneCP5_14TeV-pythia8_Phase2Spring23DIGIRECOMiniAOD-PU200/", "fileCnt" : 10000}, #1000 files
             ]
 
if filesNameLike == "ZprimeToMuMu_Phase2Spring23_PU200" :
    cscBx = 8
    matchUsingPropagation  = True 
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/crab_ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8_Phase2Spring23DIGIRECOMiniAOD-PU200/", "fileCnt" : 10000}, #1000 files
             ] 
 
 
    
if filesNameLike == "EfeMC_HTo2LongLivedTo2mu2jets" :    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cscBx = 8
    matchUsingPropagation  = True 
    paths = [
        {"path": '/eos/cms/store/user/eyigitba/dispDiMu/crabOut/CRAB_PrivateMC/', "fileCnt" : 10000},
        ]   
    
if filesNameLike == "Displaced_Dxy5m_pT0To1000_condRun3" :    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cscBx = 8
    matchUsingPropagation  = False 
    paths = [
        {"path": '/eos/user/a/akalinow/Data/SingleMu/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch0_iPt0_Run2023_13_1_0_23_11_2023', "fileCnt" : 100},
        {"path": '/eos/user/a/akalinow/Data/SingleMu/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch0_iPt1_Run2023_13_1_0_23_11_2023', "fileCnt" : 100},
        {"path": '/eos/user/a/akalinow/Data/SingleMu/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch0_iPt2_Run2023_13_1_0_23_11_2023', "fileCnt" : 100},
        {"path": '/eos/user/a/akalinow/Data/SingleMu/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch2_iPt0_Run2023_13_1_0_23_11_2023', "fileCnt" : 100},
        {"path": '/eos/user/a/akalinow/Data/SingleMu/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch2_iPt1_Run2023_13_1_0_23_11_2023', "fileCnt" : 100},
        {"path": '/eos/user/a/akalinow/Data/SingleMu/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch2_iPt2_Run2023_13_1_0_23_11_2023', "fileCnt" : 100},
        ]   
    
if filesNameLike == "MinBias_Phase2Spring23_PU140" :   
    cscBx = 8 
    matchUsingPropagation  = False 
    regeneratedL1DT = True
    paths = [
        {"path": '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/MinBias_TuneCP5_14TeV-pythia8/crab_MinBias_TuneCP5_14TeV-pythia8_Phase2Spring23DIGIRECOMiniAOD-PU140/', "fileCnt" : 10000},
        ]   
    analysisType = "rate"    
    
if filesNameLike == "MinBias_Phase2Spring23_PU200" :   
    cscBx = 8 
    matchUsingPropagation  = False 
    regeneratedL1DT = True
    paths = [
        {"path": '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/MinBias_TuneCP5_14TeV-pythia8/crab_MinBias_TuneCP5_14TeV-pythia8_Phase2Spring23DIGIRECOMiniAOD-PU200/', "fileCnt" : 10000},
        ]   
    analysisType = "rate" 
    
        
print("input data paths", paths)        

if(runDebug == "DEBUG") :
    fileCnt = 10;
        
for path in paths :
    root_files = []
    for root, dirs, files in os.walk(path["path"]):
        for file in fnmatch.filter(files, '*.root'):
            root_files.append(os.path.join(root, file))  
            
    file_num = 0    
    for root_file in root_files :
        if isfile(root_file) :
            chosenFiles.append('file://' + root_file)
            file_num += 1
        else :
            print("file not found!!!!!!!: " + root_file)   
            
        if file_num >= path["fileCnt"] :
            break         
        if file_num >= fileCnt :
            break            

print("chosenFiles")
for chFile in chosenFiles:
    print(chFile)


print("chosen file count", len(chosenFiles) )

if len(chosenFiles) == 0 :
    print("no files selected!!!!!!!!!!!!!!!")
    exit

print("running version", version)
print("analysisType", analysisType)
print("outFilesName", outFilesName)

firstEv = 0#40000
#nEvents = 1000

# input files (up to 255 files accepted)
process.source = cms.Source('PoolSource',
fileNames = cms.untracked.vstring( 
    #'file:/eos/user/k/kbunkow/cms_data/SingleMuFullEta/721_FullEta_v4/SingleMu_16_p_1_1_xTE.root',
    #'file:/afs/cern.ch/user/k/kpijanow/Neutrino_Pt-2to20_gun_50.root',
    list(chosenFiles), ),
    skipEvents =  cms.untracked.uint32(0),
    inputCommands=cms.untracked.vstring(
        'keep *',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
        'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016s_simEmtfDigis__HLT')
)
	                    
if(runDebug == "DEBUG") :
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000))
else :
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))


####Event Setup Producer
if useExtraploationAlgo :
    process.load('L1Trigger.L1TMuonOverlapPhase1.fakeOmtfParams_extrapolSimple_cff')
else: 
    process.load('L1Trigger.L1TMuonOverlapPhase1.fakeOmtfParams_cff')
    
# process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
#    toGet = cms.VPSet(
#       cms.PSet(record = cms.string('L1TMuonOverlapParamsRcd'),
#                data = cms.vstring('L1TMuonOverlapParams'))
#                    ),
#    verbose = cms.untracked.bool(False)
# )

process.TFileService = cms.Service("TFileService", fileName = cms.string(outFilesName + '.root'), closeFileFast = cms.untracked.bool(True) )
                                   
####OMTF Emulator
process.load('L1Trigger.L1TMuonOverlapPhase1.simOmtfDigis_cfi') 

if(runDebug == "DEBUG") :
    process.simOmtfDigis.dumpResultToXML = cms.bool(True)
    process.simOmtfDigis.XMLDumpFileName = cms.string("TestEvents__" + outFilesName + ".xml")
else :
    process.simOmtfDigis.dumpResultToXML = cms.bool(False)


if(runDebug == "DEBUG") :
    process.simOmtfDigis.eventCaptureDebug = cms.bool(True)
else :
    process.simOmtfDigis.eventCaptureDebug = cms.bool(False)    
#process.simOmtfDigis.simTracksTag = cms.InputTag('g4SimHits')

#needed only for the hits dumper
#process.simOmtfDigis.simTracksTag = cms.InputTag('g4SimHits')
#process.simOmtfDigis.simVertexesTag = cms.InputTag('g4SimHits')
#process.simOmtfDigis.muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root")


process.simOmtfDigis.dumpHitsToROOT = cms.bool(False)
process.simOmtfDigis.candidateSimMuonMatcher = cms.bool(False)


if customize_omtf :
    #process.simOmtfDigis.sorterType = cms.string("byLLH")
    #process.simOmtfDigis.ghostBusterType = cms.string("byRefLayer") # byLLH byRefLayer GhostBusterPreferRefDt
    
    if useExtraploationAlgo :
        #process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/Patterns_layerStat_ExtraplMB1nadMB2_t10_classProb17_recalib2_test.xml")
        #process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/Patterns_ExtraplMB1nadMB2Simplified_t14_classProb17_recalib2.xml")
        #process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/Patterns_ExtraplMB1nadMB2FullAlgo_t16_classProb17_recalib2.xml")
        #process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2.xml")
        process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_minDP0_v3.xml")
        #process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2Simplified_t27_DTQ_4_4_mcWaw2023_OneOverPt_and_iPt2_classProb17_recalib2.xml")
        #process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_0x0021_ExtraplMB1nadMB2Simplified_t27_DTQ_4_4_mcWaw2023_OneOverPt_and_iPt2_classProb22_recalib2.xml")
    else :
        process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_0x00012_oldSample_3_30Files_grouped1_classProb17_recalib2.xml")
    
    print(process.simOmtfDigis.patternsXMLFile)
      
    process.simOmtfDigis.rpcMaxClusterSize = cms.int32(3)
    process.simOmtfDigis.rpcMaxClusterCnt = cms.int32(2)
    process.simOmtfDigis.rpcDropAllClustersIfMoreThanMax = cms.bool(True)
    
    
    process.simOmtfDigis.noHitValueInPdf = cms.bool(True)
    
    process.simOmtfDigis.lctCentralBx = cms.int32(cscBx);#<<<<<<<<<<<<<<<<!!!!!!!!!!!!!!!!!!!!TODO this was changed in CMSSW 10(?) to 8. if the data were generated with the previous CMSSW then you have to use 6
    
    if useExtraploationAlgo :
        process.simOmtfDigis.dtRefHitMinQuality =  cms.int32(4)
    
        process.simOmtfDigis.usePhiBExtrapolationFromMB1 = cms.bool(True)
        process.simOmtfDigis.usePhiBExtrapolationFromMB2 = cms.bool(True)
        
        process.simOmtfDigis.goldenPatternResultFinalizeFunction = cms.int32(10) #valid values are 0, 1, 2, 3, 5
        
        process.simOmtfDigis.minDtPhiQuality = cms.int32(2)
        process.simOmtfDigis.minDtPhiBQuality = cms.int32(4) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!!!!!!!!!!
        
        #process.simOmtfDigis.useEndcapStubsRInExtr  = cms.bool(True)   #TODO REMOVE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        #process.simOmtfDigis.useFloatingPointExtrapolation  = cms.bool(False)
        #process.simOmtfDigis.extrapolFactorsFilename = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/ExtrapolationFactors_withQAndEta.xml")
    else :
        process.simOmtfDigis.minDtPhiQuality = cms.int32(2)
        process.simOmtfDigis.minDtPhiBQuality = cms.int32(2) #in 2023 it was 2, but 4 reduces the rate  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!!!!!!!!!!
         
#process.simOmtfDigis.stubEtaEncoding = cms.string("valueP1Scale")  
#process.simOmtfDigis.stubEtaEncoding = cms.string("bits")   

#process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
#process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

#process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
#process.load("Configuration.StandardSequences.MagneticField_38T_cff")

process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")


if matchUsingPropagation :
    process.L1MuonAnalyzerOmtf= cms.EDAnalyzer("L1MuonAnalyzerOmtf", 
                                 etaCutFrom = cms.double(0.82), #OMTF eta range
                                 etaCutTo = cms.double(1.24),
                                 L1OMTFInputTag  = cms.InputTag("simOmtfDigis","OMTF"),
                                 #nn_pThresholds = cms.vdouble(nn_pThresholds), 
                                 analysisType = cms.string(analysisType),
                                 
                                 simTracksTag = cms.InputTag('g4SimHits'),
                                 simVertexesTag = cms.InputTag('g4SimHits'),
                                 
                                 matchUsingPropagation = cms.bool(matchUsingPropagation),
                                 muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root") #if you want to make this file, remove this entry#if you want to make this file, remove this entry
                                 #muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_noPropagation_t74.root")
                                 )
elif analysisType == "efficiency":
    process.L1MuonAnalyzerOmtf= cms.EDAnalyzer("L1MuonAnalyzerOmtf", 
                                 etaCutFrom = cms.double(0.82), #OMTF eta range
                                 etaCutTo = cms.double(1.24),
                                 L1OMTFInputTag  = cms.InputTag("simOmtfDigis","OMTF"),
                                 #nn_pThresholds = cms.vdouble(nn_pThresholds), 
                                 analysisType = cms.string(analysisType),
                                                                  
                                 simTracksTag = cms.InputTag('g4SimHits'),
                                 simVertexesTag = cms.InputTag('g4SimHits'),
                                 matchUsingPropagation = cms.bool(matchUsingPropagation), #if this is defined, useMatcher is true, for rate analysis this mus be removed, but for efficiency is needed
                                 muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root")                                     
                                )
elif analysisType == "rate":
    process.L1MuonAnalyzerOmtf= cms.EDAnalyzer("L1MuonAnalyzerOmtf", 
                                 etaCutFrom = cms.double(0.82), #OMTF eta range
                                 etaCutTo = cms.double(1.24),
                                 L1OMTFInputTag  = cms.InputTag("simOmtfDigis","OMTF"),
                                 #nn_pThresholds = cms.vdouble(nn_pThresholds), 
                                 analysisType = cms.string(analysisType),
                                                                  
                                 simTracksTag = cms.InputTag('g4SimHits'),
                                 simVertexesTag = cms.InputTag('g4SimHits'),
                                 #matchUsingPropagation = cms.bool(matchUsingPropagation), #if this is defined, useMatcher is true, for rate analysis this mus be removed, but for efficiency is needed
                                 muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root"),
                                 phase = cms.int32(2)                                    
                                )
    
process.l1MuonAnalyzerOmtfPath = cms.Path(process.L1MuonAnalyzerOmtf)


process.L1TMuonSeq = cms.Sequence( #process.esProd+        
                                   process.simOmtfDigis 
                                   #+ process.dumpED
                                   #+ process.dumpES
)

process.L1TMuonPath = cms.Path(process.L1TMuonSeq)

process.schedule = cms.Schedule(process.L1TMuonPath, process.l1MuonAnalyzerOmtfPath)

#process.out = cms.OutputModule("PoolOutputModule", 
#   fileName = cms.untracked.string("l1tomtf_superprimitives1.root")
#)

#process.output_step = cms.EndPath(process.out)
#process.schedule = cms.Schedule(process.L1TMuonPath)
#process.schedule.extend([process.output_step])
