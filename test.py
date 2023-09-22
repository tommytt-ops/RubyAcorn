import pandas as pd

# Read the CSV file
df = pd.read_csv('./python/player_count_time.csv', delimiter='\t')

# Identify the columns for 'Date' and 'Time'
date_column = df.columns[df.columns.str.lower().str.contains('date')][0]
time_column = df.columns[df.columns.str.lower().str.contains('time')][0]

# Reshape the DataFrame using pd.melt
melted_df = pd.melt(df, id_vars=[date_column, time_column], var_name='Game', value_name='Value')

# Now, melted_df will have columns for Date, Time, Game, and Value
melted_df.to_csv('new_file.csv', index=False)
