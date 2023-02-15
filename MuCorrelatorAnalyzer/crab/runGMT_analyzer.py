# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --conditions 111X_mcRun4_realistic_T15_v3 -n 2 --era Phase2C9 --eventcontent FEVTDEBUGHLT --runUnscheduled file:/eos/cms/store/relval/CMSSW_11_0_0/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v2/10000/01054EE2-1B51-C449-91A2-5202A60D16A3.root -s RAW2DIGI,L1TrackTrigger,L1 --datatier FEVTDEBUGHLT --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,L1Trigger/Configuration/customisePhase2TTNoMC.customisePhase2TTNoMC,Configuration/DataProcessing/Utils.addMonitoring --geometry Extended2026D49 --fileout file:/tmp/step1_Reprocess_TrackTrigger_L1.root --no_exec --nThreads 8 --python step1_L1_ProdLike.py --filein das:/TT_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRWinter20DIGI-PU200_110X_mcRun4_realistic_v3-v2/GEN-SIM-DIGI-RAW
import sys
import FWCore.ParameterSet.Config as cms

from os import listdir
from os.path import isfile, join

from Configuration.Eras.Era_Phase2C9_cff import Phase2C9

process = cms.Process('L1',Phase2C9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
#process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D86Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D86_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')

process.load("FWCore.MessageLogger.MessageLogger_cfi")

verbose = True

#version = "sample2023_pilot"
version = 'sample_14_02_2023_2'

if verbose: 
    process.MessageLogger = cms.Service("MessageLogger",
       #suppressInfo       = cms.untracked.vstring('AfterSource', 'PostModule'),
       destinations   = cms.untracked.vstring(
                                               #'detailedInfo',
                                               #'critical',
                                               #'cout',
                                               #'cerr',
                                               'muCorrelatorEventPrint'
                    ),
       categories        = cms.untracked.vstring('gmtDataDumper', 'phase2L1GMT', 'MuonStub', "TrackerMuon", 'ConvertedTTTrack', "l1tMuBayesEventPrint"), #, "l1tMuBayesEventPrint"
       muCorrelatorEventPrint = cms.untracked.PSet(    
                         extension = cms.untracked.string('.txt'),  
                         filename  = cms.untracked.string('muCorrelatorEventPrint_' + version),              
                         threshold = cms.untracked.string('INFO'), #
                         default = cms.untracked.PSet( limit = cms.untracked.int32(0) ), 
                         #INFO   =  cms.untracked.int32(0),
                         #DEBUG   = cms.untracked.int32(0),
                         gmtDataDumper = cms.untracked.PSet( limit = cms.untracked.int32(100000000) ),
                         phase2L1GMT = cms.untracked.PSet( limit = cms.untracked.int32(100000000) ),
                         MuonStub = cms.untracked.PSet( limit = cms.untracked.int32(100000000) ),
                         TrackerMuon = cms.untracked.PSet( limit = cms.untracked.int32(100000000) ),
                         ConvertedTTTrack = cms.untracked.PSet( limit = cms.untracked.int32(100000000) ),
                         l1tMuBayesEventPrint = cms.untracked.PSet( limit = cms.untracked.int32(100000000) ),
                       ),
       #debugModules = cms.untracked.vstring('l1tGMTMuons', 'l1tGMTMuons.trackMatching', 'trackMatching', 'Phase2L1TGMTProducer:l1tGMTMuons', 'Phase2L1TGMTProducer') 
       debugModules = cms.untracked.vstring('muCorrelatorAnalyzer')
    )

    #process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
if not verbose:
    print("aaaa")
    #process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
    #process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False) )



process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet),
)

#path = "/eos/user/j/jwiechni/HSCP/23_01_2023/SingleMu_ch0_OneOverPt_23_01_2023/23_01_2023/230123_144305/0000/"
#path = "/eos/user/a/akalinow/Data/SingleMu/SingleMu_ch0_OneOverPt_test_14_02_2023_1/test_14_02_2023_1/230214_084703/0000/"
path = "/eos/user/a/akalinow/Data/OMTF/test_14_02_2023_2/SingleMu_ch0_OneOverPt_test_14_02_2023_2/test_14_02_2023_2/230214_165448/0000/"

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

