// -*- C++ -*-
//
// Package:    Analysis/Ntuplizer
// Class:      Ntuplizer
// 
/**\class Ntuplizer Ntuplizer.cc Analysis/Ntuplizer/plugins/Ntuplizer.cc

 Description: EDAnalyzer to produce ntuples for the CMS Higgs Analysis, meant for MSSM Hbb analysis, but it can be used in other analysis.

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Roberval Walsh
//         Created:  Mon, 20 Oct 2014 11:54:54 GMT
//
//

// system include files
#include <cstdlib>
#include <memory>
#include <type_traits>

// user include files
#include "DataFormats/Provenance/interface/Provenance.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/L1Trigger/interface/Jet.h"
#include "DataFormats/L1Trigger/interface/L1JetParticle.h"
#include "DataFormats/L1Trigger/interface/L1JetParticleFwd.h"
#include "DataFormats/L1Trigger/interface/Muon.h"
#include "DataFormats/L1Trigger/interface/L1MuonParticle.h"
#include "DataFormats/L1Trigger/interface/L1MuonParticleFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Scalers/interface/LumiScalers.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"

#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenFilterInfo.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"

#include "Analysis/Ntuplizer/interface/Candidates.h"
#include "Analysis/Ntuplizer/interface/TriggerAccepts.h"
#include "Analysis/Ntuplizer/interface/Vertices.h"
#include "Analysis/Ntuplizer/interface/EventInfo.h"
#include "Analysis/Ntuplizer/interface/Metadata.h"

#include "Analysis/Utils/interface/color_printf.h"
#include "Analysis/Utils/interface/string_utils.h"
#include "Analysis/Utils/interface/types.h"

#include <TH1.h>
#include <TFile.h>
#include <TTree.h>

using analysis::utils::string_split;

// Template aliases
template<typename T>
using Ptr = std::unique_ptr<T>;
template<typename Collection>
using Token = edm::EDGetTokenT<Collection>;
template<typename Collection>
using TokenMap = std::map<std::string, Token<Collection>>;
template<typename T>
using Collections = std::vector<Ptr<T>>;

// Aliases
using TitleIndex                   = analysis::utils::TitleIndex;
using TitleAlias                   = analysis::utils::TitleAlias;
using InputTag                     = edm::InputTag;
using InputTags                    = std::vector<InputTag>;
using String                       = std::string;
using Strings                      = std::vector<String>;

// Alias to the collections classes of candidates for the ntuple
using EventInfo                    = analysis::ntuple::EventInfo;
using Metadata                     = analysis::ntuple::Metadata;
using PatJetCandidates             = analysis::ntuple::Candidates<pat::Jet>;
using PatMuonCandidates            = analysis::ntuple::Candidates<pat::Muon>;
using PatMETCandidates             = analysis::ntuple::Candidates<pat::MET>;
using GenJetCandidates             = analysis::ntuple::Candidates<reco::GenJet>;
using GenParticleCandidates        = analysis::ntuple::Candidates<reco::GenParticle>;
using TriggerObjectCandidates      = analysis::ntuple::Candidates<pat::TriggerObject>;
using TriggerAccepts               = analysis::ntuple::TriggerAccepts;
using PrimaryVertices              = analysis::ntuple::Vertices;
using L1TJetCandidates             = analysis::ntuple::Candidates<l1t::Jet>;
using L1TMuonCandidates            = analysis::ntuple::Candidates<l1t::Muon>;

using EventCounts = analysis::ntuple::EventCounts<unsigned int>;
using WeightedEventCounts = analysis::ntuple::EventCounts<double>;

using JerESTokens                  = analysis::utils::JerESTokens;
using JecESTokens                  = analysis::utils::JecESTokens;


// Alias to the pointers to the above classes
using EventInfoPtr                  = Ptr<EventInfo>;
using MetadataPtr                   = Ptr<Metadata>;
using pPatJetCandidates             = Ptr<PatJetCandidates>;
using pPatMuonCandidates            = Ptr<PatMuonCandidates>;
using pPatMETCandidates             = Ptr<PatMETCandidates>;
using pGenJetCandidates             = Ptr<GenJetCandidates>;
using pGenParticleCandidates        = Ptr<GenParticleCandidates>;
using pTriggerObjectCandidates      = Ptr<TriggerObjectCandidates>;
using pTriggerAccepts               = Ptr<TriggerAccepts>;
using PrimaryVerticesPtr            = Ptr<PrimaryVertices>;
using pL1TJetCandidates             = Ptr<L1TJetCandidates>;
using pL1TMuonCandidates            = Ptr<L1TMuonCandidates>;

//
// class declaration
//

class Ntuplizer : public edm::one::EDAnalyzer<edm::one::SharedResources,edm::one::WatchRuns,edm::one::WatchLuminosityBlocks> {
   public:
      explicit Ntuplizer(const edm::ParameterSet&);
      ~Ntuplizer();

      //! Member function
      /*! To state exactly what you do use, even if it is no parameters. Required by EDAnalyzer?
      */
      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      void analyze(const edm::Event&, const edm::EventSetup&) override;
      void beginJob() override;
      void endJob() override;
      void beginRun(edm::Run const&, edm::EventSetup const&) override;
      void endRun(edm::Run const&, edm::EventSetup const&) override;
      void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      template<typename Product>
         void registerToken(InputTag const&, Token<Product>&, InputTag& );
      template<typename Product, edm::BranchType B>
         void registerToken(InputTag const&, Token<Product>&, InputTag& );
      template<typename Collection>
         void registerTokens(InputTags const& , TokenMap<Collection>& );
      String makeCollectionTree(InputTag const& collection, bool useFullName = false, String const& custom_tree_name = "");
      
      // ----------member data ---------------------------
      edm::ParameterSet config_;
      
      bool is_mc_;
      bool use_full_name_;
      bool do_l1jets_;
      bool do_l1muons_;
      bool do_patjets_;
      bool do_patmets_;
      bool do_patmuons_;
      bool do_genjets_;
      bool do_genparticles_;
      bool do_pileup_info_;
      bool do_geneventinfo_;
      bool do_triggeraccepts_;
      bool do_event_count_summary_;
      bool do_genfilter_;
      bool do_triggerobjects_;
      bool do_genruninfo_;
      bool do_lumiscalers_;
      bool store_prescale_;
      bool testmode_;
      bool do_metfilters_;

      Strings trig_res_process_;
      Strings inputTagsVec_;
      Strings inputTags_;
      Strings btag_discriminators_;
      Strings btag_discriminators_alias_;
      Strings triggerObjectLabels_;
      Strings triggerObjectSplits_;
      Strings triggerObjectSplitsTypes_;
      std::vector<analysis::utils::TitleAlias>  btagging_;
      std::vector<analysis::utils::TitleAlias>  bregression_;
      std::vector<analysis::utils::TitleAlias>  discriminators_;
      Strings jecRecords_;
      Strings jerRecords_;

      TokenMap<pat::JetCollection>                       patJetTokens_;
      TokenMap<pat::MuonCollection>                      patMuonTokens_;
      TokenMap<pat::METCollection>                       patMETTokens_;
      TokenMap<pat::TriggerObjectStandAloneCollection>   triggerObjTokens_;
      TokenMap<edm::TriggerResults>                      triggerResultsTokens_;
      TokenMap<l1t::JetBxCollection>                     l1tJetTokens_;
      TokenMap<l1t::MuonBxCollection>                    l1tMuonTokens_;
      TokenMap<trigger::TriggerEvent>                    triggerEventTokens_;
      TokenMap<reco::VertexCollection>                   primary_vertices_tokens_;
      TokenMap<reco::GenJetCollection>                   genJetTokens_;
      TokenMap<reco::GenParticleCollection>              genPartTokens_;

      std::shared_ptr<HLTPrescaleProvider> hltPrescaleProvider_;
      HLTConfigProvider                    hltConfigProvider_;

      InputTag genFilterInfo_;
      InputTag totalEvents_;
      InputTag filteredEvents_;
      InputTag filteredMHatEvents_;
      InputTag genRunInfo_;
      InputTag pileup_info_;
      InputTag genEventInfo_;
      InputTag lumiScalers_;
      InputTag fixedGridRhoAll_;
      InputTag prefWeight_;
      InputTag prefWeightUp_;
      InputTag prefWeightDown_;
      InputTag metfilters_;

      Token<GenFilterInfo>                    genFilterInfoToken_;
      Token<edm::MergeableCounter>            totalEventsToken_;
      Token<edm::MergeableCounter>            filteredEventsToken_;
      Token<edm::MergeableCounter>            filteredMHatEventsToken_;
      Token<GenRunInfoProduct>                genRunInfoToken_;
      Token<std::vector<PileupSummaryInfo>>   pileup_info_token_;
      Token<GenEventInfoProduct>              genEventInfoToken_;
      Token<LumiScalersCollection>            lumiScalersToken_;
      Token<double>                           fixedGridRhoAllToken_;
      Token<double>                           prefWeightToken_;
      Token<double>                           prefWeightUpToken_;
      Token<double>                           prefWeightDownToken_;
      Token<edm::TriggerResults>              metfilters_tokens_;

      
      InputTags eventCounters_;
      InputTags mHatEventCounters_;
      
      std::map<std::string, TTree*> tree_; // Non-owning pointers. TTree objects are created and owned by TFileService.

      // Ntuple stuff
      EventInfoPtr eventinfo_;
      MetadataPtr  metadata_;
      
      // Collections for the ntuples (vector)
      Collections<PatJetCandidates>             patjets_collections_;
      Collections<PatMuonCandidates>            patmuons_collections_;
      Collections<PatMETCandidates>             patmets_collections_;
      Collections<TriggerObjectCandidates>      triggerobjects_collections_;
      Collections<L1TJetCandidates>             l1tjets_collections_;
      Collections<L1TMuonCandidates>            l1tmuons_collections_;
      Collections<PrimaryVertices>              primary_vertices_collections_;
      Collections<GenJetCandidates>             genjets_collections_;
      Collections<GenParticleCandidates>        genparticles_collections_;
      Collections<TriggerAccepts>               triggeraccepts_collections_;
      
      // Collections for the ntuples (single)
      
      // metadata
      double xsection_;
      
      EventCounts event_counts_;
      WeightedEventCounts gen_event_counts_;
      
      // ESTokens
      std::vector<analysis::utils::JerESTokens> jer_es_tokens_;
      std::vector<analysis::utils::JecESTokens> jec_es_tokens_;
      
      // JER
      Strings jer_files_;
      Strings jersf_files_;
      
      // File
      TFileDirectory eventsDir_;

      int analyze_count_;
      
      
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
Ntuplizer::Ntuplizer(const edm::ParameterSet& config):config_(config) { //:   // initialization of ntuple classes
   printf_info("==> Ntuplizer::Ntuplizer() constructor...\n");

   usesResource(TFileService::kSharedResource);
   edm::Service<TFileService> file_service; // TODO:  book TTrees and branches during construction (seems CMSSW style) or during beginJob() (seems ROOT style)?  For now, do it in the constructor.
   eventsDir_ = file_service -> mkdir("Events");   

   //now do what ever initialization is needed
   is_mc_           = config_.getParameter<bool> ("MonteCarlo");
   xsection_        = config_.getParameter<double>("CrossSection");
   store_prescale_  = config_.getParameter<bool> ("StorePrescale");
   eventCounters_.resize(2);
   mHatEventCounters_.resize(2);

   // Metadata 
   metadata_ = std::make_unique<Metadata>(file_service, is_mc_);
   metadata_ -> Init();
   // Definitions of the variables to be stored in the metadata tree
   // --- Btagging algorithms (handles vstring, VPSet, or PSet mapping jet-type -> PSet containing VPSet) ---
   btagging_.clear();
   auto vpset_btag = config_.getParameter<std::vector<edm::ParameterSet>>("BTagging");
   for ( auto const & pset_btag : vpset_btag ) {
      String btag = pset_btag.getParameter<std::string>("discriminator");
      String btag_alias = pset_btag.getParameter<std::string>("alias"); // alias is obligatory!!!
      btagging_.push_back({btag, btag_alias});
   }
   metadata_ -> AddDefinitions(btagging_,"btagging");

   // --- BRegression algorithms (handles vstring, VPSet, or PSet mapping jet-type -> PSet containing VPSet) ---
   bregression_.clear();
   auto vpset_bregression = config_.getParameter<std::vector<edm::ParameterSet>>("BRegression");
   for ( auto const & pset_bregression : vpset_bregression ) {
      String bregression = pset_bregression.getParameter<std::string>("discriminator");
      String bregression_alias = pset_bregression.getParameter<std::string>("alias"); // alias is obligatory!!!
      bregression_.push_back({bregression, bregression_alias});
   }
   metadata_ -> AddDefinitions(bregression_,"bregression");
   
   discriminators_.reserve(btagging_.size() + bregression_.size());
   discriminators_.insert(discriminators_.end(), btagging_.begin(), btagging_.end());
   discriminators_.insert(discriminators_.end(), bregression_.begin(), bregression_.end());

   do_metfilters_ = config_.exists("MetFiltersResults");

   do_triggeraccepts_   = config_.exists("TriggerResults");
   trig_res_process_.clear();
   
   use_full_name_ = false;
   testmode_      = false;
   inputTagsVec_ = config_.getParameterNamesForType<InputTags>();
   inputTags_    = config_.getParameterNamesForType<InputTag>();
   
   hltPrescaleProvider_ = std::make_shared<HLTPrescaleProvider>(config_, consumesCollector(), *this);
   
   std::string name;
   std::string fullname;

   // Table-driven dispatch
   using RegistersFn = std::function<void(InputTags const&)>;
   std::unordered_map<std::string, RegistersFn> inputTagsDispatch;

   // Main stuff
   inputTagsDispatch["PatJets"] = [&](InputTags const& collections) {
      for (auto const& collection : collections) makeCollectionTree(collection);
      registerTokens<pat::JetCollection>(collections, patJetTokens_);
   };
   inputTagsDispatch["PrimaryVertices"] = [&](InputTags const& collections) {
      registerTokens<reco::VertexCollection>(collections, primary_vertices_tokens_);
      for (auto const& collection : collections) {
         String tree_name = makeCollectionTree(collection);
         primary_vertices_collections_.push_back(std::make_unique<PrimaryVertices>(collection, tree_[tree_name]));
      }
   };
   inputTagsDispatch["PatMETs"] = [&](InputTags const& collections) {
      for (auto const& collection : collections) makeCollectionTree(collection);
      registerTokens<pat::METCollection>(collections, patMETTokens_);
   };
   inputTagsDispatch["PatMuons"] = [&](InputTags const& collections) {
      for (auto const& collection : collections) makeCollectionTree(collection);
      registerTokens<pat::MuonCollection>(collections, patMuonTokens_);
   };
   inputTagsDispatch["GenJets"] = [&](InputTags const& collections) {
      for (auto const& collection : collections) makeCollectionTree(collection);
      registerTokens<reco::GenJetCollection>(collections, genJetTokens_);
   };
   inputTagsDispatch["GenParticles"] = [&](InputTags const& collections) {
      for (auto const& collection : collections) makeCollectionTree(collection);
      registerTokens<reco::GenParticleCollection>(collections, genPartTokens_);
   };


   // Trigger stuff
   inputTagsDispatch["TriggerObjectStandAlone"] = [&](InputTags const& collections) {
      registerTokens<pat::TriggerObjectStandAloneCollection>(collections, triggerObjTokens_);
   };
   inputTagsDispatch["TriggerEvent"] = [&](InputTags const& collections) {
      registerTokens<trigger::TriggerEvent>(collections, triggerEventTokens_);
   };

   inputTagsDispatch["TriggerResults"] = [&](InputTags const& collections) {
      registerTokens<edm::TriggerResults>(collections, triggerResultsTokens_);
      Strings triggerpaths;
      Strings l1seeds;
      if (config_.exists("TriggerPaths"))
         triggerpaths = config_.getParameter<Strings>("TriggerPaths");
      if (config_.exists("L1Seeds"))
         l1seeds = config_.getParameter<Strings>("L1Seeds");
      for (auto const& collection : collections) {
         makeCollectionTree(collection);
         trig_res_process_.push_back(collection.process());
         triggeraccepts_collections_.push_back( pTriggerAccepts( new TriggerAccepts(collection, tree_[collection.label()], triggerpaths, l1seeds, hltPrescaleProvider_) ));
         triggeraccepts_collections_.back()->Init();
         triggeraccepts_collections_.back()->ReadPrescaleInfo(store_prescale_);
      }
   };
   
   inputTagsDispatch["L1TJets"] = [&](InputTags const& collections) { // TODO: make it single inputtag, since we only want to make one collection of L1TJets in the ntuple
      registerTokens<l1t::JetBxCollection>(collections, l1tJetTokens_);
      for (auto const& collection : collections) {
         if (l1tjets_collections_.size() == 0) {
            String tree_name = makeCollectionTree(collection, false, "l1tJets");
            l1tjets_collections_.push_back(std::make_unique<L1TJetCandidates>(collection, tree_[tree_name], is_mc_ ));
            l1tjets_collections_.back() -> Init();
         }
      }
   };
   inputTagsDispatch["L1TMuons"] = [&](InputTags const& collections) {  // TODO: make it single inputtag, since we only want to make one collection of L1TMuons in the ntuple
      registerTokens<l1t::MuonBxCollection>(collections, l1tMuonTokens_);
      for (auto const& collection : collections) {
         if (l1tmuons_collections_.size() == 0) {
            String tree_name = makeCollectionTree(collection, false, "l1tMuons");
            l1tmuons_collections_.push_back(std::make_unique<L1TMuonCandidates>(collection, tree_[tree_name], is_mc_ ));
            l1tmuons_collections_.back() -> Init();
         }
      }
   };

   // Loop over configured input tag categories, retrieve the collection tags for each category,
   // and inputTagsDispatch registration of the corresponding tokens based on the category name.
   for ( auto & inputTags : inputTagsVec_ ) {

      InputTags collections = config_.getParameter<InputTags>(inputTags);
      auto it = inputTagsDispatch.find(inputTags);
      if (it == inputTagsDispatch.end()) {
         throw cms::Exception("Configuration") << "Unknown input tag category '" << inputTags << "'\n";
      }
      it->second(collections);

   }
   
   // Single InputTag
   using RegisterFn = std::function<void(InputTag const&)>;
   std::unordered_map<std::string, RegisterFn> inputTagDispatch;

   inputTagDispatch["PileupSummaryInfo"] = [&](InputTag const& collection) {
      registerToken< std::vector<PileupSummaryInfo> >(collection,pileup_info_token_,pileup_info_);
   };
   inputTagDispatch["GenEventInfo"] = [&](InputTag const& collection) {
      registerToken<GenEventInfoProduct>(collection,genEventInfoToken_,genEventInfo_);
   };
   inputTagDispatch["LumiScalers"] = [&](InputTag const& collection) {
      registerToken<LumiScalersCollection>(collection,lumiScalersToken_,lumiScalers_);
   };
   inputTagDispatch["FixedGridRhoAll"] = [&](InputTag const& collection) {
      registerToken<double>(collection,fixedGridRhoAllToken_,fixedGridRhoAll_);
   };
   inputTagDispatch["PrefiringWeight"] = [&](InputTag const& collection) {
      registerToken<double>(collection,prefWeightToken_,prefWeight_);
   };
   inputTagDispatch["PrefiringWeightUp"] = [&](InputTag const& collection) {
      registerToken<double>(collection,prefWeightUpToken_,prefWeightUp_);
   };
   inputTagDispatch["PrefiringWeightDown"] = [&](InputTag const& collection) {
      registerToken<double>(collection,prefWeightDownToken_,prefWeightDown_);
   };

   inputTagDispatch["GenFilterInfo"] = [&](InputTag const& collection) {
      registerToken<GenFilterInfo,edm::InLumi>(collection,genFilterInfoToken_,genFilterInfo_);
   };
   inputTagDispatch["GenRunInfo"] = [&](InputTag const& collection) {
      registerToken<GenRunInfoProduct,edm::InRun>(collection,genRunInfoToken_,genRunInfo_);
   };
   inputTagDispatch["TotalEvents"] = [&](InputTag const& collection) {
      registerToken<edm::MergeableCounter,edm::InLumi>(collection,totalEventsToken_,totalEvents_);
   };
   inputTagDispatch["FilteredEvents"] = [&](InputTag const& collection) {
      registerToken<edm::MergeableCounter,edm::InLumi>(collection,filteredEventsToken_,filteredEvents_);
   };
   inputTagDispatch["FilteredMHatEvents"] = [&](InputTag const& collection) {
      registerToken<edm::MergeableCounter,edm::InLumi>(collection,filteredMHatEventsToken_,filteredMHatEvents_);
   };
   inputTagDispatch["MetFiltersResults"] = [&](InputTag const& collection) {
      registerToken<edm::TriggerResults>(collection, metfilters_tokens_, metfilters_);
   };


   for ( auto & inputTag : inputTags_ ) {
      InputTag collection = config_.getParameter<InputTag>(inputTag);
      auto it = inputTagDispatch.find(inputTag);
      if (it != inputTagDispatch.end())
         it->second(collection);
   }
   
   // flags
   do_patjets_          = config_.exists("PatJets");

   // ESTokens
   // JER Record (from TXT files)
   // JER Record (from CondDB)
   jerRecords_.clear();
   if ( do_patjets_ && config_.exists("JERRecords") ) {
      jerRecords_ = config_.getParameter< Strings >("JERRecords");
      for ( auto & rcd : jerRecords_ ) {
         if ( rcd != "" ) {
            std::string label_pt = rcd + "_pt";
            std::string label_sf = rcd;
            JerESTokens est;
            est.record = rcd;
            est.resolutionsToken = esConsumes(edm::ESInputTag("", label_pt));
            est.scaleFactorsToken = esConsumes(edm::ESInputTag("", label_sf));
            jer_es_tokens_.push_back(est);
         }
      }
      if(config_.exists("JERResFiles")) {
      	jer_files_ = config_.getParameter< Strings >("JERResFiles");
      }
      if(config_.exists("JERSfFiles")) {
      	jersf_files_ = config_.getParameter< Strings >("JERSfFiles");
      }
      
   }
   // JEC record (from CondDB)
   // see example: https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatUtils/plugins/ShiftedPFCandidateProducerForNoPileUpPFMEt.cc
   jecRecords_.clear();
   if ( do_patjets_ && config_.exists("JECRecords") ) {
      jecRecords_ = config_.getParameter< Strings >("JECRecords");
      for ( auto & rcd : jecRecords_ ) {
         if ( rcd != "" ) {
            JecESTokens est;
            est.record = rcd;
            est.jecToken = esConsumes(edm::ESInputTag("", rcd));
            jec_es_tokens_.push_back(est);
         }
      }
   }

   analyze_count_ = 0;

}


