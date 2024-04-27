import CRABClient
from WMCore.Configuration import Configuration
config = Configuration()

runNum = '379252'

config.section_("General")
#config.General.requestName = 'omtf_run3_ZeroBias_Run2023_367883_t27a_1'
config.General.requestName = 'omtf_run3_ZeroBias_Run2024_' +  runNum + '_t27b_0'
#config.General.workArea = 'jobs_SM_Run2017E-ZMu-17Nov2017'
#config.General.workArea = 'jobs_JHT_2018D'
config.General.transferLogs = True 
config.General.transferOutputs = True 

config.section_("Data")
config.Data.inputDataset = '/EphemeralZeroBias0/Run2024B-v1/RAW'
config.Data.runRange = runNum

#config.Data.inputDataset = '/EphemeralZeroBias0/Run2023D-v1/RAW'
#config.Data.runRange = '370580'


#config.Data.lumiMask='Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
#config.Data.lumiMask='Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'

#config.Data.runRange = '282000-283000'


config.Data.useParent = False 
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 20 #number of files per jobs
config.Data.totalUnits =  10000000 #number of event
#config.Data.outLFNDirBase = '/store/user/konec/test/'
config.Data.publication = False 
#config.Data.outputDatasetTag = 'CRAB3_tutorial_May2015_Data_analysis'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'runMuonOverlap_PatsWithExtrapolation_efficiencyAnalyser.py'
#config.JobType.pyCfgParams = ['rate']
#config.JobType.disableAutomaticOutputCollection = True
#config.JobType.outputFiles = ['omtfTree.root', 'omtfHelper.root']

config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'
#config.Site.whitelist = ['T3_CH_CERNCAF']
#config.Site.whitelist = ['T2_CH_CERN']
#config.Site.storageSite = 'T2_PL_Swierk'
#config.Site.blacklist = ['T2_KR_*','T2_CN_*','T2_BR_*','T2_US_Florida','T2_US_UCSD']
