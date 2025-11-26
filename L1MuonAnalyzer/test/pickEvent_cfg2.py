import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')
# add a list of strings for events to process
# options.register ('eventsToProcess',
#                                   '',
#                                   VarParsing.multiplicity.list,
#                                   VarParsing.varType.string,
#                                   "Events to process")
# options.parseArguments()


Source_Files = cms.untracked.vstring(
         #"/store/data/Run2025G/Muon0/RAW/v1/000/398/240/00000/00204827-3486-428c-b73e-24ed8e7b7a58.root"      
         "/store/data/Run2025G/EphemeralZeroBias7/RAW/v1/000/398/121/00000/02cc782f-ecd9-45e6-a7a8-14274a2fafe2.root"  
)

process = cms.Process("PickEvent")
process.source = cms.Source ("PoolSource",
          fileNames = Source_Files, #cms.untracked.vstring (options.inputFiles),
          #eventsToProcess = cms.untracked.VEventRange (options.eventsToProcess),
          dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
          inputCommands=cms.untracked.vstring(
          'drop *',
          'keep *Mu*_*_*_*',
          'keep *_*Mu*_*_*',
          'keep *_*_*Mu*_*',
          'keep *_*_*_*Mu*',
          )                               
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

#outputFileNme = '/eos/user/k/kbunkow/cms_data/mc/PhaseIIFall17D/SingleMu_FlatPt-2to100/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/F4EEAE55-C937-E811-8C29-48FD8EE739D1_dump1000Events.root'
#outputFileNme = 'HSCPppstau_M-651_TuneZ2star_13TeV_0E0D542C-A9C8-E611-981C-A0000420FE80_dump100Events.root'
#outputFileNme = 'SingleMu_PU200_32DF01CC-A342-E811-9FE7-48D539F3863E_dump500Events.root'
#outputFileNme = 'HSCPppstau_M_871_PU200_v3-v2_1ADE9D9E-8C0C-1948-A405-5DFDA1AF5172_dump100Ev.root'
#outputFileNme = 'Nu_E10-pythia8-gun_PU200_v3-v3_FFB3195D-E113-3744-877D-44E21C060358_dump100Ev.root'
#outputFileNme = 'Phase2HLTTDRWinter20DIGI__ZprimeToMuMu_M-6000_NoPU_CFBA4AE8-00DE-1743-9B83-7582C69FC7F7_dump100Ev.root'
#outputFileNme = 'Run2018D_ZeroBias_CB56F74E-F55A-B247-AB06-D1A7406AB671_allEv.root'
#outputFileNme = 'Run2018D_ZeroBias_501FAD58-6212-8F46-812C-759AF2603F81_allEv.root'
#outputFileNme = 'Run2018D_ZeroBias_Run_325117_8BAB433D-F822-A64A-BB22-25E18AD5442F_allEv.root'
#outputFileNme = 'Run3Winter20_HTo2LongLivedTo4mu_MH-125_mcRun3_2021_03FD2A52-9B9A-544B-816F-8BF926F15CE8.root'
#outputFileNme = 'Run3Winter20_Mu_FlatPt1to1000_mcRun3_2021_003C515F-E4D1-404D-8921-36A3FD7361E9_300Ev.root'

outputFileNme = '/eos/user/k/kbunkow/cms_data/run3_data/Run2025G_EphemeralZeroBias7_test.root'

process.Out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string (outputFileNme)
)

process.end = cms.EndPath(process.Out)
