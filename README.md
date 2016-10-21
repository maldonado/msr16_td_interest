# Directory structure
HOME  
- /python_scripts   
    - *.py  
- /datasets  
    - CSV/technical_debt_summary.csv  
- /tags  
     - ant_tags  
     - jmeter_tags    
- /revs  
     - ant_tags  
     - jmeter_tags  
- /r_scritps  

# How to execute scripts
## To obtain a snapshot of each revesion for the tool "understand"
0. checkRevisions.py
1. runUND.py
## format data provided by understand
2. extract_metrics_at_method_level.py
3. calculate_interests.py
4. *.r

## to conduct an analysis on RQ3
1. git_comments.py
2. 

# branch
- tda is a branch for tda paper
- new_dataformat is a branch for new data format
- if we want to go back to work on old data format, please checkout tag/OLD_DATA