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
      
      template<typename CountType>
      struct EventCounts {
         CountType total;
         CountType passed;
         double efficiency;
      };
      
      template <typename T>
      class EventCountSummary {
         public:
            EventCountSummary();
            EventCountSummary(edm::Service<TFileService> &, const std::vector<edm::InputTag> & collections = std::vector<edm::InputTag>() );
            EventCountSummary(TFileDirectory &, const std::vector<edm::InputTag> & collections = std::vector<edm::InputTag>());
           ~EventCountSummary();
            void Collections(const std::vector<edm::InputTag> &);
            const std::vector<edm::InputTag> & Collections();
            void IncrementEventCount(edm::LuminosityBlock const& );
            template<typename CountType>
            EventCounts<CountType> Counts() const;
            TTree * Tree();
            void Fill();
      
         private:
            template<typename CountType>
            static EventCounts<CountType> make_counts_(CountType total, CountType passed);
            // ----------member data ---------------------------
            unsigned int    total_;
            unsigned int    passed_;
            double          efficiency_;
            unsigned int    tried_;
            double          total_weights_;
            double          passed_weights_;
            double          efficiency_weights_;
            
            std::vector<edm::InputTag> collections_;
            
            // Output tree
            TTree * tree_;
      };         
   }
}

#endif  // Analysis_Ntuplizer_EventCountSummary_h
