import setting as s
import os
import subprocess

def runUND(project, version, count=0, reuse=True):
    revs_dir = s.home_dir + "/revs/" + project        
    target_path = "/".join([revs_dir, version, "src"])
    und_file = "/".join([s.und_out_dir, project, version])
    und_file_w_ext = und_file + ".product.udb"

    if reuse and os.path.exists(und_file_w_ext):
        print str(count) + ': (reused) ' + und_file_w_ext
        print "  => " + ' '.join(['perl',s.perl,und_file,'java','-t',target_path])
        return 0
            
    # run
    cmd = ' '.join(['perl',s.perl,und_file,'java','-t',target_path])
    print str(count) + ':' + cmd
    subprocess.check_call(cmd, shell=True)    

if __name__ == "__main__":
    project = ""
    version = ""
    
    runUND(project, version)