chosenFiles = []

#for i in range(1, 10, 1):
#    chosenFiles.append('file://' + path + "SingleMu_OneOverPt_1_100_m_" + str(i) + ".root") 

filesNameLike = "1_100_m"

for i in range(1, 101, 1):
    for f in onlyfiles:
        #if (( filesNameLike + '_' + str(i) + '_') in f):  #TODO for 721_FullEta_v4/
        if (( filesNameLike + '_' + str(i) + '.') in f): #TODO for 9_3_14_FullEta_v2
            print(f)
            chosenFiles.append('file://' + path + f) 
            
print("chosenFiles\n", chosenFiles)
                 
# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( (
#'/store/mc/Phase2HLTTDRWinter20DIGI/JPsiToMuMu_Pt0to100-pythia8_TuneCP5-gun/GEN-SIM-DIGI-RAW/PU200_110X_mcRun4_realistic_v3-v2/20000/087AA768-91E6-124F-B226-DC00C45D967D.root',
#'/store/mc/Phase2HLTTDRWinter20DIGI/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_pilot_110X_mcRun4_realistic_v3-v2/10000/0036F7A2-BADA-1E4E-8FE7-ABE1A9AEC350.root',
#'/store/mc/Phase2HLTTDRWinter20DIGI/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_pilot_110X_mcRun4_realistic_v3-v2/10000/007C3CAA-5209-3B47-8755-4C6D0A3A5CD2.root',
#'/store/mc/Phase2HLTTDRWinter20DIGI/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_pilot_110X_mcRun4_realistic_v3-v2/10000/00AECAEC-8DFE-8D49-AF78-A55FCEBB46B7.root',
#'/store/mc/Phase2HLTTDRWinter20DIGI/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_pilot_110X_mcRun4_realistic_v3-v2/10000/00B04974-FAC3-5A4E-B5AE-9483D8FAD5B1.root',
#'/store/mc/Phase2HLTTDRWinter20DIGI/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_pilot_110X_mcRun4_realistic_v3-v2/10000/00D64490-55F9-7E4E-B3CE-BE668F1A5938.root',
#'/store/mc/Phase2HLTTDRWinter20DIGI/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_pilot_110X_mcRun4_realistic_v3-v2/10000/01708416-15F1-5B47-A8A0-B32D355622DB.root'
   
#"/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/NoPU_pilot_111X_mcRun4_realistic_T15_v1-v1/100000/0018FD1C-F75F-9E4A-A329-1E671A1CA267.root"   
#'file:///afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_7/src/L1Trigger/Phase2L1GMT/test/Phase2HLTTDRSummer20_DYToLL_M-50_noPU_0018FD1C-F75F-9E4A-A329-1E671A1CA267_1000Ev.root'
#'file:///eos/home-k/kbunkow/cms_data/mc/PhaseIISpring22/PhaseIISpring22DRMiniAOD_DYToLL_M-10To50_noPU_40000_04216b41-07a8-4ec9-a1c3-a24cda929b74_2000Ev.root'

#'file:///eos/user/k/kbunkow/cms_data/mc/mcWaw2022/HSCPppstau_M_432_TuneZ2star_13TeV_pythia6.root'     
#'file:///eos/user/k/kbunkow/cms_data/mc/mcWaw2022/DoubleMuPt1to100Eta24_1kevents.root'  
#'file:///eos/user/k/kbunkow/cms_data/mc/mcWaw2022/DoubleMuPt1to100Eta24_1kevents.root'  
#'file:///eos/user/j/jwiechni/HSCP/23_01_2023/SingleMu_ch0_OneOverPt_23_01_2023/23_01_2023/230123_144305/0000/SingleMu_OneOverPt_1_100_m_1.root'
chosenFiles
      ) ),
    
    secondaryFileNames = cms.untracked.vstring(),
