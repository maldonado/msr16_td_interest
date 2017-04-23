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

class NonSATD:
    def __init__(self):
        self.project_name = -1
        self.intro_version_name = ""
        self.last_version_name = ""
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
        return sep.join([str(self.project_name), str(self.intro_version_name), str(self.last_version_name), str(self.long_file_name), str(self.count_input_introduce), str(self.count_input_last_found), str(self.count_output_introduce), str(self.count_output_last_found),
                         str(self.count_line_introduce), str(self.count_line_last_found), str(self.cyclomatic_introduce), str(self.cyclomatic_last_found), str(self.max_nesting_introduce), str(self.max_nesting_last_found)])

    def out_all_with_key(self, key, sep="#"):
        return sep.join([str(self.project_name), key, str(self.intro_version_name), str(self.last_version_name), str(self.long_file_name), str(self.count_input_introduce), str(self.count_input_last_found), str(self.count_output_introduce), str(self.count_output_last_found),
                         str(self.count_line_introduce), str(self.count_line_last_found), str(self.cyclomatic_introduce), str(self.cyclomatic_last_found), str(self.max_nesting_introduce), str(self.max_nesting_last_found)])

# non-SATD
class NonSATDManeger():
    def __init__(self):
        self.list = {}
           
    def add_introduce_version(self, key, project_name, version, long_file_name, count_input, count_output, count_line, cyclomatic, max_nesting):
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
                    if self.list[key].long_file_name != "src/main/org/apache/tools/ant/ComponentHelper.java":
                        print "not duplicate@intro "  + key
                        print "   " + self.list[key].long_file_name + " v.s. " + long_file_name
        else:
            m = NonSATD()
            m.project_name = project_name
            m.intro_version_name = version
            m.long_file_name = long_file_name
            m.count_input_introduce = count_input
            m.count_output_introduce = count_output
            m.count_line_introduce = count_line
            m.cyclomatic_introduce = cyclomatic
            m.max_nesting_introduce = max_nesting
            self.list[key] = m            
            
    def add_last_version(self, key, version, long_file_name, count_input, count_output, count_line, cyclomatic, max_nesting):
        if self.list.has_key(key):
            m = self.list.get(key)
            if m.count_input_last_found == -1:
                m.last_version_name = version
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
                    if self.list[key].long_file_name != "src/main/org/apache/tools/ant/types/resources/StringResource.java":
                        print "not duplicate@last "  + key
                        print "   " + self.list[key].long_file_name + " v.s. " + long_file_name

def link_SATD_to_UND(project, versions, file_names, function_signatures):
    print "--"
    print project
    print versions
    print file_names
    print function_signatures
    print "--"
    
    count_input = Metrics()
    count_output = Metrics()
    count_line = Metrics()
    cyclomatic = Metrics()
    max_nesting = Metrics()
        
    i=0
    for version in versions:
        metrics_file_base = "/".join([s.und_out_dir, project, version])
        metrics_method_file = metrics_file_base + ".method-level.product.csv"
        file_name  = file_names[i] # proposal/myrmidon/src/java/org/apache/ant/util/Condition.java
        class_name = file_name.replace(".java","") #Condition
        class_name = class_name.split('/')
        class_name = class_name[(len(class_name)-1)]
        method_sig = class_name + "."
        if function_signatures[i] != "()":
            method_sig = method_sig + function_signatures[i]
        else:
            method_sig = method_sig + function_signatures[0]
        
        method_sig = re.sub(r'<.*?>','',method_sig) # add this cleaning for Everton's data since Understand does not have <String> in method sig.

        print "    P2: " + version +  ":" + method_sig
                
        tmp_f2 = open(metrics_method_file)
        f2 = csv.DictReader(tmp_f2)
        
        for line in f2:
            if file_name != line[u'File']:
                # not strict for the path
                if (not (file_name in line[u'File'])) and (not (line[u'File'] in file_name)):
                    continue
                        
            #org.apache.tools.ant.ComponentHelper.addDataTypeDefinition(String,Class)
            #ComponentHelper.addDataTypeDefinition(String,Class)
            temp_method_sig = line[u'Name']
            temp_method_sig = temp_method_sig.replace('...','[]')
            match = re.search(r'.*\.(.*\..*\(.*\))', temp_method_sig)
            if match:
                temp_method_sig = match.group(1)
                                        
            # same method name
            if method_sig == temp_method_sig:
                print i
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
        i = i + 1        
    return [count_input, count_output, count_line, cyclomatic, max_nesting]

