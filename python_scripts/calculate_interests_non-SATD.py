import csv
import re
import sys
import copy

# setting
home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'
und_out_dir = home_dir + '/und'

v1=0
v2=0
v3=0

class Metrics:
    def __init__(self):
        self.version_name = -1
        self.long_file_name = ""
        self.count_input_introduce = -1
        self.count_input_last_found = -1
        self.count_output_introduce = -1
        self.count_output_last_found = -1
        self.count_line_introduce = -1
        self.count_line_last_found = -1
        self.cyclomatic_introduce = -1
        self.cyclomatic_last_found = -1
        self.max_nesting_introduce = -1
        self.max_nesting_last_found = -1
            
    def out(self,sep="#"):
        return sep.join([str(self.introduce), str(self.last_found)])

    def out_all(self,sep="#"):
        return sep.join([str(self.version_name), str(self.count_input_introduce), str(self.count_input_last_found), str(self.count_output_introduce), str(self.count_output_last_found),
                         str(self.count_line_introduce), str(self.count_line_last_found), str(self.cyclomatic_introduce), str(self.cyclomatic_last_found), str(self.max_nesting_introduce), str(self.max_nesting_last_found)])

    #count_input.out_all(), count_output.out(), count_line.out(), cyclomatic.out(), max_nesting.out()

class MetricsManeger():
    def __init__(self):
        self.list = {}
        
    def add_version(self, key, long_file_name, value):
        if self.list.has_key(key):
            if self.list[key].long_file_name == long_file_name:
                print "duplicate@add "  + key
                print "   " + self.list[key].long_file_name + " v.s. " + long_file_name
            else:
                if self.list[key].long_file_name == "proposal/embed/src/java/org/apache/tools/ant/PropertyHelper.java":
                    self.list[key].version_name = value
                    self.list[key].long_file_name = long_file_name
                elif self.list[key].long_file_name == "src/main/org/apache/tools/ant/types/resources/StringResource.java":
                    a = 1
                else:
                    print "not duplicate@add "  + key
                    print "   " + self.list[key].long_file_name + " v.s. " + long_file_name
        else:
            m = Metrics()
            m.version_name = value
            m.long_file_name = long_file_name
            self.list[key] = m
            #print "1:" + key
            
    def add_introduce_version(self, key, long_file_name, count_input, count_output, count_line, cyclomatic, max_nesting):
        if self.list.has_key(key):
            m = self.list.get(key)
            if m.count_input_introduce == -1:
                m.count_input_introduce = count_input
                m.count_output_introduce = count_output
                m.count_line_introduce = count_line
                m.cyclomatic_introduce = cyclomatic
                m.max_nesting_introduce = max_nesting
                #print "2:" + key
            else:
                if self.list[key].long_file_name == long_file_name:
                    if long_file_name == "src/main/org/apache/tools/ant/ComponentHelper.java":
                        # src/main/org/apache/tools/ant/ComponentHelper.java is exception
                        # that one is added in first verison
                        m.count_input_introduce = count_input
                        m.count_output_introduce = count_output
                        m.count_line_introduce = count_line
                        m.cyclomatic_introduce = cyclomatic
                        m.max_nesting_introduce = max_nesting                        
                    else:
                        print "duplicate@intro "  + key
                        print "   " + self.list[key].long_file_name + " v.s. " + long_file_name
                        print "   " + self.list[key].count_input_introduce + " v.s. " + count_input
                else:
                    if self.list[key].long_file_name == "src/main/org/apache/tools/ant/ComponentHelper.java":
                        a = 1
                    else:
                        print "not duplicate@intro "  + key
                        print "   " + self.list[key].long_file_name + " v.s. " + long_file_name
        else:
            m = Metrics()
            m.version_name = count_input
            m.long_file_name = long_file_name
            m.count_input_introduce = count_input
            m.count_output_introduce = count_output
            m.count_line_introduce = count_line
            m.cyclomatic_introduce = cyclomatic
            m.max_nesting_introduce = max_nesting
            self.list[key] = m            
            
    def add_last_version(self, key, long_file_name, count_input, count_output, count_line, cyclomatic, max_nesting):
        if self.list.has_key(key):
            m = self.list.get(key)
            if m.count_input_last_found == -1:
                m.count_input_last_found = count_input
                m.count_output_last_found = count_output
                m.count_line_last_found = count_line
                m.cyclomatic_last_found = cyclomatic
                m.max_nesting_last_found = max_nesting
                #print "3:" + key

            else:
                if self.list[key].long_file_name == long_file_name:
                    print "duplicate@last "  + key
                    print "   " + self.list[key].long_file_name + " v.s. " + long_file_name
                else:
                    if self.list[key].long_file_name == "src/main/org/apache/tools/ant/types/resources/StringResource.java":
                        a = 1
                    else:
                        print "not duplicate@last "  + key
                        print "   " + self.list[key].long_file_name + " v.s. " + long_file_name
                
