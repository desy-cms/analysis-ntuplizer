/**\class Candidates Candidates.cc Analysis/Ntuplizer/src/Candidates.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Roberval Walsh Bastos Rangel
//         Created:  Mon, 20 Oct 2014 14:24:08 GMT
//
//

// system include files
// 
#include <regex>
#include <boost/core/demangle.hpp>

// user include files
#include "Analysis/Ntuplizer/interface/Candidates.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "CommonTools/Utils/interface/PtComparator.h"

#include "TTree.h"

//
// class declaration
//

using namespace analysis;
using namespace analysis::ntuple;

// member functions specialization - needed to be declared in the same namespace as the class
namespace analysis {
   namespace ntuple {
      template <> void Candidates<pat::Jet>::JECRecord(const std::string & jr);
      template <> int  Candidates<pat::Jet>::AdditionalProperties(int n, size_t i);
      template <> int  Candidates<pat::Muon>::AdditionalProperties(int n, size_t i);
      template <> int  Candidates<pat::MET>::AdditionalProperties(int n, size_t i);
      template <> int  Candidates<reco::GenJet>::AdditionalProperties(int n, size_t i);
      template <> int  Candidates<reco::GenParticle>::AdditionalProperties(int n, size_t i);
      template <> int  Candidates<l1t::Jet>::AdditionalProperties(int n, size_t i);
      template <> int  Candidates<l1t::Muon>::AdditionalProperties(int n, size_t i);
      template <> int Candidates<pat::TriggerObject>::AdditionalProperties(int n, size_t i);
      template <> void Candidates<pat::TriggerObject>::ReadFromEvent(const edm::Event& event);
      template <> void Candidates<pat::TriggerObject>::TriggerObjectType(const std::string& trigobj_type);
   }
}   
//
// constructors and destructor
//
template <typename T>
Candidates<T>::Candidates() {
   // default constructor
}

template <typename T>
Candidates<T>::Candidates(const edm::InputTag& tag, TTree* tree, const bool & mc, float minPt, float maxEta ) :
      minPt_(minPt), maxEta_(maxEta) {
   
   input_collection_ = tag;
   tree_ = tree;
   
   is_mc_              = mc;
   is_patjet_          = std::is_same<T,pat::Jet>::value;
   is_patmuon_         = std::is_same<T,pat::Muon>::value;
   is_patmet_          = std::is_same<T,pat::MET>::value;
   is_genjet_          = std::is_same<T,reco::GenJet>::value;
   is_genparticle_     = std::is_same<T,reco::GenParticle>::value;
   is_trigobject_      = std::is_same<T,pat::TriggerObject>::value;
   is_l1tjet_          = std::is_same<T,l1t::Jet>::value;
   is_l1tmuon_         = std::is_same<T,l1t::Muon>::value;
   
   do_generator_  = ( is_mc_ && is_genparticle_ );
   
   higgs_pdg_ = 36;
   
   std::string title = boost::core::demangle(typeid(T).name()) + " | " + tree_->GetTitle();
   
   tree_->SetTitle(title.c_str());
   
   // definitions
   // jetid -> TODO: move to ntuplizer like btag_vars
   id_vars_.clear();
   id_vars_.push_back({"neutralHadronEnergyFraction", "id_nHadFrac" });
   id_vars_.push_back({"neutralEmEnergyFraction",     "id_nEmFrac"  });
   id_vars_.push_back({"neutralMultiplicity",         "id_nMult"    });
   id_vars_.push_back({"chargedHadronEnergyFraction", "id_cHadFrac" });
   id_vars_.push_back({"chargedEmEnergyFraction",     "id_cEmFrac"  });
   id_vars_.push_back({"chargedMultiplicity",         "id_cMult"    });
   id_vars_.push_back({"muonEnergyFraction",          "id_muonFrac" });
   id_vars_.push_back({"numberOfDaughters",           "id_numConst" });

   // init
   btag_vars_.clear();
   
   // JEC info default
   jecRecord_ = "";
   jecFile_   = "";
   
   // trigger object split
   trigobj_type_ = "";

   // pileup id
   pileup_id_instance_ = "";
   
}

template <typename T>
Candidates<T>::~Candidates() {
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}
//
// member functions
//

template <typename T>
void Candidates<T>::ReadFromEvent(const edm::Event& event) {
   candidates_.clear();
   edm::Handle<typename CollectionTraits<T>::Collection> handler;
   event.getByLabel(input_collection_, handler);
   for (auto const& candidate : *handler) {
      candidates_.push_back(candidate);
   }
   if constexpr (std::is_same_v<typename CollectionTraits<T>::Collection,std::vector<T>>) {
      // already sorted (or no sorting needed)
    } else {
      std::sort(candidates_.begin(),
         candidates_.end(),
         NumericSafeGreaterByPt<T>{});
   }
}

// Specialization for trigger objects (pat)
template <>
void Candidates<pat::TriggerObject>::ReadFromEvent(const edm::Event& event) {
   edm::Handle<edm::TriggerResults> trhandler;
   event.getByLabel(triggerresults_collection_, trhandler);
   const edm::TriggerResults & trgres = *(trhandler.product());
   candidates_.clear();
   // The stand alone collection
   edm::Handle<pat::TriggerObjectStandAloneCollection> handler;
   event.getByLabel(input_collection_, handler);
   const std::string treename = tree_ -> GetName(); // using the label to name the tree
   const std::string delimiter = "_";
   std::string label = treename.substr(0, treename.find(delimiter));
   for ( auto ito : *handler ) {
      ito.unpackFilterLabels(event,trgres);
      if ( ito.filter(label) ) {
         if ( trigobj_type_ != "" ) {
            int type = ito.triggerObject().triggerObjectTypes().at(0);
            if ( trigobj_type_ == "l1muon" ) {
               if ( type == trigger::TriggerL1Mu )               candidates_.push_back(ito.triggerObject());
            } else if ( trigobj_type_ == "l1jet" ) {
               if ( type == trigger::TriggerL1Jet  )             candidates_.push_back(ito.triggerObject());
            } else if ( trigobj_type_ == "hltmuon" ) {
               if ( type == trigger::TriggerMuon )               candidates_.push_back(ito.triggerObject());
            } else if ( trigobj_type_ == "hltjet" ) {
               if ( type == trigger::TriggerJet )                candidates_.push_back(ito.triggerObject());
            } else if ( trigobj_type_ == "hltbjet" ) {
               if ( type == trigger::TriggerBJet )               candidates_.push_back(ito.triggerObject());
            }
         } else {
            candidates_.push_back(ito.triggerObject());
         }
      }
   }
   // Sort the objects by pt
   NumericSafeGreaterByPt<pat::TriggerObject> triggerObjectGreaterByPt;
   std::sort (candidates_.begin(), candidates_.end(),triggerObjectGreaterByPt);
}
template <>
void Candidates<pat::TriggerObject>::TriggerObjectType(const std::string& trigobj_type) {
   trigobj_type_ = trigobj_type;
}

template <typename T>
void Candidates<T>::Properties() {
   int n = 0;
   for ( size_t i = 0 ; i < candidates_.size(); ++i ) {
      if ( n >= maxCandidates ) break;
      
      if ( minPt_  >= 0. && candidates_[i].pt()  < minPt_  ) continue;
      if ( maxEta_ >= 0. && fabs(candidates_[i].eta()) > maxEta_ ) continue;

      int additional_properties = AdditionalProperties(n, i);
      if ( additional_properties != 0 ) continue;
      pt_[n]  = candidates_[i].pt();
      eta_[n] = candidates_[i].eta();
      phi_[n] = candidates_[i].phi();
      px_[n]  = candidates_[i].px();
      py_[n]  = candidates_[i].py();
      pz_[n]  = candidates_[i].pz();
      q_[n]   = candidates_[i].charge();
      e_[n]   = candidates_[i].energy();
      et_[n]  = candidates_[i].et();
      n++;
   }
   n_ = n;
}

template <>
int Candidates<pat::Jet>::AdditionalProperties(int n, size_t i) {
   pat::Jet * cand_jet = dynamic_cast<pat::Jet*> (&candidates_[i]);
            
   for ( size_t it = 0 ; it < btag_vars_.size() ; ++it )  {
      btag_[it][n] = cand_jet->bDiscriminator(btag_vars_[it].title);
   }
   if ( cand_jet -> isPFJet() || cand_jet -> isJPTJet() ) {
      jetid_[0][n] = cand_jet->neutralHadronEnergyFraction();
      jetid_[1][n] = cand_jet->neutralEmEnergyFraction();
      jetid_[2][n] = (float)cand_jet->neutralMultiplicity();
      jetid_[3][n] = cand_jet->chargedHadronEnergyFraction();
      jetid_[4][n] = cand_jet->chargedEmEnergyFraction();
      jetid_[5][n] = (float)cand_jet->chargedMultiplicity();
      jetid_[6][n] = cand_jet->muonEnergyFraction();
      jetid_[7][n] = (float)cand_jet->numberOfDaughters();
   } else {  // set some dummy values
      for ( size_t ii = 0; ii < id_vars_.size(); ++ii )  jetid_[ii][n] = -1.;
   }
   flavour_        [n] = 0;
   hadronFlavour_  [n] = 0;
   partonFlavour_  [n] = 0;
   physicsFlavour_ [n] = 0;
   if ( is_mc_ ) {
      flavour_       [n]  = cand_jet->hadronFlavour();
      hadronFlavour_ [n]  = cand_jet->hadronFlavour();
      partonFlavour_ [n]  = cand_jet->partonFlavour();
      if (cand_jet->genParton())
      physicsFlavour_[n] = cand_jet->genParton()->pdgId();
   }

   // JEC Uncertainties
   if ( jecRecord_ != "" ) {
      jecUnc_->setJetEta(eta_[n]);
      jecUnc_->setJetPt(pt_[n]);
      jecUncert_[n] = jecUnc_->getUncertainty(true);
   } else {
      jecUncert_[n] = -1.;
   }
   //JER
   if( jerRecord_ != "" ) {
      // SetUp Jet parameters
      JME::JetParameters jerParamRes;
      jerParamRes.setJetPt(pt_[n]);
      jerParamRes.setJetEta(eta_[n]);
      jerParamRes.setRho(rho_);
      
      // Return JER
      jerResolution_[n]    = res_.getResolution(jerParamRes);

      JME::JetParameters jerParamSF;
      jerParamSF.set(JME::Binning::JetPt, pt_[n]);
      jerParamSF.set(JME::Binning::JetEta, eta_[n]);
      jerParamSF.set(JME::Binning::Rho, rho_);

      jerSF_[n]       = res_sf_.getScaleFactor(jerParamSF);
      jerSFUp_[n]     = res_sf_.getScaleFactor(jerParamSF,Variation::UP);
      jerSFDown_[n]   = res_sf_.getScaleFactor(jerParamSF,Variation::DOWN);
      
   } else {
      jerResolution_[n] = -1;
      jerSF_[n]         = -1;
      jerSFUp_[n]       = -1;
      jerSFDown_[n]     = -1;
   }

   // jet pileup id
   pileup_id_fulldiscr_[n] = -10.;
   std::string pileup_id_disc_key = pileup_id_instance_+":fullDiscriminant";
   if ( cand_jet -> hasUserFloat(pileup_id_disc_key) ) {
      pileup_id_fulldiscr_[n] = cand_jet -> userFloat(pileup_id_disc_key);
   }

   return 0;
}

template <>
int Candidates<pat::Muon>::AdditionalProperties(int n, size_t i) {
   pat::Muon * cand_muon = dynamic_cast<pat::Muon*> (&candidates_[i]);
   const reco::Vertex::Point muon_vertex_point  = cand_muon->reco::LeafCandidate::vertex();
   const reco::Vertex::Error muon_vertex_error ; 

   const reco::Vertex vtx ( muon_vertex_point, muon_vertex_error ) ;

   isPFMuon_       [n] = cand_muon->isPFMuon()     ;
   isGlobalMuon_   [n] = cand_muon->isGlobalMuon() ;
   isTrackerMuon_  [n] = cand_muon->isTrackerMuon();

   isLooseMuon_    [n] = cand_muon->isLooseMuon() ; 
   isMediumMuon_   [n] = cand_muon->isMediumMuon(); 
   isTightMuon_    [n] = cand_muon->isTightMuon( vtx ) ;

   // default values
   segmentCompatibility_      [n] = -1.;
   validFraction_             [n] = -1.;
   matchedStations_           [n] = 9999.;
   validPixelHits_            [n] = 9999.;
   validMuonHits_             [n] = 9999.;
   trkLayersWithMeasurement_  [n] = 9999.;
   trkKink_                   [n] = 9999.;
   ipxy_                      [n] = 9999.;
   ipz_                       [n] = 9999.;
   normChi2_                  [n] = 9999.;
   chi2LocalPos_              [n] = 9999.;


   if ( isPFMuon_[n] && ( isGlobalMuon_[n] || isTrackerMuon_[n] ) ) {
      // muon chamber stations      
      segmentCompatibility_   [n] = cand_muon->segmentCompatibility()       ; // medium muon
      matchedStations_        [n] = cand_muon->numberOfMatchedStations()    ; // at least 2 in tight 

      //inner tracker
      validFraction_             [n] = cand_muon->innerTrack()->validFraction()                             ;  
      validPixelHits_            [n] = cand_muon->innerTrack()->hitPattern().numberOfValidPixelHits()       ; 
      trkLayersWithMeasurement_  [n] = cand_muon->innerTrack()->hitPattern().trackerLayersWithMeasurement() ;

      //transverse and longitudinal ip - tracker only 
      ipxy_[n] = fabs(cand_muon->muonBestTrack()->dxy(vtx.position()))     ; 
      ipz_ [n] = fabs(cand_muon->muonBestTrack()->dz (vtx.position()))     ; 

      //global tracker - only for GlobalMuons
      if ( isGlobalMuon_[n] ) {
         normChi2_    [n] = cand_muon->normChi2();                         
         trkKink_     [n] = cand_muon->combinedQuality().trkKink;          
         chi2LocalPos_[n] = cand_muon->combinedQuality().chi2LocalPosition;
         validMuonHits_[n] = cand_muon->globalTrack()->hitPattern().numberOfValidMuonHits();
      }
   }
   return 0;
}

template <>
int Candidates<pat::MET>::AdditionalProperties(int n, size_t i) {
   pat::MET * cand_met = dynamic_cast<pat::MET*> (&candidates_[i]);
   sigxx_[n] = cand_met->getSignificanceMatrix()(0,0);
   sigxy_[n] = cand_met->getSignificanceMatrix()(0,1);
   sigyx_[n] = cand_met->getSignificanceMatrix()(1,0);
   sigyy_[n] = cand_met->getSignificanceMatrix()(1,1);
   if ( is_mc_ )  {
      const reco::GenMET * genMET = cand_met->genMET();
      gen_px_[n] = genMET->px();;
      gen_py_[n] = genMET->py();;
      gen_pz_[n] = genMET->pz();;
   }
   return 0;
}

template <>
int Candidates<reco::GenJet>::AdditionalProperties(int n, size_t i) {
   return 0;
}

template <>
int Candidates<reco::GenParticle>::AdditionalProperties(int n, size_t i) {
   reco::GenParticle * cand_genpart = dynamic_cast<reco::GenParticle*> (&candidates_[i]);
   int pdg    = cand_genpart -> pdgId();
   if ( abs(pdg) > 38 ) return -1;
   int status = cand_genpart -> status();  // any status selection?
   indx_[n] = i;
   pdg_[n]   = pdg;
   status_[n]= status;
   mass_[n] = cand_genpart->mass();
   lastcopy_[n] = cand_genpart -> isLastCopy();
   // mothers
   mo1_[n] = -1;
   mo2_[n] = -1;
   if ( cand_genpart->numberOfMothers() > 0 ) {
      mo1_[n] = cand_genpart->motherRef(0).key();
      mo2_[n] = cand_genpart->motherRef(cand_genpart->numberOfMothers()-1).key();
   }
   // daughters
   da1_[n] = -1;
   da2_[n] = -1;
   if ( cand_genpart->numberOfDaughters() > 0 ) {
      da1_[n] = cand_genpart->daughterRef(0).key();
      da2_[n] = cand_genpart->daughterRef(cand_genpart->numberOfDaughters()-1).key();
   }
   const reco::Candidate * mother = cand_genpart->mother(0);  // Higgs daughters (TODO: improve)
   higgs_dau_[n] = false;
   if ( mother != NULL ) {  // initial protons are orphans
      if ( mother->pdgId() == 36 || mother->pdgId() == 25 )
         higgs_dau_[n] = true;
   }
   return 0;
}

template <>
int Candidates<l1t::Jet>::AdditionalProperties(int n, size_t i) {
   return 0;
}

template <>
int Candidates<l1t::Muon>::AdditionalProperties(int n, size_t i) {
   l1t::Muon * cand_l1tmuon = dynamic_cast<l1t::Muon*> (&candidates_[i]);
   hwQual_[n]   = cand_l1tmuon->hwQual();
   etaAtVtx_[n] = cand_l1tmuon->etaAtVtx();
   phiAtVtx_[n] = cand_l1tmuon->phiAtVtx();   

   return 0;
}

template <>
int Candidates<pat::TriggerObject>::AdditionalProperties(int n, size_t i) {
   pat::TriggerObject * cand_trigger_object = dynamic_cast<pat::TriggerObject*> (&candidates_[i]);
   type_[n] = 0;
   if ( cand_trigger_object->triggerObjectTypes().size() > 0 )
      type_[n] = cand_trigger_object->triggerObjectTypes().at(0);

   return 0;
}

template <typename T>
void Candidates<T>::JECRecord(const std::string& jr) {
   jecRecord_ = "";
}

template <>
void Candidates<pat::Jet>::JECRecord(const std::string& jr) {
   jecRecord_ = jr;
}

template <typename T>
void Candidates<T>::MinPt(const float& minPt) {
   minPt_ = minPt;
}

template <typename T>
void Candidates<T>::MaxEta(const float& maxEta) {
   maxEta_ = maxEta;
}

template <typename T>
void Candidates<T>::Fill() {
   tree_->Fill();
}

template <typename T>
void Candidates<T>::Fill(const edm::Event& event) {
   ReadFromEvent(event);
   Properties();
   Fill();
}

template <typename T>
void Candidates<T>::Fill(const edm::Event& event, const edm::EventSetup& setup) {
   if ( jecRecord_ != "" )  {
      if ( jecFile_ != "" )  {
         jecUnc_ = std::unique_ptr<JetCorrectionUncertainty>(new JetCorrectionUncertainty(jecFile_));
      } else { // conddb - see example: https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatUtils/plugins/ShiftedPFCandidateProducerForNoPileUpPFMEt.cc
         const JetCorrectorParametersCollection& jetCorrParameterSet = setup.getData(jec_tokens_.jecToken);
         const JetCorrectorParameters& jetCorrParameters = (jetCorrParameterSet)["Uncertainty"];
         jecUnc_ = std::make_unique<JetCorrectionUncertainty>(jetCorrParameters);   
      }
   }
   if (jerRecord_ != "" ) {
      if(jerFile_ != "" && jersfFile_ != "") {
         res_    = JME::JetResolution(jerFile_);
         res_sf_ = JME::JetResolutionScaleFactor(jersfFile_);
      } else {
         std::string label_pt = jerRecord_ + "_pt";
         res_    = JME::JetResolution::get(setup, res_tokens_.resolutionsToken);
         std::string label_sf = jerRecord_;
         res_sf_    = JME::JetResolutionScaleFactor::get(setup, res_tokens_.scaleFactorsToken);
      }
      edm::Handle<double> rhoHandler;
      event.getByLabel(rho_collection_, rhoHandler);
      rho_ = *(rhoHandler.product());     
   }
   Fill(event);
}

// ------------ method called once each job just before starting event loop  ------------

template <typename T>
void Candidates<T>::Branches() {
   // kinematics basic output info
   tree_->Branch("n",   &n_,  "n/I");
   tree_->Branch("pt",  pt_,  "pt[n]/F");
   tree_->Branch("eta", eta_, "eta[n]/F");
   tree_->Branch("phi", phi_, "phi[n]/F");
   tree_->Branch("px",  px_,  "px[n]/F");
   tree_->Branch("py",  py_,  "py[n]/F");
   tree_->Branch("pz",  pz_,  "pz[n]/F");
   tree_->Branch("q",   q_,   "q[n]/I");
   
   if ( is_genparticle_ ) {
      tree_->Branch("index",indx_,   "index[n]/I");
      tree_->Branch("pdg",   pdg_,   "pdg[n]/I");
      tree_->Branch("status",status_,"status[n]/I");
      tree_->Branch("last_copy",lastcopy_,"last_copy[n]/O");
      tree_->Branch("higgs_dau",higgs_dau_,"higgs_dau[n]/O");
      tree_->Branch("mother1",mo1_,"mother1[n]/I");
      tree_->Branch("mother2",mo2_,"mother2[n]/I");
      tree_->Branch("daughter1",da1_,"daughter1[n]/I");
      tree_->Branch("daughter2",da2_,"daughter2[n]/I");
      tree_->Branch("mass",mass_,"mass[n]/F");
   }

   if ( is_patmuon_ ) {
      tree_->Branch("isPFMuon",     isPFMuon_,     "isPFMuon[n]/O");
      tree_->Branch("isGlobalMuon", isGlobalMuon_, "isGlobalMuon[n]/O");
      tree_->Branch("isTrackerMuon",isTrackerMuon_,"isTrackerMuon[n]/O");
      tree_->Branch("isLooseMuon",  isLooseMuon_,  "isLooseMuon[n]/O");
      tree_->Branch("isMediumMuon", isMediumMuon_, "isMediumMuon[n]/O");
      tree_->Branch("isTightMuon",  isTightMuon_,  "isTightMuon[n]/O"); 
      
      tree_->Branch("validFraction",          validFraction_,          "validFraction[n]/F");
      tree_->Branch("segmentCompatibility",   segmentCompatibility_,   "segmentCompatibility[n]/F");

      tree_->Branch("matchedStations",       matchedStations_,        "matchedStations[n]/F");
      tree_->Branch("validPixelHits",        validPixelHits_,         "validPixelHits[n]/F" );
      tree_->Branch("validMuonHits",         validMuonHits_,           "validMuonHits[n]/F"  );
      tree_->Branch("trkLayersWithMeasurement",      trkLayersWithMeasurement_,        "trkLayersWithMeasurement[n]/F");
      tree_->Branch("ipxy",       ipxy_,        "ipxy[n]/F" );
      tree_->Branch("ipz",        ipz_,         "ipz[n]/F"  );


      tree_->Branch("normChi2",     normChi2_,     "normChi2[n]/F");
      tree_->Branch("trkKink",      trkKink_,      "trkKink[n]/F");
      tree_->Branch("chi2LocalPos", chi2LocalPos_, "chi2LocalPos[n]/F");
   }

   if ( is_patjet_ ) {
      btag_.resize(btag_vars_.size());
      for (auto& btag : btag_)
         btag.resize(maxCandidates);
      for ( size_t it = 0 ; it < btag_vars_.size() ; ++it )  {
         std::string title = btag_vars_[it].title;
         if (title.find(":") != std::string::npos) {
            title = std::regex_replace(title, std::regex("\\:"), "_");
         }
         tree_->Branch(btag_vars_[it].alias.c_str(), btag_[it].data(), (title+"[n]/F").c_str());
      }
      tree_->Branch("flavour",        flavour_,         "flavour[n]/I");
      tree_->Branch("hadronFlavour",  hadronFlavour_,   "hadronFlavour[n]/I" );
      tree_->Branch("partonFlavour",  partonFlavour_,   "partonFlavour[n]/I" );
      tree_->Branch("physicsFlavour", physicsFlavour_,  "physicsFlavour[n]/I");
      
      tree_->Branch("jecUncert", jecUncert_, "jecUncert[n]/F");
      tree_->Branch("jerResolution",jerResolution_,"jerResolution[n]/F");
      tree_->Branch("jerSF",jerSF_,"jerSF[n]/F");
      tree_->Branch("jerSFUp",jerSFUp_,"jerSFUp[n]/F");
      tree_->Branch("jerSFDown",jerSFDown_,"jerSFDown[n]/F");
      tree_->Branch("Rho",&rho_,"Rho/D");

      jetid_.resize(id_vars_.size());
      for (auto& jetid : jetid_)
         jetid.resize(maxCandidates);      
      for ( size_t it = 0 ; it < id_vars_.size() ; ++it )
         tree_->Branch(id_vars_[it].alias.c_str(), jetid_[it].data(), (id_vars_[it].title+"[n]/F").c_str());

      tree_->Branch("pileup_id_fulldiscr", pileup_id_fulldiscr_, "pileup_id_fulldiscr[n]/F");
   }

   if ( is_patmet_ ) {
      tree_->Branch("sigxx",  sigxx_,  "sigxx[n]/F");
      tree_->Branch("sigxy",  sigxy_,  "sigxy[n]/F");
      tree_->Branch("sigyx",  sigyx_,  "sigyx[n]/F");
      tree_->Branch("sigyy",  sigyy_,  "sigyy[n]/F");
      if ( is_mc_ ) {
         tree_->Branch("gen_px",  gen_px_,  "gen_px[n]/F");
         tree_->Branch("gen_py",  gen_py_,  "gen_py[n]/F");
         tree_->Branch("gen_pz",  gen_pz_,  "gen_pz[n]/F");
      }
   }
   
   if ( is_trigobject_ ) {
      // there may be more than one type for an object, one has to be careful depending on the trigger
      // for now only the first entry is used.
      // definitions in DataFormats/HLTReco/interface/TriggerTypeDefs.h
      tree_->Branch("type", type_, "type[n]/I");
   }
   
   if ( is_l1tmuon_ ) {
      tree_->Branch("hwQual"  ,  hwQual_  , "hwQual[n]/I");
      tree_->Branch("etaAtVtx",  etaAtVtx_, "etaAtVtx[n]/F");
      tree_->Branch("phiAtVtx",  phiAtVtx_, "phiAtVtx[n]/F");
   }
}

// Initialisation

template <typename T>
void Candidates<T>::Init() {
   Branches();
}

template <typename T>
void Candidates<T>::Init( const std::vector<analysis::utils::TitleAlias> & btagVars ) {
   btag_vars_ = btagVars;
   Init();
   
}

template <typename T>
void Candidates<T>::UseTriggerResults(edm::InputTag& tr) {
   triggerresults_collection_ = tr;
}

template <typename T>
void Candidates<T>::AddJecInfo( const std::string & jec ) {
   // Will use confDB
   jecRecord_ = jec;
}

template <typename T>
void Candidates<T>::AddJecInfo( const analysis::utils::JecESTokens & jec ) {
   // Will use confDB
   jec_tokens_ = jec;
}

template <typename T>
void Candidates<T>::AddJecInfo( const std::string & jec , const std::string & jec_file ) {
   // Will use txt file
   jecRecord_ = jec;
   jecFile_   = jec_file;
}

template <typename T>
void Candidates<T>::AddJerInfo( const std::string & jer, const edm::InputTag & rho ) {
   // Will use confDB
   jerRecord_ = jer;
   rho_collection_ = rho;
}

template <typename T>
void Candidates<T>::AddJerInfo( const analysis::utils::JerESTokens & jer, const edm::InputTag & rho ) {
   // Will use confDB
   jerRecord_ = jer.record;
   res_tokens_ = jer;
   rho_collection_ = rho;
}

template <typename T>
void Candidates<T>::AddJerInfo(const std::string & jer, const std::string & res_file, const std::string & sf_file, const edm::InputTag & rho) {
   // Will use txt file
   jerRecord_ = jer;
   jerFile_   = res_file;
   jersfFile_ = sf_file;
   rho_collection_ = rho;
}

template <typename T>
void Candidates<T>::PileupJetIdInstance(const std::string & instance) {
   pileup_id_instance_ = instance;
}

// Need to declare all possible template classes here: candidates types
template class Candidates<pat::Jet>;
template class Candidates<pat::Muon>;
template class Candidates<pat::MET>;
template class Candidates<reco::GenJet>;
template class Candidates<reco::GenParticle>;
template class Candidates<pat::TriggerObject>;
template class Candidates<l1t::Jet>;
template class Candidates<l1t::Muon>;
