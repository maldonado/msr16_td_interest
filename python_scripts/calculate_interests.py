import setting as s
import csv
import re

class Metrics:
    def __init__(self):
        self.version_name = -1
        self.introduce = -1
        self.last_found = -1
    
    def out(self,sep="#"):
        return sep.join([str(self.introduce), str(self.last_found)])

    def out_all(self,sep="#"):
        return sep.join([str(self.version_name), str(self.introduce), str(self.last_found)])

def calculate_interests(project, versions, file_name, function_signature): 
    count_input = Metrics()
    count_output = Metrics()
    count_line = Metrics()
    cyclomatic = Metrics()
    max_nesting = Metrics()
    
    return [count_input, count_output, count_line, cyclomatic, max_nesting]
    
    i=0
    for version in versions:
        metrics_file_base = "/".join([s.und_out_dir, project, version])
        metrics_method_file = metrics_file_base + ".method-level.product.csv"
                
        # case313_line1178(java.lang.Object, java.lang.Object[], int) => case313_line1178(Object, Object[], int)
        method_sig = re.sub( r'[a-zA-Z0-9]*\.','',function_signature) 
        method_sig = re.sub( r'<.*?>', '', method_sig)
        # case313_line1178(Object, Object[], int) => case313_line1178(Object,Object[],int)
        method_sig = method_sig.replace(' ','')
        
        ###TODO
        #method_sig = ".".join([class_name, method_sig])
        print "    " + version +  ":" + method_sig
        
        tmp_f2 = open(metrics_method_file)
        f2 = csv.DictReader(tmp_f2)
        
        for line in f2:
            temp_method_sig = line[u'Name']
            temp_method_sig = temp_method_sig.replace('...','[]')
            
            # same method name
            if method_sig == temp_method_sig:
                if i == 0: # for introduced
                    count_input.introduce = line[u'CountInput']
                    count_output.introduce = line[u'CountOutput']
                    count_line.introduce = line[u'CountLine']
                    cyclomatic.introduce = line[u'Cyclomatic']
                    max_nesting.introduce = line[u'MaxNesting']
                    
                if i == 1: # for last found
                    count_input.last_found = line[u'CountInput']
                    count_output.last_found = line[u'CountOutput']
                    count_line.last_found = line[u'CountLine']
                    cyclomatic.last_found = line[u'Cyclomatic']
                    max_nesting.last_found = line[u'MaxNesting']
        
        tmp_f2.close()
    return [count_input, count_output, count_line, cyclomatic, max_nesting]

if __name__ == "__main__":
    print "main"