def link_NON_SATD_to_UND(project, versions, file_names, function_signatures):
    print "--"
    print project
    print versions
    print file_names
    print function_signatures
    print "--"
                
    i=0
    non_satd = NonSATDManeger()
    for version in versions:
        metrics_file_base = "/".join([s.und_out_dir, project, version])
        metrics_method_file = metrics_file_base + ".method-level.product.csv"
        file_name  = file_names[i] # proposal/myrmidon/src/java/org/apache/ant/util/Condition.java
        class_name = file_name.replace(".java","") #Condition
        class_name = class_name.split('/')
        class_name = class_name[(len(class_name)-1)]
        method_sig = class_name + "."
        if function_signatures[i] != "()":
            method_sig = method_sig + function_signatures[i]
        else:
            method_sig = method_sig + function_signatures[0]
        
        method_sig = re.sub(r'<.*?>','',method_sig) # add this cleaning for Everton's data since Understand does not have <String> in method sig.

        print "    P2: " + version +  ":" + method_sig
                
        tmp_f2 = open(metrics_method_file)
        f2 = csv.DictReader(tmp_f2)
        
        for line in f2:
            if file_name != line[u'File']:
                # not strict for the path
                if (not (file_name in line[u'File'])) and (not (line[u'File'] in file_name)):
                    continue
            
            if (line[u'File'] == "Kind"):
                continue
                        
            #org.apache.tools.ant.ComponentHelper.addDataTypeDefinition(String,Class)
            #ComponentHelper.addDataTypeDefinition(String,Class)
            temp_method_sig = line[u'Name']
            temp_method_sig = temp_method_sig.replace('...','[]')
            match = re.search(r'.*\.(.*\..*\(.*\))', temp_method_sig)
            if match:
                temp_method_sig = match.group(1)
                                        
            # not same method name
            if method_sig != temp_method_sig:
                key_filename = file_name # metrics_line[2] is directory name + file name. Even if file name is same, but directory name is changed.
                key_filename = key_filename.split("/")
                key_filename = key_filename[(len(key_filename)-1)] #just use file name
                key = temp_method_sig + "@" + key_filename
                
                if i == 0: # for introduced
                    non_satd.add_introduce_version(key, project, version, file_name, line[u'CountInput'], line[u'CountOutput'], line[u'CountLine'], line[u'Cyclomatic'], line[u'MaxNesting'])
                if i == 1: # for last found
                    non_satd.add_last_version(key, version, file_name, line[u'CountInput'], line[u'CountOutput'], line[u'CountLine'], line[u'Cyclomatic'], line[u'MaxNesting'])        
        tmp_f2.close()
        i = i + 1

    # TODO: will return list
    return non_satd

if __name__ == "__main__":
    #project = "ant"
    #versions = ['7ac63c0bc264d9192d38abf2c1f2302c8fdee8f6', 'b30d297b23a82a97aea0cdd308239e2c05050341']
    #file_names = ['src/main/org/apache/tools/ant/taskdefs/Zip.java', 'src/main/org/apache/tools/ant/taskdefs/Zip.java']
    #function_signatures = ['setWhenempty(String)', 'setWhenempty(String)']

    # 3 samples are due to method signature pattern (we can fix)
    #project = "ant"
    #versions = ['af9325e41e16da1e00cc88f29e6b9f3d96006805', 'bed22b00f729da46ea6ed768d5f30014d919bcc6']
    #file_names = ['src/main/org/apache/tools/ant/PropertyHelper.java', 'src/main/org/apache/tools/ant/PropertyHelper.java']
    #function_signatures = ['parsePropertyStringDefault(String,Vector,Vector)', 'parsePropertyStringDefault(String,Vector<String>,Vector<String>)']

    project = "ant"
    versions = ['74f58bf0f81de6bc03df6bc1d5315bef92d8f0e4', '51ce8fac7296500ba974ee639616c82475b4f171']
    file_names = ['src/main/org/apache/tools/ant/helper/ProjectHelper2.java', 'src/main/org/apache/tools/ant/helper/ProjectHelper2.java']
    function_signatures =['onStartElement(String,String,String,Attributes,AntXMLContext)', 'onStartElement(String,String,String,Attributes,AntXMLContext)']

    project = "ant"
    versions = ['ee344eb12509b4a69af0d52f285bbd7230f2c556', 'bf6026a147e879837eaad2a16348ae2162829867']
    file_names = ['src/main/org/apache/tools/ant/taskdefs/optional/Cab.java', 'src/main/org/apache/tools/ant/taskdefs/optional/Cab.java']
    function_signatures = ['checkConfiguration()', '()']

    print "--"
    print project
    print versions
    print file_names
    print function_signatures
    print "--"
    
    link_SATD_to_UND(project, versions, file_names, function_signatures)