import subprocess
import psycopg2

print 'dumping temporary database'
subprocess.call("pg_dump -Fc -Uevermal comment_classification > /Users/evermal/Downloads/technical_debt_summary_temp.dump", shell= True)

connection = None
connection = psycopg2.connect(host='localhost', port='5432', database='comment_classification', user='evermal', password='')
cursor = connection.cursor()

print 'selecting directories names to be updated'
cursor.execute("select file_directory, version_introduced_file_directory, last_version_that_comment_was_found_file_directory, processed_comment_id from technical_debt_summary")
technical_debt_summary_resulst = cursor.fetchall()

for line in technical_debt_summary_resulst:
    file_directory =  line[0]
    version_introduced_file_directory = line[1]
    last_version_that_comment_was_found_file_directory = line[2]
    processed_comment_id = line[3]

    if file_directory is not None:
        file_directory =  file_directory.replace('/Users/evermal/git/msr16_td_interest/tags/ant_tags/', '').replace('/Users/evermal/git/msr16_td_interest/tags/jmeter_tags/', '').replace('/Users/evermal/git/msr16_td_interest/tags/jruby_tags/', '')
    else:
        file_directory = ''

    if version_introduced_file_directory is not None:
        version_introduced_file_directory =  version_introduced_file_directory.replace('/Users/evermal/git/msr16_td_interest/tags/ant_tags/', '').replace('/Users/evermal/git/msr16_td_interest/tags/jmeter_tags/', '').replace('/Users/evermal/git/msr16_td_interest/tags/jruby_tags/', '')
    else:
        version_introduced_file_directory = ''

    if last_version_that_comment_was_found_file_directory is not None:
        last_version_that_comment_was_found_file_directory = last_version_that_comment_was_found_file_directory.replace('/Users/evermal/git/msr16_td_interest/tags/ant_tags/', '').replace('/Users/evermal/git/msr16_td_interest/tags/jmeter_tags/', '').replace('/Users/evermal/git/msr16_td_interest/tags/jruby_tags/', '')
    else:
        last_version_that_comment_was_found_file_directory = ''

    # print "update technical_debt_summary set file_directory = '"+file_directory+"', version_introduced_file_directory = '"+version_introduced_file_directory+"', last_version_that_comment_was_found_file_directory = '"+last_version_that_comment_was_found_file_directory+"' where processed_comment_id = '"+str(processed_comment_id)+"'"
    cursor.execute("update technical_debt_summary set file_directory = '"+file_directory+"', version_introduced_file_directory = '"+version_introduced_file_directory+"', last_version_that_comment_was_found_file_directory = '"+last_version_that_comment_was_found_file_directory+"' where processed_comment_id = '"+str(processed_comment_id)+"'")

connection.commit()


print 'creating csv file'
cursor.execute("copy (select * from technical_debt_summary) to '/Users/evermal/git/msr16_td_interest/data/CSV/technical_debt_summary.csv' (format csv,  header true)")
cursor.execute("copy (select * from tags_information) to '/Users/evermal/git/msr16_td_interest/data/CSV/tags_information.csv' (format csv,  header true)")
connection.close()

print 'restoring database'
subprocess.call("pg_restore -Uevermal -dcomment_classification -c /Users/evermal/Downloads/technical_debt_summary_temp.dump", shell= True)