Ntuplizer::~Ntuplizer() {
   printf_info("==> Ntuplizer::~Ntuplizer() destructor...\n");
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
   printf_info("*** THE END!!! ***\n");

}


//
// member functions
//

// ------------ method called for each event  ------------
void Ntuplizer::analyze(const edm::Event& event, const edm::EventSetup& setup) {
   using namespace edm;

   ++analyze_count_;
   if ( analyze_count_ == 1 ) {
      printf_info("==> Ntuplizer::analyze()...\n");
   }

   // Event info
   eventinfo_ -> Fill(event);
   
   if ( is_mc_ ) {
      // MC only stuff
   }
      
      // Pat jets (pat)
      for ( auto & collection : patjets_collections_ )
         collection -> Fill(event, setup);
   
      // Pat mets (pat)
      for ( auto & collection : patmets_collections_ )
         collection -> Fill(event);
   
      // Pat muon (pat)
      for ( auto & collection : patmuons_collections_ )
         collection -> Fill(event);
   
      // Gen jets (reco)
      for ( auto & collection : genjets_collections_ )
         collection -> Fill(event);
      
      // Gen particles (reco)
      for ( auto & collection : genparticles_collections_ )
         collection -> Fill(event);
      
      
      // trigger accepts
      for ( auto & collection : triggeraccepts_collections_ )
         collection -> Fill(event, setup);
      
      // primary vertices
      for ( auto & collection : primary_vertices_collections_ )
         collection -> Fill(event);
   
      // trigger objects
      for ( auto & collection : triggerobjects_collections_ )
         collection -> Fill(event);
      
      // L1T jets
      for ( auto & collection : l1tjets_collections_ )
         collection -> Fill(event);
      // L1T muons
      for ( auto & collection : l1tmuons_collections_ )
         collection -> Fill(event);

}


