import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/filtered_CSI-300')

df = df.dropna()

df['Trddt'] = pd.to_datetime(df['Trddt'])

df.set_index('Trddt', inplace=True)

monthly_data = df['Clsindex'].resample('ME').last()

monthly_returns = monthly_data.pct_change() * 100

summary_stats = monthly_returns.describe()
skewness = monthly_returns.skew()
kurtosis = monthly_returns.kurtosis()

summary_stats['skewness'] = skewness
summary_stats['kurtosis'] = kurtosis

print(summary_stats)

plt.figure(figsize=(10, 6))
plt.hist(monthly_returns, bins=20, color='blue', alpha=0.7)
plt.title('Histogram of CSI-300 Monthly Returns')
plt.xlabel('Monthly Returns')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

df.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/processed_CSI-300', index=False)

print("Processing completed.")