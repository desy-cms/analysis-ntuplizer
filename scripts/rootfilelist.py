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
   jobs_finished = finished+' of the jobs finished'
   if finished != '100.0%':
      jobs_finished = 'Only '+jobs_finished
   print
   print(jobs_finished)
   return finished
   
def crab_report(cdir, outdir=None):
   status = subprocess.Popen(['crab','report','-d',cdir],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   stdout,stderr = status.communicate()
   if not outdir:
      return
   if not os.path.exists(outdir):
      os.makedirs(outdir)
   outfile = outdir+'/report.txt'
   with open(outfile,'w') as f:
      f.write(stdout)
   cmd = 'cp -pRd '+cdir+'/results ' + outdir
   os.system(cmd)
   print
   print('See crab report at: ')
   print(outdir)

def crab_log(cdir):
   crab_report(cdir)
   crablog = cdir+'/crab.log'
   myline = ''
   mytype = ''
   myntpdir = ''
   mypd= ''
   myreq = ''
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
   
   outreport = myinfodir+'/'+myreq
   crab_report(cdir,outreport)
   
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
         f.write(fl+'\n')
   print
   print('See the rootFileList at:')
   print(rootfiles)


def main():
   if len(sys.argv) < 2:
      print('Provide the directory with crab.log file')
      sys.exit()
   
   crabdir = sys.argv[1]
   finished = crab_status(crabdir)
   crab_log(crabdir)
   
   if finished != "100%":
      print
      print('*** WARNING ***  NOT ALL JOBS FINISHED!!!')
      print('                 CRAB report and rootFileList are incomplete!')
      print('                 Try again later!')
      print
      
      
         

if __name__ == '__main__':
   main()
