from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
config = config()

config.General.requestName = 'Phase2L1GMT_MC_analysis_TauTo3Mu_Summer20_PU200_withNewMB_t208'
#config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'

config.JobType.psetName = 'runGMT_analyzer.py'


config.JobType.pyCfgParams = ['efficiency']

config.Data.inputDataset = '/DsToTauTo3Mu_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v1/FEVT' 
#'/SingleMu_FlatPt-2to100/PhaseIIFall17D-L1TPU200_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'
#config.Data.inputDataset = '/SingleMu_FlatPt-2to100/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 20
#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'Phase2L1GMT_MC_analysis_TauTo3Mu_Summer20_PU200_withNewMB_t208'
config.Data.totalUnits = 247
config.Data.ignoreLocality = False

config.section_("Debug")
config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

#config.Site.storageSite = 'T2_PL_Swierk'
config.Site.storageSite = 'T2_CH_CERN'

