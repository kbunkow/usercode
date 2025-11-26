# -*- coding: utf-8 -*-
import FWCore.ParameterSet.Config as cms
process = cms.Process("L1TMuonEmulation")
import os
import sys
import re
from os import listdir
from os.path import isfile, join
import fnmatch
import argparse

process.load("FWCore.MessageLogger.MessageLogger_cfi")

verbose = True

test_mode = False

dumpHitsToROOT = True

run3_digis = False

parser = argparse.ArgumentParser()

analysisType = "efficiency"
filesNameLike = ""
genParticlesType = "simTrack"

parser.add_argument("-f", "--filesNameLike")
parser.add_argument("-a", "--analysisType", choices=["efficiency", "rate"])
args = parser.parse_args()

if args.filesNameLike :
    filesNameLike = args.filesNameLike

print("filesNameLike", filesNameLike)


if args.analysisType :
    analysisType = args.analysisType


if analysisType == "efficiency" :
    candidateSimMuonMatcherType = "simpleMatching"
elif analysisType == "rate" :
    #candidateSimMuonMatcherType = "simplePropagation"
    candidateSimMuonMatcherType = "withPropagator"
    genParticlesType = "trackingParticle" 
    

useExtraploationAlgo = True

version = 't40__'

if useExtraploationAlgo :
    #version = version + 'Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27'
    #version = version + 'Patterns_ExtraplMB1nadMB2SimplifiedFP_t17_classProb17_recalib2_gpFinalize10'
    #version = version + 'Patterns_ExtraplMB1nadMB2FullAlgo_t16_classProb17_recalib2_gpFinalize10'
    version = version + 'Phase1_2024'
else :
    version = version + 'Patterns_0x00012'

customize_omtf = False

log_threshold = 'INFO'
if test_mode :
    version = version + "_test30c_"
    log_threshold = 'DEBUG'
    #log_threshold = 'INFO' ####<<<<<<<<<<<<<<<<<<<<<<,




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
                         filename  = cms.untracked.string('omtfAnalysis2_' + version + "_" + filesNameLike),
                         extension = cms.untracked.string('.txt'),                
                         threshold = cms.untracked.string(log_threshold),
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
    process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10000)
    process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')
    process.MessageLogger.cerr.l1tOmtfEventPrint = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) )
    process.MessageLogger.cerr.OMTFReconstruction = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) )
    process.MessageLogger.cerr.l1MuonAnalyzerOmtf = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) )
    
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False), 
                                         #SkipEvent = cms.untracked.vstring('ProductNotFound') 
                                     )
    
    
process.load('Configuration.Geometry.GeometryExtended2025Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2025_cff')
############################
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')    
    
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.MagneticField_cff')
#process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgradePLS3', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '103X_upgrade2023_realistic_v2', '') 
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_mc_FULL', '') 

chosenFiles = []

cscBx = 8
#file_cnt = 100000
fileCnt = 100000 #1000 
#fileCnt = 5 #1000 
paths = []

if filesNameLike == 'mcWaw2023_iPt2_04_04_2023' :
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [
             #"{/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch0_iPt0_12_5_2_p1_22_02_2023/", "fileCnt" : 500}, 100files
             #{"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch2_iPt0_12_5_2_p1_22_02_2023/", "fileCnt" : 500},
             #{"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch0_iPt0_12_5_2_p1_15_02_2023/", "fileCnt" : 500},
             #{"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch2_iPt0_12_5_2_p1_15_02_2023/", "fileCnt" : 500},
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt2_12_5_2_p1_04_04_2023/", "fileCnt" : 500}, #500 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_iPt2_12_5_2_p1_04_04_2023/", "fileCnt" : 500},#500 files
             ]

