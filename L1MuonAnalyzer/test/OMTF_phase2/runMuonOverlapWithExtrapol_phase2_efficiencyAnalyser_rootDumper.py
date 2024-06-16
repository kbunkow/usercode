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

test_mode = False

filesNameLike = sys.argv[1]
print("filesNameLike", filesNameLike)

matchUsingPropagationInAnlyzer  = True 
matchUsingPropagationInDumper  = True #False for SingleM<u without PU, in oter cases when simple matching cannot be used it should be True

regeneratedL1DT = True

minDtPhiQuality = 2
minDtPhiBQuality = 2

version = "ExtraplMB1nadMB2DTQualAndRFixedP__pats_DT_2_4_t30____DT_" + str(minDtPhiQuality) + "_" + str(minDtPhiBQuality)

if test_mode :
    version = version + "_test1"

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
                         threshold = cms.untracked.string('INFO'),
                         default = cms.untracked.PSet( limit = cms.untracked.int32(0) ), 
                         #INFO   =  cms.untracked.int32(0),
                         #DEBUG   = cms.untracked.int32(0),
                         l1tOmtfEventPrint = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                         OMTFReconstruction = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                         l1MuonAnalyzerOmtf = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) )
                       ),
       debugModules = cms.untracked.vstring('simOmtfPhase2Digis', 'L1MuonAnalyzerOmtf') 
       #debugModules = cms.untracked.vstring('*')
    )

    #process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
if not verbose:
    process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10000)
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False), 
                                         #SkipEvent = cms.untracked.vstring('ProductNotFound') 
                                     )
    
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
#process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
#process.load('FWCore.MessageService.MessageLogger_cfi')
#process.load('Configuration.EventContent.EventContent_cff')
#process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D95Reco_cff')
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
file_cnt = 100000

if filesNameLike == 'mcWaw2023_iPt2_04_04_2023' :
    cscBx = 8
    matchUsingPropagationInAnlyzer  = False 
    matchUsingPropagationInDumper  = False 
    paths = [#"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch0_iPt0_12_5_2_p1_22_02_2023/", 100files
             #"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch2_iPt0_12_5_2_p1_22_02_2023/",
             #"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch0_iPt0_12_5_2_p1_15_02_2023/",
             #"/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch2_iPt0_12_5_2_p1_15_02_2023/"
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt2_12_5_2_p1_04_04_2023/", #500 files
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_iPt2_12_5_2_p1_04_04_2023/", #500 files
             ]
    
if filesNameLike == 'mcWaw2023_OneOverPt_allfiles' : #mcWaw2023_OneOverPt_allfiles
    matchUsingPropagationInAnlyzer  = False 
    matchUsingPropagationInDumper  = False 
    paths = [
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_20_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_20_04_2023/", #500 files
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_20_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_20_04_2023/", #500 files
             
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_14_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_14_04_2023/", #500 files
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_14_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_14_04_2023/", #500 files
             
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_04_04_2023/", #500 files
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_04_04_2023/", #500 files
             
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_22_02_2023/", #200 files
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_22_02_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_22_02_2023/", #200 files
             
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch0_OneOverPt_12_5_2_p1_15_02_2023/", ##100 files
             "/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_15_02_2023/", ##100 files
             ]
    
    #only negative eta
if filesNameLike == 'mcWaw_2024_01_03_OneOverPt' :
    matchUsingPropagationInAnlyzer  = False 
    matchUsingPropagationInDumper  = False 
    paths = [    
             "/eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_03_01_2024/", #1000 files
             "/eos/user/a/akalinow/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_03_01_2024/" #1000 files
             ]

#negaive eta only    
if filesNameLike == 'mcWaw_2024_01_04_OneOverPt' :
    matchUsingPropagationInAnlyzer  = False 
    matchUsingPropagationInDumper  = False 
    paths = [    
             "/eos/user/a/akalinow/Data/SingleMu/13_1_0_04_01_2024/SingleMu_ch0_OneOverPt_Run2029_13_1_0_04_01_2024/", #1000 files
             "/eos/user/a/akalinow/Data/SingleMu/13_1_0_04_01_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_04_01_2024/" #1000 files
             ]    

if filesNameLike == 'Displaced_cTau5m_XTo2LLTo4Mu' :
    matchUsingPropagationInAnlyzer  = True 
    matchUsingPropagationInDumper  = True 
    paths = [    
             "/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_cTau5m_XTo2LLTo4Mu_condPhase2_realistic/XTo2LLPTo4Mu_CTau5m_Phase2Exotic/231203_175643/0000/", #500 files
             ]    

if filesNameLike == 'Displaced_Dxy3m_pT0To1000_condPhase2_realistic' :
    matchUsingPropagationInAnlyzer  = True 
    matchUsingPropagationInDumper  = False 
    paths = [    
             "/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt0_Run2029_13_1_0_01_12_2023", #500 files
             "/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch2_iPt0_Run2029_13_1_0_01_12_2023", #500 files
             "/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt1_Run2029_13_1_0_01_12_2023", #500 files
             "/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch2_iPt1_Run2029_13_1_0_01_12_2023", #500 files
             "/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt2_Run2029_13_1_0_01_12_2023", #500 files
             "/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch2_iPt2_Run2029_13_1_0_01_12_2023", #500 files
             ]   
