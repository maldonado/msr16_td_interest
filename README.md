# msr16_td_interest
HOME  
 |- python_scripts   
 |  |- *.py  
 |  
 |- datasets  
 |   |- CSV/technical_debt_summary.csv  
 |  
 |- tags  
 |   | - ant_tags  
 |   | - jmeter_tags  
 |
 |- revs  
 |   | - ant_tags  
 |   | - jmeter_tags  
 | 
 |- r_scritps  

run.sh to run the following steps

# To obtain a snapshot of each revesion for the tool "understand"
0. checkRevisions.py
1. runUND.py
# 
2. extract_metrics_at_method_level.py
3. calculate_interests.py
4. *.r

# to conduct an analysis on RQ3
1. git_comments.py
2. 