if filesNameLike == 'mcWaw2023_iPt1_04_04_2023' :
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [
             #"{/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch0_iPt0_12_5_2_p1_22_02_2023/", "fileCnt" : 500}, 100files
             #{"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch2_iPt0_12_5_2_p1_22_02_2023/", "fileCnt" : 500},
             #{"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch0_iPt0_12_5_2_p1_15_02_2023/", "fileCnt" : 500},
             #{"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch2_iPt0_12_5_2_p1_15_02_2023/", "fileCnt" : 500},
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt1_12_5_2_p1_04_04_2023/", "fileCnt" : 500}, #500 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_iPt1_12_5_2_p1_04_04_2023/", "fileCnt" : 500},#500 files
             ]

if filesNameLike == 'mcWaw_2024_04_03_OneOverPt' :
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/13_1_0_03_04_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_03_04_2024/", "fileCnt" : 10000},#1000 files
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/13_1_0_03_04_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_03_04_2024/", "fileCnt" : 10000},#1000 files
             ]

#negaive eta only  
if filesNameLike == 'mcWaw_2024_03_11_OneOverPt' :
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/13_1_0_11_03_2024/SingleMu_ch0_OneOverPt_Run2023_13_1_0_11_03_2024/", "fileCnt" : 10000},#1000 files
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/13_1_0_11_03_2024/SingleMu_ch2_OneOverPt_Run2023_13_1_0_11_03_2024/", "fileCnt" : 10000},#1000 files
             ]
    
if filesNameLike == 'mcWaw_2023_04_20_OneOverPt' : #mcWaw2023_OneOverPt_allfiles
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_20_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_20_04_2023/", "fileCnt" : 500},#500 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_20_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_20_04_2023/", "fileCnt" : 500},#500 files
             ]

if filesNameLike == 'mcWaw_2023_04_14_OneOverPt' : #mcWaw2023_OneOverPt_allfiles
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [         
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_14_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_14_04_2023/", "fileCnt" : 500},#500 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_14_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_14_04_2023/", "fileCnt" : 500},#500 files
             ]
    
if filesNameLike == 'mcWaw_2023_04_04_OneOverPt' : #mcWaw2023_OneOverPt_allfiles
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [         
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_04_04_2023/", "fileCnt" : 500},#500 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_04_04_2023/", "fileCnt" : 500},#500 files
             ]    
    
if filesNameLike == 'mcWaw_2023_02_22_OneOverPt' : #mcWaw2023_OneOverPt_allfiles
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [         
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_22_02_2023/", "fileCnt" : 500},#200 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_22_02_2023/", "fileCnt" : 500},#200 files
             ]        
    
if filesNameLike == 'mcWaw_2023_02_15_OneOverPt' : #mcWaw2023_OneOverPt_allfiles
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [         
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_15_02_2023/", "fileCnt" : 500},##100 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_15_02_2023/", "fileCnt" : 500},##100 files
             ]  
       
#negaive eta only  
if filesNameLike == 'mcWaw_2024_01_03_OneOverPt_iPt2' :
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [    
             {"path": "/eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_03_01_2024/", "fileCnt" : 1000},#1000 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_03_01_2024/", "fileCnt" : 1000},#1000 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt2_12_5_2_p1_04_04_2023/", "fileCnt" : 100}, #500 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_iPt2_12_5_2_p1_04_04_2023/", "fileCnt" : 100},#500 files
             ]

