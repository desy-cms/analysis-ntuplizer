/**\class EventInfo EventInfo.cc Analysis/Ntuplizer/src/EventInfo.cc

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
#include <iostream>


// user include files
#include "FWCore/Framework/interface/Event.h"
// 
#include "FWCore/ParameterSet/interface/ParameterSet.h"
 
#include "Analysis/Ntuplizer/interface/EventInfo.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/Scalers/interface/LumiScalers.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "Analysis/Utils/interface/color_printf.h"

//
// class declaration
//

using namespace analysis;
using namespace analysis::ntuple;

//
// constructors and destructor
//
EventInfo::EventInfo() {
   // default constructor
}

EventInfo::EventInfo(edm::Service<TFileService> & fs) {
   std::string name = "eventInfo";
   tree_ = fs->make<TTree>(name.c_str(),name.c_str());
   
   // event output info
   tree_->Branch("event", &event_, "event/I");
   tree_->Branch("run"  , &run_  , "run/I");
   tree_->Branch("lumi_section" , &lumi_ , "lumi_section/I");
   tree_->Branch("bx"   , &bx_   , "bx/I");
   tree_->Branch("orbit", &orbit_, "orbit/I");
   
   do_pu_   = false;
   do_gen_event_info_  = false;
   do_lumi_ = false;
   do_rho_  = false;
   do_prefiring_weight_ = false;
}

EventInfo::EventInfo(TFileDirectory & dir) {
   std::string name = "eventInfo";
   tree_ = dir.make<TTree>(name.c_str(),name.c_str());
   
   // event output info
   tree_->Branch("event", &event_, "event/I");
   tree_->Branch("run"  , &run_  , "run/I");
   tree_->Branch("lumisection" , &lumi_ , "lumisection/I");
   tree_->Branch("bx"   , &bx_   , "bx/I");
   tree_->Branch("orbit", &orbit_, "orbit/I");

   do_pu_   = false;
   do_gen_event_info_  = false;
   do_lumi_ = false;
   do_rho_  = false;
   do_prefiring_weight_ = false;


   
}

EventInfo::~EventInfo() {
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void EventInfo::Fill(const edm::Event& event) {
   const edm::EventAuxiliary evt = event.eventAuxiliary();
   event_ = evt.event();
   run_   = evt.run();
   lumi_  = evt.luminosityBlock();
   orbit_ = evt.orbitNumber();
   bx_    = evt.bunchCrossing();
   if ( do_pu_ ) {
      ReadPileupInfo(event);
   } else {
      n_pu_ = -1;
      n_true_pu_ = -1;
   }
   if ( do_gen_event_info_ ) {
      ReadGenEventInfo(event);
   } else {
      gen_weight_  = -1.;
      gen_scale_   = -1.;
      pdf_id1_     = 0;
      pdf_id2_     = 0;
      pdf_x1_      = -1.;
      pdf_x2_      = -1.;        
   }
   if ( do_lumi_ ) {
      ReadLumiScalers(event);
   }
   if ( do_rho_ ) {
      ReadFixedGridRhoInfo(event);
   }  
   if ( do_prefiring_weight_ ) {
      ReadPrefiringWeight(event);
   }
   if ( do_met_filters_ ) {
      ReadMetFilters(event);
   }
   tree_ -> Fill();
}

// ------------ method called once each job just before starting event loop  ------------
void EventInfo::Init() {
   // init
}

// ------------ other methods ----------------
TTree * EventInfo::Tree() {
   return tree_;
}

void EventInfo::PileupInfo(const edm::InputTag& tag) {
   do_pu_ = true;
   pileup_info_ = tag;
   tree_->Branch("n_pileup"      , &n_pu_     , "n_pileup/I");
   tree_->Branch("n_true_pileup" , &n_true_pu_, "n_true_pileup/F");
}

void EventInfo::ReadPileupInfo(const edm::Event& event) {
   edm::Handle<std::vector<PileupSummaryInfo>> handler;
   event.getByLabel(pileup_info_, handler);
   std::vector<PileupSummaryInfo> pu_infos = *(handler.product());
   // Take the first entry - should be enough
   PileupSummaryInfo pu_info = pu_infos.at(0);
   n_true_pu_ = pu_info.getTrueNumInteractions();
   n_pu_      = pu_info.getPU_NumInteractions(); 
}

// GenEventInfoProduct
void EventInfo::GenEventInfo(const edm::InputTag& tag) {
   do_gen_event_info_ = true;
   gen_event_info_ = tag;   
   tree_->Branch("gen_weight" , &gen_weight_  , "gen_weight/D");
   tree_->Branch("gen_scale"  , &gen_scale_   , "gen_scale/D");
   tree_->Branch("pdf_id1"    , &pdf_id1_     , "pdf_id1/I");
   tree_->Branch("pdf_id2"    , &pdf_id2_     , "pdf_id2/I");
   tree_->Branch("pdf_x1"     , &pdf_x1_      , "pdf_x1/D");
   tree_->Branch("pdf_x2"     , &pdf_x2_      , "pdf_x2/D");
}

void EventInfo::ReadGenEventInfo(const edm::Event& event) {
   edm::Handle<GenEventInfoProduct> hepmc;
   event.getByLabel(gen_event_info_, hepmc);
   if ( hepmc.isValid() ) {
      gen_weight_ = hepmc -> weight();
      gen_scale_  = hepmc -> qScale();
      pdf_id1_    = hepmc -> pdf() -> id.first;
      pdf_id2_    = hepmc -> pdf() -> id.second;
      pdf_x1_     = hepmc -> pdf() -> x.first;
      pdf_x2_     = hepmc -> pdf() -> x.second;
   }   
}

void EventInfo::LumiScalersInfo(const edm::InputTag& tag) {
   do_lumi_  = true;
   lumi_scalers_ = tag;
   // lumiScalers
   tree_->Branch("instant_lumi", &inst_lumi_,"instant_lumi/F");
   tree_->Branch("lumi_pileup", &lumi_pu_,"lumi_pileup/F");
}

void EventInfo::ReadLumiScalers(const edm::Event& event) {
   edm::Handle<LumiScalersCollection> lumis;
   event.getByLabel(lumi_scalers_, lumis);
   inst_lumi_ = lumis -> begin() -> instantLumi();
   lumi_pu_   = lumis -> begin() -> pileup();
}

void EventInfo::FixedGridRhoInfo(const edm::InputTag& tag) {
   do_rho_ = true;
   rho_collection_ = tag;
   tree_->Branch("rho",&rho_,"rho/D");
}

void EventInfo::ReadFixedGridRhoInfo(const edm::Event& event) {
   edm::Handle<double> rhoHandler;
   event.getByLabel(rho_collection_, rhoHandler);
   rho_ = *(rhoHandler.product());
}

void EventInfo::PrefiringWeightInfo(const edm::InputTag & tag, const edm::InputTag & tag_up ,const edm::InputTag & tag_down) {
   do_prefiring_weight_ = true;
   prefiring_weight_collection_ = tag;
   prefiring_weight_up_collection_ = tag_up;
   prefiring_weight_down_collection_ = tag_down;  
   tree_->Branch("non_prefiring_prob"      , &prefiring_weight_      , "non_prefiring_prob/D");
   tree_->Branch("non_prefiring_prob_up"   , &prefiring_weight_up_   , "non_prefiring_prob_up/D");
   tree_->Branch("non_prefiring_prob_down" , &prefiring_weight_down_ , "non_prefiring_prob_down/D"); 
}

void EventInfo::ReadPrefiringWeight(const edm::Event& event) {
   edm::Handle<double> prefwHandler;
   edm::Handle<double> prefwUpHandler;
   edm::Handle<double> prefwDownHandler;
   event.getByLabel(prefiring_weight_collection_, prefwHandler);
   event.getByLabel(prefiring_weight_up_collection_, prefwUpHandler);
   event.getByLabel(prefiring_weight_down_collection_, prefwDownHandler);
   prefiring_weight_      = *(prefwHandler.product());
   prefiring_weight_up_   = *(prefwUpHandler.product());
   prefiring_weight_down_ = *(prefwDownHandler.product());
}

void EventInfo::MetFilters(const edm::InputTag & tag) {
   do_met_filters_ = true;
   met_filters_results_ = tag;
   tree_->Branch("flag_met_goodVertices"                       , &flag_goodVertices_                        , "flag_met_goodVertices/O");
   tree_->Branch("flag_met_globalSuperTightHalo2016Filter"     , &flag_globalSuperTightHalo2016Filter_      , "flag_met_globalSuperTightHalo2016Filter/O");
   tree_->Branch("flag_met_EcalDeadCellTriggerPrimitiveFilter" , &flag_EcalDeadCellTriggerPrimitiveFilter_  , "flag_met_EcalDeadCellTriggerPrimitiveFilter/O");
   tree_->Branch("flag_met_BadPFMuonFilter"                    , &flag_BadPFMuonFilter_                     , "flag_met_BadPFMuonFilter/O");
   tree_->Branch("flag_met_BadPFMuonDzFilter"                  , &flag_BadPFMuonDzFilter_                   , "flag_met_BadPFMuonDzFilter/O");
   tree_->Branch("flag_met_hfNoisyHitsFilter"                  , &flag_hfNoisyHitsFilter_                   , "flag_met_hfNoisyHitsFilter/O");
   tree_->Branch("flag_met_eeBadScFilter"                      , &flag_eeBadScFilter_                       , "flag_met_eeBadScFilter/O");
   tree_->Branch("flag_met_ecalBadCalibFilter"                 , &flag_ecalBadCalibFilter_                  , "flag_met_ecalBadCalibFilter/O");
}

void EventInfo::ReadMetFilters(const edm::Event& event) {
   flag_goodVertices_                        = false;
   flag_globalSuperTightHalo2016Filter_      = false;
   flag_EcalDeadCellTriggerPrimitiveFilter_  = false;
   flag_BadPFMuonFilter_                     = false;
   flag_BadPFMuonDzFilter_                   = false;
   flag_hfNoisyHitsFilter_                   = false;
   flag_eeBadScFilter_                       = false;
   flag_ecalBadCalibFilter_                  = false;
   edm::Handle<edm::TriggerResults> met_filter_handler;
   event.getByLabel(met_filters_results_, met_filter_handler);
   if ( met_filter_handler.isValid() ) {
      const edm::TriggerNames & met_filter_name = event.triggerNames(*met_filter_handler);
      flag_goodVertices_                        = met_filter_handler.product()->accept(met_filter_name.triggerIndex("Flag_goodVertices"));
      flag_globalSuperTightHalo2016Filter_      = met_filter_handler.product()->accept(met_filter_name.triggerIndex("Flag_globalSuperTightHalo2016Filter"));
      flag_EcalDeadCellTriggerPrimitiveFilter_  = met_filter_handler.product()->accept(met_filter_name.triggerIndex("Flag_EcalDeadCellTriggerPrimitiveFilter"));
      flag_BadPFMuonFilter_                     = met_filter_handler.product()->accept(met_filter_name.triggerIndex("Flag_BadPFMuonFilter"));
      flag_BadPFMuonDzFilter_                   = met_filter_handler.product()->accept(met_filter_name.triggerIndex("Flag_BadPFMuonDzFilter"));
      flag_hfNoisyHitsFilter_                   = met_filter_handler.product()->accept(met_filter_name.triggerIndex("Flag_hfNoisyHitsFilter"));
      flag_eeBadScFilter_                       = met_filter_handler.product()->accept(met_filter_name.triggerIndex("Flag_eeBadScFilter"));
      flag_ecalBadCalibFilter_                  = met_filter_handler.product()->accept(met_filter_name.triggerIndex("Flag_ecalBadCalibFilter")); 
   }
}
