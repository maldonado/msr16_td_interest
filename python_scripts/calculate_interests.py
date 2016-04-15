import csv
import re

# setting
home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'
und_out_dir = home_dir + '/und'

v1=0
v2=0
v3=0

class Metrics:
    def __init__(self):
        self.version_name = -1
        self.introduce = -1
        self.last_found = -1
    
    def out(self,sep="#"):
        return sep.join([str(self.introduce), str(self.last_found)])

    def out_all(self,sep="#"):
        return sep.join([str(self.version_name), str(self.introduce), str(self.last_found)])

# Run runUND.pl if there is *.und file
if __name__ == "__main__":
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
    
    with open(debt_file) as csvfile:
        f = csv.reader(csvfile)
        
        f_CountInput = open (debt_file + "interest.ssv", 'w')
        f_CountInput.write("#".join(["Project","Type","File_Name","Class_Name","Method_Signature","v1","v1_date","v2","v2_date","version_name","CountInput_v1","CountInput_v2","CountOutput_v1","CountOutput_v2","CountLine_v1","CountLine_v2","Cyclomatic_v1","Cyclomatic_v2","MaxNesting_v1","MaxNesting_v2\n"]))
        #f_CountInput.write("#".join(["Method_Signature","version_name","CountInput_v1","CountInput_v2\n"]))
        
        for line in f:          
            count = count + 1
            
            if count > 2000:
                break
            
            if line[_project] == 'project_name':
                continue
            
            if line[_type] != 'METHOD':
                #f_CountInput.write("#".join([line[_function_signature], "", "", "","\n"]))
                continue
            
            idxs = [_version,_version_introduced_name,_last_version_that_comment_was_found_name]

            print "###".join([line[_project],line[_class_name],line[_file_name], line[_function_signature]])
            
            count_input = Metrics()
            count_output = Metrics()
            count_line = Metrics()
            cyclomatic = Metrics()
            max_nesting = Metrics()
            
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
                
                #method_sig = line[_function_signature]
                # change the format
                
                # case313_line1178(java.lang.Object, java.lang.Object[], int) => case313_line1178(Object, Object[], int)
                method_sig = re.sub( r'[a-zA-Z0-9]*\.','',line[_function_signature]) 
                method_sig = re.sub( r'<.*?>', '', method_sig)
                # case313_line1178(Object, Object[], int) => case313_line1178(Object,Object[],int)
                method_sig = method_sig.replace(' ','')
                method_sig = ".".join([line[_class_name], method_sig])
                print "    " + line[idx] +  ":" + method_sig
                
                met_idx = 3
                                                
                tmp_f2 = open(metrics_method_file)
                f2 = csv.reader(tmp_f2)
                
                for metrics_line in f2:
                    metrics_line[1] = metrics_line[1].replace('...','[]')                    
                    # same method name
                    if method_sig == metrics_line[1]: #TODO magic number
                        print "    =>" + metrics_line[met_idx]
                        
                        if idx == _version:
                            count_input.version_name = metrics_line[met_idx]
                            v1 = v1 + 1
                        if idx == _version_introduced_name:
                            count_input.introduce = metrics_line[met_idx]
                            count_output.introduce = metrics_line[8]
                            count_line.introduce = metrics_line[4]
                            cyclomatic.introduce = metrics_line[13]
                            max_nesting.introduce = metrics_line[17]
                            
                            v2 = v2 + 1
                        if idx == _last_version_that_comment_was_found_name:
                            count_input.last_found = metrics_line[met_idx]
                            count_output.last_found = metrics_line[8]
                            count_line.last_found = metrics_line[4]
                            cyclomatic.last_found = metrics_line[13]
                            max_nesting.last_found = metrics_line[17]
                            
                            v3 = v3 + 1
            
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

            f_CountInput.write("#".join([line[_project],line[_comment_classification],line[_file_name],line[_class_name],line[_function_signature],line[_version_introduced_name],date_introduced,line[_last_version_that_comment_was_found_name],date_last_found,count_input.out_all(), count_output.out(), count_line.out(), cyclomatic.out(), max_nesting.out() + '\n']))
        f_CountInput.close()        
print "/".join([str(v1),str(v2),str(v3)])                          