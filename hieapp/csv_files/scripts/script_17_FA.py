"""TODO: Documentation"""

import pandas as pd 

# Read the CSV file as table, using the first row as the names for the table
table = pd.read_csv("Sample Data 17_FA.csv", header=0)

# Prints that no errors occured
print("table read correctly")

print(table.head())

# For every row in the CSV, call createStudent from init_database.py

# class, su_id, sex, pell_flag, first_gen_flag, first_race, second_race, 
# hie_type, hie_name, hie_course_number, london_flag, dc_flag, city_name, country_name, hie_term, hie_year, 
# fys_flag, fys_aes_term, fys_aes_year, graduated, grad_term, grad_year

# Included in csv: su_id, sex, first_race, first_gen_flag, fys_flag, (aes_flag), pell_flag
# Remove the (aes_flag) from table

#table.drop(index=0) Not working yet

# Ensure that the correct column was dropped
print(table.head())