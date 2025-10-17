/*
 * RateAnalyser.cc
 *
 *  Created on: Apr 1, 2020
 *      Author: kbunkow
 */

#include "usercode/L1MuonAnalyzer/interface/RateAnalyser.h"
#include "usercode/L1MuonAnalyzer/interface/MuonMatcher.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

namespace L1MuAn {

RateAnalyser::RateAnalyser(TFileDirectory subDir, std::string name, int qualityCut, int nBins, double binsFrom, double binsTo, int nProcessors):
    qualityCut(qualityCut), nProcessors(nProcessors) {
  std::ostringstream histName;
  std::ostringstream histTitle;

  histName<<"candPt_"<<"_qualityCut_"<<qualityCut;
  histTitle<<name<<" cand pt, "<<" quality >= "<<qualityCut<<";cand pt [GeV]; #events";

  candPt = subDir.make<TH1D>(histName.str().c_str(), histTitle.str().c_str(), nBins, binsFrom, binsTo);

  histName.str("");
  histTitle.str("");

  histName<<"candUPt_"<<"_qualityCut_"<<qualityCut;
  histTitle<<name<<" cand upt, "<<" quality >= "<<qualityCut<<";cand upt [GeV]; #events";

  candUPt = subDir.make<TH1D>(histName.str().c_str(), histTitle.str().c_str(), nBins, binsFrom, binsTo);

  histName.str("");
  histTitle.str("");

  histName<<"candEta_PtCut1GeV_"<<"_qualityCut_"<<qualityCut;
  histTitle<<name<<" cand Eta, ptCut 1 GeV "<<" quality >= "<<qualityCut<<";eta; #events";

  candEtaPtCut1 = subDir.make<TH1D>(histName.str().c_str(), histTitle.str().c_str(), 100, -2.1, 2.1);

  histName.str("");
  histTitle.str("");

  histName<<"candEta_PtCut10GeV_"<<"_qualityCut_"<<qualityCut;
  histTitle<<name<<" cand Eta, ptCut 10 GeV "<<" quality >= "<<qualityCut<<";eta; #events";

  candEtaPtCut10 = subDir.make<TH1D>(histName.str().c_str(), histTitle.str().c_str(), 100, -2.1, 2.1);

  histName.str("");
  histTitle.str("");

  histName<<"candEta_PtCut22GeV_"<<"_qualityCut_"<<qualityCut;
  histTitle<<name<<" cand Eta, ptCut 22 GeV "<<" quality >= "<<qualityCut<<";eta; #events";

  candEtaPtCut22 = subDir.make<TH1D>(histName.str().c_str(), histTitle.str().c_str(), 100, -2.1, 2.1);

  histName.str("");
  histTitle.str("");

  histName<<"candPhi_PtCut10GeV_"<<"_qualityCut_"<<qualityCut;
  histTitle<<name<<" cand phi, ptCut 10 GeV "<<" quality >= "<<qualityCut<<";phi [deg]; #events";

  candPhiPtCut10 = subDir.make<TH1D>(histName.str().c_str(), histTitle.str().c_str(), 180, 0, 360);

  histName.str("");
  histTitle.str("");

  histName<<"candPhi_PtCut22GeV_"<<"_qualityCut_"<<qualityCut;
  histTitle<<name<<" cand phi, ptCut 22 GeV "<<" quality >= "<<qualityCut<<";phi [deg]; #events";

  candPhiPtCut22 = subDir.make<TH1D>(histName.str().c_str(), histTitle.str().c_str(), 180, 0, 360);

}

RateAnalyser::~RateAnalyser() {
  // TODO Auto-generated destructor stub
}

///center of eta bin
double hwEtaToEta(int hwEta) {
  double etaUnit = 0.010875; //TODO from the interface note, should be defined somewhere globally

  return (hwEta * etaUnit);
}


void RateAnalyser::fill(L1MuonCand& l1MuonCand) {
  auto candPtGev = l1MuonCand.ptGev;
  if(candPtGev >= candPt->GetXaxis()->GetXmax())
    candPtGev = candPt->GetXaxis()->GetXmax() - 0.01;

  auto candUPtGev = l1MuonCand.uptGev;
  if(candUPtGev >= candUPt->GetXaxis()->GetXmax())
    candUPtGev = candUPt->GetXaxis()->GetXmax() - 0.01;

  if(l1MuonCand.hwQual >= qualityCut) {
    candPt->Fill(candPtGev);
    candUPt->Fill(candUPtGev);

    auto eta = l1MuonCand.etaRad;

    double candGlobalPhi = l1MuonCand.phiRad;
    double phi = L1MuAn::hwGmtPhiToGlobalPhi(candGlobalPhi ); //[rad]
    phi =  phi * 180. / M_PI;

    if(candPtGev >= 1.)
      candEtaPtCut1->Fill(eta);

    if(candPtGev >= 10.) {
      candEtaPtCut10->Fill(eta);
      candPhiPtCut10->Fill(phi);
    }

    if(candPtGev >= 22.) {
      candEtaPtCut22->Fill(eta);
      candPhiPtCut22->Fill(phi);
    }
  }

}

void RateAnalyser::write() {
  candPt->Write();
  candUPt->Write();

  candEtaPtCut1->Write();
  candEtaPtCut10->Write();
  candEtaPtCut22->Write();
}

/*
PtGenVsPtCand promptMuonsPtGenVsPtCand;
PtGenVsPtCand nonPromptMuonsPtGenVsPtCand;

PtGenVsPtCand muonsFromPionsPtGenVsPtCand;
PtGenVsPtCand muonsFromKaonsPtGenVsPtCand;*/

CandsMatchingAnalyser::CandsMatchingHists::CandsMatchingHists(TFileDirectory& parrentSubDir, std::string name, int qualityCut, int nBins, double binsFrom, double binsTo, int nProcessors):
    subDir(parrentSubDir.mkdir(name)),
    qualityCut(qualityCut),
    rateAn(subDir, name, qualityCut, nBins, binsFrom, binsTo, nProcessors),
    ptGenVsPtCand(subDir, "", 0.82, 1.24, qualityCut, 100, 0, 100)
{
  std::ostringstream histName;
  std::ostringstream histTitle;

  histName<<"_simVertexRhoVsPtGen_"<<"_qualityCut_"<<qualityCut;
  histTitle<<name<<" simVertexRho Vs genPt, "<<" quality >= "<<qualityCut<<"; genPt [GeV]; Rho [cm]";

  simVertexRhoVsPtGen = subDir.make<TH2I>(histName.str().c_str(), histTitle.str().c_str(), 100, binsFrom, binsTo, 30, 0, 300);
}

void CandsMatchingAnalyser::CandsMatchingHists::fill(L1MuonCand& l1MuonCand, const TrackingParticle* matchedTrackingParticle,  double simVertexRho) {
  rateAn.fill(l1MuonCand);

  ptGenVsPtCand.fill(matchedTrackingParticle->pt(), matchedTrackingParticle->eta(), matchedTrackingParticle->phi(), 0, l1MuonCand);

  if(l1MuonCand.hwQual >= qualityCut) {
    simVertexRhoVsPtGen->Fill(matchedTrackingParticle->pt(), simVertexRho);
  }

}

void CandsMatchingAnalyser::CandsMatchingHists::write() {
  rateAn.write();
  ptGenVsPtCand.write();
  simVertexRhoVsPtGen->Write();
}

CandsMatchingAnalyser::CandsMatchingAnalyser(TFileDirectory& subDir, std::string name, int qualityCut, int nBins, double binsFrom, double binsTo, int nProcessors):
    promptMuons(subDir, "promptMuons", qualityCut, nBins, binsFrom, binsTo, nProcessors),
    nonPromptMuons(subDir, "nonPromptMuons", qualityCut, nBins, binsFrom, binsTo, nProcessors),
    muonsFromPions(subDir, "muonsFromPions", qualityCut, nBins, binsFrom, binsTo, nProcessors),
    muonsFromKaons(subDir, "muonsFromKaons", qualityCut, nBins, binsFrom, binsTo, nProcessors),
    notMatchedRateAn(subDir.mkdir("notMatched"), "notMatched", qualityCut, nBins, binsFrom, binsTo, nProcessors),
    likelihoodDistribution(subDir, name, qualityCut, 0, 20, 120)
{

  std::ostringstream histName;
  std::ostringstream histTitle;

  histName<<name<<"simVertexRhoVsPtGen_"<<"_qualityCut_"<<qualityCut;
  histTitle<<name<<" simVertexRho Vs genPt, "<<" quality >= "<<qualityCut<<"; genPt [GeV]; Rho [cm]";

  simVertexRhoVsPtGen = subDir.make<TH2I>(histName.str().c_str(), histTitle.str().c_str(), 100, binsFrom, binsTo, 30, 0, 300);

}

void CandsMatchingAnalyser::fill(L1MuonCand& l1MuonCand, const TrackingParticle* matchedTrackingParticle) {
  if(matchedTrackingParticle) {
    int parentTrackPdgId = 0;


    if(matchedTrackingParticle->parentVertex().isNonnull() ) {
      LogTrace("l1MuonAnalyzerOmtf")<<" CandsMatchingAnalyser parentVertex Rho "<<matchedTrackingParticle->parentVertex()->position().Rho()
                                      <<" parentVertex()->sourceTracks().size() "<< matchedTrackingParticle->parentVertex()->sourceTracks().size() <<std::endl;
      for(auto& parentTrack : matchedTrackingParticle->parentVertex()->sourceTracks() ) {
        parentTrackPdgId = parentTrack->pdgId();
        LogTrace("l1MuonAnalyzerOmtf")<<" CandsMatchingAnalyser parentTrackPdgId "<<parentTrackPdgId<<std::endl;
      }
    }

    if (parentTrackPdgId == 0) {
      promptMuons.fill(l1MuonCand, matchedTrackingParticle, 0);
    }
    else {
      double simVertexRho = matchedTrackingParticle->parentVertex()->position().Rho();

      simVertexRhoVsPtGen->Fill(matchedTrackingParticle->pt(), simVertexRho);

      if(simVertexRho > 10) {
        nonPromptMuons.fill(l1MuonCand, matchedTrackingParticle, simVertexRho);
      }
      else {
        promptMuons.fill(l1MuonCand, matchedTrackingParticle, simVertexRho);
      }

      if(abs(parentTrackPdgId) == 211) {
        muonsFromPions.fill(l1MuonCand, matchedTrackingParticle, simVertexRho);
      }
      else if(abs(parentTrackPdgId) == 321) {
        muonsFromKaons.fill(l1MuonCand, matchedTrackingParticle, simVertexRho);
      }
    }
  }
  else {
    notMatchedRateAn.fill(l1MuonCand);
  }

  likelihoodDistribution.fill(0, 0, 0, 0, l1MuonCand);
}

/*void CandsMatchingAnalyser::fill(L1MuonCand& l1MuonCand, const SimTrack* matchedSimTrack, const edm::SimVertexContainer* simVertices) {
  if(matchedSimTrack) {
    int vtxInd = matchedSimTrack->vertIndex();
    if (vtxInd < 0) {
      promptMuonsRateAn.fill(l1MuonCand);
      simVertexRhoVsPtGen->Fill(l1MuonCand.ptGev, 0.);
    }
    else {
      const SimVertex& simVertex = simVertices->at(vtxInd);

      //simVertex.parentIndex();
      //matchedSimTrack->trackId();

      double simVertexRho = simVertex.position().Rho();

      simVertexRhoVsPtGen->Fill(l1MuonCand.ptGev, simVertexRho);

      if(simVertexRho > 10) {
        nonPromptMuonsRateAn.fill(l1MuonCand);
      }
      else {
        promptMuonsRateAn.fill(l1MuonCand);
      }
    }
  }
  else {
    notMatchedRateAn.fill(l1MuonCand);
  }

  likelihoodDistribution.fill(0, 0, 0, l1MuonCand);
}*/


void CandsMatchingAnalyser::write() {
  promptMuons.write();
  nonPromptMuons.write();
  muonsFromPions.write();
  muonsFromKaons.write();
  notMatchedRateAn.write();

  simVertexRhoVsPtGen->Write();
}
} /* namespace L1MuAn */
