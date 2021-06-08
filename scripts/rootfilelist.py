#!/usr/bin/env python
import os
import sys
import ast
import subprocess

def crab_status(cdir):
   status = subprocess.Popen(['crab','status','-d',cdir],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   stdout,stderr = status.communicate()
   stdout = stdout.split('\n')
   finished = ''
   for line in stdout:
      if not finished and 'Jobs status:                    finished' in line:
         finished = [ x for x in line.split(' ') if '%' in x ][0]
   finished = finished.replace('\t','')
   return finished
   
def crab_report(report, finished, dataset=None, outdir=None):
   if not outdir:
      return
   if not os.path.exists(outdir):
      os.makedirs(outdir)
   outfile = outdir+'/README.md'
   with open(outfile,'w') as f:
      f.write('## Dataset \n')
      if dataset:
         f.write(dataset+'\n')
      else:
         f.write('No dataset found\n')
      f.write('## Status \n')
      if finished == "100.0%":
         f.write(finished+' of the jobs finished\n')
      else:
         f.write(':warning: NOT ALL JOBS FINISHED!!!<br>')
         f.write('Only '+finished+' of the jobs finished<br>')
         f.write('Crab report, results and rootFileList are incomplete!<br>')
         f.write('Try again later!<br>\n')
      
      f.write('## CRAB Report \n')
      f.write('```\n')
      f.write(report)
      f.write('```\n')
      f.write('<br>')
      f.write('See also the [results](results) directory above<br>\n')

def crab_log(cdir):
   status = subprocess.Popen(['crab','report','-d',cdir],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   stdout,stderr = status.communicate()
   report = stdout
   crablog = cdir+'/crab.log'
   myline = ''
   mytype = ''
   myntpdir = ''
   mypd= ''
   myreq = ''
   myfullpd = ''
   finished = ''
   with open(crablog,'r') as f:
      for line in f:
         line = line.rstrip()
         if 'Result: ' in line and 'runsAndLumis' in line and 'ntuple_' in line:
            myline = line
         if not mytype and 'type              :' in line:
            mytype = line.split(':')[1].replace(' ','')
         if not myntpdir and 'triggerInfo       :' in line:
            myntpdir = line.split(':')[1].replace(' ','').replace('trigger_info.yml','')+mytype
            myinfodir = myntpdir+'/additional_info'
            if not os.path.exists(myinfodir):
               os.makedirs(myinfodir)
         if not myreq and 'config.General.requestName' in line:
            myreq = line.split("'")[1]
         if mytype == 'mc':
            if not mypd and 'config.Data.inputDataset' in line:
               mypd = line.split("'")[1]
               mypd = mypd.split('/')[1][0:mypd.find('_Tune')-1]
         else:
            mypd = myreq.split('-')[0]
         if not myfullpd and 'config.Data.inputDataset' in line:
            myfullpd = line.split("'")[1]
         if 'Jobs status:                    finished' in line:
            finished = [ x for x in line.split(' ') if '%' in x ][0]
            finished = finished.replace('\t','')
   
   outreport = myinfodir+'/'+myreq
   crab_report(report,finished,outdir=outreport,dataset=myfullpd)
   
   if not myline:
      sys.exit()
            
   results = ast.literal_eval(myline.split('Result: ')[1])
   randl = results['result'][0]['runsAndLumis']
   
   fileslist = []
   for key,value in randl.iteritems():
      if key.startswith('0-'):
         continue
      filename = value[0]['lfn']
      if 'ntuple_'  in filename:
         fileslist.append(filename.encode("ascii"))
   
   fileslist.sort()
   
   rootfiles = myntpdir+'/'+mypd+'_rootFileList.txt'
   with open(rootfiles,'w') as f:
      for fl in fileslist:
         f.write('root://dcache-cms-xrootd.desy.de/'fl+'\n')
   print
   print('See the rootFileList at:')
   print(rootfiles)

   cmd = 'cp -pRd '+cdir+'/results ' + outreport
   os.system(cmd)
   print
   print('See crab report and results at: ')
   print(outreport)

   jobs_finished = finished+' of the jobs finished'
   print
   if finished != "100.0%":
      jobs_finished = 'Only '+jobs_finished
      print(jobs_finished)
      print
      print('*** WARNING ***  NOT ALL JOBS FINISHED!!!')
      print('                 CRAB report and rootFileList are incomplete!')
      print('                 Try again later!')
      print
   else:
      # when 100% is finished crab does not update this file to empty
      with open(outreport+'/results/notFinishedLumis.json', 'w') as f:
         f.write('{}')
      print(jobs_finished)
      
#    cmd = 'cp -p '+crablog+' '+outreport
#    os.system(cmd)
#    cmd = 'gzip '+outreport+'/crab.log'
#    os.system(cmd)

def main():
   if len(sys.argv) < 2:
      print('Provide the directory with crab.log file')
      sys.exit()
   
   crabdir = sys.argv[1]
   crab_log(crabdir)
   
         

if __name__ == '__main__':
   main()
