import pandas as pd
import statsmodels.api as sm

def main():

    stock_volatility = pd.read_csv(
            "/Users/admin/Desktop/Assignment_2/processing/daily_stock_volatility_processed.csv",
        )

    merged_dt = pd.read_csv(
        "/Users/admin/Desktop/Assignment_2/processing/PB_ratios.csv",
    )
    
# filter the PB ratio dataset out by the 2010-12-31 trade date data
    merged_dt_for_Q1 = merged_dt[merged_dt["Trade_Month"] == "2010-12-01"]
    
    merged_dt_for_Q1.to_csv(
        "/Users/admin/Desktop/Assignment_2/processing/merged_dt_for_Q1.csv",
        index=False,
    )
    
# merge the stock volatility dataset with the PB ratio dataset and save the new merged dataset to a new file named regressing.csv
    regressing = pd.merge(
        merged_dt_for_Q1,
        stock_volatility,
        how="inner",
        on=["Stkcd"],
    )
    
# save the dataset for regressing
    regressing.to_csv(
        "/Users/admin/Desktop/Assignment_2/processing/regression_dataset_for_Q1.csv",
        index=False,
    )
    
    regressing = regressing.dropna(subset=["ROE", "Volatility", "PB_ratio"])
# regress the PB ratio on ROE and stock volatility

# Define the independent variables (add a constant term to allow for an intercept)
    X = sm.add_constant(regressing[['ROE', 'Volatility']])

# Define the dependent variable
    y = regressing['PB_ratio']

# Fit the model
    model = sm.OLS(y, X).fit()

# Print out the statistics
    print(model.summary())

    
    print("Processing is done!")
    
    
    

if __name__ == "__main__":
    main()