#                            skipEvents=cms.untracked.uint32(36)
    inputCommands=cms.untracked.vstring(
          'keep *',
          # 'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
          # 'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
          # 'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
          # 'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
          # 'drop l1tEMTFTrack2016s_simEmtfDigis__HLT',
          # 'drop l1tHGCalClusterBXVector_hgcalTriggerPrimitiveDigiProducer_cluster2D_HLT',
          # 'drop *HGCal*_*_*_*',
          # 'drop *hgcal*_*_*_*',
          # 'drop *Ecal*_*_*_*',
          # 'drop *Hcal*_*_*_*',
          # 'drop *Calo*_*_*_*',
          #
          # 'drop *_*HGCal*_*_*',
          # 'drop *_*hgcal*_*_*',
          # 'drop *_*Ecal*_*_*',
          # 'drop *_*Hcal*_*_*',
          # 'drop *_*Calo*_*_*',
          #
          # 'drop *_*_*HGCal*_*',
          # 'drop *_*_*hgcal*_*',
          # 'drop *_*_*Ecal*_*',
          # 'drop *_*_*Hcal*_*',
          # 'drop *_*_*Calo*_*',
          #
          # 'drop l1tPFCandidates_*_*_*',
          'drop l1tTkPrimaryVertexs_L1TkPrimaryVertex__RECO'
          )
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(

        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(1)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(1),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step1 nevts:2'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('FEVTDEBUGHLT'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('reprocess.root'),
    outputCommands = cms.untracked.vstring(
        "drop *_*_*_*",
        "keep *_l1tGMTMuons_*_*",
        "keep *_l1tGMTStubs_*_*",
        "keep *_genParticles_*_*",
        "keep *_l1tTTTracksFromTrackletEmulation_Level1TTTracks_*",
        "keep *_l1tTkMuons_*_*"
    ),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '111X_mcRun4_realistic_T15_v3', '')

##
#Calibrate Digis
process.load("L1Trigger.DTTriggerPhase2.CalibratedDigis_cfi")
process.CalibratedDigis.dtDigiTag = "simMuonDTDigis" 
process.CalibratedDigis.scenario = 0

#DTTriggerPhase2
process.load("L1Trigger.DTTriggerPhase2.dtTriggerPhase2PrimitiveDigis_cfi")
process.dtTriggerPhase2PrimitiveDigis.debug = False
process.dtTriggerPhase2PrimitiveDigis.dump = False
process.dtTriggerPhase2PrimitiveDigis.scenario = 0

process.load("L1Trigger.Phase2L1GMT.gmt_cff")
process.l1tGMTMuons.trackMatching.verbose=0
process.l1tGMTMuons.verbose=0
process.l1tGMTMuons.trackConverter.verbose=0

process.l1tGMTMuons.trackingParticleInputTag = cms.InputTag("mix", "MergedTrackTruth")
process.l1tGMTMuons.mcTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks")
process.l1tGMTMuons.dumpToRoot = cms.bool(False)
process.l1tGMTMuons.dumpToXml = cms.bool(False)


process.TFileService = cms.Service("TFileService", fileName = cms.string("muCorrelatorTTAnalysis1_"  + version + ".root"), closeFileFast = cms.untracked.bool(True))

analysisType = "efficiency" # or rate
    
for a in sys.argv :
    if a == "efficiency" or a ==  "rate" or a == "withTrackPart" :
        analysisType = a
        break;

print ("analysisType=" + analysisType)

