//#define CMSSWOLD
#ifndef Analysis_Ntuplizer_TriggerAccepts_h
#define Analysis_Ntuplizer_TriggerAccepts_h 1

// -*- C++ -*-
//
// Package:    Analysis/Ntuplizer
// Class:      TriggerAccepts
// 
/**\class TriggerAccepts TriggerAccepts.cc Analysis/Ntuplizer/src/TriggerAccepts.cc

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
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/Run.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#ifndef CMSSWOLD
#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"
#endif            

#include "TTree.h"

//
// class declaration
//

namespace analysis {
   namespace ntuple {

      class TriggerAccepts {
         public:
            TriggerAccepts();
            TriggerAccepts(const edm::InputTag&, TTree*, const std::vector<std::string> &, const std::vector<std::string> &, const std::shared_ptr<HLTPrescaleProvider> hltPrescale);
            TriggerAccepts(const edm::InputTag&, TTree*, const std::vector<std::string> &, const std::vector<std::string> &);
           ~TriggerAccepts();
            void Init();
            void Branches();
            void Fill(const edm::Event & event, const edm::EventSetup & setup);
            void Run(edm::Run const & , edm::EventSetup const& );
            void Providers(const std::shared_ptr<HLTPrescaleProvider> &, const std::shared_ptr<HLTConfigProvider> &);
            void ReadPrescaleInfo(const bool &);
            bool ReadPrescaleInfo();
      
         private:
            // ----------member data ---------------------------
            
            edm::InputTag input_collection_;
            std::shared_ptr<HLTConfigProvider> hlt_config_;
            std::shared_ptr<HLTPrescaleProvider> hlt_prescale_;
            std::vector<std::string> paths_;
            std::vector<std::string> seeds_;
            bool accept_[1000];     // hopefully 1000 is enough for the number of paths and seeds
            bool l1accept_[1000];
            float psl1_[1000];   // prescale is now double, but we store it as float in the ntuple, for the number is not large nor the precision is high
            float pshlt_[1000];  // prescale is now double, but we store it as float in the ntuple, for the number is not large nor the precision is high

            // TODO: Fractional prescale
            // float psl1_frac_num_[1000]; 
            // float psl1_frac_den_[1000]; 
            // float pshlt_frac_num_[1000];
            // float pshlt_frac_den_[1000];

            bool first_;
            TTree * tree_;
            bool psinfo_;
            
      };
   }
}

#endif  // Analysis_Ntuplizer_TriggerAccepts_h
