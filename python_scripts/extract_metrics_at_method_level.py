import csv
import pandas as pd

# setting
home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'
debt_file = home_dir + '/datasets/CSV/technical_debt_summary.csv'
und_out_dir = home_dir + '/und'

# line numbers
_project = 0
_file_name = 3
_class_name = 5
_type = 13
_version_introduced_name = 20
_version_removed_name = 23
_last_version_that_comment_was_found_name = 25
_function_signature = 15
metrics_columns = ["Kind", "Name", "File", "CountInput", "CountLine", "CountLineBlank", "CountLineCodeDecl", "CountLineComment", "CountOutput", "CountSemicolon", "CountStmt", "CountStmtDecl", "CountStmtExe", "Cyclomatic", "CyclomaticModified", "CyclomaticStrict", "Essential", "MaxNesting", "RatioCommentToCode"]
#metrics_columns = ["Kind", "Name"]
count = 0

# Run runUND.pl if there is *.und file
with open(debt_file) as csvfile:
    f = csv.reader(csvfile)
    
    for line in f:          
        count = count + 1
        
        if count > 2000:
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
                    
            metrics_file_base = "/".join([und_out_dir, line[_project], line[idx]])
            metrics_file = metrics_file_base + ".product.csv"
            metrics_method_file = metrics_file_base + ".method-level.product.csv"

            # only method level            
            f2 = pd.read_csv(metrics_file)
            f3 = open(metrics_method_file, 'w')
            csvWriter  = csv.writer(f3)
            
            csvWriter.writerow(metrics_columns)
            for index, row in f2.iterrows():
                if row["Kind"] == 'Public Implicit Method':
                    continue
                
                if 'Method' in row["Kind"]:
                    tmp = row[metrics_columns]
                    csvWriter.writerow(tmp)
            f3.close()
