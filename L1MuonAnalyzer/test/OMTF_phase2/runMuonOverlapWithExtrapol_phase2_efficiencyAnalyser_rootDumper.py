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

test_mode = True

dumpHitsToROOT = True

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
    

regeneratedL1DT = True

useNN = True

#watch out: L1Trigger/L1TMuon/data/omtf_config/ExtrapolationFactors_ExtraplMB1nadMB2DTQualAndR_EtaValueP1Scale_t25c.xml is only for the minDtPhiQuality = 2!!!!!!!!!!!!!!!!!!!
#there are no entries of quality 0 and 1 there!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
minDtPhiQuality = 2
minDtPhiBQuality = 2
dtRefHitMinQuality = 2

version = "ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35____DT_" + str(minDtPhiQuality) + "_" + str(minDtPhiBQuality) + "_" + str(dtRefHitMinQuality) + "_t37" #WK - dumping killed candidates
#version = "ExtraplMB1nadMB2DTQualAndRFixedP__pats_DT_2_2_2_t31____DT_" + str(minDtPhiQuality) + "_" + str(minDtPhiBQuality) + "_" + str(dtRefHitMinQuality) + "_t33"

log_threshold = 'INFO'
if test_mode :
    version = version + "_test21_"
    log_threshold = 'DEBUG'
    #log_threshold = 'INFO' ####<<<<<<<<<<<<<<<<<<<<<<,
    
if useNN :
    version = version + "_NN"
#version = "noExtrapl_ValueP1Scale_t18_qualConverted_min4_ipT1_deltaPhiVsPhiRef_fixedDTScale"

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
       categories        = cms.untracked.vstring('l1tOmtfEventPrint', 'OMTFReconstruction', 'l1MuonAnalyzerOmtf'),
       omtfEventPrint = cms.untracked.PSet(    
                         filename  = cms.untracked.string('omtfAnalysis2_' + version + "_" + filesNameLike),
                         extension = cms.untracked.string('.txt'),                
                         threshold = cms.untracked.string(log_threshold),
                         default = cms.untracked.PSet( limit = cms.untracked.int32(0) ), 
                         #INFO   =  cms.untracked.int32(0),
                         #DEBUG   = cms.untracked.int32(0),
                         l1tOmtfEventPrint = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                         OMTFReconstruction = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                         l1MuonAnalyzerOmtf = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) )
                       ),
       debugModules = cms.untracked.vstring('simOmtfPhase2Digis', 'L1MuonAnalyzerOmtf', 'CalibratedDigis') 
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
    
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
#process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
#process.load('FWCore.MessageService.MessageLogger_cfi')
#process.load('Configuration.EventContent.EventContent_cff')
#process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtendedRun4D110Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
#process.load('Configuration.StandardSequences.RawToDigi_cff')
#process.load('Configuration.StandardSequences.SimL1Emulator_cff')
#process.load('Configuration.StandardSequences.SimPhase2L1GlobalTriggerEmulator_cff')
#process.load('L1Trigger.Configuration.Phase2GTMenus.SeedDefinitions.prototypeSeeds')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '131X_mcRun4_realistic_v9', '')

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
    chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt2_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084329/0000/SingleMu_iPt_2_m_431.root')

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


#Calibrate Digis
process.load("L1Trigger.DTTriggerPhase2.CalibratedDigis_cfi")
process.CalibratedDigis.dtDigiTag = "simMuonDTDigis" 
process.CalibratedDigis.scenario = 0

#DTTriggerPhase2
process.load("L1Trigger.DTTriggerPhase2.dtTriggerPhase2PrimitiveDigis_cfi")
process.dtTriggerPhase2PrimitiveDigis.debug = False
process.dtTriggerPhase2PrimitiveDigis.dump = False
process.dtTriggerPhase2PrimitiveDigis.scenario = 0

process.dtTriggerPhase2PrimitiveDigis.co_option = -1 # coincidence w.r.t. : -1 = off, 0 = co all, 1 = co phi, 2 = co theta. defoult is 1, but for OMTF this coincidence filter has no sense

#using RPC in dtTriggerPhase2PrimitiveDigis has not much sense now
#process.load("RecoLocalMuon.RPCRecHit.rpcRecHits_cfi")
#process.rpcRecHits.rpcDigiLabel = cms.InputTag('simMuonRPCDigis')
#process.dtTriggerPhase2PrimitiveDigis.useRPC = False

process.TFileService = cms.Service("TFileService", fileName = cms.string('omtfAnalysis2_' + version + "_" + filesNameLike +'.root'), closeFileFast = cms.untracked.bool(True) )


#needed by candidateSimMuonMatcher
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")

####OMTF Emulator
process.load('L1Trigger.L1TMuonOverlapPhase2.simOmtfPhase2Digis_cfi')
#process.simOmtfPhase2Digis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0.xml")
#process.simOmtfPhase2Digis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2DTQualAndRFixedP_DT_2_2_t30__classProb17_recalib2.xml")
#process.simOmtfPhase2Digis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2DTQualAndRFixedP_DT_2_2_2_t31__classProb17_recalib2.xml")
#process.simOmtfPhase2Digis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2DTQualAndRFixedP_DT_2_2_4_t34__classProb17_recalib2.xml")

