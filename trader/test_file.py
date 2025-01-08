import pandas as pd

# Read the CSV file
df = pd.read_csv('your_csv_file.csv', sep='\t', quotechar='"')

# Debugging output
print(df.head())  # Check first few rows
print(df.columns)  # Check column names

# Process trades in pairs only if 'type' column exists
if 'type' in df.columns:
    for i in range(0, len(df), 2):
        if i + 1 < len(df):
            row1 = df.iloc[i]
            row2 = df.iloc[i + 1]

            #if row1['type'] == 'trade' and row2['type'] == 'trade':
                # Existing processing logic...
else:
    print("Error: 'type' column is missing from the data.")