// ------------ method called once each job just before starting event loop  ------------
void Ntuplizer::beginJob() {

   printf_info("==> Ntuplizer::beginJob()...\n");

   // TODO: move all below to constructor?
   
   do_pileup_info_      = config_.exists("PileupSummaryInfo") && is_mc_;
   do_geneventinfo_     = config_.exists("GenEventInfo") && is_mc_;
   do_lumiscalers_      = config_.exists("LumiScalers");
   do_patmets_          = config_.exists("PatMETs");
   do_patmuons_         = config_.exists("PatMuons");
   do_genjets_          = config_.exists("GenJets");
   do_genparticles_     = config_.exists("GenParticles");
   do_triggeraccepts_   = config_.exists("TriggerResults");
   do_event_count_summary_      = config_.exists("TotalEvents")  && config_.exists("FilteredEvents");
   do_genfilter_        = config_.exists("GenFilterInfo") && is_mc_;
   do_triggerobjects_   = ( config_.exists("TriggerObjectStandAlone") || config_.exists("TriggerEvent") ) &&  config_.exists("TriggerObjectLabels");
   do_genruninfo_       = config_.exists("GenRunInfo") && is_mc_ ;
   
   if ( config_.exists("TestMode") ) // This is DANGEROUS! but can be useful. So BE CAREFUL!!!!
      testmode_ = config_.getParameter<bool> ("TestMode");
   
   if ( config_.exists("UseFullName") )
      use_full_name_ = config_.getParameter<bool> ("UseFullName");

   std::string name;
   std::string fullname;
   
   gen_event_counts_  = {};
   event_counts_ = {};
   
   // -------------------------------
   // JEC Record (from TXT files)
   Strings jec_files;
   // JEC Record (from CondDB)
   if ( do_patjets_ && config_.exists("JECRecords") ) {
      if(config_.exists("JECUncertaintyFiles")) {
         jec_files = config_.getParameter< Strings >("JECUncertaintyFiles");
      }
   }
   
   size_t nPatJets = 0;
   if ( do_patjets_ )
      nPatJets = config_.getParameter<InputTags>("PatJets").size();
   
   if ( nPatJets > jecRecords_.size() && jecRecords_.size() != 0 ) {
      printf_error("Ntuplizer::beginJob *** ERROR ***  Number of JEC Records less than the number of PatJet collections.\n");
      exit(-1);
   }
   if ( nPatJets > jerRecords_.size() && jerRecords_.size() != 0 ) {
      printf_error("Ntuplizer::beginJob *** ERROR ***  Number of JER Records less than the number of PatJet collections.\n");
      exit(-1);
   }
   if ( jerRecords_.size() != 0 && jer_files_.size() != 0 && jersf_files_.size()!=0 &&(jerRecords_.size() != jer_files_.size() || jerRecords_.size() != jersf_files_.size()) ) {
      printf_error("Ntuplizer::beginJob *** ERROR *** Number of JER Records are not the same as number of provided input files.\n");
      exit(-1);
   }
   
   
   // Event info tree
   eventinfo_ = EventInfoPtr(new EventInfo(eventsDir_));
   if ( config_.exists("FixedGridRhoAll") )
      eventinfo_ -> FixedGridRhoInfo(config_.getParameter<InputTag>("FixedGridRhoAll"));
   if ( do_pileup_info_ )
      eventinfo_ -> PileupInfo(config_.getParameter<InputTag>("PileupSummaryInfo"));
   if ( do_geneventinfo_ )
      eventinfo_ -> GenEventInfo(config_.getParameter<InputTag>("GenEventInfo"));
   if ( do_lumiscalers_ )
      eventinfo_ -> LumiScalersInfo(config_.getParameter<InputTag>("LumiScalers"));
   
   if ( config_.exists("PrefiringWeight") &&  config_.exists("PrefiringWeightUp") && config_.exists("PrefiringWeightDown"))
      eventinfo_ -> PrefiringWeightInfo(prefWeight_, prefWeightUp_, prefWeightDown_);

   
   InputTag trgRes;
   if ( do_triggeraccepts_ ) {
      InputTags trs = config_.getParameter<InputTags>("TriggerResults");
      trgRes = trs[0];
   }
   
   // split trigger objects
   bool splitTriggerObject = config_.exists("TriggerObjectSplits");
   if ( do_triggerobjects_ && triggerObjectSplits_.empty() && splitTriggerObject ) {
      triggerObjectSplits_  = config_.getParameter< Strings >("TriggerObjectSplits");
      if ( ! triggerObjectSplits_.empty() && triggerObjectSplitsTypes_.empty() && config_.exists("TriggerObjectSplitsTypes") ) {
         triggerObjectSplitsTypes_ = config_.getParameter< Strings >("TriggerObjectSplitsTypes");
         for ( auto & tot : triggerObjectSplitsTypes_ ) std::transform(tot.begin(), tot.end(), tot.begin(), ::tolower);
         splitTriggerObject = !triggerObjectSplitsTypes_.empty();
      }
   }
   
   if ( triggerObjectSplits_.size() != triggerObjectSplitsTypes_.size() ) {
      std::cout << "-w- Ntuplizer: Size of trigger splits and splits types do not match!" << std::endl;
      std::cout << "               No splitting will be done" << std::endl;
      splitTriggerObject = false;
   }
   
   // Input tags (vector)
   for ( auto & inputTags : inputTagsVec_ ) {
      InputTags collections = config_.getParameter<InputTags>(inputTags);
      int patJetCounter = 0;
      for ( auto & collection : collections ) {
   
         // Names for the trees, from inputs
         std::string label = collection.label();
         std::string inst  = collection.instance();
         std::string proc  = collection.process();
         name = label;
         fullname = name + "_" + inst + "_" + proc;
         // name += inputTags == "L1ExtraJets" && ! use_full_name_ ? "_" + inst : "";
         if ( collection.instance() != "" && collections.size() > 1 )
            name += "_" + inst;
         if ( use_full_name_ ) name = fullname;
         
         // Pat Jets
         if ( inputTags == "PatJets" ) {
            patjets_collections_.push_back( pPatJetCandidates( new PatJetCandidates(collection, tree_[name], is_mc_ ) ));
            patjets_collections_.back() -> Init(discriminators_);
            patjets_collections_.back() -> PileupJetIdInstance("pileupJetId");
            
            if ( patJetCounter == 0 && jecRecords_.size() > 0  ) 
            std::cout << "*** Jet Energy Corrections Records - PatJets ***" << std::endl;
            if ( jecRecords_.size() > 0  ) {
               if ( jec_files.size() > 0 && jec_files[patJetCounter] != "" )
                  patjets_collections_.back() -> AddJecInfo(jecRecords_[patJetCounter],jec_files[patJetCounter]);  // use txt file
               else
               //   patjets_collections_.back() -> AddJecInfo(jecRecords_[patJetCounter]);                           // use confdb
                  patjets_collections_.back() -> AddJecInfo(jec_es_tokens_[patJetCounter]);                           // use confdb

            }
            
            if ( patJetCounter == 0 && jerRecords_.size() > 0  ) std::cout << "*** Jet Energy Resolutions Records - PatJets ***" << std::endl;
            if ( jerRecords_.size() > 0 && is_mc_  ) {
               if ( jer_files_.size() > 0 && jer_files_[patJetCounter] != "" )
                  patjets_collections_.back() -> AddJerInfo(jerRecords_[patJetCounter],jer_files_[patJetCounter], jersf_files_[patJetCounter],fixedGridRhoAll_);  // use txt file
               else
               //   patjets_collections_.back() -> AddJerInfo(jerRecords_[patJetCounter],fixedGridRhoAll_);  // use txt file
                  patjets_collections_.back() -> AddJerInfo(jer_es_tokens_[patJetCounter],fixedGridRhoAll_);  // use txt file

            }
            ++patJetCounter;
         }
         // Pat METs
         if ( inputTags == "PatMETs" ) {
            patmets_collections_.push_back( pPatMETCandidates( new PatMETCandidates(collection, tree_[name], is_mc_) ));
            patmets_collections_.back() -> Init();
         }
         // Pat Muons
         if ( inputTags == "PatMuons" ) {
            patmuons_collections_.push_back( pPatMuonCandidates( new PatMuonCandidates(collection, tree_[name], is_mc_ ) ));
            patmuons_collections_.back() -> Init();
         }
         // Gen Jets
         if ( inputTags == "GenJets" ) {
            genjets_collections_.push_back( pGenJetCandidates( new GenJetCandidates(collection, tree_[name], is_mc_ ) ));
            genjets_collections_.back() -> Init();
         }
         // Gen Particles
         if ( inputTags == "GenParticles" ) {
            genparticles_collections_.push_back( pGenParticleCandidates( new GenParticleCandidates(collection, tree_[name], is_mc_ ) ));
            genparticles_collections_.back() -> Init();
        }
         
         // Trigger Objects
         if ( do_triggeraccepts_  && do_triggerobjects_ && inputTags == "TriggerObjectStandAlone"  ) {
            if ( triggerObjectLabels_.empty() )
               triggerObjectLabels_ = config_.getParameter< Strings >("TriggerObjectLabels");
            sort( triggerObjectLabels_.begin(), triggerObjectLabels_.end() );
            triggerObjectLabels_.erase( unique( triggerObjectLabels_.begin(), triggerObjectLabels_.end() ), triggerObjectLabels_.end() );
            std::string dir = name;
            TFileDirectory triggerObjectsDir = eventsDir_.mkdir(dir);
      
            for ( auto & triggerObjectLabel : triggerObjectLabels_ ) {
               name = triggerObjectLabel;
               if ( use_full_name_ ) name += "_" + dir;
               tree_[name] = triggerObjectsDir.make<TTree>(name.c_str(),name.c_str());
               triggerobjects_collections_.push_back(pTriggerObjectCandidates( new TriggerObjectCandidates(collection, tree_[name], is_mc_ ) ));
               triggerobjects_collections_.back() -> Init();
               triggerobjects_collections_.back() -> UseTriggerResults(trgRes);
               if ( splitTriggerObject ) {
                  Strings types;
                  for ( size_t tos = 0; tos < triggerObjectSplits_.size() ; ++tos ) {
                     if ( triggerObjectSplits_.at(tos) == name ) {
                        types = string_split(triggerObjectSplitsTypes_.at(tos), ':');
                        break;
                     }
                  }
                  sort( types.begin(), types.end() );
                  types.erase( unique( types.begin(), types.end() ), types.end() );
                  for ( auto & tot : types ) {
                     std::string namesplit = name + "_" + tot;
                     tree_[namesplit] = triggerObjectsDir.make<TTree>(namesplit.c_str(),namesplit.c_str());
                     triggerobjects_collections_.push_back(pTriggerObjectCandidates( new TriggerObjectCandidates(collection, tree_[namesplit], is_mc_ ) ));
                     triggerobjects_collections_.back() -> Init();
                     triggerobjects_collections_.back() -> UseTriggerResults(trgRes);
                     triggerobjects_collections_.back() -> TriggerObjectType(tot);
                  }

               }
               
            }
         }   

         if ( do_triggerobjects_ && inputTags == "TriggerEvent"  ) {
            if ( triggerObjectLabels_.empty() )
               triggerObjectLabels_ = config_.getParameter< Strings >("TriggerObjectLabels");
            sort( triggerObjectLabels_.begin(), triggerObjectLabels_.end() );
            triggerObjectLabels_.erase( unique( triggerObjectLabels_.begin(), triggerObjectLabels_.end() ), triggerObjectLabels_.end() );
            std::string dir = name;
            TFileDirectory triggerObjectsDir = eventsDir_.mkdir(dir);
      
         }
         
      }
   }

   // Metadata stuff
   int n_filter_counters = 0;
   int n_mhat_filter_counters = 0;

   // InputTag (single, i.e. not vector)
   for ( auto & inputTag : inputTags_ ) { 
      InputTag collection = config_.getParameter<InputTag>(inputTag);
      // Names for the trees, from inputs
      std::string label = collection.label();
      std::string inst  = collection.instance();
      std::string proc  = collection.process();
      name = label;
      fullname = name + "_" + inst + "_" + proc;
      if ( use_full_name_ ) name = fullname;
         
      // Generator filter
      if ( do_genfilter_ && inputTag == "GenFilterInfo" )
         metadata_ -> SetGeneratorFilter(config_.getParameter<InputTag> ("GenFilterInfo"));

      // Event filter
      if ( do_event_count_summary_ ) {
         if ( inputTag == "TotalEvents" ) {
            eventCounters_[0] = totalEvents_;
            mHatEventCounters_[0] = totalEvents_;
            ++n_filter_counters;
            ++n_mhat_filter_counters;
         }
         if ( inputTag == "FilteredEvents" ) {
            eventCounters_[1] = filteredEvents_;
            ++n_filter_counters;
         }
         if ( inputTag == "FilteredMHatEvents" ) {
            mHatEventCounters_[1] = filteredMHatEvents_;
            ++n_mhat_filter_counters;
         }

         if ( n_filter_counters == 2 ) 		metadata_ -> SetEventCountSummary(eventCounters_);
         if ( n_mhat_filter_counters == 2)	metadata_ -> SetMHatEventCountSummary(mHatEventCounters_);
      }

   } 
   
}

