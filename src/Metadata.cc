/**\class Metadata Metadata.cc Analysis/Ntuplizer/src/Metadata.cc

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
#include <iostream>
// 
// user include files
#include "Analysis/Ntuplizer/interface/Metadata.h"
#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"

//
// class declaration
//

//
// constructors and destructor
//
analysis::ntuple::Metadata::Metadata() {
   // default constructor
}

analysis::ntuple::Metadata::Metadata(edm::Service<TFileService> & fs, const bool & is_mc, const String & metadata_folder ) {
   is_mc_ = is_mc;
   is_gen_filter_ = false;
   is_evt_filter_ = false;
   is_mhat_evt_filter_ = false;
   
   vdefinitions_.clear();

   main_folder_ = fs->mkdir(metadata_folder);
   if ( is_mc_ ) {
      // Cross sections tree
      xsection_tree_ = main_folder_.make<TTree>("CrossSections","Cross Sections");
      // cross section branches
      xsection_tree_ -> Branch("run"            , &run_xsection_          , "run/i");
      xsection_tree_ -> Branch("myCrossSection" , &my_xsection_           , "myCrossSection/D");
      xsection_tree_ -> Branch("crossSection"   , &xsection_              , "crossSection_generator/D");
      xsection_tree_ -> Branch("internalXSec"   , &internal_xsection_     , "internalXSec_generator/D");
      xsection_tree_ -> Branch("externalXSecLO" , &external_xsection_lo_  , "externalXSecLO_generator/D");
      xsection_tree_ -> Branch("externalXSecNLO", &external_xsection_nlo_ , "externalXSecNLO_generator/D");
   }
   // Dataset
   dataset_tree_ = main_folder_.make<TTree>("Dataset","Dataset info");
   dataset_tree_ -> Branch("isMC"            , &is_mc_            , "isMC/O");

   mhat_folder_ = fs->mkdir("mHatFilter");
   
}

analysis::ntuple::Metadata::~Metadata() {
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

void analysis::ntuple::Metadata::Init() {
   // if ( is_mc_ )
   //    XSectionTreeBranches_();
   // DatasetTreeBranches_();
}

void analysis::ntuple::Metadata::XSectionTreeBranches_() {
   // Cross sections tree
   xsection_tree_ = main_folder_.make<TTree>("CrossSections","Cross Sections");
   // cross section branches
   xsection_tree_ -> Branch("run"            , &run_xsection_          , "run/i");
   xsection_tree_ -> Branch("myCrossSection" , &my_xsection_           , "myCrossSection/D");
   xsection_tree_ -> Branch("crossSection"   , &xsection_              , "crossSection_generator/D");
   xsection_tree_ -> Branch("internalXSec"   , &internal_xsection_     , "internalXSec_generator/D");
   xsection_tree_ -> Branch("externalXSecLO" , &external_xsection_lo_  , "externalXSecLO_generator/D");
   xsection_tree_ -> Branch("externalXSecNLO", &external_xsection_nlo_ , "externalXSecNLO_generator/D");
}   

void analysis::ntuple::Metadata::DatasetTreeBranches_() {
   // Dataset
   dataset_tree_ = main_folder_.make<TTree>("Dataset","Dataset info");
   dataset_tree_ -> Branch("isMC"            , &is_mc_            , "isMC/O");
}

// ------------ method called for each event  ------------
void analysis::ntuple::Metadata::Fill() {
   // for ( auto & definitions : vdefinitions_ )
   //    definitions -> Fill();
   
   if ( is_gen_filter_ )      gen_filter_       -> Fill();
   if ( is_evt_filter_ )      evt_filter_       -> Fill();
   if ( is_mhat_evt_filter_)  m_hat_evt_filter_ -> Fill();
   
   dataset_tree_ -> Fill();
   
}

// ------------ method called once each job just before starting event loop  ------------
void analysis::ntuple::Metadata::AddDefinitions(const Strings & names, const Strings & aliases) {
   vdefinitions_.push_back(std::make_unique<Definitions>(main_folder_));
   vdefinitions_.back() -> Add(names,aliases);
}

void analysis::ntuple::Metadata::AddDefinitions(const Strings & names, const Strings & aliases, const String & category) {
   vdefinitions_.push_back(std::make_unique<Definitions>(main_folder_, category));
   vdefinitions_.back() -> Add(names,aliases);
}

void analysis::ntuple::Metadata::AddDefinitions(const Vector<TitleAlias> & tas, const String & category) {
   Strings names;
   Strings aliases;
   for ( auto & ta : tas ) {
      names.push_back(ta.title);
      aliases.push_back(ta.alias);
   }
   vdefinitions_.push_back(std::make_unique<Definitions>(main_folder_, category));
   vdefinitions_.back() -> Add(names,aliases);
}

void analysis::ntuple::Metadata::SetGeneratorFilter(const InputTag & genFilterInfo ) {
   gen_filter_ = std::make_unique<GenFilter>(main_folder_, InputTags{genFilterInfo});
   is_gen_filter_ = true;
}

void analysis::ntuple::Metadata::SetEventFilter(const InputTags & filter_infos_ ) {
   evt_filter_ = std::make_unique<EvtFilter>(main_folder_, filter_infos_);
   is_evt_filter_ = true;
}

void analysis::ntuple::Metadata::SetMHatEventFilter(const InputTags & filter_infos_ ) {
   m_hat_evt_filter_ = std::make_unique<EvtFilter>(mhat_folder_, filter_infos_);
   is_mhat_evt_filter_ = true;
}

void analysis::ntuple::Metadata::IncrementEventFilters( LuminosityBlock const& lumi ) {
   if ( is_gen_filter_ )      gen_filter_       -> Increment(lumi);
   if ( is_evt_filter_ )      evt_filter_       -> Increment(lumi);
   if ( is_mhat_evt_filter_)  m_hat_evt_filter_ -> Increment(lumi);
}

GenFilter & analysis::ntuple::Metadata::GetGeneratorFilter() {
   // gen_filter_ should not go out of scope after returning the reference, should be safe(?)
   return *gen_filter_;
}
EvtFilter & analysis::ntuple::Metadata::GetEventFilter() {
   return *evt_filter_;
}

void analysis::ntuple::Metadata::SetCrossSections( const Run  & run, const InputTag & collection, const double & my_xsection ) {
   if ( is_mc_ ) {
      run_xsection_ = run.run();
      edm::Handle<GenRunInfoProduct> gen_run_info;
      run.getByLabel( collection, gen_run_info );
      my_xsection_          = my_xsection;
      xsection_            = gen_run_info -> crossSection();
      internal_xsection_    = gen_run_info -> internalXSec().value();
      external_xsection_lo_  = gen_run_info -> externalXSecLO().value();
      external_xsection_nlo_ = gen_run_info -> externalXSecNLO().value();
      xsection_tree_ -> Fill();
   }
}
            

