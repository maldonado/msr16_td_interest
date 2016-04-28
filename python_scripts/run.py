import setting as s
import checkoutRevisions
import runUND
import extract_metrics_at_method_level
import git_comments

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
    
    fo_comment_file = open(s.comment_file,"w")  # for git_comments
    csvWriter_comment_file = csv.writer(fo_comment_file) #for git_comments
    csvWriter_comment_file.writerow(["Type", "Debt","Introduce Date", "Introduce Author", "Introduce Comment", "Remove Date", "Remove Author", "Remove Comment", "Introduce ID", "Remove ID"])
    
    #################################################################
    #for checkoutRevisions
    #################################################################
    for line in reader:
        if count > s.MAX_LOOP:
            break
        
        print line
        count = count + 1
        project =  line[u'project']
        versions = [] #for git_comments
                
        for idx in idxs:
            version = line[idx]
            if idx != "last_found_commit_hash":  #for git_comments
                versions.append(version)
            
            if idx == "removed_version_commit_hash" and line[u'has_removed_version'] == "f":
                version = get_latest_version(project)

            checkoutRevisions.checkoutRevision(project, version, count, reuse=False)
            runUND.runUND(project, version, count, reuse=True)
            extract_metrics_at_method_level.extract_metrics(project, version, count, reuse=True)
        
        #for git_comments
        debt = git_comments.git_comments(project, versions, count)
        debt.type = line[u'td_classification']
        debt.debt = line[u'comment_text']
        csvWriter_comment_file.writerow(debt.out())
    fo_comment_file.close()        
    
    #################################################################
    #for template
    #################################################################
    if False:    
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