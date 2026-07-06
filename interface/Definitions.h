#ifndef Analysis_Ntuplizer_Definitions_h
#define Analysis_Ntuplizer_Definitions_h 1

// -*- C++ -*-
//
// Package:    Analysis/Ntuplizer
// Class:      Definitions
// 
/**\class Definitions Definitions.cc Analysis/Ntuplizer/src/Definitions.cc

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
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"

//
// class declaration
//

namespace analysis {
   namespace ntuple {

      class Definitions {
         public:
            Definitions();
            Definitions(TFileDirectory &);
            Definitions(TFileDirectory &, const std::string &);
           ~Definitions();
            void Init();
            void Fill();
            void Add(const std::vector<std::string> &, const std::vector<std::string> &);
      
         private:
            // ----------member data ---------------------------
            std::vector<std::string> names_;
            std::vector<std::string> aliases_;
            std::string category_;
            // Output tree
            TTree * tree_;
            
      };
   }
}

#endif  // Analysis_Ntuplizer_Definitions_h
