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
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "SimDataFormats/GeneratorProducts/interface/GenFilterInfo.h"

#include "Analysis/Ntuplizer/interface/EventCountSummary.h"

//
// class declaration
//

using namespace analysis;
using namespace analysis::ntuple;

// member functions specialization - needed to be declared in the same namespace as the class
namespace analysis {
   namespace ntuple {
      template <> void EventCountSummary<edm::MergeableCounter>::IncrementEventCount(edm::LuminosityBlock const&);
      template <> void EventCountSummary<edm::MergeableCounter>::Fill();
 }
}   

//
// constructors and destructor
//
template <typename T>
EventCountSummary<T>::EventCountSummary() {
   // default constructor
}

template <typename T>
EventCountSummary<T>::EventCountSummary(edm::Service<TFileService> & fs, const std::vector<edm::InputTag> & collections) :
      total_(0), passed_(0), collections_(collections) {

   std::string category = "GeneratorFilter";
   if ( std::is_same<T,edm::MergeableCounter>::value )
      category = "EventCountSummary";
   
   tree_ = fs->make<TTree>(category.c_str(),category.c_str());
   
   tree_ -> Branch("nEventsTotal"    , &this->total_     , "nEventsTotal/i");
   tree_ -> Branch("nEventsFiltered" , &this->passed_     , "nEventsFiltered/i");
   tree_ -> Branch("filterEfficiency", &this->efficiency_ , "filterEfficiency/D");

   if ( category == "GeneratorFilter" ) {
      tree_ -> Branch("nEventsTried"     , &this->tried_      , "nEventsTried/i");
      tree_ -> Branch("weightsTotal"     , &this->total_weights_      , "weightsTotal/D");
      tree_ -> Branch("weightsFiltered"  , &this->passed_weights_      , "weightsTotal/D");
      tree_ -> Branch("weightsEfficiency", &this->efficiency_weights_ , "weightsEfficiency/D");
   }
   
}

template <typename T>
EventCountSummary<T>::EventCountSummary(TFileDirectory & subDir, const std::vector<edm::InputTag> & collections) :
      total_(0), passed_(0), collections_(collections) {

   std::string category = "GeneratorFilter";
   if ( std::is_same<T,edm::MergeableCounter>::value )
      category = "EventCountSummary";

   tree_ = subDir.make<TTree>(category.c_str(),category.c_str());
   
   tree_ -> Branch("nEventsTotal"    , &this->total_     , "nEventsTotal/i");
   tree_ -> Branch("nEventsFiltered" , &this->passed_     , "nEventsFiltered/i");
   tree_ -> Branch("filterEfficiency", &this->efficiency_ , "filterEfficiency/D");

   if ( category == "GeneratorFilter" ) {
      tree_ -> Branch("nEventsTried"     , &this->tried_      , "nEventsTried/i");
      tree_ -> Branch("weightsTotal"     , &this->total_weights_      , "weightsTotal/D");
      tree_ -> Branch("weightsFiltered"  , &this->passed_weights_      , "weightsTotal/D");
      tree_ -> Branch("weightsEfficiency", &this->efficiency_weights_ , "weightsEfficiency/D");
   }
}

template <typename T>
EventCountSummary<T>::~EventCountSummary() {
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}

// ------------ other methods ----------------
template <typename T>
TTree * EventCountSummary<T>::Tree() {
   return tree_;
}

// ------------ method called once each job just before starting event loop  ------------
template <typename T>
void EventCountSummary<T>::Collections(const std::vector<edm::InputTag> & collections) {
   collections_ = collections;
}
template <typename T>
const std::vector<edm::InputTag> & EventCountSummary<T>::Collections() {
   return collections_;
}

// ------------ method called at the end of the EDAnalyzer job  ------------
template <typename T>
void EventCountSummary<T>::Fill() {
   efficiency_ = this -> Counts<unsigned int>().efficiency;
   tree_ -> Fill();
}

template <>
void EventCountSummary<edm::MergeableCounter>::Fill() {
   efficiency_  = this -> Counts<unsigned int>().efficiency;
   efficiency_weights_ = this -> Counts<double>().efficiency;
   tree_ -> Fill();
}


//
// member functions

template<typename T>
template<typename CountType>
EventCounts<CountType> EventCountSummary<T>::Counts() const {
   if constexpr (std::is_same_v<CountType, unsigned int>) {
      return make_counts_(total_, passed_);
   }
   else if constexpr (std::is_same_v<CountType, double>) {
      return make_counts_(total_weights_, passed_weights_);
   }
}

template<typename T>
template<typename CountType>
EventCounts<CountType> EventCountSummary<T>::make_counts_(CountType total, CountType passed) {
   EventCounts<CountType> res;
   res.total = total;
   res.passed = passed;
   res.efficiency = total > CountType{0}
                  ? static_cast<double>(passed) / static_cast<double>(total)
                  : 0.0;

   return res;
}

// ------------ method called for each lumi  ------------
template <typename T>
void EventCountSummary<T>::IncrementEventCount(edm::LuminosityBlock const& lumi) {
   
   if ( collections_.size() > 0 ) {
      edm::Handle<T> handler;
      lumi.getByLabel(collections_[0], handler);
       
      total_  += handler->numEventsTotal();
      passed_  += handler->numEventsPassed();
      tried_  += handler->numEventsTried();
      
      total_weights_  += handler->sumWeights();
      passed_weights_  += handler->sumPassWeights();
   }   
}

template <>
void EventCountSummary<edm::MergeableCounter>::IncrementEventCount(edm::LuminosityBlock const& lumi) {
   
   if ( collections_.size() > 1 ) {
      edm::Handle <edm::MergeableCounter> totalHandler;
      lumi.getByLabel(collections_[0],totalHandler);
      total_ += totalHandler -> value;
      
      edm::Handle <edm::MergeableCounter> filtrHandler;
      lumi.getByLabel(collections_[1],filtrHandler);
      passed_ += filtrHandler -> value;

   }
   
}

// Need to declare all possible template classes here
template class EventCountSummary<edm::MergeableCounter>;
template class EventCountSummary<GenFilterInfo>;