#negaive eta only    
if filesNameLike == 'mcWaw_2024_01_04_OneOverPt' :
    candidateSimMuonMatcherType = "simpleMatching"
    paths = [    
             {"path": "/eos/user/a/akalinow/Data/SingleMu/13_1_0_04_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_04_01_2024/", "fileCnt" : 1000},#1000 files
             {"path": "/eos/user/a/akalinow/Data/SingleMu/13_1_0_04_01_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_04_01_2024/", "fileCnt" : 1000},#1000 files
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
    candidateSimMuonMatcherType = "withPropagator"
    paths = [
        #{"path": '/eos/cms/store/user/eyigitba/dispDiMu/crabOut/CRAB_PrivateMC/', "fileCnt" : 10000},
        {"path": '/data2/kbunkow/cmsdata/EfeMC2023_HTo2LongLivedTo2mu2jets/CRAB_PrivateMC/', "fileCnt" : 100000},
        ]  

if filesNameLike == 'Displaced_cTau5m_XTo2LLTo4Mu' :
    candidateSimMuonMatcherType = "withPropagator"
    paths = [
             {"path": "/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_cTau5m_XTo2LLTo4Mu_condPhase2_realistic/XTo2LLPTo4Mu_CTau5m_Phase2Exotic/231203_175643/0000/", "fileCnt" : 500},#500 files
        ]   

if filesNameLike == 'LLPGun_mH20_1000_cTau10_5000mm' :
    candidateSimMuonMatcherType = "withPropagator"
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/eyigitba/crab/LLPGun_mH20_1000_cTau10_5000mm/LLPGun_mH20_1000_cTau10_5000mm_GS_DR_v2/", "fileCnt" : 1000},#100 files
             ]    
    
if filesNameLike == 'Displaced_Dxy3m_pT0To1000_condPhase2_realistic' :
    candidateSimMuonMatcherType = "withPropagator"
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt0_Run2029_13_1_0_01_12_2023", "fileCnt" : 500},#500 files
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch2_iPt0_Run2029_13_1_0_01_12_2023", "fileCnt" : 500},#500 files
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt1_Run2029_13_1_0_01_12_2023", "fileCnt" : 500},#500 files
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch2_iPt1_Run2029_13_1_0_01_12_2023", "fileCnt" : 500},#500 files
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt2_Run2029_13_1_0_01_12_2023", "fileCnt" : 500},#500 files
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch2_iPt2_Run2029_13_1_0_01_12_2023", "fileCnt" : 500},#500 files
             ]   
    
if filesNameLike == 'Displaced_cTau5m_XTo2LLTo4Mu_condPhase2_GP2024' :
    candidateSimMuonMatcherType = "withPropagator"
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/Displaced_cTau5m_XTo2LLTo4Mu_condPhase2_GP2024/", "fileCnt" : 10000},#995 files
             ]    
    
if filesNameLike == '14_1_0pre3_11_06_2024_Dxy5m_PhaseII' :
    candidateSimMuonMatcherType = "withPropagator"
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/14_1_0pre3_11_06_2024_Dxy5m_PhaseII/", "fileCnt" : 10000},#2311 files
             ]  
    
if filesNameLike == 'MinBias_Phase2Spring23_PU200' :
    candidateSimMuonMatcherType = "collectMuonCands"
    genParticlesType = "" 
    analysisType = "rate" # or rate efficiency
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/ThinnedOfficialMC/MinBias_TuneCP5_14TeV-pythia8/crab_MinBias_TuneCP5_14TeV-pythia8_Phase2Spring23DIGIRECOMiniAOD-PU200/", "fileCnt" : 10000},#2311 files
             ]      
           
    
if filesNameLike == 'MinBias_Phase2Spring23_PU140' :
    candidateSimMuonMatcherType = "collectMuonCands"
    genParticlesType = "" 
    analysisType = "rate" # or rate efficiency
    paths = [    
             {"path": "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/ThinnedOfficialMC/MinBias_TuneCP5_14TeV-pythia8/crab_MinBias_TuneCP5_14TeV-pythia8_Phase2Spring23DIGIRECOMiniAOD-PU140/", "fileCnt" : 10000},#2311 files
             ]  
    
if filesNameLike == 'EphemeralZeroBias7_Run2025G' :
    candidateSimMuonMatcherType = "collectMuonCands"
    genParticlesType = "" 
    analysisType = "rate" # or rate efficiency
    run3_digis = True
    paths = [
             {"path": "/eos/home-k/kbunkow/cms_data/run3_data/muon_digi_EphemeralZeroBias7_Run2025G-v1/", "fileCnt" : 10000},#2311 files
        ]   
    
