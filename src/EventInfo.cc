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
   std::string name = "EventInfo";
   tree_ = fs->make<TTree>(name.c_str(),name.c_str());
   
   // event output info
   tree_->Branch("event", &event_, "event/I");
   tree_->Branch("run"  , &run_  , "run/I");
   tree_->Branch("lumisection" , &lumi_ , "lumisection/I");
   tree_->Branch("bx"   , &bx_   , "bx/I");
   tree_->Branch("orbit", &orbit_, "orbit/I");
   
   do_pu_   = false;
   do_gen_  = false;
   do_lumi_ = false;
   do_rho_  = false;
   do_prefw_ = false;
   
   
}

EventInfo::EventInfo(TFileDirectory & dir) {
   std::string name = "EventInfo";
   tree_ = dir.make<TTree>(name.c_str(),name.c_str());
   
   // event output info
   tree_->Branch("event", &event_, "event/I");
   tree_->Branch("run"  , &run_  , "run/I");
   tree_->Branch("lumisection" , &lumi_ , "lumisection/I");
   tree_->Branch("bx"   , &bx_   , "bx/I");
   tree_->Branch("orbit", &orbit_, "orbit/I");

   do_pu_   = false;
   do_gen_  = false;
   do_lumi_ = false;
   do_rho_  = false;
   do_prefw_ = false;


   
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
   using namespace edm;
   
   const edm::EventAuxiliary evt = event.eventAuxiliary();

   event_ = evt.event();
   run_   = evt.run();
   lumi_  = evt.luminosityBlock();
   orbit_ = evt.orbitNumber();
   bx_    = evt.bunchCrossing();

   if ( do_pu_ ) {
      ReadPileupInfo(event);
   }
   else {
      n_pu_ = -1;
      n_true_pu_ = -1;
   }

   if ( do_gen_ ) {
      ReadGenEventInfo(event);
   }
   else
   {
      genWeight_  = -1.;
      genScale_   = -1.;
      pdfid1_     = 0;
      pdfid2_     = 0;
      pdfx1_      = -1.;
      pdfx2_      = -1.;        
   }

   if ( do_lumi_ ) {
      ReadLumiScalers(event);
   }

   if ( do_rho_ ) {
      ReadFixedGridRhoInfo(event);
   }
      
   if ( do_prefw_ ) {
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
      
   tree_->Branch("nPileup"     , &n_pu_     , "nPileup/I");
   tree_->Branch("nTruePileup" , &n_true_pu_, "nTruePileup/F");
   
}

void EventInfo::ReadPileupInfo(const edm::Event& event) {
   using namespace edm;
   // 
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
   do_gen_ = true;
   
   genInfo_ = tag;
      
   tree_->Branch("genWeight" , &genWeight_  , "genWeight/D");
   tree_->Branch("genScale"  , &genScale_   , "genScale/D");
   tree_->Branch("pdfid1"    , &pdfid1_     , "pdfid1/I");
   tree_->Branch("pdfid2"    , &pdfid2_     , "pdfid2/I");
   tree_->Branch("pdfx1"     , &pdfx1_      , "pdfx1/D");
   tree_->Branch("pdfx2"     , &pdfx2_      , "pdfx2/D");
   
}

void EventInfo::ReadGenEventInfo(const edm::Event& event) {
   using namespace edm;
   
   // 
   edm::Handle<GenEventInfoProduct> hepmc;
   event.getByLabel(genInfo_, hepmc);
   
   if ( hepmc.isValid() )
   {
      genWeight_ = hepmc -> weight();
      genScale_  = hepmc -> qScale();
      pdfid1_    = hepmc -> pdf() -> id.first;
      pdfid2_    = hepmc -> pdf() -> id.second;
      pdfx1_     = hepmc -> pdf() -> x.first;
      pdfx2_     = hepmc -> pdf() -> x.second;
   }

   
}

void EventInfo::LumiScalersInfo(const edm::InputTag& tag) {
   do_lumi_  = true;
   
   lumiScalers_ = tag;
   
   // lumiScalers
   tree_->Branch("instantLumi", &instLumi_,"instantLumi/F");
   tree_->Branch("lumiPileup", &lumiPU_,"lumiPileup/F");
}

void EventInfo::ReadLumiScalers(const edm::Event& event) {
   edm::Handle<LumiScalersCollection> lumis;
   event.getByLabel(lumiScalers_, lumis);
   
   instLumi_ = lumis -> begin() -> instantLumi();
   lumiPU_   = lumis -> begin() -> pileup();
   
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
   do_prefw_ = true;
   
   prefweight_collection_ = tag;
   prefweight_up_collection_ = tag_up;
   prefweight_down_collection_ = tag_down;
      
   tree_->Branch("nonPrefiringProb"     , &prefw_      , "nonPrefiringProb/D");
   tree_->Branch("nonPrefiringProbUp"   , &prefw_up_   , "nonPrefiringProbUp/D");
   tree_->Branch("nonPrefiringProbDown" , &prefw_down_ , "nonPrefiringProbDown/D");
   
   
}

void EventInfo::ReadPrefiringWeight(const edm::Event& event) {
   edm::Handle<double> prefwHandler;
   edm::Handle<double> prefwUpHandler;
   edm::Handle<double> prefwDownHandler;

   event.getByLabel(prefweight_collection_, prefwHandler);
   event.getByLabel(prefweight_up_collection_, prefwUpHandler);
   event.getByLabel(prefweight_down_collection_, prefwDownHandler);

   prefw_ = *(prefwHandler.product());
   prefw_up_ = *(prefwUpHandler.product());
   prefw_down_ = *(prefwDownHandler.product());

}

void EventInfo::MetFilters(const edm::InputTag & tag) {
   do_met_filters_ = true;
   met_filters_results_ = tag;

   tree_->Branch("flag_goodVertices"                       , &flag_goodVertices_                        , "flag_goodVertices/O");
   tree_->Branch("flag_globalSuperTightHalo2016Filter"     , &flag_globalSuperTightHalo2016Filter_      , "flag_globalSuperTightHalo2016Filter/O");
   tree_->Branch("flag_EcalDeadCellTriggerPrimitiveFilter" , &flag_EcalDeadCellTriggerPrimitiveFilter_  , "flag_EcalDeadCellTriggerPrimitiveFilter/O");
   tree_->Branch("flag_BadPFMuonFilter"                    , &flag_BadPFMuonFilter_                     , "flag_BadPFMuonFilter/O");
   tree_->Branch("flag_BadPFMuonDzFilter"                  , &flag_BadPFMuonDzFilter_                   , "flag_BadPFMuonDzFilter/O");
   tree_->Branch("flag_hfNoisyHitsFilter"                  , &flag_hfNoisyHitsFilter_                   , "flag_hfNoisyHitsFilter/O");
   tree_->Branch("flag_eeBadScFilter"                      , &flag_eeBadScFilter_                       , "flag_eeBadScFilter/O");
   tree_->Branch("flag_ecalBadCalibFilter"                 , &flag_ecalBadCalibFilter_                  , "flag_ecalBadCalibFilter/O");
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
