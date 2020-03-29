"""TODO: Documentation"""

import pandas as pd 
from init_database import db

table = pd.read_csv("Sample Data 17_FA.csv")

print(len(table.index))
# read CSV
# for each row
# --> get info from row
# --> create student from row
# commit to db