process.simOmtfPhase2Digis.candidateSimMuonMatcher = cms.bool(True)
#process.simOmtfPhase2Digis.muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root")
process.simOmtfPhase2Digis.muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/deltaPhi_cand_simMu.root")

if genParticlesType == "trackingParticle" :
    process.simOmtfPhase2Digis.trackingParticleTag = cms.InputTag("mix", "MergedTrackTruth")
    #process.simOmtfPhase2Digis.trackingParticleTag = cms.InputTag("prunedTrackingParticles")
    
elif genParticlesType == "simTrack" :
    process.simOmtfPhase2Digis.simTracksTag = cms.InputTag('g4SimHits')
    process.simOmtfPhase2Digis.simVertexesTag = cms.InputTag('g4SimHits')


process.simOmtfPhase2Digis.dumpResultToXML = cms.bool(test_mode)
process.simOmtfPhase2Digis.XMLDumpFileName = cms.string("TestEvents__" + version + "_" + filesNameLike + ".xml")
process.simOmtfPhase2Digis.dumpHitsToROOT = cms.bool(dumpHitsToROOT)
process.simOmtfPhase2Digis.dumpKilledOmtfCands = cms.bool(False)
process.simOmtfPhase2Digis.eventCaptureDebug = cms.bool(test_mode)

process.simOmtfPhase2Digis.cleanStubs = cms.bool(False)

process.simOmtfPhase2Digis.minDtPhiQuality = cms.int32(minDtPhiQuality)
process.simOmtfPhase2Digis.minDtPhiBQuality = cms.int32(minDtPhiBQuality)
process.simOmtfPhase2Digis.dtRefHitMinQuality =  cms.int32(dtRefHitMinQuality)
process.simOmtfPhase2Digis.ghostBusterType = cms.string("byRefLayerAndHitQual") #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if useNN :
    process.simOmtfPhase2Digis.neuralNetworkFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/lutNN_omtfRegression_v435_FP.xml")

#TODO tune the matching thresholds in CandidateSimMuonMatcher::matchSimple
#or CandidateSimMuonMatcher::match
#if matchUsingPropagationInDumper == True :
#    process.simOmtfPhase2Digis.candidateSimMuonMatcherType = cms.string("withPropagator")
#else :
#    process.simOmtfPhase2Digis.candidateSimMuonMatcherType = cms.string("matchSimple")
    
process.simOmtfPhase2Digis.candidateSimMuonMatcherType = cms.string(candidateSimMuonMatcherType)

process.L1MuonAnalyzerOmtf = cms.EDAnalyzer("L1MuonAnalyzerOmtf", 
                                 etaCutFrom = cms.double(0.82), #OMTF eta range
                                 etaCutTo = cms.double(1.24),
                                 L1OMTFInputTag  = cms.InputTag("simOmtfPhase2Digis","OMTF"),
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
                                 phase = cms.int32(2)
                                 )

if genParticlesType == "trackingParticle" :
    process.L1MuonAnalyzerOmtf.trackingParticleTag = cms.InputTag("mix", "MergedTrackTruth")
    #process.L1MuonAnalyzerOmtf.trackingParticleTag = cms.InputTag("prunedTrackingParticles")
elif genParticlesType == "simTrack" :
    process.L1MuonAnalyzerOmtf.simTracksTag = cms.InputTag('g4SimHits')
    process.L1MuonAnalyzerOmtf.simVertexesTag = cms.InputTag('g4SimHits')

process.l1MuonAnalyzerOmtfPath = cms.Path(process.L1MuonAnalyzerOmtf)


#process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
#process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

process.L1TMuonSeq = cms.Sequence( process.simOmtfPhase2Digis 
                                   #+ process.dumpED
                                   #+ process.dumpES
)

if not regeneratedL1DT :
    process.L1TMuonPath = cms.Path(process.L1TMuonSeq) ########################################<<<<<<!!!!!!!!!!!!!!!!!!!!!!!!!!!
    print("regeneratedL1DT = ", regeneratedL1DT)
else :                             #process.rpcRecHits *    
    process.L1TMuonPath = cms.Path(process.CalibratedDigis * process.dtTriggerPhase2PrimitiveDigis * process.L1TMuonSeq)
    print("regeneratedL1DT = ", regeneratedL1DT, " process.dtTriggerPhase2PrimitiveDigis")

process.schedule = cms.Schedule(process.L1TMuonPath, process.l1MuonAnalyzerOmtfPath)
#process.schedule = cms.Schedule(process.L1TMuonPath)
#process.out = cms.OutputModule("PoolOutputModule", 
#   fileName = cms.untracked.string("l1tomtf_superprimitives1.root")
#)

#process.output_step = cms.EndPath(process.out)
#process.schedule = cms.Schedule(process.L1TMuonPath)
#process.schedule.extend([process.output_step])
