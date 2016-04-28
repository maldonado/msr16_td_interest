import setting as s
import os
import subprocess

def runUND(project, version, count=0):
    revs_dir = s.home_dir + "/revs/" + project        
    target_path = "/".join([s.home_dir, revs_dir, version, "src"])
    und_file = "/".join([s.und_out_dir, project, version])

    und_file_w_ext = und_file + ".product.udb"
            
    if not os.path.exists(und_file_w_ext):
        # run
        cmd = ' '.join(['perl',s.perl,und_file,'java','-t',target_path])
        print str(count) + ':' + cmd
        subprocess.check_call(cmd, shell=True)    

if __name__ == "__main__":
    project = ""
    version = ""
    
    runUND(project, version)