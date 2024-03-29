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
_version_introduced_name = 25
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
            tags_dir = '/tags/jruby_tags'
        elif line[_project] == 'apache-jmeter':
            tags_dir = '/tags/jmeter_tags'
        else:
            continue
        
        if line[_version_introduced_name] == '' or line[_version_introduced_name] == 'not_removed':
            if line[_project] == 'apache-ant':
                line[_version_introduced_name] = 'ANT_193'
            elif line[_project] == 'jruby':
                line[_version_introduced_name] = '9.0.1.0'
            elif line[_project] == 'apache-jmeter':
                line[_version_introduced_name] = 'v2_13_RC2'
            else:
                continue            
        
        root_path = home_dir + tags_dir + "/" + line[_version_introduced_name] + "/src"
        
        class_name = line[_class_name]
        class_name = class_name.replace(".","_")
        key = line[_project] + "_" + line[_version_introduced_name]
        key_for_each_file = line[_project] + "_" + line[_version_introduced_name] + "_" + class_name
        
        jar_list_path = home_dir + "/datasets/MISC" + str(_version_introduced_name) + "/jar_list_" + key + ".txt"
        java_list_path = home_dir + "/datasets/MISC" + str(_version_introduced_name) + "/java_list_" + key_for_each_file + ".txt"
        #path = home_dir + "/datasets/MISC" + str(_version_introduced_name) + "/path_" + line[_project] + "_" + line[_version_introduced_name] + ".txt"
        output_path  = home_dir + "/datasets/MISC" + str(_version_introduced_name) + "/methodinvocation_" + key_for_each_file + ".txt"
        log_path = home_dir + "/datasets/MISC" + str(_version_introduced_name) + "/log_" + line[_project] + "_" + line[_version_introduced_name] + ".txt"
                
        # print line[_project] + "," + line[_file_name] + "," +  line[_version_introduced_name] + "," +  line[_function_signature]
        if not os.path.exists(output_path):
            print "no method invocation file"
            print line[_project] + "," + line[_file_name] + "," +  line[_version_introduced_name] + "," +  line[_function_signature]
            continue

        if line[_version_introduced_name] == 'MYRMIDON_PRE_CONF_MUNGE':
            continue
        
        if line[_version_introduced_name] == 'TOMCAT_31_M1_RC1' and line[_file_name] == 'Jikes.java':
            continue
        
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