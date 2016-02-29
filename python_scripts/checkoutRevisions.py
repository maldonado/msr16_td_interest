import csv
import os.path
import subprocess
import sys

# setting
home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'
und_bin_dir = '/Applications/scitools/bin/macosx'
debt_file = home_dir + '/datasets/CSV/technical_debt_summary.csv'
#debt_file = home_dir + '/datasets/CSV/technical_debt_summary_test.csv'
und_out_dir = home_dir + '/und'
perl  = '/Users/kamei/Research/src/metrics/runUND.pl'

# line numbers
_project = 0
_file_name = 3
_class_name = 5
_type = 13
_version_name = 1
#_version_introduced_name = 20
#_version_removed_name = 23
#_last_version_that_comment_was_found_name = 25
_version_introduced_name = 28
_version_removed_name = 31
_last_version_that_comment_was_found_name = 26

_function_signature = 15

idxs = [_version_introduced_name, _version_removed_name, _last_version_that_comment_was_found_name]

count = 0

# Run runUND.pl if there is *.und file
with open(debt_file) as csvfile:
    f = csv.reader(csvfile)
    
    for line in f:          
        count = count + 1
        
        if count > 2000:
            break
        
        if line[_project] == 'project_name':
            continue
        
        if line[_type] != 'METHOD':
            continue
        
        tags_dir=''
        git_dir=''
        if line[_project] == 'apache-ant':
            git_dir  = home_dir + "/repos/ant"
            tags_dir = home_dir + '/revs/ant'
        elif line[_project] == 'jruby':
            git_dir  = home_dir + "/repos/jruby"
            tags_dir = home_dir + '/revs/jruby'
        elif line[_project] == 'apache-jmeter':
            git_dir  = home_dir + "/repos/jmeter"
            tags_dir = home_dir + '/revs/jmeter'
        else:
            continue
        
        for idx in idxs:        
            if line[idx] == '' or line[idx] == 'not_removed':
                if line[_project] == 'apache-ant':
                    line[idx] = 'ANT_193'
                elif line[_project] == 'jruby':
                    line[idx] = '9.0.1.0'
                elif line[_project] == 'apache-jmeter':
                    line[idx] = 'v2_13_RC2'
                else:
                    continue
            
            tags_dir_per_project = tags_dir + '/' + line[idx]
                                
            if not os.path.exists(tags_dir_per_project):
                os.chdir(git_dir)
                
                try:
                    cmd = 'git co ' + line[idx] + " -b " + line[idx]
                    print str(count) + ':' + cmd
                    res = subprocess.check_call(cmd, shell=True)
                except subprocess.CalledProcessError:
                    cmd = 'git co ' + line[idx]
                    print str(count) + ':' + cmd
                    res = subprocess.check_call(cmd, shell=True)
                
                cmd = 'mkdir ' + tags_dir_per_project
                print str(count) + ':' + cmd
                res = subprocess.check_call(cmd, shell=True)
                
                try:
                    cmd = 'cp -r ' + git_dir + " " + tags_dir_per_project + "/src"
                    print str(count) + ':' + cmd
                    res = subprocess.check_call(cmd, shell=True)
                except subprocess.CalledProcessError:
                    print sys.exc_info()[0]
                
                
                os.chdir(tags_dir_per_project + "/src")
                cmd = 'rm -rf .[^.] .??*'
                print str(count) + ':' + cmd
                res = subprocess.check_call(cmd, shell=True)
                