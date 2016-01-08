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

    all_exact_match = 0
    all_unsoloved_method = 0
    all_t1 = 0
    all_t2 = 0
    all_t0 = 0
    all_method_match = 0

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
        
        jar_list_path = home_dir + "/datasets/MISC/jar_list_" + line[_project] + "_" + line[_version_introduced_name] + ".txt"
        java_list_path = home_dir + "/datasets/MISC/java_list_" + line[_project] + "_" + line[_version_introduced_name] + ".txt"
        path = home_dir + "/datasets/MISC/path_" + line[_project] + "_" + line[_version_introduced_name] + ".txt"
        output_path  = home_dir + "/datasets/MISC/methodinvocation_" + line[_project] + "_" + line[_version_introduced_name] + ".txt"
        log_path = home_dir + "/datasets/MISC/log_" + line[_project] + "_" + line[_version_introduced_name] + ".txt"
                
        # print line[_project] + "," + line[_file_name] + "," +  line[_version_introduced_name] + "," +  line[_function_signature]
        if not os.path.exists(output_path):
            cmd = "find " + root_path + " -name *.jar > " + jar_list_path
            res = subprocess.check_call(cmd, shell=True)
            
            if line[_version_introduced_name] == 'MYRMIDON_PRE_CONF_MUNGE':
                cmd = "find " + root_path + " -name *.java > " + java_list_path
            else:
                cmd = "find " + root_path + "/src" + " -name *.java > " + java_list_path
            res = subprocess.check_call(cmd, shell=True)
            
            # run java-callgraph
            cmd = 'java -jar ' + jar_file + ' ' + root_path + ' ' + jar_list_path + ' ' + java_list_path + ' ' + output_path + ' DEBUG > ' + log_path
            res = subprocess.check_call(cmd, shell=True)
            
        # Calculate interest 
        target_class_name = line[_class_name]
        target_function_signature = line[_function_signature]
        matchOB = re.match(r"(.*)\(.*\)" , target_function_signature)
        target_function = matchOB.group(1) + "()"
        
        target_function_signature = target_class_name + "." + target_function_signature
        
        #print target_function_signature
        
        exact_match = 0
        unsoloved_method = 0
        method_match = 0

        t1 = 0
        t2 = 0
        t0 = 0
        
        f2 = open(output_path)
        for line2 in f2:
            line2 = line2.rstrip()
            function_signature = line2.split("#")[1]
            
            matchOB = re.match(r"(.*)\.(.*)\(.*\)" , function_signature)
            class_name = matchOB.group(1)
            function = matchOB.group(2) + "()"
            
            if target_function_signature == function_signature:
                exact_match = exact_match + 1
            
            if target_function == function:
                #print "   " + target_function_signature
                #print "   " + function_signature
                method_match = method_match + 1
                
                matchOB = re.match(r"(.*_NOCLASS)_RANK_\d" , class_name)
                if matchOB:
                    class_name = matchOB.group(1)
                
                if class_name == "1_NOCLASS" or class_name == "2_NOCLASS" or class_name == "_0_NOCLASS":
                    unsoloved_method = unsoloved_method + 1

                if class_name == "1_NOCLASS":
                    t1 = t1 + 1
                    
                if class_name == "2_NOCLASS":
                    t2 = t2 + 1                
        
                if class_name == "_0_NOCLASS":
                    t0 = t0 + 1
                            
        all_exact_match = all_exact_match + exact_match
        all_unsoloved_method = all_unsoloved_method + unsoloved_method
        all_method_match = all_method_match + method_match

        all_t1 = all_t1 + t1
        all_t2 = all_t2 + t2
        all_t0 = all_t0 + t0
        
        #print target_function_signature
        print str(exact_match) + "," + str(unsoloved_method) + "," + str(t1) + "," + str(t2) + "," + str(t0) + "," + str(method_match) + "," + target_function_signature
            
    print str(all_exact_match) + "," + str(all_unsoloved_method) + "," + str(all_t1) + "," + str(all_t2) + "," + str(all_t0) +  "," + str(all_method_match) + "," + str(float(all_exact_match)/float(all_method_match) * 100) 