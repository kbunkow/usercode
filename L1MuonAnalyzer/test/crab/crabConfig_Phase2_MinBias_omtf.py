import CRABClient
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
#config.General.requestName = 'omtf_run3_ZeroBias_Run2023_367883_t27a_1'
config.General.requestName = 'omtf_Phase2Spring24_MinBias_' + '_t36'
#config.General.workArea = 'jobs_SM_Run2017E-ZMu-17Nov2017'
#config.General.workArea = 'jobs_JHT_2018D'
config.General.transferLogs = True 
config.General.transferOutputs = True 

config.section_("Data")
config.Data.inputDataset = '/MinBias_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200ALCA_140X_mcRun4_realistic_v4-v2/GEN-SIM-DIGI-RAW-MINIAOD'


config.Data.useParent = False 
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 300  #number of files per jobs
config.Data.totalUnits =  10000000 #10000000 #number of event
#config.Data.outLFNDirBase = '/store/user/konec/test/'
config.Data.publication = False 
#config.Data.outputDatasetTag = 'CRAB3_tutorial_May2015_Data_analysis'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../OMTF_phase2/runMuonOverlapWithExtrapol_phase2_efficiencyAnalyser_rootDumper.py'
#config.JobType.pyCfgParams = ['rate']
#config.JobType.disableAutomaticOutputCollection = True
#config.JobType.outputFiles = ['omtfTree.root', 'omtfHelper.root']
config.JobType.pyCfgParams = ['--analysisType', 'rate']

config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'
#config.Site.whitelist = ['T3_CH_CERNCAF']
#config.Site.whitelist = ['T2_CH_CERN']
#config.Site.storageSite = 'T2_PL_Swierk'
#config.Site.blacklist = ['T2_KR_*','T2_CN_*','T2_BR_*','T2_US_Florida','T2_US_UCSD']
