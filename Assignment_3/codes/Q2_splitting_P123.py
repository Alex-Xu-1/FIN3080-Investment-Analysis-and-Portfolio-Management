import pandas as pd


processed_weekly_returns = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/processed_weekly_returns.csv')
merged_weekly_market_rf = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/merged_weekly_market_rf.csv')

#merge the merged_weekly_market_rf with processed_weekly_returns on year_week
merged_general = pd.merge(processed_weekly_returns, merged_weekly_market_rf, on='year_week')
merged_general.dropna()

#create two new columns
merged_general['ri_rf'] = merged_general['weekly_stock_return'] - merged_general['weekly_rf_rate']
merged_general['rm_rf'] = merged_general['weekly_mkt_return'] - merged_general['weekly_rf_rate']

#split the merged general into three different datasets based on time: [2017-01, 2018-52], [2019-01, 2020-52], [2021-01, 2022-52]
P1 = merged_general[merged_general['year_week'].between('2017-01', '2018-52')]
P2 = merged_general[merged_general['year_week'].between('2019-01', '2020-52')]
P3 = merged_general[merged_general['year_week'].between('2021-01', '2022-52')]


merged_general.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/merged_general.csv', index=False)
P1.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P1.csv', index=False)
P2.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P2.csv', index=False)
P3.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P3.csv', index=False)
print("Processing completed.")