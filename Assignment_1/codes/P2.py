import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read in the dataset
# Note that this is the output dataset (ready_for_further_analyze.csv) from the P1_analyzing_outputting.py, we leverage it to use it in Problem 2.
df = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/output/ready_for_further_analyze.csv')

# Convert 'Trade_Month' to datetime for proper grouping
df['Trade_Month'] = pd.to_datetime(df['Trade_Month'])

# Categorize each stock into 'Main Board' or 'GEM Board' based on 'Market_Type'
df['Board_Categorization'] = df['Market_Type'].apply(lambda x: 'Main_Board' if x in [1, 4, 64] else 'GEM_Board' if x in [16, 32] else 'Unknown')

# Grouping by Board Categorization and Trade Month, then calculating median P/E Ratio
pe_ratios_median = df.groupby(['Board_Categorization', df['Trade_Month'].dt.to_period('M')])['Monthly_P/E_Ratio'].median().reset_index()

# Converting Trade_Month back to datetime for plotting
pe_ratios_median['Trade_Month'] = pe_ratios_median['Trade_Month'].dt.to_timestamp()

# Plotting the two time-series for each board categorization
plt.figure(figsize=(14, 7))
sns.lineplot(data=pe_ratios_median, x='Trade_Month', y='Monthly_P/E_Ratio', hue='Board_Categorization')
plt.title('Median P/E Ratio by Board Categorization Over Time')
plt.xlabel('Month')
plt.ylabel('Median P/E Ratio')
plt.legend(title='Board Categorization')
plt.grid(True)
plt.show()

print("The two time-series plot of the median P/E ratio by market type over time has been successfully created.")
