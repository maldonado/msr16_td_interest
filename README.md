# Directory structure
HOME  
- /python_scripts   
    - *.py  
- /datasets  
    - CSV/classification/
        - all_automated_classification.csv
            - $sh merge.sh to genarete it from each project classification.csv  
        - [PROJECT_NAME]_automated_classification.csv
            - new datasets provided by Everton
    - CSV/
        - comments.csv
            - includes git comments
            - it's now unclear how we got
            - I guess git_comments.py
        - interest.ssv
            - includes all metrics to compute interst
            - the output of run.py 
- /tags  
     - ant_tags  
     - jmeter_tags    
- /revs  
     - ant_tags  
     - jmeter_tags  
- /r_scritps  

# How to execute scripts
- run.py executes the following python scripts
- setting.py indluces directory information

## To obtain a snapshot of each revesion for the tool "understand"
- 0. checkRevisions.py
- 1. runUND.py 
- 2. extract_metrics_at_method_level.py
    - it formats data that is provided by understand
- 3. link_SATD_to_UND.py
- 4. *.r

## to conduct an analysis on RQ3
1. git_comments.py
2. 

# branch
- tda is a branch for tda paper
- new_dataformat is a branch for new data format
- if we want to go back to work on old data format, please checkout tag/OLD_DATA