if filesNameLike == "test":
    paths = [ ]

if test_mode :
    fileCnt = 1
        
print("input data paths", paths)        

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
            
        if file_num > path["fileCnt"] :
            break         
        if file_num >= fileCnt :
            break            

if filesNameLike == "test":
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt2_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084329/0000/SingleMu_iPt_2_m_212.root')
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_14_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_14_04_2023/12_5_2_p1_14_04_2023/230414_115927/0000/SingleMu_OneOverPt_1_100_m_472.root')
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt2_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084329/0000/SingleMu_iPt_2_m_431.root')
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_03_01_2024/13_1_0_03_01_2024/240103_094044/0000/SingleMu_OneOverPt_1_100_m_770.root')    
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_03_01_2024/13_1_0_03_01_2024/240103_094121/0000/SingleMu_OneOverPt_1_100_p_299.root')      
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_03_01_2024/13_1_0_03_01_2024/240103_094121/0000/SingleMu_OneOverPt_1_100_p_3.root')    
        
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_03_01_2024/13_1_0_03_01_2024/240103_094044/0000/SingleMu_OneOverPt_1_100_m_289.root')
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_03_01_2024/13_1_0_03_01_2024/240103_094044/0000/SingleMu_OneOverPt_1_100_m_29.root')
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_03_01_2024/13_1_0_03_01_2024/240103_094044/0000/SingleMu_OneOverPt_1_100_m_290.root')
    #chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_03_01_2024/13_1_0_03_01_2024/240103_094044/0000/SingleMu_OneOverPt_1_100_m_291.root')
    chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_03_01_2024/13_1_0_03_01_2024/240103_094121/0000/SingleMu_OneOverPt_1_100_p_656.root')
    
    #chosenFiles.append('file:///afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_16_x_x/CMSSW_16_0_0_pre1/src/L1Trigger/L1TMuonOverlapPhase1/test/omtfStage2Digis_output.root')
    candidateSimMuonMatcherType = "collectMuonCands"
    genParticlesType = "" 
    analysisType = "rate" # or rate efficiency

   
if filesNameLike == "MinBias_Phase2Spring24":
    candidateSimMuonMatcherType = "withPropagator"
    genParticlesType = "trackingParticle" 
    
    analysisType = "rate" # or rate efficiency
    chosenFiles.append('/store/mc/Phase2Spring24DIGIRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200ALCA_140X_mcRun4_realistic_v4-v2/120000/004dd3c5-29c9-4283-95f3-baf57220dce2.root')
    chosenFiles.append('/store/mc/Phase2Spring24DIGIRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200ALCA_140X_mcRun4_realistic_v4-v2/120000/004f52f5-5cac-4a87-ab4d-ac7fcea30858.root')
    chosenFiles.append('/store/mc/Phase2Spring24DIGIRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200ALCA_140X_mcRun4_realistic_v4-v2/120000/00be05a9-68a9-4947-b279-39f694cd536c.root')

print("analysisType", analysisType)
   
print("chosenFiles")
for chFile in chosenFiles:
    print(chFile)

print("number of chosen files:", len(chosenFiles))

if len(chosenFiles) == 0 :
    print("no files selected!!!!!!!!!!!!!!!")
    exit

print("running version", version)
print(filesNameLike)
print("dumpHitsToROOT", dumpHitsToROOT)

firstEv = 0#40000
#nEvents = 1000

# input files (up to 255 files accepted)
process.source = cms.Source('PoolSource',
fileNames = cms.untracked.vstring( 
    *(list(chosenFiles)) ),
    skipEvents =  cms.untracked.uint32(0),
    inputCommands=cms.untracked.vstring(
        'keep *',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
        'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016s_simEmtfDigis__HLT')
)
	                    
if test_mode : 
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000))
else :
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10))

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

process.TFileService = cms.Service("TFileService", fileName = cms.string('omtfAnalysis2_' + version + "_" + filesNameLike +'.root'), closeFileFast = cms.untracked.bool(True) )

