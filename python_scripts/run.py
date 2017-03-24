import setting as s
import checkoutRevisions
import runUND
import extract_metrics_at_method_level
import git_comments
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
    else:
        raise ValueError(project + "is not defined in this function") 

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

count = 0   
with open(s.debt_file) as csvfile:
    csvfile = open(s.debt_file)
    reader = csv.DictReader(csvfile)
    
    # for git_comments
    fo_comment_file = open(s.comment_file,"w")
    csvWriter_comment_file = csv.writer(fo_comment_file)
    csvWriter_comment_file.writerow(["Type", "Debt","Introduce Date", "Introduce Author", "Introduce Comment", "Remove Date", "Remove Author", "Remove Comment", "Introduce ID", "Remove ID"])

    #for calculate_interest
    fo_interest = open (s.interest_file, 'w')
    fo_interest.write("#".join(["Project","Type","File_Name","Method_Signature","v1","v1_date","v2","v2_date","version_name","CountInput_v1","CountInput_v2","CountOutput_v1","CountOutput_v2","CountLine_v1","CountLine_v2","Cyclomatic_v1","Cyclomatic_v2","MaxNesting_v1","MaxNesting_v2", "Debt", "Intro_ID", "Intro_Comment","Remove_ID","Remove_Comment\n"]))

    print("#################################################################")
    print("#for pre-process")
    print("#################################################################")
    for line in reader:
        count = count + 1
        
        if count < s.START_LOOP:
            continue
        
        if count > s.MAX_LOOP:
            break
        
        if line[u'comment_location'] != "FUNCTION":
            continue
        
        print line
        project =  line[u'project']
        versions = [] #for git_comments
                
        for idx in idxs:
            version = line[idx]
            if idx != "last_found_commit_hash":  #for git_comments
                versions.append(version)
            
            if idx == "removed_version_commit_hash" and line[u'has_removed_version'] == "f":
                version = get_latest_version(project)

            checkoutRevisions.checkoutRevision(project, version, count, reuse=True)
            runUND.runUND(project, version, count, reuse=True)
            extract_metrics_at_method_level.extract_metrics(project, version, count, reuse=True)
        
        #for git_comments
        debt = git_comments.git_comments(project, versions, count)
        debt.type = line[u'td_classification']
        debt.debt = line[u'comment_text']
        csvWriter_comment_file.writerow(debt.out())
    fo_comment_file.close()        

    print("#################################################################")
    print("#for read comments")
    print("#################################################################")
    comments_intro = {}
    comments_remove = {}
    with open(s.comment_file) as csv_comment_file:
        csv_comment_file = open(s.comment_file)
        comment_reader = csv.DictReader(csv_comment_file)
    
        for line in comment_reader:
            # 0:Type 1:Debt 2:Introduce Date 3:Introduce Author 4:Introduce Comment
            # 5:Remove Date 6:Remove Author 7:Remove Comment 8:Introduce ID 9:Remove ID
            comments_intro[line[u'Introduce ID']] = line[u'Introduce Comment']
            comments_remove[line[u'Remove ID']] = line[u'Remove Comment']

    print("#################################################################")
    print("#for calculate_interests")
    print("#################################################################")
    print ""
    csvfile.seek(0, 0)
    next(reader)
        
    count = 0    
    for line in reader:
        count = count + 1
        
        if count < s.START_LOOP:
            continue
        
        if count > s.MAX_LOOP:
            break
        
        if line[u'comment_location'] != "FUNCTION":
            continue
        
        print "P1: ",
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

        set_metrics = link_SATD_to_UND.link_SATD_to_UND(project, versions, file_names, function_signatures)
        count_input, count_output, count_line, cyclomatic, max_nesting = set_metrics
        
        debt = line[u'comment_text']
        debt = debt.replace("#", "")
        debt = debt.replace('\n','')
        debt = debt.replace('\r','')

        date_introduced = line[u'introduced_version_date']
        date_last_found = line[u'last_found_date']

        intro_id = line[u'introduced_version_commit_hash']
        intro_comment = ""
        remove_id = line[u'removed_version_commit_hash']
        remove_comment = ""
        last_id = line[u'last_found_commit_hash']

        try:
            intro_comment = comments_intro[intro_id]
            intro_comment = intro_comment.replace("#", "")
        except KeyError:
            intro_comment = ""
        
        try:
            remove_comment = comments_remove[remove_id]
            remove_comment = remove_comment.replace("#", "")
        except KeyError:
            remove_comment = ""
        
        fo_interest.write("#".join([project,td_classification,file_names[0], function_signatures[0],intro_id,date_introduced,last_id,date_last_found,count_input.out_all(), count_output.out(), count_line.out(), cyclomatic.out(), max_nesting.out(), debt, intro_id, intro_comment, remove_id, remove_comment  + '\n']))
    fo_interest.close()