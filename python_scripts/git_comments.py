import csv
import os
import sys
import re
import subprocess

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import *

# setting
home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'

class Debt:
    def __init__(self):
        self.project = ""
        self.type = ""
        self.debt = ""
        self.introduced = ""
        self.idate = ""
        self.iauthor = ""
        self.removed = "NULL"
        self.rdate = "NULL"
        self.rauthor = "NULL"
    
    def out(self):
        return [self.type, self.debt, self.idate, self.iauthor, self.introduced, self.rdate, self.rauthor, self.removed]
    
    def out_processed(self):
        return [self.type, text_clean(self.debt), self.idate, self.iauthor, text_clean(self.introduced), self.rdate, self.rauthor, text_clean(self.removed)]

    def out_processded_introduced(self):
        return text_clean(self.introduced)

stop_words = stopwords.words('english')
st1 = PorterStemmer()
punctuation = re.compile(r'[-.?!,":;()|0-9]')
def text_clean(str_input, st=st1):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(str_input)
    filtered_tokens = [st.stem(word.lower()) for word in tokens if word.lower() not in stop_words]
    #filtered_tokens = [punctuation.sub("", word) for word in filtered_tokens]    
    res = " ".join(filtered_tokens)
    return res

# Run runUND.pl if there is *.und file
if __name__ == "__main__":
    #sys.exit()
    
    #debt_file = home_dir + '/datasets/CSV/technical_debt_summary_test.csv'
    debt_file = home_dir + '/datasets/CSV/technical_debt_summary.csv'
    comment_file = home_dir + '/datasets/CSV/comments.csv'
    
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
    _comment_text = 19
    metrics_columns = ["Kind", "Name", "File", "CountInput", "CountLine", "CountLineBlank", "CountLineCodeDecl", "CountLineComment", "CountOutput", "CountSemicolon", "CountStmt", "CountStmtDecl", "CountStmtExe", "Cyclomatic", "CyclomaticModified", "CyclomaticStrict", "Essential", "MaxNesting", "RatioCommentToCode"]
    #metrics_columns = ["Kind", "Name"]
    count = 0
    
    fo_ant = open("/Users/kamei/Research/src/Twitter-LDA/data/Data4Model/techdebt/ant.txt","w")
    fo_jmeter = open("/Users/kamei/Research/src/Twitter-LDA/data/Data4Model/techdebt/jmeter.txt","w")
    fo_jruby = open("/Users/kamei/Research/src/Twitter-LDA/data/Data4Model/techdebt/jruby.txt","w")
    
    with open(debt_file) as csvfile:
        f = csv.reader(csvfile)
        fo = open(comment_file,"w")
        csvWriter = csv.writer(fo)
        csvWriter.writerow(["Type", "Debt","Introduce Date", "Introduce Author", "Introduce Comment", "Remove Date", "Remove Author", "Remove Comment"])
        
        for line in f:          
            count = count + 1
            
            if count > 2000:
                break
            
            if line[_project] == 'project_name':
                continue
            
            if line[_type] != 'METHOD':
                #f_CountInput.write("#".join([line[_function_signature], "", "", "","\n"]))
                continue
            
            out = Debt()
            out.type = line[_comment_classification]
            out.debt = line[_comment_text]
            print line[_comment_text] + "\n"
            
            idxs = [_version_introduced_name,_version_removed_name]
            for idx in idxs:        
                if line[idx] == '' or line[idx] == 'not_removed':
                        continue
                
                project = ""
                if line[_project] == 'apache-ant':
                    project = "ant"
                elif line[_project] == 'jruby':
                    project = "jruby"
                elif line[_project] == 'apache-jmeter':
                    project = "jmeter"
                else:
                    continue
                
                path = "/Users/kamei/Research/techdebt/msr16_td_interest/repos/" + project
                out.project = project
                os.chdir(path)
                cmd = "git log " + line[idx] + " -n 1 --pretty=format:""%s"""
                if idx == _version_introduced_name:
                    out.introduced = subprocess.check_output( cmd.split(" ") )
                elif idx == _version_removed_name:
                    out.removed = subprocess.check_output( cmd.split(" ") )

                cmd = "git log --date=short " + line[idx] + " -n 1 --pretty=format:""%ad"""
                if idx == _version_introduced_name:
                    out.idate = subprocess.check_output( cmd.split(" ") )
                elif idx == _version_removed_name:
                    out.rdate = subprocess.check_output( cmd.split(" ") )

                cmd = "git log " + line[idx] + " -n 1 --pretty=format:""%an"""
                if idx == _version_introduced_name:
                    out.iauthor = subprocess.check_output( cmd.split(" ") )
                elif idx == _version_removed_name:
                    out.rauthor = subprocess.check_output( cmd.split(" ") )
            
            csvWriter.writerow(out.out())
            fo_all = open("/Users/kamei/Research/techdebt/msr16_td_interest/datasets/CSV/comments/" + str(count) + ".txt","w")
            fo_all.write(out.out_processded_introduced() + "\n")
            fo_all.close()
            
            if out.project == "ant":
                fo_ant.write(out.out_processded_introduced() + "\n")
            elif out.project == "jmeter":
                fo_jmeter.write(out.out_processded_introduced() + "\n")
            elif out.project == "jruby":
                fo_jruby.write(out.out_processded_introduced() + "\n")
            
            #csvWriter.writerow(out.out_processed())
            