if filesNameLike == "test":
    paths = [ ]

if test_mode :
    file_cnt = 1

print("input data paths", paths)        
    
for path in paths :
    root_files = []
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, '*.root'):
            root_files.append(os.path.join(root, file))  
            
    file_num = 0    
    for root_file in root_files :
        if isfile(root_file) :
            chosenFiles.append('file://' + root_file)
            file_num += 1
        else :
            print("file not found!!!!!!!: " + root_file)   
            
        if file_num >= file_cnt :
            break                 

chosenFiles.append('file:///eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt2_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084329/0000/SingleMu_iPt_2_m_212.root')

    
print("chosenFiles")
for chFile in chosenFiles:
    print(chFile)

print("number of chosen files:", len(chosenFiles))

if len(chosenFiles) == 0 :
    print("no files selected!!!!!!!!!!!!!!! (argumetn should be e.g. 20_p")
    exit 

print("running version", version)
                                 
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
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500))
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

process.TFileService = cms.Service("TFileService", fileName = cms.string('omtfAnalysis2_' + version + "_" + filesNameLike +'.root'), closeFileFast = cms.untracked.bool(True) )


#needed by candidateSimMuonMatcher
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")

####OMTF Emulator
process.load('L1Trigger.L1TMuonOverlapPhase2.simOmtfPhase2Digis_cfi')
#process.simOmtfPhase2Digis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2DTQualAndEtaFixedP_ValueP1Scale_t20_v1_SingleMu_iPt_and_OneOverPt_classProb17_recalib2_minDP0.xml")
process.simOmtfPhase2Digis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2DTQualAndRFixedP_DT_2_4_t30__classProb17_recalib2.xml")

process.simOmtfPhase2Digis.candidateSimMuonMatcher = cms.bool(True)
process.simOmtfPhase2Digis.simTracksTag = cms.InputTag('g4SimHits')
process.simOmtfPhase2Digis.simVertexesTag = cms.InputTag('g4SimHits')
process.simOmtfPhase2Digis.muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root")


process.simOmtfPhase2Digis.dumpResultToXML = cms.bool(False)
process.simOmtfPhase2Digis.dumpHitsToROOT = cms.bool(True)
process.simOmtfPhase2Digis.eventCaptureDebug = cms.bool(False)

process.simOmtfPhase2Digis.cleanStubs = cms.bool(False)

process.simOmtfPhase2Digis.minDtPhiQuality = cms.int32(minDtPhiQuality)
process.simOmtfPhase2Digis.minDtPhiBQuality = cms.int32(minDtPhiBQuality)

#TODO tune the matching thresholds in CandidateSimMuonMatcher::matchSimple
#or CandidateSimMuonMatcher::match
if matchUsingPropagationInDumper == True :
    process.simOmtfPhase2Digis.candidateSimMuonMatcherType = cms.string("propagation")
else :
    process.simOmtfPhase2Digis.candidateSimMuonMatcherType = cms.string("matchSimple")

analysisType = "efficiency" # or rate

process.L1MuonAnalyzerOmtf= cms.EDAnalyzer("L1MuonAnalyzerOmtf", 
                                 etaCutFrom = cms.double(0.82), #OMTF eta range
                                 etaCutTo = cms.double(1.24),
                                 L1OMTFInputTag  = cms.InputTag("simOmtfPhase2Digis","OMTF"),
                                 #nn_pThresholds = cms.vdouble(nn_pThresholds), 
                                 analysisType = cms.string(analysisType),
                                 
                                 simTracksTag = cms.InputTag('g4SimHits'),
                                 simVertexesTag = cms.InputTag('g4SimHits'),
                                 
                                 matchUsingPropagation = cms.bool(matchUsingPropagationInAnlyzer),
                                 muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root"), #if you want to make this file, remove this entry#if you want to make this file, remove this entry
                                 #muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_noPropagation_t74.root")
                                 phase = cms.int32(2)
                                 )

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
else :
    process.L1TMuonPath = cms.Path(process.CalibratedDigis * process.dtTriggerPhase2PrimitiveDigis * process.L1TMuonSeq)
    print("regeneratedL1DT = ", regeneratedL1DT, " process.dtTriggerPhase2PrimitiveDigis")

process.schedule = cms.Schedule(process.L1TMuonPath, process.l1MuonAnalyzerOmtfPath)

#process.out = cms.OutputModule("PoolOutputModule", 
#   fileName = cms.untracked.string("l1tomtf_superprimitives1.root")
#)

#process.output_step = cms.EndPath(process.out)
#process.schedule = cms.Schedule(process.L1TMuonPath)
#process.schedule.extend([process.output_step])
