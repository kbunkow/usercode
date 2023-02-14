# -*- coding: utf-8 -*-
import FWCore.ParameterSet.Config as cms
process = cms.Process("L1TMuonEmulation")
import os
import sys
import re
from os import listdir
from os.path import isfile, join


process.load("FWCore.MessageLogger.MessageLogger_cfi")

verbose = True
version = '130_allFiles'

runDebug = "INFO" # or "INFO" DEBUG
useExtraploationAlgo = True;

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
                         filename  = cms.untracked.string('log_MuonOverlap_newPats_t' + version),
                         extension = cms.untracked.string('.txt'),                
                         threshold = cms.untracked.string(runDebug), #DEBUG
                         default = cms.untracked.PSet( limit = cms.untracked.int32(0) ), 
                         #INFO   =  cms.untracked.int32(0),
                         #DEBUG   = cms.untracked.int32(0),
                         l1tOmtfEventPrint = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                         OMTFReconstruction = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                         l1MuonAnalyzerOmtf = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                       ),
       debugModules = cms.untracked.vstring('L1MuonAnalyzerOmtf', 'simOmtfDigis') #'L1MuonAnalyzerOmtf',
       #debugModules = cms.untracked.vstring('*')
    )

    #process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
if not verbose:
    process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False), 
                                         #SkipEvent = cms.untracked.vstring('ProductNotFound') 
                                     )
    
    
# PostLS1 geometry used
#process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
#process.load('Configuration.Geometry.GeometryExtended2015_cff')
############################
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
#from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')    
    
    
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.Geometry.GeometryExtended2017Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('EventFilter.L1TRawToDigi.omtfStage2Digis_cfi')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')


process.source = cms.Source('PoolSource',
 #fileNames = cms.untracked.vstring('file:/afs/cern.ch/work/g/gflouris/public/SingleMuPt6180_noanti_10k_eta1.root')
 #fileNames = cms.untracked.vstring('file:///afs/cern.ch/work/k/kbunkow/private/omtf_data/SingleMu_15_p_1_1_qtl.root')
 #fileNames = cms.untracked.vstring('file:///afs/cern.ch/work/k/kbunkow/private/omtf_data/SingleMu_20_p_100_2_B7Z.root')
 #fileNames = cms.untracked.vstring('file:///afs/cern.ch/work/k/kbunkow/private/omtf_data/SingleMu_5_p_1_1_Meh.root')
 #fileNames = cms.untracked.vstring('file:///afs/cern.ch/work/k/kbunkow/private/omtf_data/SingleMu_7_p_1_1_DkC.root')
 #fileNames = cms.untracked.vstring('file:///afs/cern.ch/work/k/kbunkow/private/omtf_data/SingleMu_18_p_1_1_2KD.root')
 #fileNames = cms.untracked.vstring('file:///afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_10_x_x_l1tOfflinePhase2/CMSSW_10_6_0_pre4/src/L1Trigger/L1TMuonOverlapPhase1/test/expert/DisplacedMuonGun_Pt30To100_Dxy_0_1000_E68C6334-7F62-E911-8AA5-0025905B8610_dump2000Ev.root')
 
 #fileNames = cms.untracked.vstring('file:///eos/user/k/kbunkow/cms_data/SingleMuFullEta/721_FullEta_v4/SingleMu_31_p_101_2_DzU.root')
 #fileNames = cms.untracked.vstring('file:///eos/user/a/akalinow/Data/SingleMu/9_3_14_FullEta_v2/SingleMu_6_p_1.root'),
 #fileNames = cms.untracked.vstring("file:///eos/user/k/kbunkow/cms_data/mc/PhaseIITDRSpring19DR/PhaseIITDRSpring19DR_Mu_FlatPt2to100_noPU_v31_E0D5C6A5-B855-D14F-9124-0B2C9B28D0EA_dump4000Ev.root"),
 #fileNames = cms.untracked.vstring('file:///eos/home-k/konec/FFCFF986-ED0B-B74F-B253-C511D19B8249.root'),
 #fileNames = cms.untracked.vstring('file:///afs/cern.ch/user/k/konec/work/CMSSW_10_6_1_patch2.displaced/src/UserCode/OmtfAnalysis/jobs/FFCFF986-ED0B-B74F-B253-C511D19B8249.root'),
 
 #fileNames = cms.untracked.vstring("file:///eos/user/k/kbunkow/cms_data/run2_data/Run2018D_ZeroBias_CB56F74E-F55A-B247-AB06-D1A7406AB671_1000Ev.root"),
 fileNames = cms.untracked.vstring("file:///eos/user/k/kbunkow/cms_data/run2_data/Run2018D_ZeroBias_501FAD58-6212-8F46-812C-759AF2603F81_allEv.root"),
  
 
 
 
        inputCommands=cms.untracked.vstring(
        'keep *',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
        'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016s_simEmtfDigis__HLT')
)
	                    
if(runDebug == "DEBUG") :
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000)) ###TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
else :
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))


####Event Setup Producer
process.load('L1Trigger.L1TMuonOverlapPhase1.fakeOmtfParams_cff')
process.omtfParams.configXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/hwToLogicLayer_0x0008.xml")

# process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
#    toGet = cms.VPSet(
#       cms.PSet(record = cms.string('L1TMuonOverlapParamsRcd'),
#                data = cms.vstring('L1TMuonOverlapParams'))
#                    ),
#    verbose = cms.untracked.bool(False)
# )

analysisType = "efficiency" # or rate
  
for a in sys.argv :
    if a == "efficiency" or a ==  "rate" or a == "withTrackPart" :
        analysisType = a
        break;
    
print("analysisType=" + analysisType)

process.TFileService = cms.Service("TFileService", fileName = cms.string('omtfAnalysis2.root'), closeFileFast = cms.untracked.bool(True) )
                                   
