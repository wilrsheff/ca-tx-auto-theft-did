import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Load datasets
df_ca_mvt = pd.read_csv("CA_MVT_Counts.csv")  # California MVT counts
df_tx_mvt = pd.read_csv("TX_MVT_Counts.csv")  # Texas MVT counts
df_ca_pop = pd.read_csv("CA_Population.csv")  # California population
df_tx_pop = pd.read_csv("TX_Population.csv")  # Texas population

# Merge datasets on "Year-Month"
df = df_ca_mvt.merge(df_tx_mvt, on="Year-Month", how="inner")
df = df.merge(df_ca_pop, on="Year-Month", how="inner")
df = df.merge(df_tx_pop, on="Year-Month", how="inner")

# Rename columns for clarity
df.columns = ["Year-Month", "CA_MVT_Count", "TX_MVT_Count", "CA_Population", "TX_Population"]

# Convert values to numeric types
df["CA_MVT_Count"] = pd.to_numeric(df["CA_MVT_Count"], errors="coerce")
df["TX_MVT_Count"] = pd.to_numeric(df["TX_MVT_Count"], errors="coerce")
df["CA_Population"] = pd.to_numeric(df["CA_Population"], errors="coerce")
df["TX_Population"] = pd.to_numeric(df["TX_Population"], errors="coerce")

# Compute Motor Vehicle Theft Rate per 100,000 people
df["CA_MVT_Rate"] = (df["CA_MVT_Count"] / df["CA_Population"]) * 100000
df["TX_MVT_Rate"] = (df["TX_MVT_Count"] / df["TX_Population"]) * 100000

# Convert "Year-Month" to datetime format
df["Year-Month"] = pd.to_datetime(df["Year-Month"])
df["Year"] = df["Year-Month"].dt.year

# Reshape data to long format for proper DiD structure
df_long = pd.melt(df, id_vars=["Year", "Year-Month"], value_vars=["CA_MVT_Rate", "TX_MVT_Rate"],
                  var_name="State", value_name="MVT_Rate")

# Assign treatment group: 1 for California, 0 for Texas
df_long["California"] = np.where(df_long["State"] == "CA_MVT_Rate", 1, 0)

# Create Post variable: 1 for years 2011 and beyond, 0 otherwise
df_long["Post"] = (df_long["Year"] >= 2011).astype(int)

# Create interaction term: Post x California
df_long["Post_x_California"] = df_long["Post"] * df_long["California"]

# Prepare data for Difference-in-Differences regression
df_did = df_long[["Year", "MVT_Rate", "Post", "California", "Post_x_California"]]

# Aggregate yearly averages for regression
df_did = df_did.groupby(["Year", "California"]).mean().reset_index()

# Set dependent and independent variables
y = df_did["MVT_Rate"]
X = df_did[["Post", "California", "Post_x_California"]]
X = sm.add_constant(X)  # Add intercept

# Run Difference-in-Differences regression
model = sm.OLS(y, X).fit()
results_summary = model.summary()

# Save DiD results
with open("DiD_regression_results.txt", "w") as f:
    f.write(results_summary.as_text())

# Parallel Trends Visualization (2006-2016)
plt.figure(figsize=(10, 5))

# Compute yearly average theft rates
ca_avg = df[df["Year"].between(2006, 2016)].groupby("Year")["CA_MVT_Rate"].mean()
tx_avg = df[df["Year"].between(2006, 2016)].groupby("Year")["TX_MVT_Rate"].mean()

# Plot parallel trends
plt.plot(ca_avg.index, ca_avg, label="CA Auto Theft Rate (per 100,000)", color="blue")
plt.plot(tx_avg.index, tx_avg, label="TX Auto Theft Rate (per 100,000)", color="orange")

# Policy implementation vertical line (2011)
plt.axvline(x=2011, color="red", linestyle="--", label="Policy Implementation (2011)")

# Formatting
plt.xlim(2006, 2016)
plt.xlabel("Year")
plt.ylabel("Auto Theft Rate per 100,000 People")
plt.title("Parallel Trends in Auto Theft Rates (CA vs TX)")
plt.legend()
plt.grid(True)

# Save figure
plt.savefig("parallel_trends_analysis.png")

print("Analysis complete. Check 'DiD_regression_results.txt' and 'parallel_trends_analysis.png'.")
