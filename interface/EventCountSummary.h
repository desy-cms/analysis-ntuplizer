#ifndef Analysis_Ntuplizer_EventCountSummary_h
#define Analysis_Ntuplizer_EventCountSummary_h 1

// -*- C++ -*-
//
// Package:    Analysis/Ntuplizer
// Class:      EventCountSummary
// 
/**\class EventCountSummary EventCountSummary.cc Analysis/Ntuplizer/src/EventCountSummary.cc

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
// user include files
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"

//
// class declaration
//

namespace analysis {
   namespace ntuple {
      
      struct FilterResults {
         unsigned int total;
         unsigned int filtered;
         double efficiency;
      };
      
      struct WeightedFilterResults {
         double total;
         double filtered;
         double efficiency;
      };

      template <typename T>
      class EventCountSummary {
         public:
            EventCountSummary(edm::Service<TFileService> &, const std::vector<edm::InputTag> & collections = std::vector<edm::InputTag>() );
            EventCountSummary(TFileDirectory &, const std::vector<edm::InputTag> & collections = std::vector<edm::InputTag>());
           ~EventCountSummary();
            void SetCollections(const std::vector<edm::InputTag> &);
            void Increment(edm::LuminosityBlock const& );
            FilterResults Results();
            WeightedFilterResults WeightedResults();
            TTree * Tree();
            void Fill();
      
         private:
            // ----------member data ---------------------------
            unsigned int    nTotal_;
            unsigned int    nFiltr_;
            double          efficiency_;
            unsigned int    nTried_;
            double          wTotal_;
            double          wFiltr_;
            double          wEfficiency_;
            
            std::vector<edm::InputTag> collections_;
            
            // Output tree
            TTree * tree_;
      };         
   }
}

#endif  // Analysis_Ntuplizer_EventCountSummary_h
