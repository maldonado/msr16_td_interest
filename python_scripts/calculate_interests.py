import csv
import os.path
import subprocess
    
# setting
home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'
debt_file = home_dir + '/datasets/CSV/technical_debt_summary_test.csv'
# debt_file = home_dir + '/datasets/CSV/technical_debt_summary.csv'
jar_file  = home_dir + '/java-callgraph.jar'

# setting for java-callgraph
root_path = "/Users/kamei/Research/techdebt/msr16_td_interest/tags/ant_tags/7.ANT_13_B1/src/";
jar_list_path = "/Users/kamei/Research/techdebt/jar.txt";
java_list_path = "/Users/kamei/Research/techdebt/list.txt";
output_path  = "/Users/kamei/Downloads/out/outout.txt";

# line numbers
_project = 0
_file_name = 3
_version_introduced_name = 20
_function_signature = 15

# Run java-callgraph if there is no method invocation file
with open(debt_file) as csvfile:
    f = csv.reader(csvfile)

    for line in f:
        if line[_project] == 'project_name':
            continue
        
        # print line[_project] + "," + line[_file_name] + "," +  line[_version_introduced_name] + "," +  line[_function_signature]
        if not os.path.exists(home_dir + '/datasets/' + line[_version_introduced_name]):
            # run java-callgraph
            cmd = 'java -jar ' + jar_file + ' ' + root_path + ' ' + jar_list_path + ' ' + java_list_path + ' ' + output_path + ' DEBUG'
            res = subprocess.check_call(cmd, shell=True)

# Calculate interest 
# TODO