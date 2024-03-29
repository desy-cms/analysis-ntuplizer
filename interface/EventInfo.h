#ifndef Analysis_Ntuplizer_EventInfo_h
#define Analysis_Ntuplizer_EventInfo_h 1

// -*- C++ -*-
//
// Package:    Analysis/Ntuplizer
// Class:      EventInfo
// 
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
#include <memory>
// 
// user include files
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"

//
// class declaration
//

namespace analysis {
   namespace ntuple {

      class EventInfo {
         public:
            EventInfo();
            EventInfo(edm::Service<TFileService> &);
            EventInfo(TFileDirectory &);
           ~EventInfo();
            void Fill(const edm::Event&);
            void Init();
            void PileupInfo(const edm::InputTag&);
            void GenEventInfo(const edm::InputTag&);
            void LumiScalersInfo(const edm::InputTag&);
            void ReadPileupInfo(const edm::Event&);
            void ReadGenEventInfo(const edm::Event&);
            void ReadLumiScalers(const edm::Event&);
            void FixedGridRhoInfo(const edm::InputTag&);
            void ReadFixedGridRhoInfo(const edm::Event&);
            void PrefiringWeightInfo(const edm::InputTag &, const edm::InputTag &, const edm::InputTag & );
            void ReadPrefiringWeight(const edm::Event&);
            TTree * Tree();
      
         private:
            // ----------member data ---------------------------
            
            // event information
            int event_;
            int run_;
            int lumi_;
            int bx_;
            int orbit_;
            
            // Output tree
            TTree * tree_;
            
            // PileupInfo
            edm::InputTag puInfo_;
            bool do_pu_;
            int n_pu_;
            float n_true_pu_;
            
            // GenEventInfo
            edm::InputTag genInfo_;
            bool do_gen_;
            double genWeight_;
            double genScale_;
            int    pdfid1_;
            int    pdfid2_;
            double pdfx1_;
            double pdfx2_;
            
            // Lumi scalers
            bool  do_lumi_;
            edm::InputTag lumiScalers_;
            float instLumi_;
            float lumiPU_;
            
            // FixedGridRho
            bool do_rho_;
            edm::InputTag rho_collection_;
            double rho_;

            // L1 prefiring weight
            bool do_prefw_;
            edm::InputTag prefweight_collection_;
            edm::InputTag prefweight_up_collection_;
            edm::InputTag prefweight_down_collection_;
            double prefw_;
            double prefw_up_;
            double prefw_down_;

      };
   }
}

#endif  // Analysis_Ntuplizer_EventInfo_h
