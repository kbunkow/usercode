/*
 * MuonMatcher.cc
 *
 *  Created on: Jun 16, 2020
 *      Author: kbunkow
 */

#include "usercode/L1MuonAnalyzer/interface/MuonMatcher.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CLHEP/Random/RandFlat.h"
#include "CLHEP/Units/GlobalPhysicalConstants.h"

#include "Geometry/CommonDetUnit/interface/GeomDet.h"

#include "DataFormats/GeometrySurface/interface/BoundCylinder.h"
#include "DataFormats/GeometrySurface/interface/SimpleCylinderBounds.h"
#include "DataFormats/GeometrySurface/interface/BoundDisk.h"
#include "DataFormats/GeometrySurface/interface/SimpleDiskBounds.h"
#include "DataFormats/MuonDetId/interface/RPCDetId.h"

#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"

#include "L1Trigger/L1TMuon/interface/MicroGMTConfiguration.h"

#include <math.h>

#include "TFile.h"


namespace L1MuAn {

double hwGmtPhiToGlobalPhi(int phi) {
  double phiGmtUnit = 2. * M_PI / 576.;
  return phi * phiGmtUnit;
}

int calcGlobalPhi(int locPhi, int proc, int nProcessors) {
  int globPhi = 0;
  //60 degree sectors = 96 in int-scale
  globPhi = (proc)*96 * 6/nProcessors + locPhi;
  // first processor starts at CMS phi = 15 degrees (24 in int)... Handle wrap-around with %. Add 576 to make sure the number is positive
  globPhi = (globPhi + 24 + 576) % 576;
  return globPhi;
}

double foldPhi(double phi) {
  if(phi > M_PI)
    return (phi - 2 * M_PI );
  else if(phi < -M_PI)
    return (phi +  2 * M_PI );

  return phi;
}

MuonMatcher::MuonMatcher(const edm::ParameterSet& edmCfg,
    const edm::ESGetToken<MagneticField, IdealMagneticFieldRecord>& magneticFieldEsToken,
    const edm::ESGetToken<Propagator, TrackingComponentsRecord>& propagatorEsToken):
          magneticFieldEsToken(magneticFieldEsToken),
          propagatorEsToken(propagatorEsToken)
{
  edm::Service<TFileService> fs;
  TFileDirectory subDir =  fs->mkdir("MuonMatcher");

  deltaPhiPropCand   =      subDir.make<TH2F>("deltaPhiPropCand",         "delta Phi propagated track - muonCand Vs Pt", 200, 0, 1000, 100, -1.5, 1.5); //delta phi between propagated track and muon candidate,
  deltaPhiPropCandMatched = subDir.make<TH2F>("deltaPhiPropCandMatched",  "delta Phi matched propagated track - muonCand Vs Pt", 200, 0, 1000, 100, -0.5 -0.005, 0.5 -0.005); //delta phi between propagated track and muon candidate,
  deltaPhiVertexProp = subDir.make<TH2F>("deltaPhiVertexProp", "delta Phi vertex - propagated track Vs Pt", 200, 0, 1000, 100, -1, 1);; //delta phi between phi at vertex and propagated track phi)

  muonsPerEvent = fs->make<TH1D>("muonsPerEvent", "muonsPerEvent", 21, -0.5, 20.5);
  muonsPerEventInOmtf = fs->make<TH1D>("muonsPerEventInOmtf", "muonsPerEventInOmtf", 21, -0.5, 20.5);

  if(edmCfg.exists("phase") ) {
    if(edmCfg.getParameter<int>("phase") == 2)
      nProcessors = 3;
  }

  if(edmCfg.exists("matchUsingPropagation") )
    matchUsingPropagation = edmCfg.getParameter<bool>("matchUsingPropagation");

  edm::LogImportant("l1MuonAnalyzerOmtf") <<" MuonMatcher: line "<<__LINE__<<" matchUsingPropagation "<<matchUsingPropagation<<std::endl;
  if(edmCfg.exists("muonMatcherFile") ) {
    std::string muonMatcherFileName =  edmCfg.getParameter<edm::FileInPath>("muonMatcherFile").fullPath();
    TFile inFile(muonMatcherFileName.c_str());
    edm::LogImportant("l1MuonAnalyzerOmtf") <<" MuonMatcher: using muonMatcherFileName "<<muonMatcherFileName<<std::endl;
    if(matchUsingPropagation) {
      deltaPhiPropCandMean = (TH1D*)inFile.Get("deltaPhiPropCandMean");
      deltaPhiPropCandStdDev = (TH1D*)inFile.Get("deltaPhiPropCandStdDev");
    }
    else {
      deltaPhiVertexCand_Mean_pos =   (TH1D*)inFile.Get("deltaPhiVertexCand_Mean_pos");
      deltaPhiVertexCand_StdDev_pos = (TH1D*)inFile.Get("deltaPhiVertexCand_StdDev_pos");

      deltaPhiVertexCand_Mean_neg =   (TH1D*)inFile.Get("deltaPhiVertexCand_Mean_neg");
      deltaPhiVertexCand_StdDev_neg = (TH1D*)inFile.Get("deltaPhiVertexCand_StdDev_neg");
    }

    fillMean =  false;
  }
  else {
    if(matchUsingPropagation) {
      deltaPhiPropCandMean = new TH1D("deltaPhiPropCandMean", "mean #DELTA#phi propagated track - muonCand Vs pT", 100, 0, 100); //TODO the bins must be the same as in the deltaPhiPropCand
      deltaPhiPropCandStdDev = new TH1D("deltaPhiPropCandStdDev", "StdDev #delta#phi propagated track - muonCand Vs pT", 100, 0, 100); //TODO the bins must be the same as in the deltaPhiPropCand
    }
    else {
      edm::LogImportant("l1MuonAnalyzerOmtf") <<" MuonMatcher: line "<<__LINE__<<std::endl;
      ptGen_pos = new TH1D("ptGen_pos", "candidates number vs ptGen, positive charge", 200, 0, 100);
      deltaPhiVertexCand_Mean_pos = new TH1D("delgentaPhiVertexCand_Mean_pos", "mean #DELTA#phi track at vertex - muonCand Vs pT, positive charge", 200, 0, 100);;
      deltaPhiVertexCand_StdDev_pos = new TH1D("deltaPhiVertexCand_StdDev_pos", "StdDev #DELTA#phi track at vertex - muonCand Vs pT, positive charge", 200, 0, 100);;

      ptGen_neg = new TH1D("ptGen_neg", "candidates number vs ptGen, negative charge", 200, 0, 100);
      deltaPhiVertexCand_Mean_neg = new TH1D("deltaPhiVertexCand_Mean_neg", "mean #DELTA#phi track at vertex - muonCand Vs pT, negative charge", 200, 0, 100);;
      deltaPhiVertexCand_StdDev_neg = new TH1D("deltaPhiVertexCand_StdDev_neg", "StdDev #DELTA#phi track at vertex - muonCand Vs pT, negative charge", 200, 0, 100);;
    }

    fillMean =  true;
  }

}

void MuonMatcher::beginRun(const edm::EventSetup& eventSetup) {
  //TODO use edm::ESWatcher<MagneticField> magneticFieldRecordWatcher;
  magField = eventSetup.getHandle(magneticFieldEsToken);
  propagator = eventSetup.getHandle(propagatorEsToken);
}

/*void MuonMatcher::setup(const edm::EventSetup& eventSetup) {
  eventSetup.get<GlobalTrackingGeometryRecord>().get(globalGeometry);
  eventSetup.get<IdealMagneticFieldRecord>().get(magField);

  eventSetup.get<TrackingComponentsRecord>().get("SteppingHelixPropagatorAlong", propagator);
}*/

MuonMatcher::~MuonMatcher() {


}

void MuonMatcher::saveHists() {
  if(fillMean) {
    std::string rootFileName = "muonMatcherHists.root";
    //gStyle->SetOptStat(111111);
    TFile outfile(rootFileName.c_str(), "RECREATE");
    edm::LogImportant("l1MuonAnalyzerOmtf")<<__FUNCTION__<<": "<<__LINE__<<" out fileName "<<rootFileName<<" outfile->GetName() "<<outfile.GetName()<<endl;
    outfile.cd();
    deltaPhiPropCand->Write();
    deltaPhiPropCandMatched->Write();
    deltaPhiVertexProp->Write();

    if(matchUsingPropagation) {
      for(int iBin = 0; iBin <= deltaPhiPropCand->GetXaxis()->GetNbins() +1; iBin++) {
        auto projection = deltaPhiPropCand->ProjectionY( (std::string("deltaPhiPropCand") + std::to_string(iBin)).c_str(), iBin, iBin);

        double mean = 0;
        double stdDev = 0;
        double entries = projection->Integral(0, projection->GetNbinsX() +1); //to iniclude the under and overflow bins
        if(entries) {
          mean = deltaPhiPropCandMean->GetBinContent(iBin) / entries ;

          stdDev = deltaPhiPropCandStdDev->GetBinContent(iBin) / entries;
          stdDev = sqrt(stdDev - mean * mean);
        }
        deltaPhiPropCandMean->SetBinContent(iBin, mean);
        deltaPhiPropCandStdDev->SetBinContent(iBin, stdDev);

        edm::LogImportant("l1MuonAnalyzerOmtf") <<" MuonMatcher::saveHists() "<<std::setw(5)<<iBin<<" mean "<<std::setw(8)<<mean<<" GetMean "<<projection->GetMean()<<
            " stdDev "<<stdDev<<" GetRMS "<<projection->GetRMS()<<" Entries "<<entries<<std::endl;
      }

      deltaPhiPropCandMean->Write();
      deltaPhiPropCandStdDev->Write();

      TH1* deltaPhiPropCandStdDevSmooth = (TH1*)deltaPhiPropCandStdDev->Clone("deltaPhiPropCandStdDevSmooth");
      deltaPhiPropCandStdDevSmooth->GetXaxis()->SetRangeUser(3, 100);
      deltaPhiPropCandStdDevSmooth->Smooth(1, "R");
      deltaPhiPropCandStdDevSmooth->Write();
    }
    else {
      //lambda
      auto calculateMaenAndStd = [](TH1D* ptGen_pos, TH1D* deltaPhiVertexCand_Mean_pos, TH1D* deltaPhiVertexCand_StdDev_pos) {
        for(int iBin = 0; iBin <= deltaPhiVertexCand_Mean_pos->GetXaxis()->GetNbins() +1; iBin++) {
          double mean = 0;
          double stdDev = 0;
          double entries = ptGen_pos->GetBinContent(iBin); //to iniclude the under and overflow bins
          if(entries) {
            mean = deltaPhiVertexCand_Mean_pos->GetBinContent(iBin) / entries ;

            stdDev = deltaPhiVertexCand_StdDev_pos->GetBinContent(iBin) / entries;
            stdDev = sqrt(stdDev - mean * mean);
          }
          deltaPhiVertexCand_Mean_pos->SetBinContent(iBin, mean);
          deltaPhiVertexCand_StdDev_pos->SetBinContent(iBin, stdDev);

          edm::LogImportant("l1MuonAnalyzerOmtf") <<" MuonMatcher::saveHists() lambda "<<std::setw(5)<<iBin<<" mean "<<std::setw(8)<<mean<<
              " stdDev "<<stdDev<<" Entries "<<entries<<std::endl;
        }

        edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::SaveHist: "<<__LINE__<<std::endl;
        ptGen_pos->Write();
        deltaPhiVertexCand_Mean_pos->Write();
        deltaPhiVertexCand_StdDev_pos->Write();

        edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::SaveHist: "<<__LINE__<<std::endl;

        TH1* deltaPhiVertexCand_Mean_pos_smooth = (TH1*)deltaPhiVertexCand_Mean_pos->Clone( (std::string(deltaPhiVertexCand_Mean_pos->GetName()) + "_smooth").c_str());
        edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::SaveHist: "<<__LINE__<<std::endl;
        deltaPhiVertexCand_Mean_pos_smooth->GetXaxis()->SetRangeUser(2.5, 100);
        deltaPhiVertexCand_Mean_pos_smooth->Smooth(1, "R");
        edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::SaveHist: "<<__LINE__<<std::endl;
        deltaPhiVertexCand_Mean_pos_smooth->Write();
        edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::SaveHist: "<<__LINE__<<std::endl;

        TH1* deltaPhiVertexCand_StdDev_pos_smooth = (TH1*)deltaPhiVertexCand_StdDev_pos->Clone((std::string(deltaPhiVertexCand_StdDev_pos->GetName()) + "_smooth").c_str());
        deltaPhiVertexCand_StdDev_pos_smooth->GetXaxis()->SetRangeUser(2.5, 100);
        deltaPhiVertexCand_StdDev_pos_smooth->Smooth(1, "R");
        deltaPhiVertexCand_StdDev_pos_smooth->Write();

        edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::SaveHist: "<<__LINE__<<std::endl;

      };//lambda end

      calculateMaenAndStd(ptGen_pos, deltaPhiVertexCand_Mean_pos, deltaPhiVertexCand_StdDev_pos);
      calculateMaenAndStd(ptGen_neg, deltaPhiVertexCand_Mean_neg, deltaPhiVertexCand_StdDev_neg);
    }
  }
}


TrajectoryStateOnSurface MuonMatcher::atStation2(FreeTrajectoryState ftsStart, float eta) const {
  eta = 0; //fix me!!!!! in case of displaced muon the vertex eta has no sense
  ReferenceCountingPointer<Surface> rpc;
  if (eta < -1.24)  //negative endcap, RE2
    rpc = ReferenceCountingPointer<Surface>(
        new BoundDisk(GlobalPoint(0., 0., -790.), TkRotation<float>(), SimpleDiskBounds(300., 810., -10., 10.)));
  else if (eta < 1.24)  //barrel + overlap, 512.401cm is R of middle of the MB2
    rpc = ReferenceCountingPointer<Surface>(new BoundCylinder(
        GlobalPoint(0., 0., 0.), TkRotation<float>(), SimpleCylinderBounds(512.401, 512.401, -900, 900)));
  else
    rpc = ReferenceCountingPointer<Surface>(  //positive endcap, RE2
        new BoundDisk(GlobalPoint(0., 0., 790.), TkRotation<float>(), SimpleDiskBounds(300., 810., -10., 10.)));

  TrajectoryStateOnSurface trackAtRPC = propagator->propagate(ftsStart, *rpc);
  return trackAtRPC;
}


TrajectoryStateOnSurface MuonMatcher::atMB1(FreeTrajectoryState ftsStart, bool& isInW2MB1) const {
  ReferenceCountingPointer<Surface> mb1;

  float w2Mb1_zMin = 410;
  float w2Mb1_zMax = 660;
  mb1 = ReferenceCountingPointer<Surface>(new BoundCylinder(
        GlobalPoint(0., 0., 0.), TkRotation<float>(), SimpleCylinderBounds(431.133, 431.133, w2Mb1_zMin, w2Mb1_zMax)));


  TrajectoryStateOnSurface trackAtMb1 = propagator->propagate(ftsStart, *mb1);
  if(!trackAtMb1.isValid()) {
    isInW2MB1 = false;
    LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::atMB1: "
            <<" ftsStart.position x: "<<ftsStart.position().x()<<" y " <<ftsStart.position().y()<<" z "<<ftsStart.position().z()<<" rho "<<ftsStart.position().perp()
            <<" ftsStart.momentum eta: "<<ftsStart.momentum().eta()<<" phi " <<ftsStart.momentum().phi()<<" propagation failed";
  }
  else {
    float trackZ = trackAtMb1.globalPosition().z();
    if( abs(trackZ) > w2Mb1_zMin && abs(trackZ) < w2Mb1_zMax)
      isInW2MB1 = true;

    LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::atMB1: "
        <<" ftsStart.position x: "<<ftsStart.position().x()<<" y " <<ftsStart.position().y()<<" z "<<ftsStart.position().z()<<" rho "<<ftsStart.position().perp()
        <<" ftsStart.momentum eta: "<<ftsStart.momentum().eta()<<" phi " <<ftsStart.momentum().phi()
        <<" trackAtMb1 eta "<<std::setw(8)<<trackAtMb1.globalPosition().eta()<<" phi "<<trackAtMb1.globalPosition().phi()<<" z "<<trackAtMb1.globalPosition().z()
        <<" isInW2MB1 "<<isInW2MB1<< std::endl;
  }

  return trackAtMb1;
}

FreeTrajectoryState MuonMatcher::simTrackToFts(const SimTrack& simTrackPtr, const edm::SimVertexContainer* simVertices) {
  //first find the vertex
  SimVertex simVertex;
  int vtxInd = simTrackPtr.vertIndex();
  if (vtxInd < 0){
    std::cout<<"Track with no vertex, defaulting to (0,0,0)"<<std::endl;
  }
  else {
    simVertex = simVertices->at(vtxInd);
    if(((int)simVertex.vertexId()) != vtxInd) {
      std::cout<<"simVertex.vertexId() != vtxInd !!!!!!!!!!!!!!!!!"<<std::endl;
      edm::LogImportant("l1MuonAnalyzerOmtf") <<"simVertex.vertexId() != vtxInd. simVertex.vertexId() "<<simVertex.vertexId()<<" vtxInd "<<vtxInd<<" !!!!!!!!!!!!!!!!!";
    }
  }


  int charge = simTrackPtr.type() > 0 ? -1 : 1; //works for muons

  CLHEP::Hep3Vector p3T(simTrackPtr.momentum().x(), simTrackPtr.momentum().y(), simTrackPtr.momentum().z());
  //if (p3T.mag()< 2.) continue;

  CLHEP::Hep3Vector  r3T = CLHEP::Hep3Vector(simVertex.position().x(),
                            simVertex.position().y(),
                            simVertex.position().z());


  GlobalVector p3GV(p3T.x(), p3T.y(), p3T.z());
  GlobalPoint r3GP(r3T.x(), r3T.y(), r3T.z());

  GlobalTrajectoryParameters tPars(r3GP, p3GV, charge, &*magField);

  //CartesianTrajectoryError tCov(cov);

  //return cov.kRows == 6 ? FreeTrajectoryState(tPars, tCov) : FreeTrajectoryState(tPars) ;

  return FreeTrajectoryState(tPars) ;
}

FreeTrajectoryState MuonMatcher::simTrackToFts(const TrackingParticle& trackingParticle) {
  int charge = trackingParticle.pdgId() > 0 ? -1 : 1; //works for muons

  CLHEP::Hep3Vector p3T(trackingParticle.momentum().x(), trackingParticle.momentum().y(), trackingParticle.momentum().z());
  //if (p3T.mag()< 2.) continue;

  CLHEP::Hep3Vector  r3T = CLHEP::Hep3Vector(trackingParticle.vx(), trackingParticle.vy(), trackingParticle.vz());


  GlobalVector p3GV(p3T.x(), p3T.y(), p3T.z());
  GlobalPoint r3GP(r3T.x(), r3T.y(), r3T.z());

  GlobalTrajectoryParameters tPars(r3GP, p3GV, charge, &*magField);

  //CartesianTrajectoryError tCov(cov);

  //return cov.kRows == 6 ? FreeTrajectoryState(tPars, tCov) : FreeTrajectoryState(tPars) ;

  return FreeTrajectoryState(tPars) ;
}

TrajectoryStateOnSurface MuonMatcher::propagate(const SimTrack& simTrack, const edm::SimVertexContainer* simVertices) {

  FreeTrajectoryState ftsTrack = simTrackToFts(simTrack, simVertices);

  TrajectoryStateOnSurface tsof = atStation2(ftsTrack, simTrack.momentum().eta() ); //propagation

  return tsof;
}


TrajectoryStateOnSurface MuonMatcher::propagate(const TrackingParticle& trackingParticle) {
  FreeTrajectoryState ftsTrack = simTrackToFts(trackingParticle);

  TrajectoryStateOnSurface tsof = atStation2(ftsTrack, trackingParticle.momentum().eta() ); //propagation

  return tsof;
}


float normal_pdf(float x, float m, float s) {
    static const float inv_sqrt_2pi = 0.3989422804014327;
    float a = (x - m) / s;

    return inv_sqrt_2pi / s * std::exp(-0.5 * a * a);
}

MatchingResult MuonMatcher::match(const l1t::RegionalMuonCand* muonCand, const SimTrack& simTrack, TrajectoryStateOnSurface& tsof) {
  MatchingResult result(simTrack);

  double candGloablEta  = muonCand->hwEta() * 0.010875;
  //if( abs(simTrack.momentum().eta() - candGloablEta ) < 0.3 ) TODO  in principle is replaced by using atMB1 !!!!!!!!!!!!!!!!!!!!!!!! check!!!!!!!!!!!!!!!
  {
    double candGlobalPhi = calcGlobalPhi( muonCand->hwPhi(), muonCand->processor(), nProcessors );
    candGlobalPhi = hwGmtPhiToGlobalPhi(candGlobalPhi );

    if(candGlobalPhi > M_PI)
      candGlobalPhi = candGlobalPhi -(2.*M_PI);

    result.deltaPhi = foldPhi(tsof.globalPosition().phi() - candGlobalPhi);
    result.deltaEta = tsof.globalPosition().eta() - candGloablEta;

    result.propagatedPhi = tsof.globalPosition().phi() ;
    result.propagatedEta = tsof.globalPosition().eta() ;

    double mean = 0;
    double sigma = 1;
    if(!fillMean) {
      auto ptBin = deltaPhiPropCandMean->FindBin(simTrack.momentum().pt());
      mean = deltaPhiPropCandMean->GetBinContent(ptBin);
      sigma = deltaPhiPropCandStdDev->GetBinContent(ptBin);
    }
    result.matchingLikelihood = normal_pdf(result.deltaPhi, mean, sigma); //TODO temporary solution

    result.muonCand = muonCand;

    //TODO chose the right sigma
    double treshold = 6. * sigma;
    if(simTrack.momentum().pt() > 20)
      treshold = 7. * sigma;
    if(simTrack.momentum().pt() > 100)
      treshold = 20. * sigma;

    if(simTrack.momentum().pt() > 20) //TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! tune the threshold!!!!!! - it is very big, why like that?
      treshold = 0.6;

    treshold = 0.3; //should be good for all pts in Displaced_Dxy3m_pT0To1000_condPhase2_realistic

    //for displaced muons in H2ll
    treshold = 0.15; //pt > 30
    if(simTrack.momentum().pt() < 10) //TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! tune the threshold!!!!!! - it is very big, why like that?
      treshold = 0.3;
    else if(simTrack.momentum().pt() < 30) //TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! tune the threshold!!!!!! - it is very big, why like that?
      treshold = 0.2;

    if( abs(result.deltaPhi - mean) < treshold)
      result.result = MatchingResult::ResultType::matched;

    LogTrace("l1MuonAnalyzerOmtf") <<"\nMuonMatcher::match: simTrack type "<<simTrack.type()<<" pt "<<std::setw(8)<<simTrack.momentum().pt()
        <<" eta "<<std::setw(8)<<simTrack.momentum().eta()<<" phi "<<std::setw(8)<<simTrack.momentum().phi()
        <<" propagation eta "<<std::setw(8)<<tsof.globalPosition().eta()<<" phi "<<tsof.globalPosition().phi()
        <<"\n             muonCand pt "<<std::setw(8)<<muonCand->hwPt()<<" candGloablEta "<<std::setw(8)<<candGloablEta<<" candGlobalPhi "<<std::setw(8)<<candGlobalPhi<<" hwQual "<<muonCand->hwQual()
        <<" deltaEta "<<std::setw(8)<<result.deltaEta<<" deltaPhi "<<std::setw(8)<<result.deltaPhi<<" sigma "<<std::setw(8)<<sigma<<" Likelihood "<<std::setw(8)<<result.matchingLikelihood <<" result "<<(short)result.result
        << std::endl;

/*    if(abs(result.deltaPhi) > 0.4)
      edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::match: simTrack type "<<simTrack.type()<<" pt "<<std::setw(8)<<simTrack.momentum().pt()
          <<" eta "<<std::setw(8)<<simTrack.momentum().eta()<<" phi "<<std::setw(8)<<simTrack.momentum().phi()
          <<" propagation eta "<<std::setw(8)<<tsof.globalPosition().eta()<<" phi "<<tsof.globalPosition().phi()
          <<" muonCand pt "<<std::setw(8)<<muonCand->hwPt()<<" candGloablEta "<<std::setw(8)<<candGloablEta<<" candGlobalPhi "<<std::setw(8)<<candGlobalPhi<<" hwQual "<<muonCand->hwQual()
          <<" deltaEta "<<std::setw(8)<<result.deltaEta<<" deltaPhi "<<std::setw(8)<<result.deltaPhi<<" Likelihood "<<std::setw(8)<<result.matchingLikelihood <<" result "<<(short)result.result
          << std::endl;*/

  }

  return result;
}

MatchingResult MuonMatcher::match(const l1t::RegionalMuonCand* muonCand, const TrackingParticle& trackingParticle, TrajectoryStateOnSurface& tsof) {
  MatchingResult result(trackingParticle);

  double candGloablEta  = muonCand->hwEta() * 0.010875;
  //if( abs(trackingParticle.momentum().eta() - candGloablEta ) < 0.3 ) TODO  in principle is replaced by using atMB1 !!!!!!!!!!!!!!!!!!!!!!!! check!!!!!!!!!!!!!!!
  {
    double candGlobalPhi = calcGlobalPhi( muonCand->hwPhi(), muonCand->processor(), nProcessors );
    candGlobalPhi = hwGmtPhiToGlobalPhi(candGlobalPhi );

    if(candGlobalPhi > M_PI)
      candGlobalPhi = candGlobalPhi -(2.*M_PI);

    result.deltaPhi = foldPhi(tsof.globalPosition().phi() - candGlobalPhi);
    result.deltaEta = tsof.globalPosition().eta() - candGloablEta;

    result.propagatedPhi = tsof.globalPosition().phi() ;
    result.propagatedEta = tsof.globalPosition().eta() ;


    double mean = 0;
    double sigma = 1;
    if(!fillMean) {
      auto ptBin = deltaPhiPropCandMean->FindBin(trackingParticle.pt());

      mean = deltaPhiPropCandMean->GetBinContent(ptBin);
      sigma = deltaPhiPropCandStdDev->GetBinContent(ptBin);
    }

    result.matchingLikelihood = normal_pdf(result.deltaPhi, mean, sigma); //TODO temporary solution

    result.muonCand = muonCand;

    double treshold = 6. * sigma;
    if(trackingParticle.pt() > 20)
      treshold = 7. * sigma;
    if(trackingParticle.pt() > 100)
      treshold = 20. * sigma;

    if( abs(result.deltaPhi - mean) < treshold)
      result.result = MatchingResult::ResultType::matched;

    LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::match: simTrack type "<<trackingParticle.pdgId()<<" pt "<<std::setw(8)<<trackingParticle.pt()
        <<" eta "<<std::setw(8)<<trackingParticle.momentum().eta()<<" phi "<<std::setw(8)<<trackingParticle.momentum().phi()
        <<" propagation eta "<<std::setw(8)<<tsof.globalPosition().eta()<<" phi "<<tsof.globalPosition().phi()
        <<" muonCand pt "<<std::setw(8)<<muonCand->hwPt()<<" candGloablEta "<<std::setw(8)<<candGloablEta<<" candGlobalPhi "<<std::setw(8)<<candGlobalPhi<<" hwQual "<<muonCand->hwQual()
        <<" deltaEta "<<std::setw(8)<<result.deltaEta<<" deltaPhi "<<std::setw(8)<<result.deltaPhi<<" Likelihood "<<std::setw(8)<<result.matchingLikelihood <<" result "<<(short)result.result
        << std::endl;

/*    if(abs(result.deltaPhi) > 0.4)
      edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::match: simTrack type "<<simTrack.type()<<" pt "<<std::setw(8)<<simTrack.momentum().pt()
          <<" eta "<<std::setw(8)<<simTrack.momentum().eta()<<" phi "<<std::setw(8)<<simTrack.momentum().phi()
          <<" propagation eta "<<std::setw(8)<<tsof.globalPosition().eta()<<" phi "<<tsof.globalPosition().phi()
          <<" muonCand pt "<<std::setw(8)<<muonCand->hwPt()<<" candGloablEta "<<std::setw(8)<<candGloablEta<<" candGlobalPhi "<<std::setw(8)<<candGlobalPhi<<" hwQual "<<muonCand->hwQual()
          <<" deltaEta "<<std::setw(8)<<result.deltaEta<<" deltaPhi "<<std::setw(8)<<result.deltaPhi<<" Likelihood "<<std::setw(8)<<result.matchingLikelihood <<" result "<<(short)result.result
          << std::endl;*/

  }

  return result;
}


std::vector<MatchingResult> MuonMatcher::cleanMatching(std::vector<MatchingResult> matchingResults, std::vector<const l1t::RegionalMuonCand*>& muonCands) {
  //Cleaning the matching
  std::sort(matchingResults.begin(), matchingResults.end(),
      [](const MatchingResult& a, const MatchingResult& b)->bool { return a.matchingLikelihood > b.matchingLikelihood; } );
  for(unsigned int i1 = 0; i1 < matchingResults.size(); i1++) {
    if(matchingResults[i1].result == MatchingResult::ResultType::matched) {
      for(unsigned int i2 = i1 + 1; i2 < matchingResults.size(); i2++) {
        if( (matchingResults[i1].trackingParticle && matchingResults[i1].trackingParticle == matchingResults[i2].trackingParticle) ||
            (matchingResults[i1].simTrack && matchingResults[i1].simTrack == matchingResults[i2].simTrack) ||
            (matchingResults[i1].muonCand == matchingResults[i2].muonCand) ) {
          //if matchingResults[i1].muonCand == false, then it is also OK here
          matchingResults[i2].result = MatchingResult::ResultType::duplicate;
        }
      }
    }
  }

  std::vector<MatchingResult> cleanedMatchingResults;
  for(auto& matchingResult : matchingResults) {
    if(matchingResult.result == MatchingResult::ResultType::matched  || matchingResult.muonCand == nullptr) //adding also the simTracks that are not matched at all, before it is assured that they are not duplicates
      cleanedMatchingResults.push_back(matchingResult);
    if(matchingResult.result == MatchingResult::ResultType::matched) {
      double ptGen = 0;

      ptGen = matchingResult.genPt;

      if(ptGen >= deltaPhiPropCand->GetXaxis()->GetXmax())
        ptGen = deltaPhiPropCand->GetXaxis()->GetXmax() - 0.01;

      deltaPhiPropCand->Fill(ptGen, matchingResult.deltaPhi);
      if(fillMean) {
        deltaPhiPropCandMean->Fill(ptGen, matchingResult.deltaPhi); //filling oveflow is ok here
        deltaPhiPropCandStdDev->Fill(ptGen, matchingResult.deltaPhi * matchingResult.deltaPhi);
      }
    }
  }

  //adding the muonCand-s that were not matched, i.e. in order to analyze them later
  for(auto& muonCand : muonCands) {
    bool isMatched = false;
    for(auto& matchingResult : cleanedMatchingResults) {
      if(matchingResult.muonCand == muonCand) {
        isMatched =  true;
        break;
      }
    }

    if(!isMatched) {
      MatchingResult result;
      result.muonCand = muonCand;
      cleanedMatchingResults.push_back(result);
    }
  }


  LogTrace("l1MuonAnalyzerOmtf")<<"\nMuonMatcher::match cleanedMatchingResults:"<<std::endl;
  for(auto& result : cleanedMatchingResults) {
    if(result.trackingParticle || result.simTrack)
      LogTrace("l1MuonAnalyzerOmtf")<<" simTrack type "<<result.pdgId<<" pt "<<std::setw(8)<<result.genPt
        <<" eta "<<std::setw(8)<<result.genEta<<" phi "<<std::setw(8)<<result.genPhi<< std::endl;
    else
      LogTrace("l1MuonAnalyzerOmtf")<<" no matched track";

        //<<" propagation eta "<<std::setw(8)<<tsof.globalPosition().eta()<<" phi "<<tsof.globalPosition().phi()
    if(result.muonCand)
      LogTrace("l1MuonAnalyzerOmtf")<<" muonCand pt "<<std::setw(8)<<result.muonCand->hwPt()
        <<std::setw(8)<<" upt "<<result.muonCand->hwPtUnconstrained()
        <<" hwQual "<<result.muonCand->hwQual()<<" hwEta "<<result.muonCand->hwEta()
        <<" deltaEta "<<std::setw(8)<<result.deltaEta<<" deltaPhi "<<std::setw(8)<<result.deltaPhi<<" Likelihood "<<std::setw(8)<<result.matchingLikelihood <<" result "<<(short)result.result
        << std::endl;
    else
      LogTrace("l1MuonAnalyzerOmtf")<<" no muonCand "<<" result "<<(short)result.result<< std::endl;

    LogTrace("l1MuonAnalyzerOmtf")<<std::endl;
  }
  LogTrace("l1MuonAnalyzerOmtf")<<"\n"<<std::endl;

  return cleanedMatchingResults;
}

std::vector<MatchingResult> MuonMatcher::match(std::vector<const l1t::RegionalMuonCand*>& muonCands, const edm::SimTrackContainer* simTracks, const edm::SimVertexContainer* simVertices,
    std::function<bool(const SimTrack& )> const& simTrackFilter, bool checkIsInW2MB1)
{
  std::vector<MatchingResult> matchingResults;

  int muonCnt = 0;
  int muonCntInOmtf = 0;
  for (auto& simTrack : *simTracks ) {

    if (abs(simTrack.type()) == 13 || abs(simTrack.type()) == 1000015 )
      muonCnt++;

    if(!simTrackFilter(simTrack))
      continue;

    FreeTrajectoryState ftsStart = simTrackToFts(simTrack, simVertices);
    if(checkIsInW2MB1) {
      bool isInW2MB1 = false;

      auto trackAtMb1 =  atMB1(ftsStart, isInW2MB1);

      if(!isInW2MB1)
        continue;
    }

    bool matched = false;

    TrajectoryStateOnSurface tsof = atStation2(ftsStart, simTrack.momentum().eta() ); //propagation

    if(!tsof.isValid()) {
      LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::match: simTrack type "<<std::setw(3)<<simTrack.type()<<" pt "<<std::setw(9)<<simTrack.momentum().pt()<<" eta "<<std::setw(9)<<simTrack.momentum().eta()<<" phi "<<std::setw(9)<<simTrack.momentum().phi()<<std::endl;
      LogTrace("l1MuonAnalyzerOmtf") <<__FUNCTION__<<":"<<__LINE__<<" propagation failed"<<std::endl;
      MatchingResult result;
      result.result = MatchingResult::ResultType::propagationFailed;
      continue; //no sense to do matching
    }

    //checking if the propagated track is inside the OMTF range, TODO - tune the range!!!!!!!!!!!!!!!!!
    //eta 0.7 is the beginning of the MB2,
    //this complates the cut from atMB1
    if( (fabs( tsof.globalPosition().eta()) >= 0.7 ) && (fabs( tsof.globalPosition().eta()) <= 1.3) ) {
      LogTrace("l1tOmtfEventPrint") << "CandidateSimMuonMatcher::match trackingParticle IS in OMTF region, matching to the omtfCands";
    }
    else {
      LogTrace("l1tOmtfEventPrint") << "trackingParticle NOT in OMTF region ";
      continue;
    }

    muonCntInOmtf++;

    double ptGen = simTrack.momentum().pt();
    if(ptGen >= deltaPhiVertexProp->GetXaxis()->GetXmax())
      ptGen = deltaPhiVertexProp->GetXaxis()->GetXmax() - 0.01;


    deltaPhiVertexProp->Fill(ptGen, simTrack.momentum().phi() - tsof.globalPosition().phi());


    for(auto& muonCand : muonCands) {
      //int refLayer = (int)omtfCand->trackAddress().at(1);
      //int layerHits = (int)omtfCand->trackAddress().at(0);
      //std::bitset<18> layerHitBits(layerHits);

      if(muonCand->hwQual() <= 1) //dropping very low quality candidates, as they are fakes usually
        continue;

      MatchingResult result = match(muonCand, simTrack, tsof);

      int vtxInd = simTrack.vertIndex();
      if (vtxInd >= 0) {
        result.simVertex = &(simVertices->at(vtxInd));
      }

      if(result.result == MatchingResult::ResultType::matched) {
        matchingResults.push_back(result);
        matched = true;
      }
    }

    if(!matched) { //we are adding also if it was not matching to any candidate
      MatchingResult result(simTrack);
      //result.simTrack = &simTrack;
      /*auto trackingParticle = new TrackingParticle();//work arroung -- theefficiency analysis works on the tracking particles
      trackingParticle->addG4Track(simTrack);
      result.trackingParticle = trackingParticle;*/

      result.propagatedPhi = tsof.globalPosition().phi() ;
      result.propagatedEta = tsof.globalPosition().eta() ;

      int vtxInd = simTrack.vertIndex();
      if (vtxInd >= 0) {
        result.simVertex = &(simVertices->at(vtxInd));
      }

      matchingResults.push_back(result);
      LogTrace("l1MuonAnalyzerOmtf") <<__FUNCTION__<<":"<<__LINE__<<" no matching candidate found"<<std::endl;
    }
  }

  muonsPerEvent->Fill(muonCnt);
  muonsPerEventInOmtf->Fill(muonCntInOmtf);

  return cleanMatching(matchingResults, muonCands);
}

std::vector<MatchingResult> MuonMatcher::match(std::vector<const l1t::RegionalMuonCand*>& muonCands, const TrackingParticleCollection* trackingParticles,
    std::function<bool(const TrackingParticle& )> const& simTrackFilter)
{
  std::vector<MatchingResult> matchingResults;
  LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::match trackingParticles->size() "<<trackingParticles->size()<<std::endl;

  for (auto& trackingParticle : *trackingParticles ) {
    //LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::match:"<<__LINE__<<" trackingParticle type "<<std::setw(3)<<trackingParticle.pdgId()<<" pt "<<std::setw(9)<<trackingParticle.pt()<<" eta "<<std::setw(9)<<trackingParticle.momentum().eta()<<" phi "<<std::setw(9)<<trackingParticle.momentum().phi()<<std::endl;

    if(simTrackFilter(trackingParticle) == false)
      continue;

    LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::match, trackingParticle type "<<std::setw(3)<<trackingParticle.pdgId()<<" pt "<<std::setw(9)<<trackingParticle.pt()<<" eta "<<std::setw(9)<<trackingParticle.momentum().eta()<<" phi "<<std::setw(9)<<trackingParticle.momentum().phi()<<std::endl;

    bool matched = false;

    TrajectoryStateOnSurface tsof = propagate(trackingParticle);
    if(!tsof.isValid()) {
      LogTrace("l1MuonAnalyzerOmtf") <<__FUNCTION__<<":"<<__LINE__<<" propagation failed"<<std::endl;
      MatchingResult result;
      result.result = MatchingResult::ResultType::propagationFailed;
      continue; //no sense to do matching
    }

    //checking if the propagated track is inside the OMTF range, TODO - tune the range!!!!!!!!!!!!!!!!!
    //eta 0.7 is the beginning of the MB2,
    if( (fabs( tsof.globalPosition().eta()) >= 0.7 ) && (fabs( tsof.globalPosition().eta()) <= 1.3) ) {
      LogTrace("l1tOmtfEventPrint") << "CandidateSimMuonMatcher::match trackingParticle IS in OMTF region, matching to the omtfCands";
    }
    else {
      LogTrace("l1tOmtfEventPrint") << "trackingParticle NOT in OMTF region ";
      continue;
    }

    double ptGen = trackingParticle.pt();
    if(ptGen >= deltaPhiVertexProp->GetXaxis()->GetXmax())
      ptGen = deltaPhiVertexProp->GetXaxis()->GetXmax() - 0.01;


    deltaPhiVertexProp->Fill(ptGen, trackingParticle.momentum().phi() - tsof.globalPosition().phi());

    for(auto& muonCand : muonCands) {
      //int refLayer = (int)omtfCand->trackAddress().at(1);
      //int layerHits = (int)omtfCand->trackAddress().at(0);
      //std::bitset<18> layerHitBits(layerHits);

      /*if(muonCand->hwQual() <= 1) //dropping very low quality candidates, as they are fakes usually
        continue; has no sense, then the results are not conclusive*/

      MatchingResult result;
      if(tsof.isValid()) {
        result = match(muonCand, trackingParticle, tsof);
      }
      else //only for muons with pt < 3.5
        result = match(muonCand, trackingParticle);

      if(result.result == MatchingResult::ResultType::matched) {
        matchingResults.push_back(result);
        matched = true;
      }
    }

    if(!matched) { //we are adding also if it was not matching to any candidate
      MatchingResult result(trackingParticle);
      matchingResults.push_back(result);
      LogTrace("l1MuonAnalyzerOmtf") <<__FUNCTION__<<":"<<__LINE__<<" no matching candidate found"<<std::endl;
    }
  }

  return cleanMatching(matchingResults, muonCands);
}

void MuonMatcher::fillHists(std::vector<const l1t::RegionalMuonCand*>& muonCands, const edm::SimTrackContainer* simTracks,  std::function<bool(const SimTrack& )> const& simTrackFilter)
{
  std::vector<MatchingResult> matchingResults;

  for (auto& simTrack : *simTracks ) {

    if(!simTrackFilter(simTrack))
      continue;

    LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::fillHists, simTrack type "<<std::setw(3)<<simTrack.type()<<" pt "<<std::setw(9)<<simTrack.momentum().pt()<<" eta "<<std::setw(9)<<simTrack.momentum().eta()<<" phi "<<std::setw(9)<<simTrack.momentum().phi()<<std::endl;

    double ptGen = simTrack.momentum().pt();
    if(ptGen >= deltaPhiVertexProp->GetXaxis()->GetXmax())
      ptGen = deltaPhiVertexProp->GetXaxis()->GetXmax() - 0.01;

    for(auto& muonCand : muonCands) {
      if(muonCand->hwQual() <= 1) //dropping very low quality candidates, as they are fakes usually
        continue;


      double candGloablEta  = muonCand->hwEta() * 0.010875;
      if( abs(simTrack.momentum().eta() - candGloablEta ) < 0.3 ) {
        double candGlobalPhi = calcGlobalPhi( muonCand->hwPhi(), muonCand->processor(), nProcessors );
        candGlobalPhi = hwGmtPhiToGlobalPhi(candGlobalPhi );

        if(candGlobalPhi > M_PI)
          candGlobalPhi = candGlobalPhi -(2.*M_PI);

        double deltaPhi = foldPhi(simTrack.momentum().phi() - candGlobalPhi);

        if(simTrack.type() > 0) {
          ptGen_pos->Fill(simTrack.momentum().pt());
          deltaPhiVertexCand_Mean_pos->Fill(simTrack.momentum().pt(), deltaPhi); //filling overflow is ok here
          deltaPhiVertexCand_StdDev_pos->Fill(simTrack.momentum().pt(), deltaPhi * deltaPhi);
        }
        else {
          ptGen_neg->Fill(simTrack.momentum().pt());
          deltaPhiVertexCand_Mean_neg->Fill(simTrack.momentum().pt(), deltaPhi); //filling overflow is ok here
          deltaPhiVertexCand_StdDev_neg->Fill(simTrack.momentum().pt(), deltaPhi * deltaPhi);
        }

        deltaPhiVertexProp->Fill(ptGen, deltaPhi);
      }
    }
  }
}

MatchingResult MuonMatcher::match(const l1t::RegionalMuonCand* muonCand, const TrackingParticle& trackingParticle) {
  MatchingResult result(trackingParticle);

  double candGloablEta  = muonCand->hwEta() * 0.010875;

  result.deltaEta = trackingParticle.momentum().eta() - candGloablEta;
  if( abs(result.deltaEta) < 0.3 ) {
    double candGlobalPhi = calcGlobalPhi( muonCand->hwPhi(), muonCand->processor(), nProcessors );
    candGlobalPhi = hwGmtPhiToGlobalPhi(candGlobalPhi );

    if(candGlobalPhi > M_PI)
      candGlobalPhi = candGlobalPhi -(2.*M_PI);

    result.deltaPhi = foldPhi(trackingParticle.momentum().phi() - candGlobalPhi);


    double meanDeltaPhi = 0;
    double sigma = 1;
    /* makes no difference on the single nu sample
    if(trackingParticle.pt() > 3 && trackingParticle.pt() < 3.5) {
      meanDeltaPhi = 0.94; //values based on muonMatcherHists_noPropagation_t74.root
      sigma = 0.12;
    }
    else if (trackingParticle.pt() < 3) {
      meanDeltaPhi = 1;
      sigma = 0.2;
    }
    else
      return result;

    if(trackingParticle.pdgId() > 0) {
      meanDeltaPhi *= -1;
    }*/

    if(trackingParticle.pdgId() > 0) {
      auto ptBin = deltaPhiVertexCand_Mean_pos->FindBin(trackingParticle.pt());

      meanDeltaPhi  = deltaPhiVertexCand_Mean_pos->GetBinContent(ptBin);
      sigma = deltaPhiVertexCand_StdDev_pos->GetBinContent(ptBin);
    }
    else {
      auto ptBin = deltaPhiVertexCand_Mean_neg->FindBin(trackingParticle.pt());

      meanDeltaPhi  = deltaPhiVertexCand_Mean_neg->GetBinContent(ptBin);
      sigma = deltaPhiVertexCand_StdDev_neg->GetBinContent(ptBin);
    }

    result.propagatedPhi = foldPhi(trackingParticle.momentum().phi() + meanDeltaPhi) ;
    result.propagatedEta = trackingParticle.momentum().eta() ;

    result.matchingLikelihood = normal_pdf(result.deltaPhi, meanDeltaPhi, sigma); //TODO temporary solution

    result.muonCand = muonCand;

    double treshold = 6. * sigma;
    if(trackingParticle.pt() > 20)
      treshold = 7. * sigma;
    if(trackingParticle.pt() > 100)
      treshold = 20. * sigma;

    if( abs(result.deltaPhi - meanDeltaPhi) < treshold)
      result.result = MatchingResult::ResultType::matched;

    edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::match without propoagation: simTrack type "<<trackingParticle.pdgId()<<" pt "<<std::setw(8)<<trackingParticle.pt()
        <<" eta "<<std::setw(8)<<trackingParticle.momentum().eta()<<" phi "<<std::setw(8)<<trackingParticle.momentum().phi()
        <<" propagation eta "<<std::setw(8)<<result.propagatedEta<<" phi "<<result.propagatedPhi
        <<" muonCand pt "<<std::setw(8)<<muonCand->hwPt()<<" candGloablEta "<<std::setw(8)<<candGloablEta<<" candGlobalPhi "<<std::setw(8)<<candGlobalPhi<<" hwQual "<<muonCand->hwQual()
        <<" deltaEta "<<std::setw(8)<<result.deltaEta<<" deltaPhi "<<std::setw(8)<<result.deltaPhi<<" Likelihood "<<std::setw(8)<<result.matchingLikelihood <<" result "<<(short)result.result
        << std::endl;

/*    if(abs(result.deltaPhi) > 0.4)
      edm::LogImportant("l1MuonAnalyzerOmtf") <<"MuonMatcher::match: simTrack type "<<simTrack.type()<<" pt "<<std::setw(8)<<simTrack.momentum().pt()
          <<" eta "<<std::setw(8)<<simTrack.momentum().eta()<<" phi "<<std::setw(8)<<simTrack.momentum().phi()
          <<" propagation eta "<<std::setw(8)<<tsof.globalPosition().eta()<<" phi "<<tsof.globalPosition().phi()
          <<" muonCand pt "<<std::setw(8)<<muonCand->hwPt()<<" candGloablEta "<<std::setw(8)<<candGloablEta<<" candGlobalPhi "<<std::setw(8)<<candGlobalPhi<<" hwQual "<<muonCand->hwQual()
          <<" deltaEta "<<std::setw(8)<<result.deltaEta<<" deltaPhi "<<std::setw(8)<<result.deltaPhi<<" Likelihood "<<std::setw(8)<<result.matchingLikelihood <<" result "<<(short)result.result
          << std::endl;*/

  }

  return result;
}

/*
 * Using this matching has sense only for the prompt muons.
 */
std::vector<MatchingResult> MuonMatcher::matchSimple(std::vector<const l1t::RegionalMuonCand*>& muonCands,
    const edm::SimTrackContainer* simTracks,
    const edm::SimVertexContainer* simVertices,
    std::function<bool(const SimTrack&)> const& simTrackFilter) {
  std::vector<MatchingResult> matchingResults;

  int muonCnt = 0;
  int muonCntInOmtf = 0;

  for (auto& simTrack : *simTracks) {
    if (abs(simTrack.type()) == 13 || abs(simTrack.type()) == 1000015 )
      muonCnt++;

    if (!simTrackFilter(simTrack))
      continue;

    LogTrace("l1tOmtfEventPrint") << "MuonMatcher::matchSimple: simTrack type " << std::setw(3) << simTrack.type()
                                          << " pt " << std::setw(9) << simTrack.momentum().pt() << " eta " << std::setw(9)
                                          << simTrack.momentum().eta() << " phi " << std::setw(9) << simTrack.momentum().phi()
                                          << std::endl;

    muonCntInOmtf++;

    bool matched = false;

    unsigned int iCand = 0;
    for (auto& muonCand : muonCands) {
      //dropping very low quality candidates, as they are fakes usually - but it has no sense, then the results are not conclusive
      //if(muonCand->hwQual() > 1)
      {
        MatchingResult result(simTrack);

        double candGloablEta = muonCand->hwEta() * 0.010875;
        double candGlobalPhi = calcGlobalPhi( muonCand->hwPhi(), muonCand->processor(), nProcessors );
        candGlobalPhi = hwGmtPhiToGlobalPhi(candGlobalPhi );

        if (candGlobalPhi > M_PI)
          candGlobalPhi = candGlobalPhi - (2. * M_PI);

        result.deltaPhi = foldPhi(result.genPhi - candGlobalPhi);
        result.deltaEta = result.genEta - candGloablEta;

        result.propagatedPhi = result.genPhi;
        result.propagatedEta = result.genEta;

        result.muonCand = muonCand;

        //TODO histogram can be used, like in the MuonMatcher::matchWithoutPorpagation
        //for prompt muons
        double treshold = 0.3;
        if (simTrack.momentum().pt() < 5)
          treshold = 1.5;
        else if (simTrack.momentum().pt() < 8)
          treshold = 1.0;
        else if (simTrack.momentum().pt() < 10)
          treshold = 0.8;
        else if (simTrack.momentum().pt() < 20)
          treshold = 0.5;

        //for displaced muons
        /*double treshold = 0.7;
        if (simTrack.momentum().pt() < 5)
          treshold = 1.5;
        else if (simTrack.momentum().pt() < 10)
          treshold = 1.0;
        else if (simTrack.momentum().pt() < 20)
          treshold = 0.7;*/

        if (std::abs(result.deltaPhi) < treshold && std::abs(result.deltaEta) < 0.5) {
          result.result = MatchingResult::ResultType::matched;
          //matchingLikelihood is needed in the cleanMatching, so we put something
          if(std::abs(result.deltaPhi) < 0.001)
            result.matchingLikelihood = 1./ 0.001;
          else
            result.matchingLikelihood = 1./ std::abs(result.deltaPhi);
        }

        LogTrace("l1tOmtfEventPrint") << "MuonMatcher::matchSimple: simTrack type " << simTrack.type() << " pt "
            << std::setw(8) << simTrack.momentum().pt() << " eta " << std::setw(8)
            << simTrack.momentum().eta() << " phi " << std::setw(8) << simTrack.momentum().phi()
            << "\n             muonCand pt " << std::setw(8)
            << muonCand->hwPt() << " candGloablEta " << std::setw(8) << candGloablEta
            << " candGlobalPhi " << std::setw(8) << candGlobalPhi
            << " hwQual "<< muonCand->hwQual()
            << " deltaEta " << std::setw(8) << result.deltaEta
            << " deltaPhi " << std::setw(8) << result.deltaPhi
            << " matchingLikelihood " << result.matchingLikelihood
            << " result " << (short)result.result << std::endl;


        int vtxInd = simTrack.vertIndex();
        if (vtxInd >= 0) {
          result.simVertex = &(
              simVertices->at(vtxInd));
        }
        if (result.result == MatchingResult::ResultType::matched) {
          matchingResults.push_back(result);
          matched = true;
        }
      }
      iCand++;
    }


    if (!matched) {  //we are adding also if it was not matched to any candidate
      MatchingResult result(simTrack);
      matchingResults.push_back(result);
      LogTrace("l1tOmtfEventPrint") << __FUNCTION__ << ":" << __LINE__ << " no matching candidate found" << std::endl;
    }
  }

  muonsPerEvent->Fill(muonCnt);
  muonsPerEventInOmtf->Fill(muonCntInOmtf);

  return cleanMatching(matchingResults, muonCands);
}


/*
 * Using tis matching has sense only for the prompt muons.
 * The delta phi (phi at vertex - phi cand) distributions are wider then with the propagation,
 * because the distribution (phi at vertex - phi propagated) is not symmetric, (not Gaussian) due to energy losses
 * so matching is worse ten this with propagation
 */
std::vector<MatchingResult> MuonMatcher::matchWithoutPorpagation(std::vector<const l1t::RegionalMuonCand*>& muonCands, const TrackingParticleCollection* trackingParticles,
    std::function<bool(const TrackingParticle& )> const& simTrackFilter)
{
  std::vector<MatchingResult> matchingResults;
  LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::match trackingParticles->size() "<<trackingParticles->size()<<std::endl;

  for (auto& trackingParticle : *trackingParticles ) {
    //LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::match:"<<__LINE__<<" trackingParticle type "<<std::setw(3)<<trackingParticle.pdgId()<<" pt "<<std::setw(9)<<trackingParticle.pt()<<" eta "<<std::setw(9)<<trackingParticle.momentum().eta()<<" phi "<<std::setw(9)<<trackingParticle.momentum().phi()<<std::endl;

    if(simTrackFilter(trackingParticle) == false)
      continue;

    LogTrace("l1MuonAnalyzerOmtf") <<"MuonMatcher::match, trackingParticle type "<<std::setw(3)<<trackingParticle.pdgId()<<" pt "<<std::setw(9)<<trackingParticle.pt()<<" eta "<<std::setw(9)<<trackingParticle.momentum().eta()<<" phi "<<std::setw(9)<<trackingParticle.momentum().phi()<<std::endl;

    bool matched = false;

    double ptGen = trackingParticle.pt();
    if(ptGen >= deltaPhiVertexCand_Mean_pos->GetXaxis()->GetXmax())
      ptGen = deltaPhiVertexCand_Mean_pos->GetXaxis()->GetXmax() - 0.01;


    for(auto& muonCand : muonCands) {
      //int refLayer = (int)omtfCand->trackAddress().at(1);
      //int layerHits = (int)omtfCand->trackAddress().at(0);
      //std::bitset<18> layerHitBits(layerHits);

      /*if(muonCand->hwQual() <= 1) //dropping very low quality candidates, as they are fakes usually
        continue; has no sense, then the results are not conclusive*/

      MatchingResult result = match(muonCand, trackingParticle);
      if(result.result == MatchingResult::ResultType::matched) {
        matchingResults.push_back(result);
        matched = true;
      }

      deltaPhiVertexProp->Fill(ptGen, trackingParticle.momentum().phi() - result.deltaPhi);
    }

    if(!matched) { //we are adding the track also if it was not matching to any candidate
      MatchingResult result(trackingParticle);
      matchingResults.push_back(result);
      LogTrace("l1MuonAnalyzerOmtf") <<__FUNCTION__<<":"<<__LINE__<<" no matching candidate found"<<std::endl;
    }
  }

  return cleanMatching(matchingResults, muonCands);
}

}