#needed by candidateSimMuonMatcher
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")
                                   
####OMTF Emulator
process.load('L1Trigger.L1TMuonOverlapPhase1.simOmtfDigis_cfi') 

if run3_digis :
    process.simOmtfDigis.srcDTPh = cms.InputTag('omtfStage2Digis')
    process.simOmtfDigis.srcDTTh = cms.InputTag('omtfStage2Digis')
    process.simOmtfDigis.srcCSC = cms.InputTag('omtfStage2Digis')
    process.simOmtfDigis.srcRPC = cms.InputTag('omtfStage2Digis')

process.simOmtfDigis.candidateSimMuonMatcher = cms.bool(True)
#process.simOmtfDigis.muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root")
process.simOmtfDigis.muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/deltaPhi_cand_simMu.root")

if genParticlesType == "trackingParticle" :
    process.simOmtfDigis.trackingParticleTag = cms.InputTag("mix", "MergedTrackTruth")
    #process.simOmtfDigis.trackingParticleTag = cms.InputTag("prunedTrackingParticles")
    
elif genParticlesType == "simTrack" :
    process.simOmtfDigis.simTracksTag = cms.InputTag('g4SimHits')
    process.simOmtfDigis.simVertexesTag = cms.InputTag('g4SimHits')


process.simOmtfDigis.dumpResultToXML = cms.bool(test_mode)
process.simOmtfDigis.XMLDumpFileName = cms.string("TestEvents__" + version + "_" + filesNameLike + ".xml")
process.simOmtfDigis.dumpHitsToROOT = cms.bool(dumpHitsToROOT)
process.simOmtfDigis.dumpKilledOmtfCands = cms.bool(False)
process.simOmtfDigis.eventCaptureDebug = cms.bool(test_mode)


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

process.simOmtfDigis.candidateSimMuonMatcherType = cms.string(candidateSimMuonMatcherType)

process.L1MuonAnalyzerOmtf = cms.EDAnalyzer("L1MuonAnalyzerOmtf", 
                                 etaCutFrom = cms.double(0.82), #OMTF eta range
                                 etaCutTo = cms.double(1.24),
                                 L1OMTFInputTag  = cms.InputTag("simOmtfDigis","OMTF"),
                                 #nn_pThresholds = cms.vdouble(nn_pThresholds), 
                                 analysisType = cms.string(analysisType),
                                 
                                 #simTracksTag = cms.InputTag('g4SimHits'),
                                 #simVertexesTag = cms.InputTag('g4SimHits'),
                                 #trackingParticleTag = cms.InputTag("mix", "MergedTrackTruth"),
                                 
                                 #matchUsingPropagation = cms.bool(matchUsingPropagationInAnlyzer),
                                 #muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root"), #if you want to make this file, remove this entry#if you want to make this file, remove this entry
                                 #muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_noPropagation_t74.root")
                                 
                                 candidateSimMuonMatcherType = cms.string(candidateSimMuonMatcherType),
                                 muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/deltaPhi_cand_simMu.root"),
                                 phase = cms.int32(1)
                                 )

if genParticlesType == "trackingParticle" :
    process.L1MuonAnalyzerOmtf.trackingParticleTag = cms.InputTag("mix", "MergedTrackTruth")
    #process.L1MuonAnalyzerOmtf.trackingParticleTag = cms.InputTag("prunedTrackingParticles")
elif genParticlesType == "simTrack" :
    process.L1MuonAnalyzerOmtf.simTracksTag = cms.InputTag('g4SimHits')
    process.L1MuonAnalyzerOmtf.simVertexesTag = cms.InputTag('g4SimHits')

process.l1MuonAnalyzerOmtfPath = cms.Path(process.L1MuonAnalyzerOmtf)

process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
    ignoreTotal = cms.untracked.int32(1)
)

#process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
#process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

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
