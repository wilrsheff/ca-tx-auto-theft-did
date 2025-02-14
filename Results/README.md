# Results  
This folder contains the outputs of the Difference-in-Differences (DiD) analysis conducted on California and Texas auto theft rates from 2006 to 2016.  

## Files  

- **[`DiD_regression_results.txt`](DiD_regression_results.txt)** – Regression output from the Difference-in-Differences analysis.  
- **[`parallel_trends_analysis.png`](parallel_trends_analysis.png)** – Graph showing the parallel trends in auto theft rates between CA and TX before and after the policy change in 2011.  

## About These Results  

- The **DiD regression results** provide statistical insights into how the policy change affected auto theft rates in California, compared to Texas.  
- The **parallel trends graph** visually evaluates whether the trends in auto theft rates were similar before the policy, supporting the validity of the DiD approach.  

These results help assess whether reducing the penalty for auto theft in California influenced crime rates.  

## Transparency Note  
The results in this folder were generated using a **precomputed theft rate dataset**, while the provided script dynamically calculates rates from raw theft counts and population data.  

Both approaches use the same underlying data, but small differences may exist due to variations in processing order, rounding, or missing data handling. This choice was made to balance clarity in presenting results with the ability to demonstrate more advanced data handling in the script.
