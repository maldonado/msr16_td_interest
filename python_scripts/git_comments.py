import setting as s
import csv
import os
import re
import subprocess

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import *

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
        self.iID = ""
        self.rID = "NULL"
    
    def out(self):
        return [self.type, self.debt, self.idate, self.iauthor, self.introduced, self.rdate, self.rauthor, self.removed, self.iID, self.rID]
    
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

def git_comments(project, versions, count=0):
    git_dir  = s.home_dir + "/repos/" + project 
    out = Debt()
    out.project = project
    os.chdir(git_dir)

    i=0
    for version in versions:        
        if version == '':
            continue

        cmd = "git log " + version + " -n 1 --pretty=format:""%s"""
        comment = subprocess.check_output( cmd.split(" ") )
        cmd = "git log --date=short " + version + " -n 1 --pretty=format:""%ad"""
        date = subprocess.check_output( cmd.split(" ") )
        cmd = "git log " + version + " -n 1 --pretty=format:""%an"""
        author = subprocess.check_output( cmd.split(" ") )
   
        if i == 0:
            out.introduced = comment
            out.idate = date
            out.iauthor = author
            out.iID = version

        elif i == 1:
            out.removed = comment
            out.rdate = date
            out.rauthor = author
            out.rID = version
            
        i = i + 1
    return out

if __name__ == "__main__":
    project = ""
    versions = ""
                
    git_comments(project, versions)