process.muCorrelatorAnalyzer= cms.EDAnalyzer("MuCorrelatorAnalyzer", 
                                 outRootFile = cms.string("muCorrelatorTTAnalysis1.root"),
                                 etaCutFrom = cms.double(0.), #OMTF eta range
                                 etaCutTo = cms.double(2.4),
                                          
                                       MyProcess = cms.int32(1),
                                       DebugMode = cms.bool(verbose),      # printout lots of debug statements
                                       SaveAllTracks = cms.bool(True),   # save *all* L1 tracks, not just truth matched to primary particle
                                       SaveStubs = cms.bool(False),      # save some info for *all* stubs
                                       LooseMatch = cms.bool(True),     # turn on to use "loose" MC truth association
                                       L1Tk_minNStub = cms.int32(4),     # L1 tracks with >= 4 stubs
                                       TP_minNStub = cms.int32(4),       # require TP to have >= X number of stubs associated with it
                                       TP_minNStubLayer = cms.int32(4),  # require TP to have stubs in >= X layers/disks
                                       TP_minPt = cms.double(1.0),       # only save TPs with pt > X GeV
                                       TP_maxEta = cms.double(2.4),      # only save TPs with |eta| < X
                                       TP_maxZ0 = cms.double(30.0),      # only save TPs with |z0| < X cm
                                       TP_maxRho = cms.double(30.0),     # for efficiency analysis, to not inlude the muons from the far decays 
                                       L1TrackInputTag = cms.InputTag("l1tTTTracksFromTrackletEmulation", "Level1TTTracks") ,               ## TTTrack input
                                       MCTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks"), ## MCTruth input 
                                       # other input collections
                                       L1StubInputTag = cms.InputTag("TTStubsFromPhase2TrackerDigis","StubAccepted"),
                                       MCTruthClusterInputTag = cms.InputTag("TTClusterAssociatorFromPixelDigis", "ClusterAccepted"),
                                       MCTruthStubInputTag = cms.InputTag("TTStubAssociatorFromPixelDigis", "StubAccepted"),
                                       TrackingParticleInputTag = cms.InputTag("mix", "MergedTrackTruth"),
                                       TrackingVertexInputTag = cms.InputTag("mix", "MergedTrackTruth"),
                                       
                                       muCandQualityCut = cms.int32(12),
                                       analysisType = cms.string(analysisType)
                                        )
process.muCorrelatorAnalyzerPath = cms.Path(process.muCorrelatorAnalyzer)






#process.schedule = cms.Schedule(process.L1TrackTrigger_step,process.pL1TMuonTPS,process.endjob_step,process.e) # Adding MuonTPS


# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
#process.pL1TkPrimaryVertex = cms.Path(process.L1TkPrimaryVertex)
#process.pL1TkPhotonsCrystal = cms.Path(process.L1TkPhotonsCrystal)
#process.pL1TkIsoElectronsCrystal = cms.Path(process.L1TkIsoElectronsCrystal)
#process.pL1TkElectronsLooseCrystal = cms.Path(process.L1TkElectronsLooseCrystal)
#process.pL1TkElectronsLooseHGC = cms.Path(process.L1TkElectronsLooseHGC)
#process.pL1TkElectronsHGC = cms.Path(process.L1TkElectronsHGC)
#process.pL1TkMuon = cms.Path(process.L1TkMuons+process.L1TkMuonsTP)
#process.pL1TkElectronsEllipticMatchHGC = cms.Path(process.L1TkElectronsEllipticMatchHGC)
#process.pL1TkElectronsCrystal = cms.Path(process.L1TkElectronsCrystal)
#process.pL1TkPhotonsHGC = cms.Path(process.L1TkPhotonsHGC)
#process.pL1TkIsoElectronsHGC = cms.Path(process.L1TkIsoElectronsHGC)
#process.pL1TkElectronsEllipticMatchCrystal = cms.Path(process.L1TkElectronsEllipticMatchCrystal)
#process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.testpath=cms.Path(process.CalibratedDigis*process.dtTriggerPhase2PrimitiveDigis*process.phase2GMT)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition 
#process.raw2digi_step, process.L1TrackTrigger_step, process.FEVTDEBUGHLToutput_step, 
process.schedule = cms.Schedule(process.testpath,process.endjob_step,process.muCorrelatorAnalyzerPath)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
#process.options.numberOfThreads=cms.untracked.uint32(1)
#process.options.numberOfStreams=cms.untracked.uint32(0)
#process.options.numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(1)

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.aging
from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000 

#call to customisation function customise_aging_1000 imported from SLHCUpgradeSimulations.Configuration.aging
#process = customise_aging_1000(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customisePhase2TTNoMC
from L1Trigger.Configuration.customisePhase2TTNoMC import customisePhase2TTNoMC 

#call to customisation function customisePhase2TTNoMC imported from L1Trigger.Configuration.customisePhase2TTNoMC
process = customisePhase2TTNoMC(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
