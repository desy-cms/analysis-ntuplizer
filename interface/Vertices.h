#ifndef Analysis_Ntuplizer_Vertices_h
#define Analysis_Ntuplizer_Vertices_h 1

// -*- C++ -*-
//
// Package:    Analysis/Ntuplizer
// Class:      Vertices
// 
/**\class Vertices Vertices.cc Analysis/Ntuplizer/src/Vertices.cc

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
// 
#include "FWCore/ParameterSet/interface/ParameterSet.h"
 
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "TTree.h"

//
// class declaration
//

namespace analysis {
   namespace ntuple {

      class Vertices {
         public:
            Vertices();
            Vertices(const edm::InputTag&, TTree*);
           ~Vertices();
            void ReadFromEvent(const edm::Event&);
            void Fill(const edm::Event&);
      
         private:
            // ----------member data ---------------------------
            static const int max_vertices_ = 200;
            reco::VertexCollection vertex_candidates_;
            edm::InputTag input_collection_;
            TTree * tree_;
            
            // particles kinematics for the ntuple
            int   n_;
            float x_[max_vertices_]{};
            float y_[max_vertices_]{};
            float z_[max_vertices_]{};
            float xe_[max_vertices_]{};
            float ye_[max_vertices_]{};
            float ze_[max_vertices_]{};
            bool  fake_[max_vertices_]{};
            float chi2_[max_vertices_]{};
            float ndof_[max_vertices_]{};
            float rho_[max_vertices_]{};
            
         private:
      };
   
   }
}

#endif  // Analysis_Ntuplizer_Vertices_h
