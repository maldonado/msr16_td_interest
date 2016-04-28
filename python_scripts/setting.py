home_dir = '/Users/kamei/Research/techdebt/msr16_td_interest'
debt_file = home_dir + '/datasets/CSV/classification/all_automated_classification.csv'
#debt_file = home_dir + '/datasets/CSV/technical_debt_summary_test.csv'
und_out_dir = home_dir + '/und'
perl  = '/Users/kamei/Research/src/metrics_posl/runUND.pl'
metrics_columns = ["Kind", "Name", "File", "CountInput", "CountLine", "CountLineBlank", "CountLineCodeDecl", "CountLineComment", "CountOutput", "CountSemicolon", "CountStmt", "CountStmtDecl", "CountStmtExe", "Cyclomatic", "CyclomaticModified", "CyclomaticStrict", "Essential", "MaxNesting", "RatioCommentToCode"]
comment_file = home_dir + '/datasets/CSV/comments.csv'
MAX_LOOP=5