import setting as s
import checkoutRevisions
import runUND

import csv
import os.path
import subprocess
import sys

idxs = ["introduced_version_commit_hash", "removed_version_commit_hash", "last_found_commit_hash"]

def get_latest_version(project):
    if project == 'ant':
        return 'ANT_193'
    elif project == 'jruby':
        return '9.0.1.0'
    elif project == 'jmeter':
        return 'v2_13_RC2'
    else:
        raise ValueError(project + "is not defined in this function") 
    
count = 0   
with open(s.debt_file) as csvfile:
    csvfile = open(s.debt_file)
    reader = csv.DictReader(csvfile)
    
    #################################################################
    #for checkoutRevisions
    #################################################################
    for line in reader:
        if count > s.MAX_LOOP:
            break
        
        print line
        count = count + 1
        
        project =  line[u'project']
                
        for idx in idxs:
            version = line[idx]
            if idx == "removed_version_commit_hash" and line[u'has_removed_version'] == "f":
                version = get_latest_version(project)

            checkoutRevisions.checkoutRevision(project, version, count)
            runUND.runUND(project, version, count)
            
    #################################################################
    #for runUND
    #################################################################    
    print ""
    csvfile.seek(0, 0)
    next(reader)
        
    count = 0    
    for line in reader:
        if count > s.MAX_LOOP:
            break

        print line
        count = count + 1
                
        tags_dir=''
        git_dir=''
        
    #################################################################
    #for xxx
    #################################################################    
    print ""
    csvfile.seek(0, 0)
    next(reader)
        
    count = 0    
    for line in reader:
        if count > s.MAX_LOOP:
            break

        print line
        count = count + 1
                
        tags_dir=''
        git_dir=''