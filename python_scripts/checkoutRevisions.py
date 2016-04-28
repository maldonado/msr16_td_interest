import setting as s
import os.path
import subprocess
import sys

def checkoutRevision(project, version, count=0, reuse=True):
    git_dir  = s.home_dir + "/repos/" + project 
    revs_dir = s.home_dir + "/revs/" + project    
    revs_dir_per_project = revs_dir + '/' + version
                        
    if reuse and os.path.exists(revs_dir_per_project):
        print str(count) + ': (reused) ' + revs_dir_per_project
        return 0
    
    os.chdir(git_dir)    
    try:
        cmd = 'git co ' + version + " -b br_" + version
        print str(count) + ':' + cmd
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        cmd = 'git co br_' + version
        print str(count) + ':' + cmd
        subprocess.check_call(cmd, shell=True)
    
    if os.path.exists(revs_dir_per_project):
        cmd = 'rm -rf ' + revs_dir_per_project
        print str(count) + ':' + cmd
        subprocess.check_call(cmd, shell=True)
            
    cmd = 'mkdir ' + revs_dir_per_project
    print str(count) + ':' + cmd
    subprocess.check_call(cmd, shell=True)
    
    try:
        cmd = 'cp -r ' + git_dir + " " + revs_dir_per_project + "/src"
        print str(count) + ':' + cmd
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        print sys.exc_info()[0]
    
    os.chdir(revs_dir_per_project + "/src")
    cmd = 'rm -rf .[^.] .??*' # for deleting dot files
    print str(count) + ':' + cmd
    subprocess.check_call(cmd, shell=True)

if __name__ == "__main__":
    project = ""
    version = ""
                
    checkoutRevision(project, version)