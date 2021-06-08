
### For 2017, 94X, ntuple v4

cmsrel CMSSW_9_4_12
cd CMSSW_9_4_12/src
cmsenv

git cms-init

git cms-merge-topic cms-nanoAOD:master-94X
git checkout -b nanoAOD cms-nanoAOD/master-94X
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

git cms-addpkg RecoBTag/TensorFlow
git cherry-pick 94ceae257f846998c357fcad408986cc8a039152

git clone git@github.com:robervalwalsh/analysis-ntuplizer.git Analysis/Ntuplizer

