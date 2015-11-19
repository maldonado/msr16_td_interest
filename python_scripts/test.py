# import difflib
import distance
import os
import sys
import psycopg2
 
# file_name_path = '/Users/evermal/git/msr16_td_interest/tags/ant_tags/53.ANT_170/src/src/main/org/apache/tools/ant/taskdefs/AbstractCvsTask.java'
# compared_file_name_path = '/Users/evermal/git/msr16_td_interest/tags/ant_tags/23.ANT_15_B1/src/src/main/org/apache/tools/ant/taskdefs/AbstractCvsTask.java'
# compared_file_name_path = '/Users/evermal/git/msr16_td_interest/tags/ant_tags/53.ANT_170/src/src/main/org/apache/tools/bzip2/BZip2Constants.java'
compared_file_name_path = '/Users/evermal/git/msr16_td_interest/tags/ant_tags/53.ANT_170/src/src/main/org/apache/tools/ant/taskdefs/AntStructure.java'

# comment = "// XXX: we should use JCVS (www.ice.com/JCVS) instead of // command line execution so that we don't rely on having // native CVS stuff around (SM)"

connection = None

# connect to the database to retrieve the file name linked with the commit
connection = psycopg2.connect(host='localhost', port='5432', database='comment_classification', user='evermal', password='')
cursor = connection.cursor()

def parse_line_comment (comment):
    result = []
    for line in comment.split('//'):
        if '' is not line:
            result.append(('//'+line).strip())
    return result

def parse_block_comment (comment):
    result = []
    for line in comment.split('\n'):
        new_line = (line.replace('/**', '').replace('*/', '').replace('/*', '')).strip()
        if '' is not new_line:
            result.append(new_line)
    return result

cursor.execute("select comment_type, comment_text from technical_debt_summary where comment_type = 'BLOCK' limit 1")
results = cursor.fetchall()

for result in results:
    comment_type =  result[0]
    comment_text =  result[1]
    # print comment_text

    if 'MULTLINE' == comment_type or 'LINE' == comment_type:
        comment = parse_line_comment(comment_text)
        # print comment
    else:
        comment = parse_block_comment(comment_text)
        # print comment

    with open (compared_file_name_path,'r') as f:
        comment_index = 0
        comment_distance_threshold = 0
        comment_total_distance = 0
        java_file = []
        for line in f:
            value = distance.levenshtein(comment[comment_index], line.strip())
            # print str(value)+' - '+line 
            if value < 10:
                print str(value)+' - '+line 
                comment_total_distance = comment_total_distance + value
                comment_index = comment_index + 1
                if comment_index == len(comment):
                    break
            
    # print comment_total_distance





# with open (compared_file_name_path,'r') as f:
#     counter = 1
#     java_file = []
#     for line in f:
        # java_file.append((str(counter)+'.- '+line))
        # counter = counter + 1

# file_with_line_number = ''.join(java_file)




# print ''.join(java_file)

# with open (file_name_path,'r') as f:
#     analyzed_version_file  = f.read()

# with open (compared_file_name_path) as f:
#     other_version_file = f.read()

# print analyzed_version_file

# lines2 = '''
# cat
# dog
# bird
# buffalo
# gopher
# horse
# mouse
# '''.strip().splitlines()

# # Changes:
# # swapped positions of cat and dog
# # changed gophers to gopher
# # removed hound
# # added mouse

# for line in difflib.unified_diff(analyzed_version_file.splitlines(1), other_version_file.splitlines(1), fromfile='file1', tofile='file2', n=0):
#     print line



