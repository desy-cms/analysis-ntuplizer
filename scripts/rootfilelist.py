#!/usr/bin/env python
import os
import sys
import ast
import subprocess
import glob

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

def crab_log(cdir,ntp_name):
   finished_jobs_list = finished_jobs(cdir)
   print("Getting crab report... ")
   status = subprocess.Popen(['crab','report','-d',cdir],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   stdout,stderr = status.communicate()
   print("done!")
   report = stdout
   crablog = cdir+'/crab.log'
   ntplog = cdir+"/ntuple_crab.log"
   myline = ''
   mytype = ''
   myntpdir = ''
   mypd= ''
   myreq = ''
   myfullpd = ''
   finished = ''
   
   # job logs
   jobids = ""
   for j in finished_jobs_list:
      jobids += j+","
   jobids = jobids[:-1]
   print("Getting finished jobs log files... ")
   cmd = "crab getlog -d "+cdir+" --short --jobids="+jobids+" >& /dev/null"
   os.system(cmd)
   print("done!")
   job_log_list = glob.glob(cdir+"/results/job_out.*.*.txt")
   ntuples_list = {}
   for jlog in job_log_list:
      jid = os.path.basename(jlog).split(".")[1]
      crab_dest = subprocess.Popen(['grep','CRAB_Destination','-d',cdir],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      grep_ntuple_path = subprocess.Popen(['grep','CRAB_Destination',jlog ],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      stdout_grep,stderr_grep = grep_ntuple_path.communicate()
      grep_ntp = stdout_grep.split(",")[-1]
      grep_ntp = grep_ntp.replace('"','')
      grep_ntp = grep_ntp.replace(' ','')
      root_pos = grep_ntp.find("ntuple_"+jid+".root")
      if root_pos < 0:  # no root file
         continue
      store_pos = grep_ntp.find("store")
      grep_ntp = grep_ntp[store_pos-1:]
      ntuples_list[jid] = grep_ntp
   if len(ntuples_list) != len(finished_jobs_list):
      print("*** warning ***: the size of the list of ntuples differ from the number of finished jobs")
   
   
   # ntuple_crab.log
   with open(ntplog,"r") as f:
      for line in f:
         line = line.rstrip().replace(' ','')
         if not mytype and 'TYPE=' in line:
            mytype = line.split('=')[1].replace(' ','')
         if not myntpdir and 'NTUPLES_REPO_DIR=' in line:
            myntpdir = line.split('=')[1].replace(' ','')
   myinfodir = myntpdir+'/additional_info'
   if not os.path.exists(myinfodir):
      os.makedirs(myinfodir)
            
   # crab.log         
   with open(crablog,'r') as f:
      for line in f:
         line = line.rstrip()
         if 'Result: ' in line and 'runsAndLumis' in line and ntp_name in line:
            myline = line
         if not myreq and 'config.General.requestName' in line:  # could be in the ntuple_crab.log
            myreq = line.split("'")[1]
         if mytype == 'mc':
            if not mypd and 'config.Data.inputDataset' in line:  # could be in the ntuple_crab.log
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
   
   fileslist = [value.replace("\n","") for key,value in ntuples_list.iteritems()]
#    fileslist = []
#    for key,value in randl.iteritems():
#       if key.startswith('0-'):
#          continue
#       filename = value[0]['lfn']
#       if ntp_name  in filename:
#          fileslist.append(filename.encode("ascii"))
   
   fileslist.sort()
   
   rootfiles = myntpdir+'/'+mypd+'_rootFileList.txt'
   with open(rootfiles,'w') as f:
      for fl in fileslist:
         f.write('root://dcache-cms-xrootd.desy.de/'+fl+'\n')
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

def finished_jobs(cdir):
   print("Getting list of finished jobs... ")
   status = subprocess.Popen(['crab','status','-d',cdir,'--long'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   stdout,stderr = status.communicate()
   stdout = stdout.split('\n')
   # check whether lines are from the job status table
   jobs_table = False
   job_status = {}
   for line in stdout:
      line_split = line.split(' ')
      line_split = [x for x in line_split if x!='']
      # at the end of the status table the line is empty
      if len(line_split)<2:
         if jobs_table:
            jobs_table = False
         continue
      # header of the status table
      if line_split[0] == 'Job' and line_split[1] == 'State':
         jobs_table = True
         continue
      # skip lines outside the status table
      if not jobs_table:
         continue
      # get the job id and its status
      job_status[line_split[0]] = line_split[1]
      
   runs_done = [ job for job, status in job_status.iteritems() if status=="finished"]
   print("done!")
   return runs_done


def main():
   if len(sys.argv) < 2:
      print('Provide the directory with crab.log file')
      sys.exit()
      
   crabdir = sys.argv[1]
   if not os.path.exists(crabdir):
      print(crabdir+" does not exist!")
      sys.exit()
   ntuple_crab_log = crabdir+"/ntuple_crab.log"
   if not os.path.exists(ntuple_crab_log):
      print(ntuple_crab_log+" does not exist!")
      sys.exit()
   
   ntp_name = 'ntuple_'
   if len(sys.argv) == 3:
      ntp_name = os.path.splitext(sys.argv[2])[0]+'_'
      
   crab_log(crabdir,ntp_name)
   
         

if __name__ == '__main__':
   main()
