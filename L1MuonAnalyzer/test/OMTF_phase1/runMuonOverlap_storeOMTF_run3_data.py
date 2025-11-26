# -*- coding: utf-8 -*-
import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_2025_cff import Run3_2025
process = cms.Process("STOREOMTFDIGIS", Run3_2025)

# Basic messaging
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# Input RAW data file (as requested)
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        '/store/data/Run2025G/EphemeralZeroBias7/RAW/v1/000/398/121/00000/02cc782f-ecd9-45e6-a7a8-14274a2fafe2.root'
    )
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

# Standard setup: geometry, global tag, raw->digi
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_data', '')

# Load the OMTF unpacker and emulator
process.load('EventFilter.L1TRawToDigi.omtfStage2Digis_cfi')
process.load('L1Trigger.L1TMuonOverlapPhase1.simOmtfDigis_cfi')

# Ensure simOmtfDigis uses the unpacked omtfStage2Digis as input
process.simOmtfDigis.srcDTPh = cms.InputTag('omtfStage2Digis')
process.simOmtfDigis.srcDTTh = cms.InputTag('omtfStage2Digis')
process.simOmtfDigis.srcCSC = cms.InputTag('omtfStage2Digis')
process.simOmtfDigis.srcRPC = cms.InputTag('omtfStage2Digis')

# Keep the bx range minimal by default (can be changed by user)
process.simOmtfDigis.bxMin = cms.int32(0)
process.simOmtfDigis.bxMax = cms.int32(0)

# Add DT unpacker to produce DT digis (MuonDigiCollection)
#process.load('EventFilter.DTRawToDigi.dtunpacker_cfi')
# Typical input label from RAW files
#process.muonDTDigis.inputLabel = 'rawDataCollector'

# Output: write only the omtfStage2Digis collections and DT digis
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('omtfStage2Digis_output.root'),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_omtfStage2Digis_*_*',
        'keep *_simOmtfDigis_*_*',
        'keep *_muonDTDigis_*_*',
        'keep *_muonCSCDigis_*_*',
        'keep *_muonRPCDigis_*_*',
    )
)

# Paths and schedule
process.unpackOMTF = cms.Path(process.omtfStage2Digis)
process.runOMTFemu = cms.Path(process.simOmtfDigis)
# Path to produce DT digis
process.unpackDT = cms.Path(process.muonDTDigis)
process.unpackCSC = cms.Path(process.muonCSCDigis)
process.unpackRPC = cms.Path(process.rpcCPPFRawToDigi * process.rpcTwinMuxRawToDigi * process.muonRPCDigis)
process.output_step = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.unpackOMTF, process.unpackCSC, process.unpackDT, process.unpackRPC, process.output_step) #process.runOMTFemu,  

# Minimal options
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# End of config