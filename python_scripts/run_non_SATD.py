import setting_non_SATD as s
import link_SATD_to_UND

import csv
import re

idxs = ["introduced_version_commit_hash", "removed_version_commit_hash", "last_found_commit_hash"]

def get_latest_version(project):
    if project == 'ant':
        return 'ANT_193'
    elif project == 'jruby':
        return '9.0.1.0'
    elif project == 'jmeter':
        return 'v2_13_RC2'
    elif project == 'camel': #git log --before="2016-04-28"
        return '017dffc3728e8114e180f64806e0dce8d59dce23'    
    elif project == 'gerrit':
        return '8b39fb4bc01809f20a2998c55dede18717682a56'
    elif project == 'hadoop':
        return '6f26b665874f923d50087f68357ac822fa9fe709'
    elif project == 'log4j':
        return '7be00eed88152dd011a619e8bae5a631235c3f4c'
    elif project == 'tomcat':
        return '1a1adb39819b3181c448bd7aaf2516bb92cb7a35'
    else:
        raise ValueError(project + " is not defined in this function") 

def get_func_signature(func_name, func_parameter_list):
    if func_parameter_list == "":
        return func_name + "()"
    
    func_parameter_list = func_parameter_list.rstrip() # drop blank
    print "    get_func_sig 1"
    print "        " + func_parameter_list
    params = func_parameter_list.split(', ')
    signature = func_name + "("
    param = []
    for temp in params:
        temp = re.sub(r'^final ', "", temp) # remove final
        m = re.search(r'(.*)\s+.*', temp)
        
        if m != None:
            temp = m.group(1)
        
        temp = temp.replace(" ", "") # remove blank
        
        if temp.count("<"):
            if temp.count(">") == 0:
                temp = temp + ">"
                print "========> " + temp

        param.append(temp)
    signature = signature + ",".join(param) + ")"
    
    signature = signature.replace("/*","")
    signature = signature.replace("*/","")

    print "    get_func_sig 2"    
    print "        " +  signature
     
    return signature

with open(s.debt_file) as csvfile:
    csvfile = open(s.debt_file)
    reader = csv.DictReader(csvfile)
    
    # for git_comments
    fo_comment_file = open(s.comment_file,"w")
    csvWriter_comment_file = csv.writer(fo_comment_file)
    csvWriter_comment_file.writerow(["Type", "Debt","Introduce Date", "Introduce Author", "Introduce Comment", "Remove Date", "Remove Author", "Remove Comment", "Introduce ID", "Remove ID"])

    #for calculate_interest
    fo_interest = open (s.interest_file, 'w')
    fo_interest.write("#".join(["Project_name","Signature", "Intro", "Last", "Long_file_name","CountInput_v1","CountInput_v2","CountOutput_v1","CountOutput_v2","CountLine_v1","CountLine_v2","Cyclomatic_v1","Cyclomatic_v2","MaxNesting_v1","MaxNesting_v2\n"]))

    print("#################################################################")
    print("#for calculate_interests")
    print("#################################################################")
    print ""
        
    count = 1 # consider header   
    for line in reader:
        count = count + 1
                
        if count < s.START_LOOP:
            continue
        
        if count > s.MAX_LOOP:
            break
        
        if line[u'comment_location'] != "FUNCTION":
            continue
        
        print str(count) + " [P1]: ",
        print line
        project =  line[u'project']
        td_classification= line[u'td_classification']

        versions = [] #for calculate_interests
        
        file_names = []
        file_names.append(line[u'file_introduced_path'])
        file_names.append(line[u'last_found_path'])

        function_signatures = []
        function_signatures.append(get_func_signature(line[u'func_name'],line[u'func_parameter_list']))
        function_signatures.append(get_func_signature(line[u'last_found_func_name'],line[u'last_found_func_parameter_list']))
        
        for idx in idxs:
            version = line[idx]
            if idx != "removed_version_commit_hash":  #for calculate_interests
                versions.append(version)
            
            if idx == "removed_version_commit_hash" and line[u'has_removed_version'] == "f":
                version = get_latest_version(project)

        non_satd = link_SATD_to_UND.link_NON_SATD_to_UND(project, versions, file_names, function_signatures)
        for key in non_satd.list.iterkeys():
            m = non_satd.list[key]
            fo_interest.write(m.out_all_with_key(key) + '\n')
        
        #count_input, count_output, count_line, cyclomatic, max_nesting = set_metrics
        
        #debt = line[u'comment_text']
        #debt = debt.replace("#", "")
        #debt = debt.replace('\n','')
        #debt = debt.replace('\r','')

        #date_introduced = line[u'introduced_version_date']
        #date_last_found = line[u'last_found_date']

        #intro_id = line[u'introduced_version_commit_hash']
        #intro_comment = ""
        #remove_id = line[u'removed_version_commit_hash']
        #remove_comment = ""
        #last_id = line[u'last_found_commit_hash']
        
        #fo_interest.write("#".join([project,td_classification,file_names[0], function_signatures[0],intro_id,date_introduced,last_id,date_last_found,count_input.out_all(), count_output.out(), count_line.out(), cyclomatic.out(), max_nesting.out(), debt, intro_id, intro_comment, remove_id, remove_comment  + '\n']))
    fo_interest.close()