// ------------ method called once each job just after ending the event loop  ------------
void Ntuplizer::endJob() {
   printf_info("==> NTuplizer::endJob()...\n");
   metadata_ -> Fill();
}

// ------------ method called when starting to processes a run  ------------
void Ntuplizer::beginRun(edm::Run const& run, edm::EventSetup const& setup) {
   printf_info("==> Ntuplizer::beginRun(): Run = %d ...\n", (int)run.run());

   bool changed(true);

   std::string proc;
   if ( !trig_res_process_.empty() ) {
      proc = trig_res_process_[0];        // for the time being only one TriggerResults is used TODO: simplify and always allow only one entry, i.e. remove vector
      if (hltPrescaleProvider_->init(run, setup, proc, changed)) {
         hltConfigProvider_ = hltPrescaleProvider_->hltConfigProvider();
      }
      // trigger accepts
      for ( auto & collection : triggeraccepts_collections_ )
         collection -> Providers(hltPrescaleProvider_, std::make_shared<HLTConfigProvider>(hltConfigProvider_));
   }
   else {
      std::cout << "Error: TriggerResults is empty!" << std::endl;
      exit(-1);
   }

}


// ------------ method called when ending the processing of a run  ------------
void Ntuplizer::endRun(edm::Run const& run, edm::EventSetup const& setup) {
   printf_info("==> Ntuplizer::endRun(): Run = %d ...\n", (int)run.run());

   if ( do_genruninfo_ ) {
      metadata_ -> SetCrossSections(run,genRunInfo_,xsection_);
   }

}

