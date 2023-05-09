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
#include <iostream>
#include <boost/algorithm/string.hpp>

// 
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
//#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
 
#include "Analysis/Ntuplizer/interface/TriggerAccepts.h"

//
// class declaration
//

using namespace analysis;
using namespace analysis::ntuple;

//
// constructors and destructor
//
TriggerAccepts::TriggerAccepts()
{
   // default constructor
}

TriggerAccepts::TriggerAccepts(const edm::InputTag& tag, TTree* tree, const std::vector<std::string>& paths, const std::vector<std::string>& seeds, const std::shared_ptr<HLTPrescaleProvider> hltPrescale)
{
   hlt_prescale_ = hltPrescale;
   input_collection_ = tag;
   tree_ = tree;
   paths_.clear();
   seeds_.clear();
   paths_ = paths;
   seeds_ = seeds;
   
   // remove duplicates of paths
   sort( paths_.begin(), paths_.end() );
   paths_.erase( unique( paths_.begin(), paths_.end() ), paths_.end() );
   // remove duplicates of seeds
   sort( seeds_.begin(), seeds_.end() );
   seeds_.erase( unique( seeds_.begin(), seeds_.end() ), seeds_.end() );
   
   first_ = true;
   psinfo_ = true;
}

TriggerAccepts::TriggerAccepts(const edm::InputTag& tag, TTree* tree, const std::vector<std::string>& paths, const std::vector<std::string>& seeds)
{
   input_collection_ = tag;
   tree_ = tree;
   paths_.clear();
   seeds_.clear();
   paths_ = paths;
   seeds_ = seeds;
   
   // remove duplicates of paths
   sort( paths_.begin(), paths_.end() );
   paths_.erase( unique( paths_.begin(), paths_.end() ), paths_.end() );
   // remove duplicates of seeds
   sort( seeds_.begin(), seeds_.end() );
   seeds_.erase( unique( seeds_.begin(), seeds_.end() ), seeds_.end() );
   
   first_ = true;
   psinfo_ = true;
}

TriggerAccepts::~TriggerAccepts()
{
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void TriggerAccepts::Fill(const edm::Event& event, const edm::EventSetup & setup)
{
   using namespace edm;
   
   // reset trigger accepts and prescales to default -1
   for (size_t i = 0; i < paths_.size() ; ++i )
   {
      accept_[i] = false;
      pshlt_[i] = -1;
   }
   std::map<std::string, bool> l1done; // L1 prescale only once per event
   for (size_t i = 0; i < seeds_.size() ; ++i )
   {
      psl1_[i] = -1;
      l1accept_[i] = false;
      l1done[seeds_[i]] = false;
   }

   Handle<TriggerResults> handler;
   event.getByLabel(input_collection_, handler);
   const TriggerResults & triggers = *(handler.product());
      
   // l1 accept
   for ( size_t j = 0 ; j < hlt_config_->size() ; ++j )
   {
      for (size_t i = 0; i < paths_.size() ; ++i )
      {
         if ( hlt_config_->triggerName(j).find(paths_[i]) == 0 )
         {
            // trigger accepted?
            accept_[i] = triggers.accept(j);
            
            // get prescale info if requested
            if ( psinfo_ )
            {
               // // const std::pair<std::vector<std::pair<std::string,int> >,int> ps = hlt_prescale_->prescaleValuesInDetail(event,setup,hlt_config_->triggerName(j));
               // auto ps = hlt_prescale_->prescaleValuesInDetail(event,setup,hlt_config_->triggerName(j));
               // // HLT prescale
               // pshlt_[i] = ps.second;
               // // Get L1 prescale of all seeds of the path
               // for ( size_t k = 0; k < ps.first.size(); ++k ) // loop over seeds of the path
               // {
               //    for ( size_t l = 0; l < seeds_.size(); ++l ) // loop over seeds passed by python config
               //    {
               //       if ( ! l1done[seeds_[l]] && ps.first[k].first == seeds_[l] )  // if prescale of L1 seed not read and seed is in path
               //       {
               //          psl1_[l] = ps.first[k].second;
               //          l1done[seeds_[l]] = true;
               //          hlt_prescale_->l1tGlobalUtil().getFinalDecisionByName (seeds_[l], l1accept_[l]);
               //          break;
               //       }
               //    }
               // }
            }
            else
            {
               std::vector<std::string> l1seeds = hlt_config_->hltL1TSeeds(hlt_config_->triggerName(j));
               for ( size_t l = 0; l < seeds_.size(); ++l ) // loop over seeds passed by python config
               {
                  for ( auto & l1 : l1seeds )
                  {
                     if ( l1.find(seeds_[l]) == 0 && ! l1done[seeds_[l]] )
                     {
//                        hlt_prescale_->l1tGlobalUtil().getFinalDecisionByName (seeds_[l], l1accept_[l]);
                        l1done[seeds_[l]] = true;
                        break;
                     }
                  }
               }
            }
         }
      }
   }
   
   tree_ -> Fill();
   
}

// ------------ method called once each job just before starting event loop  ------------
void TriggerAccepts::Branches()
{
   // two loops for separation of accepts and prescales(?)
   for (size_t i = 0; i < paths_.size() ; ++i )
   {
      tree_->Branch(paths_[i].c_str(), &accept_[i], (paths_[i]+"/O").c_str());
   }
   for (size_t i = 0; i < seeds_.size() ; ++i )
   {
      tree_->Branch(seeds_[i].c_str(), &l1accept_[i], (seeds_[i]+"/O").c_str());
   }
   for (size_t i = 0; i < paths_.size() ; ++i )
   {
      tree_->Branch(("ps_"+paths_[i]).c_str(), &pshlt_[i], ("ps_"+paths_[i]+"/I").c_str());
   }
   for (size_t i = 0; i < seeds_.size() ; ++i )
   {
      tree_->Branch(("ps_"+seeds_[i]).c_str(), &psl1_[i], ("ps_"+seeds_[i]+"/I").c_str());
   }
   // std::cout << "TriggerAccepts Branches ok" << std::endl;
}

void TriggerAccepts::Run(edm::Run const & run, edm::EventSetup const& setup)
{
//   bool changed;
//   hlt_prescale_->init(run, setup, input_collection_.process(), changed);
//   hlt_config_ = hlt_prescale_->hltConfigProvider();
   
}
void TriggerAccepts::ReadPrescaleInfo(const bool & ok)
{
   psinfo_ = ok;
}
bool TriggerAccepts::ReadPrescaleInfo()
{
   return psinfo_;
}

void TriggerAccepts::Init()
{
   Branches();
}

void TriggerAccepts::Providers(const std::shared_ptr<HLTPrescaleProvider> & hltpsprov, const std::shared_ptr<HLTConfigProvider> &hltcfgprov)
{
   hlt_config_ = hltcfgprov;
   hlt_prescale_ = hltpsprov;
}