####OMTF Emulator
process.load('L1Trigger.L1TMuonOverlapPhase1.simOmtfDigis_cfi')

process.simOmtfDigis.srcDTPh = cms.InputTag('omtfStage2Digis')
process.simOmtfDigis.srcDTTh = cms.InputTag('omtfStage2Digis')
process.simOmtfDigis.srcCSC = cms.InputTag('omtfStage2Digis')
process.simOmtfDigis.srcRPC = cms.InputTag('omtfStage2Digis')
#process.simOmtfDigis.dropRPCPrimitives = cms.bool(False)
#process.simOmtfDigis.dropDTPrimitives = cms.bool(False)
#process.simOmtfDigis.dropCSCPrimitives = cms.bool(False)
process.simOmtfDigis.bxMin = cms.int32(0)
process.simOmtfDigis.bxMax = cms.int32(0)

process.simOmtfDigis.dumpResultToXML = cms.bool(False)
process.simOmtfDigis.dumpResultToROOT = cms.bool(False)

if(runDebug == "DEBUG") :
    process.simOmtfDigis.eventCaptureDebug = cms.bool(True)
else :
    process.simOmtfDigis.eventCaptureDebug = cms.bool(False)    
#process.simOmtfDigis.simTracksTag = cms.InputTag('g4SimHits')

process.simOmtfDigis.sorterType = cms.string("byLLH")
process.simOmtfDigis.ghostBusterType = cms.string("byRefLayer") # byLLH byRefLayer GhostBusterPreferRefDt
#process.simOmtfDigis.ghostBusterType = cms.string("GhostBusterPreferRefDt")

#process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_0x0009_oldSample_3_10Files.xml")
#process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/Patterns_0x0009_oldSample_3_10Files_classProb1.xml")
#process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/GPs_parametrised_v1_classProb3.xml")
#process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/Patterns_0x00012_oldSample_3_30Files_grouped1_classProb1_recalib.xml")
#process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/Patterns_0x00012_oldSample_3_30Files_grouped1_classProb11_recalib2.xml")
#process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_0x00012_oldSample_3_30Files_grouped1_classProb17_recalib2.xml")

#process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_0x0003.xml")
#process.simOmtfDigis.patternsXMLFiles = cms.VPSet(cms.PSet(patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/GPs_parametrised_plus_v1.xml")),
#                                                       cms.PSet(patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/GPs_parametrised_minus_v1.xml"))
#)

if useExtraploationAlgo :
    process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuonOverlapPhase1/test/expert/omtf/Patterns_layerStat_ExtraplMB1nadMB2_t10_classProb17_recalib2_test.xml")
else :
    process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_0x00012_oldSample_3_30Files_grouped1_classProb17_recalib2.xml")

  
process.simOmtfDigis.rpcMaxClusterSize = cms.int32(3)
process.simOmtfDigis.rpcMaxClusterCnt = cms.int32(2)
process.simOmtfDigis.rpcDropAllClustersIfMoreThanMax = cms.bool(True)

process.simOmtfDigis.goldenPatternResultFinalizeFunction = cms.int32(10) #valid values are 0, 1, 2, 3, 5

process.simOmtfDigis.noHitValueInPdf = cms.bool(True)

process.simOmtfDigis.minDtPhiQuality = cms.int32(2)
process.simOmtfDigis.minDtPhiBQuality = cms.int32(4)

process.simOmtfDigis.lctCentralBx = cms.int32(6);#<<<<<<<<<<<<<<<<!!!!!!!!!!!!!!!!!!!!TODO this was changed in CMSSW 10(?) to 8. if the data were generated with the previous CMSSW then you have to use 6

if useExtraploationAlgo :
    process.simOmtfDigis.dtRefHitMinQuality =  cms.int32(4)

    process.simOmtfDigis.usePhiBExtrapolationFromMB1 = cms.bool(True)
    process.simOmtfDigis.usePhiBExtrapolationFromMB2 = cms.bool(True)

#nn_pThresholds = [0.36, 0.38, 0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.52, 0.54 ]
#nn_pThresholds = [0.40, 0.50] 
#nn_pThresholds = [0.35, 0.40, 0.45, 0.50, 0.55] 
 
#process.simOmtfDigis.neuralNetworkFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/omtfClassifier_withPtBins_v34.txt")
#process.simOmtfDigis.ptCalibrationFileName = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/PtCalibration_v34.root")

#process.simOmtfDigis.nn_pThresholds = cms.vdouble(nn_pThresholds)


#process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
#process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

#process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
#process.load("Configuration.StandardSequences.MagneticField_38T_cff")

process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi")
#process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")


process.L1MuonAnalyzerOmtf= cms.EDAnalyzer("L1MuonAnalyzerOmtf", 
                                 etaCutFrom = cms.double(0.82), #OMTF eta range
                                 etaCutTo = cms.double(1.24),
                                 L1OMTFInputTag  = cms.InputTag("simOmtfDigis","OMTF"),
                                 #nn_pThresholds = cms.vdouble(nn_pThresholds), 
                                 analysisType = cms.string(analysisType),
                                 
                                 #simTracksTag = cms.InputTag('g4SimHits'),
                                 #simVertexesTag = cms.InputTag('g4SimHits'),
                                 
                                 #matchUsingPropagation = cms.bool(True),
                                 #muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root") #if you want to make this file, remove this entry#if you want to make this file, remove this entry
                                 #muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_noPropagation_t74.root")
                                        )

process.l1MuonAnalyzerOmtfPath = cms.Path(process.L1MuonAnalyzerOmtf)


process.L1TMuonSeq = cms.Sequence( #process.esProd         
                                   process.omtfStage2Digis 
                                   + process.simOmtfDigis 
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
