from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
config = config()

config.General.requestName = 'OMTF_NN_Regression_FP_analysis_DYToLL_M-10To50_Summer20_noPU_t230'
#config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'

config.JobType.psetName = 'runMuonOverlap_NN_Regression_FP_analyzer.py'


config.JobType.pyCfgParams = ['efficiency']

config.Data.inputDataset = '/DYToLL_M-10To50_TuneCP5_14TeV-pythia8/Phase2Fall22DRMiniAOD-noPU_Pilot_125X_mcRun4_realistic_v2-v1/GEN-SIM-DIGI-RAW-MINIAOD' 
#'/SingleMu_FlatPt-2to100/PhaseIIFall17D-L1TPU200_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'
#config.Data.inputDataset = '/SingleMu_FlatPt-2to100/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'OMTF_NN_Regression_FP_analysis_DYToLL_M-10To50_Summer20_noPU_t230'
config.Data.totalUnits = 332
config.Data.ignoreLocality = False

config.section_("Debug")
config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

#config.Site.storageSite = 'T2_PL_Swierk'
config.Site.storageSite = 'T2_CH_CERN'

