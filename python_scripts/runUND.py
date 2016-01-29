import csv
import os.path
import subprocess

# setting
home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'
und_bin_dir = '/Applications/scitools/bin/macosx'
debt_file = home_dir + '/datasets/CSV/technical_debt_summary.csv'
und_out_dir = home_dir + '/und'
perl  = '/Users/kamei/Research/src/metrics/runUND.pl'

# line numbers
_project = 0
_file_name = 3
_class_name = 5
_type = 13
_version_introduced_name = 20
_version_removed_name = 23
_last_version_that_comment_was_found_name = 25
_function_signature = 15

count = 0

# Run runUND.pl if there is *.und file
with open(debt_file) as csvfile:
    f = csv.reader(csvfile)
    
    for line in f:          
        count = count + 1
        
        if count > 5:
            break
        
        if line[_project] == 'project_name':
            continue
        
        if line[_type] != 'METHOD':
            continue
        
        tags_dir=''
        if line[_project] == 'apache-ant':
            tags_dir = '/tags/ant_tags'
        elif line[_project] == 'jruby':
            tags_dir = '/tags/jruby_tags'
        elif line[_project] == 'apache-jmeter':
            tags_dir = '/tags/jmeter_tags'
        else:
            continue
        
        idxs = [_version_introduced_name, _version_removed_name, _last_version_that_comment_was_found_name]
        
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
                    
            tags_dir = line[_project] +  "_tags"
            target_path = "/".join([home_dir, "tags", tags_dir, line[idx], "src"])
            und_file = "/".join([und_out_dir, line[_project], line[idx]])
            und_file_w_ext = und_file + ".und"
                    
            if not os.path.exists(und_file_w_ext):
                # run
                cmd = ' '.join(['perl',perl,und_file,'java','-t',target_path])
                print cmd
                res = subprocess.check_call(cmd, shell=True)
        