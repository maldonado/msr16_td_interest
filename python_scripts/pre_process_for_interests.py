import csv
import os.path
import subprocess
    
# setting
home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'
# debt_file = home_dir + '/datasets/CSV/technical_debt_summary_test.csv'
debt_file = home_dir + '/datasets/CSV/technical_debt_summary.csv'
java_callgraph  = home_dir + '/java-callgraph.jar'
extractfiles = home_dir + '/FilterTargetFiles.jar'

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
    
#     # Here is the part to merge functions that are called in one version
#     # target method signatures
#     d = {} 
#     for line in f:
#         if line[_project] == 'project_name':
#             continue
#         
#         if line[_type] != 'METHOD':
#             continue
#         
#         key = line[_project] + "_"+ line[_version_introduced_name]
#         if d.has_key(key):
#             d[key] = d[key] + "," + line[_class_name]
#         else:
#             d.update({key : line[_class_name]})                         
#     csvfile.seek(0)
#     f = csv.reader(csvfile)
    
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
        
        class_name = line[_class_name]
        class_name = class_name.replace(".","_")
        key = line[_project] + "_" + line[_version_introduced_name]
        key_for_each_file = line[_project] + "_" + line[_version_introduced_name] + "_" + class_name
        
        jar_list_path = home_dir + "/datasets/MISC/jar_list_" + key + ".txt"
        all_java_list_path = home_dir + "/datasets/MISC/all_java_list_" + key + ".txt"
        
        java_list_path = home_dir + "/datasets/MISC/java_list_" + key_for_each_file + ".txt"        
        log_extractfiles_path = home_dir + "/datasets/MISC/log_extractfiles_" + key_for_each_file + ".txt"

        #path = home_dir + "/datasets/MISC/path_" + key + ".txt"
        invocation_path  = home_dir + "/datasets/MISC/methodinvocation_" + key_for_each_file + ".txt"
        log_invocation_path = home_dir + "/datasets/MISC/log_" + key_for_each_file + ".txt"

        # print line[_project] + "," + line[_file_name] + "," +  line[_version_introduced_name] + "," +  line[_function_signature]
        if not os.path.exists(java_list_path):
            cmd = "find " + root_path + " -name *.java > " + all_java_list_path
            res = subprocess.check_call(cmd, shell=True)
            
            # run java-callgraph
            cmd = 'java -jar ' + extractfiles + ' ' + line[_class_name] + ' ' + all_java_list_path + ' ' + java_list_path
            res = subprocess.check_call(cmd, shell=True)
            
            cmd = 'echo ' + line[_class_name] + " > " + log_extractfiles_path
            res = subprocess.check_call(cmd, shell=True)
            
            cmd = 'cat ' + java_list_path + ' >> ' + log_extractfiles_path
            res = subprocess.check_call(cmd, shell=True)
        
        # print line[_project] + "," + line[_file_name] + "," +  line[_version_introduced_name] + "," +  line[_function_signature]
        if not os.path.exists(invocation_path):
            cmd = "find " + root_path + " -name *.jar > " + jar_list_path
            res = subprocess.check_call(cmd, shell=True)

            # run java-callgraph
            cmd = 'java -jar ' + java_callgraph + ' ' + root_path + ' ' + jar_list_path + ' ' + java_list_path + ' ' + invocation_path + ' DEBUG > ' + log_invocation_path
            res = subprocess.check_call(cmd, shell=True)
            