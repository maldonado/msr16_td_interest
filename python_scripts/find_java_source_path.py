import csv
import re
import os.path
import subprocess
    
# setting
home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'
# debt_file = home_dir + '/datasets/CSV/technical_debt_summary_test.csv'
debt_file = home_dir + '/datasets/CSV/technical_debt_summary.csv'
jar_file  = home_dir + '/java-callgraph.jar'

# line numbers
_project = 0
_file_name = 3
_class_name = 5
_type = 13
_version_introduced_name = 20
_function_signature = 15

count = 0

# Run java-callgraph if there is no method invocation file
with open(debt_file) as csvfile:
    f = csv.reader(csvfile)

    for line in f:
        count = count + 1
                
        if line[_project] == 'project_name':
            continue
        
        if line[_type] != 'METHOD':
            continue

        if count > 2000:
            break
        
        tags_dir=''
        if line[_project] == 'apache-ant':
            tags_dir = '/tags/ant_tags'
        elif line[_project] == 'jruby':
            continue
            tags_dir = '/tags/jruby_tags'
        elif line[_project] == 'apache-jmeter':
            tags_dir = '/tags/jmeter_tags'
        else:
            continue
        
        root_path = home_dir + tags_dir + "/" + line[_version_introduced_name] + "/src"
        
        java_list_path = home_dir + "/datasets/MISC/temp_list_" + line[_project] + "_" + line[_version_introduced_name] + ".txt"
        output_path  = home_dir + "/datasets/MISC/path_" + line[_project] + "_" + line[_version_introduced_name] + ".txt"
                
        # print line[_project] + "," + line[_file_name] + "," +  line[_version_introduced_name] + "," +  line[_function_signature]
        if not os.path.exists(output_path):
            cmd = "find " + root_path + " -name *.java > " + java_list_path
            res = subprocess.check_call(cmd, shell=True)
        
        temp_list = []
        path_list = []
        
        f2 = open(java_list_path)
        for line2 in f2:
            line2 = line2.rstrip()
            matchOB = re.match(r"(.*)/org/.*" , line2)
            if matchOB:
                path = matchOB.group(1)
                temp_list.append(path)
            else:
                matchOB = re.match(r"(.*/src/proposal/sandbox/embed/).*" , line2)
                if matchOB:
                    path = matchOB.group(1)
                    temp_list.append(path)
                else:
                    matchOB = re.match(r"(.*/junit/).*" , line2)
                    if matchOB:
                        path = matchOB.group(1)
                        temp_list.append(path)
                    else:
                        matchOB = re.match(r"(.*/testcases/).*" , line2)
                        if matchOB:
                            path = matchOB.group(1)
                            temp_list.append(path)
                        else:
                            matchOB = re.match(r"(.*)/com/.*" , line2)
                            if matchOB:
                                path = matchOB.group(1)
                                temp_list.append(path)
                            else:
                                matchOB = re.match(r"(.*)/anteater/.*" , line2)
                                if matchOB:
                                    path = matchOB.group(1)
                                    temp_list.append(path)
                                else:
                                    matchOB = re.match(r"(.*)/antfarm/.*" , line2)
                                    if matchOB:
                                        path = matchOB.group(1)
                                        temp_list.append(path)
                                    else:
                                        matchOB = re.match(r"(.*)/antunit/.*" , line2)
                                        if matchOB:
                                            path = matchOB.group(1)
                                            temp_list.append(path)
                                        else:
                                            matchOB = re.match(r"(.*)/jndi/.*" , line2)
                                            if matchOB:
                                                path = matchOB.group(1)
                                                temp_list.append(path)
                                            else:
                                                print line2          
        for x in temp_list:
            if x not in path_list:
                path_list.append(x)
        
        f3 = open(output_path, 'w')
        for x in path_list:
            f3.write(x + '\n')
        f3.close()
