import pandas as pd
import numpy as np


# Read in the merged_dataset
# The merged_dataset is the output of the P1_processing.py script
# Note that the merged_dataset.csv file should be in the processing folder
# Note that the column[date_yq] is actually lagged for 1 quarter, details in the P1_processing.py script line 162
df = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/processing/merged_dataset.csv')


def monthly_P_E_ratios(df):
    # Creating a new column "Monthly_P/E_ratios" by dividing the "Monthly_Stock_Price" by the "EPS" (quarterly Earnings per Share) and then divide by 3
    # Calculate the P/E ratio, handling cases where EPS is zero or missing
    df['Monthly_P/E_Ratio'] = np.where(df['EPS'] == 0, np.nan, df['Monthly_Closing_Price'] / df['EPS'] / 3) # Specific adjustment for EPS-1
    # Replace infinite calculated output values with NaN
    df['Monthly_P/E_Ratio'].replace([np.inf, -np.inf], np.nan, inplace=True)
    print("Monthly_P/E_ratios have been calculated successfully.")
    return df

def monthly_P_B_ratios(df):
    # Creating a new column "Monthly_P/B_ratios" by dividing the "Monthly_Stock_Price" by the "Net_Assets_per_Share" and then divide by 3
    # Calculate the P/B ratio, handling cases where Net_Assets_per_Share is zero or missing
    df['Monthly_P/B_Ratio'] = np.where(df['Net_Assets_per_Share'] == 0, np.nan, df['Monthly_Closing_Price'] / df['Net_Assets_per_Share'] / 3) # Specific adjustment for Net_Assets_per_Share-1
    # Replace infinite calculated output values with NaN
    df['Monthly_P/B_Ratio'].replace([np.inf, -np.inf], np.nan, inplace=True)
    print("Monthly_P/B_ratios have been calculated successfully.")
    return df

def quarterly_RD_Expenses_divided_by_TA(df):
    # Creating a new column "Quarterly_R&D_Expenses/Total_Asset_ratios" by dividing the "RD_Expenses" by the "Total_Assets"
    # Calculate the RD expenses divided by Total Assets, handling cases where Total Assets is zero or missing
    df['Quarterly_R&D_Expenses/Total_Asset_ratios'] = np.where(df['Total_Assets'] == 0, np.nan, df['R&D_Expenses'] / df['Total_Assets'])
    # Replace infinite calculated output values with NaN
    df['Quarterly_R&D_Expenses/Total_Asset_ratios'].replace([np.inf, -np.inf], np.nan, inplace=True)
    print("Quarterly_R&D_Expenses/Total_Asset_ratios have been calculated successfully.")
    return df

def quarterly_Firm_Ages(df):
    # Convert the 'Trade_Month' and 'Establishment_Date' columns to datetime format
    df['Trade_Month'] = pd.to_datetime(df['Trade_Month'])
    df['Establishment_Date'] = pd.to_datetime(df['Establishment_Date'])
    
    # Creating a new column "Quarterly_Firm_Ages" by subtracting the "Establishment_Date" from the "Trade_Month"
    # Calculate the Firm Ages, handling cases where Establishment Date is missing
    df['Quaterly_Firm_Ages (years)'] = np.where(df['Establishment_Date'].isnull(), np.nan, ((df['Trade_Month'] - df['Establishment_Date']).dt.days / 365))
    # Replace infinite calculated output values with NaN
    df['Quaterly_Firm_Ages (years)'].replace([np.inf, -np.inf], np.nan, inplace=True)
    print("Quarterly_Firm_Ages have been calculated successfully.")
    return df



# Define the calculate_summary_statistics function
def calculate_summary_statistics(data, column_name):
    return {
        'count': data[column_name].count(),
        'mean': data[column_name].mean(),
        'median': data[column_name].median(),
        'p25': data[column_name].quantile(0.25),
        'p75': data[column_name].quantile(0.75),
        'std': data[column_name].std()
    }



def main():
    monthly_P_E_ratios(df)
    monthly_P_B_ratios(df)
    quarterly_RD_Expenses_divided_by_TA(df)
    quarterly_Firm_Ages(df)
    print("All calculations have been completed successfully.")

    # After the calculations, we can now categorize each A-share stock into 'Main Board' or 'GEM Board' based on their 'Market_Type'
    # Categorize each stock into 'Main Board' or 'GEM Board' bsed on their 'Market_Type' == [1, 4, 64] for 'Main_Board' and [16, 32] for 'GEM_Board'
    # # Main_Board: 1=SSE A share market (excluding STAR Market); 4= SZSE A share market (excluding ChiNext); 64= BSE A share market (SMEs);
    # # GEM_Board: 16= ChiNext; 32= STAR Market;
    df['Board_Category'] = df['Market_Type'].apply(lambda x: 'Main_Board' if x in [1, 4, 64] else 'GEM_Board' if x in [16, 32] else 'Unknown')

    # Define the metrics to calculate summary statistics for
    metrics = ['Monthly_Returns', 'Monthly_P/E_Ratio', 'Monthly_P/B_Ratio', 'ROA', 'ROE', 'Quarterly_R&D_Expenses/Total_Asset_ratios', 'Quaterly_Firm_Ages (years)']

    # Calculate summary statistics for each metric by board category (Main Board vs GEM Board)
    summary_statistics = {board: {metric: calculate_summary_statistics(df[df['Board_Category'] == board], metric) for metric in metrics} for board in ['Main_Board', 'GEM_Board']}

    # Flattening the summary_statistics dictionary into a list of records, correctly using 'board' as the category
    records = []
    for board, metrics in summary_statistics.items():
        for metric, stats in metrics.items():
            record = stats.copy()  # Copy stats to avoid altering the original dictionary
            record['Board_Category'] = board # Add the board category to the record
            record['Metric'] = metric # Add the metric to the record
            records.append(record) # Append the record to the list of records
            
    # Creating a DataFrame from the records with Board Category and Metric as a MultiIndex
    df_records = pd.DataFrame(records)
    multi_index = pd.MultiIndex.from_frame(df_records[['Board_Category', 'Metric']])
    summary_df = pd.DataFrame(df_records.drop(columns=['Board_Category', 'Metric']).values, index=multi_index, columns=['Count', 'Mean', 'Median', '25th Percentile (p25)', '75th Percentile (p75)', 'Standard Deviation'])

    # Displaying the structured DataFrame for comparison
    print(summary_df)
    
    print("Summary statistics have been calculated & presented successfully.")

    df.to_csv('/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/output/ready_for_further_analyze.csv', index=False)

    print("Analyzing.py has been executed successfully.")


if __name__ == "__main__":
    main()