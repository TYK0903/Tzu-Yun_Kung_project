import pandas as pd

# Read the CSV file
df = pd.read_csv('/Users/kungtzuyun/Lab/ACTI/psychopy_data/behavior_analysis_data/All_VRIT_beh.csv', delimiter=',')

# Replace missing values with 'NA'
df = df.fillna('NA')

# Save the modified dataframe back to CSV
df.to_csv('ACIT_all_clean_modified.csv', index=False)

print("Missing values replaced with 'NA' and saved to new CSV file")