#ifndef Analysis_Ntuplizer_Metadata_h
#define Analysis_Ntuplizer_Metadata_h 1

// -*- C++ -*-
//
// Package:    Analysis/Ntuplizer
// Class:      Metadata
// 
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
#include <memory>
// 
// user include files
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "SimDataFormats/GeneratorProducts/interface/GenFilterInfo.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "Analysis/Ntuplizer/interface/Definitions.h"
#include "Analysis/Ntuplizer/interface/EventFilter.h"
#include "Analysis/Utils/interface/types.h"
#include "TTree.h"

template<typename T>
using Ptr = std::unique_ptr<T>;
template<typename T>
using Vector = std::vector<T>;


using String = std::string;
using Strings = Vector<String>;
using InputTag = edm::InputTag;
using InputTags = Vector<InputTag>;
using LuminosityBlock = edm::LuminosityBlock;
using Run = edm::Run;
using Definitions = analysis::ntuple::Definitions;
using DefinitionsPtr = Ptr<Definitions>;
using GenFilter = analysis::ntuple::EventFilter<GenFilterInfo>;
using EvtFilter = analysis::ntuple::EventFilter<edm::MergeableCounter>;
using GenFilterPtr = Ptr<GenFilter>;
using EvtFilterPtr = Ptr<EvtFilter>;

//
// class declaration
//

namespace analysis {
   namespace ntuple {
      class Metadata {
         public:
            Metadata();
            Metadata(edm::Service<TFileService> &, const bool &, const String & metadata_folder = "Metadata" );
            Metadata(TFileDirectory & );
           ~Metadata();
            void Init();
            void Fill();
            void AddDefinitions(const Strings &, const Strings &);
            void AddDefinitions(const Strings &, const Strings &, const String &);
            void AddDefinitions(const Vector<analysis::utils::TitleAlias> &, const String &);
            void SetGeneratorFilter(const InputTag & );
            void SetEventFilter(const InputTags &);
            void SetMHatEventFilter(const InputTags &);
            void IncrementEventFilters( LuminosityBlock const& );
            void SetCrossSections( const Run &, const InputTag &, const double & myxs = -1. );
            
            GenFilter & GetGeneratorFilter();
            EvtFilter & GetEventFilter();

         private:
            // ----------member data ---------------------------
            void XSectionTreeBranches_();
            void DatasetTreeBranches_();
            Vector<DefinitionsPtr> vdefinitions_;
            
            bool is_gen_filter_;
            bool is_evt_filter_;
            bool is_mhat_evt_filter_;
            GenFilterPtr  gen_filter_;
            EvtFilterPtr  evt_filter_;
            EvtFilterPtr  m_hat_evt_filter_;
            
            // Cross sections tree
            TTree * xsection_tree_;
            double my_xsection_;
            double xsection_;
            double internal_xsection_;
            double external_xsection_lo_;
            double external_xsection_nlo_;
            unsigned int run_xsection_;
            
            // Dataset tree
            TTree * dataset_tree_;
            bool is_mc_;

            // Tree folders
            TFileDirectory main_folder_;
            TFileDirectory mhat_folder_;   
      };
   }
}

#endif  // Analysis_Ntuplizer_Metadata_h
