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
#include <optional>
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
            void PrefiringWeightInfo(const edm::InputTag & nominal, std::optional<edm::InputTag> up = std::nullopt, std::optional<edm::InputTag> down = std::nullopt );
            void ReadPrefiringWeight(const edm::Event&);
            void MetFilters(const edm::InputTag&);
            void ReadMetFilters(const edm::Event&);
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
            edm::InputTag pileup_info_;
            bool do_pu_;
            int n_pu_;
            float n_true_pu_;
            
            // GenEventInfo
            edm::InputTag gen_event_info_;
            bool do_gen_event_info_;
            double gen_weight_;
            double gen_scale_;
            int    pdf_id1_;
            int    pdf_id2_;
            double pdf_x1_;
            double pdf_x2_;
            
            // Lumi scalers
            bool  do_lumi_scalers_;
            edm::InputTag lumi_scalers_;
            float inst_lumi_;
            float lumi_pu_;
            
            // FixedGridRho
            bool do_rho_;
            edm::InputTag rho_collection_;
            double rho_;

            // L1 prefiring weight
            bool do_prefiring_weight_;
            edm::InputTag prefiring_weight_collection_;
            std::optional<edm::InputTag> prefiring_weight_up_collection_;
            std::optional<edm::InputTag> prefiring_weight_down_collection_;
            
            double prefiring_weight_;
            double prefiring_weight_up_;
            double prefiring_weight_down_;

            // MET filters
            bool do_met_filters_;
            edm::InputTag met_filters_results_;
            bool flag_goodVertices_;
            bool flag_globalSuperTightHalo2016Filter_;
            bool flag_EcalDeadCellTriggerPrimitiveFilter_;
            bool flag_BadPFMuonFilter_;
            bool flag_BadPFMuonDzFilter_;
            bool flag_hfNoisyHitsFilter_;
            bool flag_eeBadScFilter_;
            bool flag_ecalBadCalibFilter_;
      };
   }
}

#endif  // Analysis_Ntuplizer_EventInfo_h
