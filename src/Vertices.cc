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
// 
// user include files
#include "DataFormats/Provenance/interface/Provenance.h"
#include "FWCore/Framework/interface/Event.h" 
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "CommonTools/Utils/interface/PtComparator.h"
#include "Analysis/Ntuplizer/interface/Vertices.h"
#include "TTree.h"
#include "Analysis/Utils/interface/color_printf.h"

//
// class declaration
//

using namespace analysis;
using namespace analysis::ntuple;

//
// constructors and destructor
//
Vertices::Vertices() {
   // default constructor
}

Vertices::Vertices(const edm::InputTag& collection, TTree* tree) : input_collection_(collection), tree_(tree), n_(0) {
   // Main constructor
   if (!tree_) {
      throw cms::Exception("Configuration") << "==> Vertices::Vertices() received a null TTree pointer \n";
   }

   tree_->Branch("n",      &this->n_,    "n/I");
   tree_->Branch("x",       this->x_,    "x[n]/F");
   tree_->Branch("y",       this->y_,    "y[n]/F");
   tree_->Branch("z",       this->z_,    "z[n]/F");
   tree_->Branch("x_error", this->xe_,   "x_error[n]/F");
   tree_->Branch("y_error", this->ye_,   "y_error[n]/F");
   tree_->Branch("z_error", this->ze_,   "z_error[n]/F");
   tree_->Branch("rho",     this->rho_,  "rho[n]/F");
   tree_->Branch("chi2",    this->chi2_, "chi2[n]/F");
   tree_->Branch("ndof",    this->ndof_, "ndof[n]/F");
   tree_->Branch("fake",    this->fake_, "fake[n]/O");
      
}

Vertices::~Vertices() {
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void Vertices::ReadFromEvent(const edm::Event& event) {

   edm::Handle<reco::VertexCollection> handler;
   event.getByLabel(this->input_collection_, handler);
   vertex_candidates_ = *(handler.product());
   
   int n = 0;
   for (const auto& vertex : vertex_candidates_) {
      if (n == max_vertices_) {
         const edm::EventAuxiliary event_aux = event.eventAuxiliary();
         auto run = event_aux.run();
         auto lumi = event_aux.luminosityBlock();
         auto event_number = event_aux.event();
         printf_warning("==> Vertices::ReadFromEvent(): n vertices > max_vertices! (Run=%d, Lumisection=%d, Event=%d) \n",run,lumi,event_number);
         break;
      }
      x_[n]    = vertex.x();
      y_[n]    = vertex.y();
      z_[n]    = vertex.z();
      xe_[n]   = vertex.xError();
      ye_[n]   = vertex.yError();
      ze_[n]   = vertex.zError();
      fake_[n] = vertex.isFake();
      ndof_[n] = vertex.ndof();
      chi2_[n] = vertex.chi2();
      rho_[n]  = vertex.position().Rho();
      ++n;
   }
   n_ = n;
}

void Vertices::Fill(const edm::Event& event) {
   this->ReadFromEvent(event);
   tree_->Fill();
}

// ------------ method called once each job just before starting event loop  ------------