// ------------ method called when starting to processes a luminosity block  ------------
void  Ntuplizer::beginLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& setup) {
   printf_info("==> Ntuplizer::beginLuminosityBlock(): Run = %d, LumiSection = %d ...\n", (int)lumi.run(), (int)lumi.id().value());

}


// ------------ method called when ending the processing of a luminosity block  ------------
void Ntuplizer::endLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& setup) {
   printf_info("==> Ntuplizer::endLuminosityBlock(): Run = %d, LumiSection = %d ...\n", (int)lumi.run(), (int)lumi.id().value());
   metadata_ -> IncrementEventCount(lumi);
}

template<typename Collection>
void Ntuplizer::registerTokens(InputTags const& collections, TokenMap<Collection>& tokenMap) {
   for (auto const& collection : collections) {
      std::string collection_name = collection.label() + "_" + collection.instance() + "_" + collection.process();
      tokenMap[collection_name] = consumes<Collection>(collection);
   }
}

template<typename Product>
void Ntuplizer::registerToken(InputTag const& collection, Token<Product>& token, InputTag& storedCollection) {
   token = consumes<Product>(collection);
   storedCollection = collection;
}

template<typename Product, edm::BranchType B>
void Ntuplizer::registerToken(InputTag const& collection, Token<Product>& token, InputTag& storedCollection) {
   token = consumes<Product,B>(collection);
   storedCollection = collection;
}

