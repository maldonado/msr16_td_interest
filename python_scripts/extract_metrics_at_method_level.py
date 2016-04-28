import setting as s
import os
import csv
import pandas as pd

def extract_metrics (project, version, count=0, reuse=True):
    metrics_file_base = "/".join([s.und_out_dir, project, version])
    metrics_file = metrics_file_base + ".product.csv"
    metrics_method_file = metrics_file_base + ".method-level.product.csv"
    
    if reuse and os.path.exists(metrics_method_file):
        print str(count) + ': (reused) ' + metrics_method_file
        return 0
    
    print str(count) + ':' + metrics_method_file

    # only method level            
    f2 = pd.read_csv(metrics_file)
    f3 = open(metrics_method_file, 'w')
    csvWriter  = csv.writer(f3)
                
    csvWriter.writerow(s.metrics_columns)
    for index, row in f2.iterrows():
        if row["Kind"] == 'Public Implicit Method':
            continue
        
        if 'Method' in row["Kind"]:
            tmp = row[s.metrics_columns]
            csvWriter.writerow(tmp)
    f3.close()

if __name__ == "__main__":
    project = ""
    version = ""
                
    extract_metrics(project, version)