# Run runUND.pl if there is *.und file
if __name__ == "__main__":               
    #sys.exit()
    
    print "========================================="
    
    #debt_file = home_dir + '/datasets/CSV/technical_debt_summary_test.csv'
    debt_file = home_dir + '/datasets/CSV/technical_debt_summary.csv'
    tags_file = home_dir + '/datasets/CSV/tags_information.csv'
    revs_file = home_dir + '/datasets/CSV/revs_information.csv'
    
    tags = {}
    with open(tags_file) as csvfile:
        f = csv.reader(csvfile)
        
        for line in f:
            if line[0] == 'project_name':
                continue
    
            tags[line[1]] = line[3]

    revs = {}
    with open(revs_file) as csvfile:
        f = csv.reader(csvfile)
        
        for line in f:
            if line[0] == 'project_name':
                continue
    
            revs[line[1]] = line[3]
        
    # line numbers
    _project = 0
    _file_name = 3
    _class_name = 5
    _type = 13
    _version = 1
    #_version_introduced_name = 20
    #_version_removed_name = 23
    #_last_version_that_comment_was_found_name = 25
    _version_introduced_name = 28
    _version_removed_name = 31
    _last_version_that_comment_was_found_name = 26
    _function_signature = 15
    _comment_classification = 18
    metrics_columns = ["Kind", "Name", "File", "CountInput", "CountLine", "CountLineBlank", "CountLineCodeDecl", "CountLineComment", "CountOutput", "CountSemicolon", "CountStmt", "CountStmtDecl", "CountStmtExe", "Cyclomatic", "CyclomaticModified", "CyclomaticStrict", "Essential", "MaxNesting", "RatioCommentToCode"]
    #metrics_columns = ["Kind", "Name"]
    count = 0
    
    #analyazed = {}
    
    with open(debt_file) as csvfile:
        f = csv.reader(csvfile)
        
        f_CountInput = open (debt_file + "interest-non-SATD.ssv", 'w')
        f_CountInput.write("#".join(["Project","Type","File_Name","Class_Name","Method_Signature","v1","v1_date","v2","v2_date","version_name","CountInput_v1","CountInput_v2","CountOutput_v1","CountOutput_v2","CountLine_v1","CountLine_v2","Cyclomatic_v1","Cyclomatic_v2","MaxNesting_v1","MaxNesting_v2\n"]))
        #f_CountInput.write("#".join(["Method_Signature","version_name","CountInput_v1","CountInput_v2\n"]))
        
        for line in f:
            list = MetricsManeger()
            count = count + 1
            
            if count > 2000:
                break
            
            if line[_project] == 'project_name':
                continue
            
            if line[_type] != 'METHOD':
                #f_CountInput.write("#".join([line[_function_signature], "", "", "","\n"]))
                continue
            
            idxs = [_version,_version_introduced_name,_last_version_that_comment_was_found_name]

            #print "###".join([line[_project],line[_class_name],line[_file_name], line[_function_signature]])
                        
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
                                
                metrics_file_base = "/".join([und_out_dir, line[_project], line[idx]])
                metrics_method_file = metrics_file_base + ".method-level.product.csv"

                #if analyazed.has_key(metrics_method_file+line[_file_name]):
                #    print "skip:" + metrics_method_file+line[_file_name]
                #    continue
                #analyazed[metrics_method_file+line[_file_name]] = 1
                                                
                # case313_line1178(java.lang.Object, java.lang.Object[], int) => case313_line1178(Object, Object[], int)
                method_sig = re.sub( r'[a-zA-Z0-9]*\.','',line[_function_signature]) 
                method_sig = re.sub( r'<.*?>', '', method_sig)
                # case313_line1178(Object, Object[], int) => case313_line1178(Object,Object[],int)
                method_sig = method_sig.replace(' ','')
                method_sig = ".".join([line[_class_name], method_sig])
                #print "    " + line[idx] +  ":" + method_sig
                
                met_idx = 3
                                                
                tmp_f2 = open(metrics_method_file)
                f2 = csv.reader(tmp_f2)
                
                lnum = 0
                
                for metrics_line in f2:
                    lnum = lnum + 1
                    # skip header
                    if metrics_line[0].find("Method") == -1:
                        continue
                    
                    # skip non same file
                    if metrics_line[2].find(line[_file_name]) == -1:
                        continue
                    
                    metrics_line[1] = metrics_line[1].replace('...','[]')                                        
                    # skip function in non main class
                    if metrics_line[1].find(".(Anon_") != -1:
                        continue
                    
                    # not same method name
                    if method_sig != metrics_line[1]:
                        key_filename = metrics_line[2] # metrics_line[2] is directory name + file name. Even if file name is same, but directory name is changed.
                        key_filename = key_filename.split("/")
                        key_filename = key_filename[(len(key_filename)-1)] #just use file name
                        key = metrics_line[1] + "@" + key_filename
                        #print "    =>" + metrics_line[1] + " " + metrics_line[met_idx] 
                        #print "       " + str(lnum) + metrics_line[2] 
                        if idx == _version:
                            list.add_version(key, metrics_line[2], metrics_line[met_idx])
                                                        
                        if idx == _version_introduced_name:
                            #list.add_introduce_version(key, metrics_line[2], metrics_line[met_idx], metrics_line[8], metrics_line[4], metrics_line[13], metrics_line[17])
                            list.add_introduce_version(key, metrics_line[2], str(lnum), metrics_line[8], metrics_line[4], metrics_line[13], metrics_line[17])
                        if idx == _last_version_that_comment_was_found_name:
                            list.add_last_version(key, metrics_line[2], metrics_line[met_idx], metrics_line[8], metrics_line[4], metrics_line[13], metrics_line[17])
    
            date_introduced = ""
            date_last_found = ""
            try:
                date_introduced = revs[line[_version_introduced_name]]
            except KeyError:
                date_introduced = tags[line[_version_introduced_name]]

            try:
                date_last_found = revs[line[_last_version_that_comment_was_found_name]]                                                   
            except KeyError:
                date_last_found = tags[line[_last_version_that_comment_was_found_name]]  
            
            for key in list.list.iterkeys():
                m = list.list[key]
                f_CountInput.write("#".join([line[_project],line[_comment_classification],line[_file_name],line[_class_name],key,line[_version_introduced_name],date_introduced,line[_last_version_that_comment_was_found_name],date_last_found, m.out_all() + '\n']))
        f_CountInput.close()