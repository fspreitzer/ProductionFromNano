#!/usr/bin/env python

import os

from ROOT import gSystem, TChain, TSystem, TFile
from PSet import process

#doSvFit = True
doSvFit = False
if doSvFit :
    print "Run with SVFit computation"

#Some system have problem runnig compilation (missing glibc-static library?).
#First we try to compile, and only ther we start time consuming cmssw
status = gSystem.CompileMacro('HTTEvent.cxx')
status *= gSystem.CompileMacro('NanoEventsSkeleton.C')
gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libTauAnalysisClassicSVfit.so')
gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libTauAnalysisSVfitTF.so')
gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHTT-utilitiesRecoilCorrections.so')
status *= gSystem.CompileMacro('HTauTauTreeFromNanoBase.C')
status *= gSystem.CompileMacro('HMuTauhTreeFromNano.C')
status *= gSystem.CompileMacro('HTauhTauhTreeFromNano.C')

print "Compilation status: ",status
if status==0:
    exit(-1)

#Produce framework report required by CRAB
command = "cmsRun -j FrameworkJobReport.xml -p PSet.py"
os.system(command)
from ROOT import HMuTauhTreeFromNano, HTauhTauhTreeFromNano
fileNames = ["test80X_NANO_1.root",
             "test80X_NANO_2.root",
             "test80X_NANO_3.root",
             "test80X_NANO_4.root",
             "test80X_NANO_5.root",
             "test80X_NANO_6.root"
             ]
for name in fileNames:
    aFile = "file:///home/mbluj/work/data/NanoAOD/80X_with941/VBFHToTauTau_M-125_80X/v3/"+name
    print "Adding file: ",aFile
    print "Making the MuTau tree"
    aROOTFile = TFile.Open(aFile)
    aTree = aROOTFile.Get("Events")
    print "TTree entries: ",aTree.GetEntries()
    HMuTauhTreeFromNano(aTree,doSvFit).Loop()
    print "Making the TauTau tree"
    aROOTFile = TFile.Open(aFile)
    aTree = aROOTFile.Get("Events")
    HTauhTauhTreeFromNano(aTree,doSvFit).Loop()    

exit(0)