import pandas as pd
import matplotlib.pyplot as plt


# Renaming datasets columns
def renaming_columns(df, new_names):
    df = df.rename(columns=new_names)
    return df

# Load the dataset and filter out firms with incomplete records from 2011 to 2020.
def load_and_preprocess_data(filepath):
    data = pd.read_csv(filepath)

    # Convert 'EndDate' to datetime type
    data['EndDate'] = pd.to_datetime(data['EndDate'])

    # Extract year from 'EndDate' and create a new column 'Year'
    data['Year'] = data['EndDate'].dt.year

    # Filter rows for years within 2010 to 2020
    data = data[(data['Year'] >= 2010) & (data['Year'] <= 2020)]

    # Change column names
    data = renaming_columns(
        data, {"Symbol": "Stock_Codes", "ROEC": "Annual_ROE", "TotalRevenue": "Total_Revenue"}
    )
    
    # Drop rows with missing values in 'Annual_ROE' and 'Total_Revenue'
    data.dropna(subset=['Annual_ROE', 'Total_Revenue'], inplace=True)
    
    # Filter firms with complete records from 2010 to 2020
    complete_firms = data.groupby('Stock_Codes').filter(lambda x: set(x['Year']) == set(range(2010, 2021)))

    return complete_firms

# Calculate the annual median ROE and the revenue growth rate for each year.
def calculate_metrics(data):
    
    median_roe = data.groupby('Year')['Annual_ROE'].median()
    
    data.sort_values(by=['Stock_Codes', 'Year'], inplace=True)
    data['Total_Revenue_Growth_Rate'] = data.groupby('Stock_Codes')['Total_Revenue'].pct_change().fillna(0) * 100
    return median_roe, data

# Analyze the data to find percentages of firms consistently maintaining above-median metrics and plot the results.
def analyze_and_plot(data, median_roe):
    years = list(range(2010, 2021))
    all_firms = set(data['Stock_Codes'].unique())
    
    # Initialize with all firms for 2011, then update based on performance
    consistent_outperformers_roe = all_firms.copy()
    consistent_outperformers_growth = all_firms.copy()
    percent_above_median_roe = [50]
    percent_above_growth_rate = [50]

    for year in years[1:]:  # Start analysis from 2011
        # Median calculations for ROE and Growth
        median_roe_for_year = median_roe.loc[year]
        # Recalculate median growth rate for year directly from filtered data to ensure accuracy
        median_growth_rate_for_year = data[data['Year'] == year]['Total_Revenue_Growth_Rate'].median()

        # Outperformers for the year
        current_year_outperformers_roe = set(data[(data['Year'] == year) & (data['Annual_ROE'] > median_roe_for_year)]['Stock_Codes'])
        current_year_outperformers_growth = set(data[(data['Year'] == year) & (data['Total_Revenue_Growth_Rate'] > median_growth_rate_for_year)]['Stock_Codes'])

        # Update consistent outperformers
        consistent_outperformers_roe &= current_year_outperformers_roe
        # Update logic to correctly maintain growth outperformers set
        consistent_outperformers_growth &= current_year_outperformers_growth

        # Update percentages
        percent_above_median_roe.append(len(consistent_outperformers_roe) / len(all_firms) * 100)
        percent_above_growth_rate.append(len(consistent_outperformers_growth) / len(all_firms) * 100)

    plt.figure(figsize=(12, 6))
    plt.plot(years, percent_above_median_roe, label='Percentage of Firms Consistently Above Median ROE', marker='o')
    plt.plot(years, percent_above_growth_rate, label='Percentage of Firms Consistently Above Median Revenue Growth', marker='x')
    plt.title('Percentage of Firms Consistently Outperforming Market Median Over Time')
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.ylim(0, 50)  # Ensure y-axis starts from 0 to avoid negative values
    plt.xticks(years[1:])  # Ensure all years are displayed
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    filepath = '/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/raw_data/problem3_data.csv'
    data = load_and_preprocess_data(filepath)
    median_roe, data_with_growth = calculate_metrics(data)
    analyze_and_plot(data_with_growth, median_roe)
    
    print("Success.")



if __name__ == "__main__":
    main()
