-- 1
drop table if exists technical_debt_summary;
CREATE TABLE technical_debt_summary (
  project_name   text,
  version_name   text, 
  version_hash   text,
  file_name      text,
  class_id       integer, 
  class_name     text,
  class_access   text,
  is_class_abstract   text,
  is_class_enum       text,
  is_class_interface  text,
  class_start_line integer, 
  class_end_line   integer,
  processed_comment_id integer, 
  comment_location text,
  comment_type     text, 
  function_signature text,
  comment_start_line integer,
  comment_end_line   integer,
  comment_classification text,
  comment_text text,
  version_introduced_name text, 
  version_introduced_hash text,
  version_introduced_dependencies_number  integer, 
  version_removed_name    text, 
  version_removed_hash    text,
  last_version_that_comment_was_found_name text,
  last_version_that_comment_was_found_hash text,
  last_version_that_comment_was_found_dependencies_number text
);

alter table technical_debt_summary add column version_introduced_commit_hash text;
alter table technical_debt_summary add column version_introduced_author text;
alter table technical_debt_summary add column version_introduced_lines text;
alter table technical_debt_summary add column version_removed_commit_hash text;
alter table technical_debt_summary add column version_removed_author text ;
alter table technical_debt_summary add column version_removed_lines text;
alter table technical_debt_summary add column last_version_that_comment_was_found_lines text;


-- 2
insert into technical_debt_summary (project_name, file_name, class_id, class_name, class_access, is_class_abstract, is_class_enum, is_class_interface, class_start_line, class_end_line, processed_comment_id, comment_location, comment_type, function_signature,comment_start_line,comment_end_line,comment_classification,comment_text) 
    select b.projectname, b.filename, b.id , b.classname, b.access, b.isabstract, b.isenum, b.isinterface, b.startline, b.endline, a.id, a.location, a.type, a.description,   a.startline, a.endline, a.classification , a.commenttext from processed_comment a , comment_class b where a.commentclassid = b.id and b.projectname in ('apache-ant-1.7.0','apache-jmeter-2.10','jruby-1.4.0') and a.classification not in ('WITHOUT_CLASSIFICATION', 'BUG_FIX_COMMENT') order by 1, 2, 4,  9, 5;

-- 3
drop table if exists tags_information;
CREATE TABLE tags_information (
  project_name text, 
  version_name text,
  version_hash text,
  version_date timestamp without time zone, 
  version_order numeric
);

-- 4 
--(18, november 2015 21:23)
-- for some reasson the old tags that I had before was not matching if the current tags (even old ones), so I ran the tag extactor again. 
-- run populate_tags_information.py in each git repository

-- 5
update technical_debt_summary set comment_classification = 'REQUIREMENT' where comment_classification = 'IMPLEMENTATION';
update technical_debt_summary set project_name = 'apache-ant' where project_name = 'apache-ant-1.7.0';
update technical_debt_summary set version_name = 'ANT_170', version_hash = '6bfe7759b0d7662f764a6efd97436b48aa74da2a' where project_name = 'apache-ant';
update technical_debt_summary set project_name = 'apache-jmeter' where project_name = 'apache-jmeter-2.10';
update technical_debt_summary set version_name = 'v2_10', version_hash = '05e19dd900305b43296a89a8fbbd4669b987546b' where project_name = 'apache-jmeter';
update technical_debt_summary set project_name = 'jruby' where project_name = 'jruby-1.4.0';
update technical_debt_summary set version_name = '1.4.0', version_hash = '69fbfa336591fb1a65d4000556b3fedda30baf8f' where project_name = 'jruby';

--6
drop table if exists file_directory_per_version;
CREATE TABLE file_directory_per_version (
  project_name text, 
  version_name text,
  version_hash text,
  version_order text,
  file_name text,
  file_directory text, 
  matched_analyzed_file_directory text
);

--7
alter table file_directory_per_version add column repository_directory text;

--8
drop table if exists file_blame_per_version;
CREATE TABLE file_blame_per_version (
  project_name text, 
  version_name text,
  version_hash text,
  version_order text,
  file_name text,
  file_directory text, 
  commit_short_hash text,
  author_name text,
  author_date timestamp with time zone,
  file_line numeric,
  line_content text
);

create index CONCURRENTLY idx_version_hash_file_name on file_blame_per_version (version_hash, file_name);

-- aux --
pg_dump -Fc -Uevermal comment_classification > ~/Downloads/technical_debt_summary_investigation.dump

-- create script to clean the file directory before copying the csv file
copy (select * from technical_debt_summary) to '/Users/evermal/Downloads/technical_debt_summary.csv' (format csv,  header true);


with temp as (
  select file_directory, version_introduced_name, version_introduced_hash, version_introduced_file_directory, version_removed_name,version_removed_hash,version_removed_file_directory,last_version_that_comment_was_found_name,last_version_that_comment_was_found_hash,last_version_that_comment_was_found_file_directory,last_version_that_comment_was_found_dependencies_number, processed_comment_id
    from technical_debt_summary_temp   
  )
update technical_debt_summary set file_directory = t.file_directory, version_introduced_name = t.version_introduced_name, version_introduced_hash = t.version_introduced_hash, version_introduced_file_directory = t.version_introduced_file_directory, version_removed_name = t.version_removed_name,version_removed_hash = t.version_removed_hash,version_removed_file_directory = t.version_removed_file_directory,last_version_that_comment_was_found_name = t.last_version_that_comment_was_found_name,last_version_that_comment_was_found_hash = t.last_version_that_comment_was_found_hash,last_version_that_comment_was_found_file_directory = t.last_version_that_comment_was_found_file_directory   from temp t where t.processed_comment_id = technical_debt_summary.processed_comment_id;

update technical_debt_summary set version_introduced_name  = null, version_introduced_hash = null, version_removed_name = null, version_removed_hash = null, last_version_that_comment_was_found_name = null, last_version_that_comment_was_found_hash = null;

select * from file_directory_per_version where version_hash = '92dd8b805b5fc4ae4821ad9713840a99bc0ff2eb' and file_name = 'RubyIO.java';

select * from file_directory_per_version where file_name ='IR_Builder.java';

regex to parse blame files
-- 