String Ntuplizer::makeCollectionTree(InputTag const& collection, bool use_full_name, String const& custom_tree_name) {
   String label = collection.label();
   String inst  = collection.instance();
   String proc  = collection.process();
   String full_name = label + "_" + inst + "_" + proc;
   String tree_name;
   if (!custom_tree_name.empty()) {
      tree_name = custom_tree_name;
   } else {
      tree_name = use_full_name ? full_name : label;
   }
   tree_[tree_name] = eventsDir_.make<TTree>(tree_name.c_str(), full_name.c_str());
   return tree_name;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void Ntuplizer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
   edm::ParameterSetDescription desc;

   // desc.setAllowAnything();

   desc.add<unsigned int>("stageL1Trigger", 2);
   desc.add<bool>("StorePrescale", false);
   desc.add<bool>("MonteCarlo");

   desc.add<InputTag>("FixedGridRhoAll", InputTag("fixedGridRhoAll"));
   desc.add<InputTags>("TriggerResults", { InputTag("TriggerResults", "", "HLT") });
   //or    desc.add<InputTags>("TriggerResults", InputTags{ InputTag("TriggerResults", "", "HLT") });
   desc.add<InputTags>("PatJets", { InputTag("slimmedJetsPuppi") });
   desc.add<Strings>("JECRecords", { "AK4PFPuppi" });
   desc.add<Strings>("JERRecords", { "AK4PFPuppi" });
   desc.add<InputTags>( "PatMuons", { InputTag("slimmedMuons") });
   desc.add<InputTags>( "L1TJets", { InputTag("caloStage2Digis","Jet","RECO") });
   desc.add<InputTags>( "L1TMuons", { InputTag("gmtStage2Digis","Muon","RECO") });
   desc.add<InputTags>( "PrimaryVertices", { InputTag("offlineSlimmedPrimaryVertices") });
   desc.add<InputTag>("MetFiltersResults", InputTag("TriggerResults", "", "PAT"));

   // Optionals
   desc.addOptional<InputTags>("TriggerObjectStandAlone");
   desc.addOptional<InputTag>("FilteredEvents");
   desc.addOptional<InputTag>("TotalEvents");
   desc.addOptional<Strings>("L1Seeds");
   desc.addOptional<Strings>("TriggerPaths");
   desc.addOptional<Strings>("TriggerObjectLabels");
   desc.addOptional<Strings>("TriggerObjectSplits");
   desc.addOptional<Strings>("TriggerObjectSplitsTypes");

   desc.add<double>("CrossSection", -1.0);
   desc.addOptional<InputTag>("GenEventInfo");
   desc.addOptional<InputTag>("GenFilterInfo");
   desc.addOptional<InputTag>("GenRunInfo");
   desc.addOptional<InputTag>("PileupSummaryInfo");
   desc.addOptional<InputTags>("GenJets");
   desc.addOptional<InputTags>("GenParticles");

   desc.addOptional<InputTag>("FilteredMHatEvents");

   edm::ParameterSetDescription desc_btag;
   desc_btag.add<std::string>("discriminator");
   desc_btag.add<std::string>("alias");
   desc.addVPSetOptional("BTagging",desc_btag);

   edm::ParameterSetDescription desc_bregression;
   desc_bregression.add<std::string>("discriminator");
   desc_bregression.add<std::string>("alias");
   desc.addVPSetOptional("BRegression",desc_bregression);
   
   descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(Ntuplizer);
