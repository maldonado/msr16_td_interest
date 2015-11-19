-- 1
drop table if exists technical_debt_summary;
CREATE TABLE technical_debt_summary (
  project_name  text,
  version_name  text, 
  version_hash  text,
  file_name     text,
  file_directory text, 
  class_id      integer, 
  class_name    text,
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
  version_introduced_hash text, 
  version_introduced_dependencies_number  integer, 
  version_removed_hash    text,
  version_removed_dependencies_number  integer
);

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
-- run link_tags.py in each git repository

-- 5
update technical_debt_summary set comment_classification = 'REQUIREMENT' where comment_classification = 'IMPLEMENTATION';
update technical_debt_summary set version_name = 'ANT_170', version_hash = '' where comment_classification = 'IMPLEMENTATION';


-- 6
copy (select * from technical_debt_summary) to '/Users/evermal/Downloads/technical_debt_summary.csv' (format csv,  header true);

