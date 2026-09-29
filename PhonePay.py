#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# # 1 - Data Loading and Understanding

# ## 1.1 - Loading Each Dataset and Displaying it's Structure

# In[2]:


FILE = r"C:\Users\achar\OneDrive\Desktop\data sets\Python\phonepe-pulse_raw-data.xlsx"


# In[3]:


state_txn_and_users = pd.read_excel(FILE,sheet_name = "State_Txn and Users")


# In[4]:


state_txn_and_users.head()


# In[5]:


state_txn_split = pd.read_excel(FILE,sheet_name = "State_TxnSplit")


# In[6]:


state_txn_split.tail(10)


# In[7]:


state_device_data = pd.read_excel(FILE,sheet_name = "State_DeviceData")


# In[8]:


total_rows = len(state_device_data)
starting_index = (total_rows//2) - 5
middle_10_rows = state_device_data.iloc[starting_index:starting_index+10]
print(middle_10_rows)


# In[9]:


district_txn_and_users = pd.read_excel(FILE,sheet_name = "District_Txn and Users")


# In[10]:


district_txn_and_users.head(10)


# In[11]:


district_txn_and_users.tail(10)


# In[12]:


district_demographics = pd.read_excel(FILE,sheet_name = "District Demographics")


# In[13]:


#Every 10th row
every_10th_row = district_demographics[::10] 
print(every_10th_row)


# ## 1.2 - Displaying basic statistics and data types for each dataset

# In[14]:


district_demographics.info()


# In[15]:


district_demographics.describe()


# In[16]:


district_txn_and_users.describe()


# In[17]:


district_txn_and_users.info()


# In[18]:


state_txn_and_users.describe()


# In[19]:


state_txn_and_users.info()


# In[20]:


state_txn_split.describe()


# In[21]:


state_txn_split.info()


# In[22]:


state_device_data.describe()


# In[23]:


state_device_data.info()


# In[24]:


datasets = {
    "State_Txn and Users": state_txn_and_users,
    "State_TxnSplit": state_txn_split,
    "State_DeviceData": state_device_data,
    "District_Txn and Users": district_txn_and_users,
    "District Demographics": district_demographics
}


# # 1.3 - Checking for missing values

# ## Identify any missing values

# In[25]:


for name, df in datasets.items():
    print(name)
    print(df.isnull().sum())


# ## %of missing values for each column

# In[26]:


for name, df in datasets.items():
    print(f"--- Percentage of Missing Values in {name} ---")

    # Calculate missing percentage per column
    missing_pct = (df.isnull().sum() / len(df)) * 100

    # Filter for columns that actually have missing values (> 0%)
    missing_pct_filtered = missing_pct[missing_pct > 0]

    if missing_pct_filtered.empty:
        print("No missing values found in any column.\n")
    else:
        print(missing_pct_filtered.round(2).astype(str) + "%\n")


# ## columns with highest % of missing values in each dataset

# In[27]:


for name, df in datasets.items():
    # Calculate missing percentage per column
    missing_pct = (df.isnull().sum() / len(df)) * 100

    # Check if there are any missing values in the dataset
    if missing_pct.max() == 0:
        print(f"**{name}**: No missing values found in any column.")
    else:
        # Find the column with the highest percentage of missing values
        max_missing_col = missing_pct.idxmax()
        max_missing_val = round(missing_pct.max(),2)

        print(
            f"**{name}**: Column with highest missing values -> "
            f"'{max_missing_col}' ({max_missing_val}%)"
        )


# # 1.4 - Creating Summary on States and districts

# In[28]:


# 1. Calculate total unique states
total_states = state_txn_and_users["State"].nunique()

# 2. Clean whitespace in State and District columns
district_demo_clean = district_demographics.copy()
district_demo_clean["State"] = district_demo_clean["State"].astype(str).str.strip()
district_demo_clean["District"] = district_demo_clean["District"].astype(str).str.strip()

# 3. Calculate unique (State, District) pairs
unique_districts_df = district_demo_clean[["State", "District"]].drop_duplicates()
total_districts = len(unique_districts_df)

# Print results
print(f"Total Number of Unique States: {total_states}")
print(f"Total Number of Unique Districts: {total_districts}")


# ## State with highest number of districts

# In[29]:


# Count districts per state in the demographics dataset
district_counts = district_demographics["State"].value_counts()

# Identify state with the maximum number of districts
max_state = district_counts.idxmax()
max_count = district_counts.max()

print(f"State with the highest number of districts: {max_state} ({max_count} districts)")


# # 2. Exploratory Data Analysis (EDA)

# ## 2.1 - Total number of transaction and total amount of transaction for each state over the years

# In[30]:


# Group by State and Year, then aggregate Transactions and Amount
state_yearly_trends = (
    state_txn_and_users.groupby(["State", "Year"])[["Transactions", "Amount (INR)"]]
    .sum()
    .reset_index()
)

# Display in tabular format
print("--- Total Transactions and Amount per State Over the Years ---")
print(state_yearly_trends)


# ## states with highest transaction volume and lowest transaction volume

# In[31]:


# Calculate total transaction volume per state across all years
total_volume_per_state = (
    state_txn_and_users.groupby("State")["Transactions"].sum().reset_index()
)

# Top 5 states with highest transaction volumes
top_5_states = total_volume_per_state.sort_values(
    by="Transactions", ascending=False
).head(5)

# Top 5 states with lowest transaction volumes
bottom_5_states = total_volume_per_state.sort_values(
    by="Transactions", ascending=True
).head(5)

print("--- Top 5 States by Highest Transaction Volume ---")
print(top_5_states)

print("\n--- Top 5 States by Lowest Transaction Volume ---")
print(bottom_5_states)


# ## 2.2 - Most common transaction type in each state and quater

# In[32]:


# Group by State, Quarter, and Transaction Type to find the total volume for each combination
type_counts = (
    state_txn_split.groupby(["State", "Year","Quarter", "Transaction Type"])[
        "Transactions"
    ]
    .sum()
    .reset_index()
)

# Sort by State, Quarter, and Transactions descending
type_counts_sorted = type_counts.sort_values(
    by=["State","Year", "Quarter", "Transactions"], ascending=[True, True, True, False]
)

# Pick the top (most frequent) transaction type for each State and Quarter
most_frequent_types = type_counts_sorted.groupby(["State", "Year", "Quarter"]).first().reset_index()

# Display in tabular format
print("--- Most Frequent Transaction Type per State and Quarter ---")
print(most_frequent_types)


# ## 2.3 - Device brand with highest number of registered users in each state

# In[33]:


_dy = state_device_data["Year"].max()
_dq = state_device_data[state_device_data["Year"] == _dy]["Quarter"].max()
brand_by_state = (
    state_device_data[(state_device_data["Year"] == _dy) & (state_device_data["Quarter"] == _dq)]
    .groupby(["State", "Brand"])["Registered Users"]
    .sum()
    .reset_index()
)
print(f"Device brand analysis uses latest period: Q{_dq} {_dy}")
 
# 2. Extract the brand with the maximum registered users for each state
top_brand_per_state = brand_by_state.loc[
    brand_by_state.groupby("State")["Registered Users"].idxmax()
].reset_index(drop=True)
 
# 3. Sort and format the output table
top_brand_per_state = top_brand_per_state.sort_values(by="State").rename(
    columns={"Registered Users": "Total Registered Users"}
)
 
# Display tabular result
print("--- Device Brand with Highest Registered Users in Each State ---")
print(top_brand_per_state)


# ## 2.4 - Top districts based on population

# In[34]:


# Sort by State and Population descending
pop_sorted = district_demographics.sort_values(
    by=["State", "Population"], ascending=[True, False]
)

# Extract the highest population district per state
top_district_per_state = pop_sorted.groupby("State").first().reset_index()

# Filter relevant columns for display
top_district_table = top_district_per_state[["State", "District", "Population"]]

print("--- District with Highest Population for Each State ---")
print(top_district_table)


# In[35]:


import matplotlib.pyplot as plt
import seaborn as sns

# Set plot style
plt.figure(figsize=(14, 6))
sns.set_theme(style="whitegrid")

# Create column (bar) chart
ax = sns.barplot(
    data=top_district_table,
    x="State",
    y="Population",
    hue="State",
    palette="viridis",
    legend=False
)

# Formatting chart
plt.xticks(rotation=90)
plt.title(
    "Highest Population District per State", fontsize=14, fontweight="bold"
)
plt.xlabel("State", fontsize=12)
plt.ylabel("Population", fontsize=12)

# Annotate district names on top of each bar
for p, district in zip(ax.patches, top_district_table["District"]):
    height = p.get_height()
    if not pd.isna(height) and height > 0:
        ax.annotate(
            f"{district}",
            (p.get_x() + p.get_width() / 2.0, height),
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=90,
            xytext=(0, 5),
            textcoords="offset points",
        )

plt.tight_layout()
plt.show()


# ## 2.5 - Average transaction value (ATV) for each state

# In[36]:


# Aggregate total transaction amount and total transaction count per state
state_atv = (
    state_txn_and_users.groupby("State")[["Amount (INR)", "Transactions"]]
    .sum()
    .reset_index()
)

# Calculate Average Transaction Value (ATV)
state_atv["Calculated_ATV"] = (
    state_atv["Amount (INR)"] / state_atv["Transactions"]
)

# Display in tabular format
print("--- Average Transaction Value (ATV) for Each State ---")
print(
    state_atv[["State", "Calculated_ATV"]].sort_values(
        by="Calculated_ATV", ascending=False
    )
)


# ## top 5 highest and top 5 lowest ATV

# In[37]:


# Sort by Calculated_ATV
sorted_atv = state_atv.sort_values(by="Calculated_ATV", ascending=False)

# Top 5 states with highest ATV
top_5_atv = sorted_atv.head(5)

# Top 5 states with lowest ATV
bottom_5_atv = sorted_atv.tail(5).iloc[::-1]  # Display in ascending order

print("--- Top 5 States with Highest ATV ---")
print(top_5_atv[["State", "Calculated_ATV"]])

print("\n--- Top 5 States with Lowest ATV ---")
print(bottom_5_atv[["State", "Calculated_ATV"]])


# ## 2.6 - App usage trends

# In[38]:


# Group by State, Year, and Quarter to aggregate total App Opens
app_opens_summary = (
    state_txn_and_users.groupby(["State", "Year", "Quarter"])["App Opens"]
    .sum()
    .reset_index()
)

# Display in tabular format
print("--- Total App Opens per State over Years and Quarters ---")
print(app_opens_summary)


# In[39]:


import matplotlib.pyplot as plt
import seaborn as sns

# Select a state to analyze (e.g., 'Maharashtra' or any state from your dataset)
selected_state = "Odisha"

# Filter dataset for the selected state
state_app_data = state_txn_and_users[
    state_txn_and_users["State"] == selected_state
].copy()

# Create a combined 'Year_Quarter' string for chronological x-axis plotting
state_app_data["Time_Period"] = (
    state_app_data["Year"].astype(str)
    + " Q"
    + state_app_data["Quarter"].astype(str)
)

# Sort chronologically
state_app_data = state_app_data.sort_values(by=["Year", "Quarter"])

# Plotting the line chart
plt.figure(figsize=(12, 5))
sns.lineplot(
    data=state_app_data,
    x="Time_Period",
    y="App Opens",
    marker="o",
    linewidth=2.5,
    color="purple",
)

plt.title(
    f"App Opens Trend Over Time for {selected_state}",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Time Period (Year & Quarter)", fontsize=11)
plt.ylabel("Total App Opens", fontsize=11)
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.show()


# ## 2.7 - Distribution of transaction types

# In[40]:


# 1. Identify the most recent Year and Quarter in the dataset
latest_year = state_txn_split["Year"].max()
latest_quarter = state_txn_split[
    state_txn_split["Year"] == latest_year
]["Quarter"].max()

print(f"Most recent period: Year {latest_year}, Quarter {latest_quarter}")

# 2. Filter dataset for the most recent quarter
recent_split_df = state_txn_split[
    (state_txn_split["Year"] == latest_year)
    & (state_txn_split["Quarter"] == latest_quarter)
]

# 3. Create the grouped bar plot
plt.figure(figsize=(16, 8))
sns.set_theme(style="whitegrid")

# Grouped bar chart: States on X-axis, Transaction count on Y-axis, colored by Transaction Type
sns.barplot(
    data=recent_split_df,
    x="State",
    y="Transactions",
    hue="Transaction Type",
    palette="tab10",
)

# Formatting chart
plt.xticks(rotation=90)
plt.title(
    f"Distribution of Transaction Types by State (Q{latest_quarter} {latest_year})",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("State", fontsize=12)
plt.ylabel("Number of Transactions", fontsize=12)
plt.legend(title="Transaction Type", bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()


# ## 2.8 - Unique maping between district name and district code

# In[41]:


# Extract unique mappings of District and Code from the district demographics dataset
district_mapping = district_demographics[["State","District", "Code"]].drop_duplicates()

# Sort by District name for clean organization
district_mapping = district_mapping.sort_values(by=["State","District"]).reset_index(
    drop=True
)

# Display the first few rows
print("--- Unique Mapping Between District Name and District Code ---")
print(district_mapping.head(10))

# Export the dataframe to a CSV file
district_mapping.to_csv("district_code_mapping.csv", index=False)

print("\nSuccessfully exported 'district_code_mapping.csv'!")


# # 3. - Data quality check

# ## 3.1 - Ensureing data consistency accross states and districts level

# In[42]:


# 1. Aggregate district-level data to the state level
district_agg = (
    district_txn_and_users.groupby(["State", "Year", "Quarter"])[
        ["Transactions", "Amount (INR)", "Registered Users"]
    ]
    .sum()
    .reset_index()
)

# Rename columns for clear comparison
district_agg = district_agg.rename(
    columns={
        "Transactions": "District_Sum_Txns",
        "Amount (INR)": "District_Sum_Amount",
        "Registered Users": "District_Sum_Users",
    }
)

# 2. Merge district aggregates with state-level data
comparison_df = pd.merge(
    state_txn_and_users[
        [
            "State",
            "Year",
            "Quarter",
            "Transactions",
            "Amount (INR)",
            "Registered Users",
        ]
    ],
    district_agg,
    on=["State", "Year", "Quarter"],
    how="outer",
)

# 3. Calculate discrepancies (differences)
comparison_df["Txn_Diff"] = (
    comparison_df["Transactions"] - comparison_df["District_Sum_Txns"]
)
comparison_df["Amount_Diff"] = (
    comparison_df["Amount (INR)"] - comparison_df["District_Sum_Amount"]
)
comparison_df["Users_Diff"] = (
    comparison_df["Registered Users"] - comparison_df["District_Sum_Users"]
)

# Filter rows where there is any discrepancy (allowing for small float tolerance if needed)
_ok_txn = np.isclose(comparison_df["Transactions"], comparison_df["District_Sum_Txns"], rtol=1e-9, atol=0)
_ok_amt = np.isclose(comparison_df["Amount (INR)"], comparison_df["District_Sum_Amount"], rtol=1e-9, atol=0)
_ok_usr = np.isclose(comparison_df["Registered Users"], comparison_df["District_Sum_Users"], rtol=1e-9, atol=0)
discrepancies = comparison_df[~(_ok_txn & _ok_amt & _ok_usr)]
 

# Display results
if discrepancies.empty:
    print("No discrepancies found! District data perfectly matches state-level totals.")
else:
    print(f"Found {len(discrepancies)} discrepancy records between District and State data:")
    print(discrepancies)


# # 4. - Data merging and advance analysis

# ## 4.1 - Ratio to users to population by state

# In[43]:


# 1. Calculate total population per state from district demographics
state_pop = (
    district_demographics.groupby("State")["Population"].sum().reset_index()
)

# 2. Get the latest number of registered users per state
# (Taking the max year/quarter to avoid summing cumulative user counts)
latest_year = state_txn_and_users["Year"].max()
latest_quarter = state_txn_and_users[state_txn_and_users["Year"] == latest_year][
    "Quarter"
].max()

state_users = state_txn_and_users[
    (state_txn_and_users["Year"] == latest_year)
    & (state_txn_and_users["Quarter"] == latest_quarter)
][["State", "Registered Users"]]

# 3. Merge datasets
user_pop_df = pd.merge(state_users, state_pop, on="State", how="inner")

# 4. Compute User to Population Ratio
user_pop_df["User_to_Pop_Ratio"] = (
    user_pop_df["Registered Users"] / user_pop_df["Population"]
)

# Sort descending
user_pop_df = user_pop_df.sort_values(by="User_to_Pop_Ratio", ascending=False)

print("--- Registered Users to Population Ratio by State ---")
print(user_pop_df)


# In[44]:


plt.figure(figsize=(14, 6))
sns.set_theme(style="whitegrid")

# Create column bar chart
ax = sns.barplot(
    data=user_pop_df,
    x="State",
    y="User_to_Pop_Ratio",
    hue="State",
    palette="mako",
    legend=False
)

plt.xticks(rotation=90)
plt.title(
    f"Ratio of Registered Users to Population by State (Q{latest_quarter} {latest_year})",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("State", fontsize=12)
plt.ylabel("User to Population Ratio", fontsize=12)

plt.tight_layout()
plt.show()


# ## 4.2 - Correlate population density with transaction volume

# In[45]:


# 1. Aggregate total transaction volume (and amount) per district
district_txn_summary = (
    district_txn_and_users.groupby(["State", "District", "Code"])["Transactions"]
    .sum()
    .reset_index()
)
 
# 2. Merge district transaction data with district demographics
merged_district_df = pd.merge(
    district_txn_summary,
    district_demographics[["Code", "Density", "Population"]].drop_duplicates("Code"),
    on="Code",
    how="inner",
)
print(f"Districts matched: {len(merged_district_df)} of {len(district_txn_summary)}")
 
# 3. Ensure Density is numeric (clean commas or spaces if any exist)
merged_district_df["Density"] = pd.to_numeric(
    merged_district_df["Density"].astype(str).str.replace(",", ""),
    errors="coerce",
)
 
# 4. Calculate Pearson correlation between Density and Transactions
correlation_value = merged_district_df["Density"].corr(
    merged_district_df["Transactions"]
)
 
spearman_value = merged_district_df["Density"].corr(merged_district_df["Transactions"], method="spearman")
print(
    f"Pearson correlation between Population Density and Transaction Volume: {correlation_value:.4f}"
)
print(f"Spearman (rank) correlation: {spearman_value:.4f}")
 


# In[46]:


plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

# Create scatter plot with regression line
sns.regplot(
    data=merged_district_df,
    x="Density",
    y="Transactions",
    scatter_kws={"alpha": 0.6, "color": "teal"},
    line_kws={"color": "red", "linewidth": 2},
)

# Set log scale if density/transactions span multiple orders of magnitude
plt.xscale("log")
plt.yscale("log")

plt.title(
    f"Population Density vs Transaction Volume (Correlation: {correlation_value:.2f})",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Population Density", fontsize=12)
plt.ylabel("Total Transaction Volume", fontsize=12)

plt.tight_layout()
plt.show()


# ## 4.3 - Average transaction amount per User

# In[47]:


# 1. Total transaction amount per state across all quarters/years
total_amount_per_state = (
    state_txn_and_users.groupby("State")["Amount (INR)"].sum().reset_index()
)

# 2. Latest registered user count per state (since user counts are cumulative)
latest_year = state_txn_and_users["Year"].max()
latest_quarter = state_txn_and_users[state_txn_and_users["Year"] == latest_year][
    "Quarter"
].max()

latest_users_per_state = state_txn_and_users[
    (state_txn_and_users["Year"] == latest_year)
    & (state_txn_and_users["Quarter"] == latest_quarter)
][["State", "Registered Users"]]

# 3. Merge datasets
user_amount_df = pd.merge(
    total_amount_per_state, latest_users_per_state, on="State", how="inner"
)

# 4. Calculate Average Transaction Amount per User
user_amount_df["Avg_Amount_Per_User"] = round((
    user_amount_df["Amount (INR)"] / user_amount_df["Registered Users"]
),2)

# Display tabular format
print("--- Average Transaction Amount Per User for Each State ---")
print(
    user_amount_df.sort_values(by="Avg_Amount_Per_User", ascending=False)
)


# In[48]:


# Sort states by Avg_Amount_Per_User descending
sorted_user_amount = user_amount_df.sort_values(
    by="Avg_Amount_Per_User", ascending=False
)

# Top 5 states with highest average transaction amount per user
top_5_user_amount = sorted_user_amount.head(5)

# Top 5 states with lowest average transaction amount per user
bottom_5_user_amount = sorted_user_amount.tail(5).iloc[::-1]

print("--- Top 5 States with Highest Average Transaction Amount Per User ---")
print(top_5_user_amount[["State", "Avg_Amount_Per_User"]])

print("\n--- Top 5 States with Lowest Average Transaction Amount Per User ---")
print(bottom_5_user_amount[["State", "Avg_Amount_Per_User"]])


# ## 4.4 - Device brand usage ratio

# In[49]:


# 1. Merge State_DeviceData with State_Txn and Users
device_merged = pd.merge(
    state_device_data,
    state_txn_and_users[["State", "Year", "Quarter", "Registered Users"]],
    on=["State", "Year", "Quarter"],
    how="inner",
    suffixes=("_Brand", "_TotalState"),
)

# 2. Calculate the brand usage ratio
# (Brand Registered Users / Total State Registered Users)
device_merged["Brand_Usage_Ratio"] = (
    device_merged["Registered Users_Brand"]
    / device_merged["Registered Users_TotalState"]
)

# Display tabular summary for the latest time period or across all data
latest_year = device_merged["Year"].max()
latest_quarter = device_merged[device_merged["Year"] == latest_year][
    "Quarter"
].max()

latest_device_ratio = device_merged[
    (device_merged["Year"] == latest_year)
    & (device_merged["Quarter"] == latest_quarter)
][["State", "Brand", "Registered Users_Brand", "Registered Users_TotalState", "Brand_Usage_Ratio"]]

print(
    f"--- Device Brand Usage Ratio by State (Q{latest_quarter} {latest_year}) ---"
)
print(latest_device_ratio.sort_values(["State", "Brand_Usage_Ratio"], ascending=[True, False]).to_string(index=False))


# In[50]:


plt.figure(figsize=(16, 8))
sns.set_theme(style="whitegrid")

# Create grouped bar chart for brand usage ratio per state
sns.barplot(
    data=latest_device_ratio,
    x="State",
    y="Brand_Usage_Ratio",
    hue="Brand",
    palette="Set2",
)

plt.xticks(rotation=90)
plt.title(
    f"Device Brand Usage Ratio by State (Q{latest_quarter} {latest_year})",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("State", fontsize=12)
plt.ylabel("Brand Usage Ratio", fontsize=12)
plt.legend(title="Device Brand", bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()


# # 5 - Data Visualization

# In[51]:


# 1. Select a state to analyze
selected_state = "Odisha"

# 2. Filter dataset for the selected state
state_trend_df = state_txn_and_users[
    state_txn_and_users["State"] == selected_state
].copy()

# 3. Create a combined chronological 'Period' column (e.g., '2022 Q1')
state_trend_df["Period"] = (
    state_trend_df["Year"].astype(str)
    + " Q"
    + state_trend_df["Quarter"].astype(str)
)

# Sort chronologically by Year and Quarter
state_trend_df = state_trend_df.sort_values(by=["Year", "Quarter"])

# 4. Create dual-axis line plot
fig, ax1 = plt.subplots(figsize=(14, 6))
sns.set_theme(style="whitegrid")

# Primary Y-Axis: Total Transactions (Count)
color_txns = "#1f77b4"
ax1.set_xlabel("Time Period (Year & Quarter)", fontsize=12)
ax1.set_ylabel("Total Transactions", color=color_txns, fontsize=12)
line1 = ax1.plot(
    state_trend_df["Period"],
    state_trend_df["Transactions"],
    color=color_txns,
    marker="o",
    linewidth=2.5,
    label="Transactions Count",
)
ax1.tick_params(axis="y", labelcolor=color_txns)
plt.xticks(rotation=45)

# Secondary Y-Axis: Total Transaction Amount (INR)
ax2 = ax1.twinx()
color_amt = "#2ca02c"
ax2.set_ylabel(
    "Total Transaction Amount (INR)", color=color_amt, fontsize=12
)
line2 = ax2.plot(
    state_trend_df["Period"],
    state_trend_df["Amount (INR)"],
    color=color_amt,
    marker="s",
    linestyle="--",
    linewidth=2.5,
    label="Transaction Amount (INR)",
)
ax2.tick_params(axis="y", labelcolor=color_amt)

# Combine legends
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper left")

plt.title(
    f"Transaction Volume and Amount Over Time ({selected_state})",
    fontsize=14,
    fontweight="bold",
)
plt.tight_layout()
plt.show()


# In[52]:


# 1. Specify selected State, Year, and Quarter
selected_state = "Odisha"
selected_year = 2021
selected_quarter = 2

# 2. Filter df_state_txnsplit for the specified selection
pie_data = state_txn_split[
    (state_txn_split["State"] == selected_state)
    & (state_txn_split["Year"] == selected_year)
    & (state_txn_split["Quarter"] == selected_quarter)
]

# 3. Create Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(
    pie_data["Transactions"],
    labels=pie_data["Transaction Type"],
    autopct="%1.1f%%",
    startangle=140,
    colors=plt.cm.Paired.colors,
    wedgeprops={"edgecolor": "black", "linewidth": 1},
)

plt.title(
    f"Transaction Type Distribution - {selected_state} (Q{selected_quarter} {selected_year})",
    fontsize=14,
    fontweight="bold",
)

plt.tight_layout()
plt.show()


# In[53]:


import matplotlib.pyplot as plt
import seaborn as sns

# 1. Select a state to analyze
selected_state = "Odisha"

# 2. Filter df_district_demo for the selected state
state_demo = district_demographics[
    district_demographics["State"] == selected_state
].copy()

# 3. Ensure 'Density' is numeric (clean commas or spaces if present)
state_demo["Density"] = pd.to_numeric(
    state_demo["Density"].astype(str).str.replace(",", ""), errors="coerce"
)

# 4. Sort districts by population density descending
state_demo = state_demo.sort_values(by="Density", ascending=False)

# 5. Create Bar Plot
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

sns.barplot(
    data=state_demo,
    x="District",
    y="Density",
    hue="District",
    palette="Blues_r",
    legend=False
)

plt.xticks(rotation=90)
plt.title(
    f"Population Density of Districts in {selected_state}",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("District", fontsize=12)
plt.ylabel("Population Density", fontsize=12)

plt.tight_layout()
plt.show()


# # 6 - Insights and Conclusion

# In[54]:


# 1. Aggregate total transactions and total amount across all states by Year and Quarter
national_trend = (
    state_txn_and_users.groupby(["Year", "Quarter"])[["Transactions", "Amount (INR)"]]
    .sum()
    .reset_index()
)

# Create chronological Period column (e.g., '2022 Q1')
national_trend["Period"] = (
    national_trend["Year"].astype(str)
    + " Q"
    + national_trend["Quarter"].astype(str)
)
national_trend = national_trend.sort_values(by=["Year", "Quarter"])

# 2. Plot overall transaction volume growth trajectory
plt.figure(figsize=(12, 5))
sns.set_theme(style="whitegrid")

sns.lineplot(
    data=national_trend,
    x="Period",
    y="Transactions",
    marker="o",
    linewidth=2.5,
    color="darkblue",
)

plt.title("National Digital Transaction Volume Trend Over Time", fontsize=14, fontweight="bold")
plt.xlabel("Time Period", fontsize=11)
plt.ylabel("Total Transactions (Count)", fontsize=11)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Quarterly Growth Rate Analysis
national_trend["QoQ_Txn_Growth_%"] = national_trend["Transactions"].pct_change() * 100
national_trend["QoQ_Amount_Growth_%"] = national_trend["Amount (INR)"].pct_change() * 100

print("--- National Transaction Growth Trends ---")
print(national_trend[["Period", "Transactions", "Amount (INR)", "QoQ_Txn_Growth_%", "QoQ_Amount_Growth_%"]])

# 4. Summary Findings Output
g = national_trend.dropna(subset=["QoQ_Txn_Growth_%"])
declines = g[g["QoQ_Txn_Growth_%"] < 0]
best = g.loc[g["QoQ_Txn_Growth_%"].idxmax()]
by_q = g.groupby("Quarter")["QoQ_Txn_Growth_%"].mean().round(1).to_dict()
first, last = national_trend.iloc[0], national_trend.iloc[-1]
decline_txt = "; ".join(f"{r.Period} ({r['QoQ_Txn_Growth_%']:.1f}%)" for _, r in declines.iterrows()) or "none"
summary_text = f"""
Key Findings & Observations (Task 6.1):
--------------------------------------------------------------------------------
1. Strong growth: quarterly transactions rose from {first.Transactions:,.0f} ({first.Period}) to {last.Transactions:,.0f} ({last.Period}).
2. Quarters with a QoQ decline: {decline_txt}. The 2020 Q2 dip coincides with COVID-19 lockdowns.
3. Largest QoQ jump: {best.Period} (+{best['QoQ_Txn_Growth_%']:.1f}%).
4. Average QoQ growth by quarter number (Q1..Q4): {by_q}. Seasonality is only partly visible; adoption growth dominates.
"""
print(summary_text)
 


# In[55]:


# 1. Aggregate district transaction data (Total Volume, Amount, Registered Users, App Opens)
district_txn_agg = (
    district_txn_and_users.groupby(["State", "District","Code"])[
        ["Transactions", "Amount (INR)", "Registered Users", "App Opens"]
    ]
    .sum()
    .reset_index()
)

# 2. Merge with District Demographics
merged_demo_txn = pd.merge(
    district_txn_agg,
    district_demographics[["Code", "Population", "Area (sq km)", "Density"]].drop_duplicates("Code"),
    on = "Code",
    how="inner",
)

# 3. Clean numeric columns (remove commas/spaces if present)
for col in ["Population", "Area (sq km)", "Density"]:
    merged_demo_txn[col] = pd.to_numeric(
        merged_demo_txn[col].astype(str).str.replace(",", ""), errors="coerce"
    )

# 4. Compute correlation matrix for demographic vs transaction variables
corr_cols = [
    "Population",
    "Density",
    "Area (sq km)",
    "Transactions",
    "Amount (INR)",
    "Registered Users",
    "App Opens",
]
correlation_matrix = merged_demo_txn[corr_cols].corr()

print("--- Correlation Matrix: Demographics vs Transaction Data ---")
print(correlation_matrix)


# In[56]:


# Visualize correlation matrix using a heatmap
plt.figure(figsize=(9, 7))
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    cbar=True,
    square=True,
)

plt.title(
    "Correlation Matrix: Demographic Factors vs Transaction Metrics",
    fontsize=13,
    fontweight="bold",
)
plt.tight_layout()
plt.show()

# Print summary insights
cm = correlation_matrix
def _label(r):
    r = abs(r)
    return "strong" if r >= 0.7 else "moderate" if r >= 0.4 else "weak"
summary_insights = f"""
Key Observations & Findings:
--------------------------------------------------------------------------------
1. Population vs Transactions: r = {cm.loc['Population','Transactions']:.2f} ({_label(cm.loc['Population','Transactions'])}); vs Registered Users: r = {cm.loc['Population','Registered Users']:.2f} ({_label(cm.loc['Population','Registered Users'])}).
2. Density vs Transactions: r = {cm.loc['Density','Transactions']:.2f} ({_label(cm.loc['Density','Transactions'])}). Density is a weaker driver than raw population.
3. Area vs Transactions: r = {cm.loc['Area (sq km)','Transactions']:.2f} ({_label(cm.loc['Area (sq km)','Transactions'])}); land area barely matters.
"""
print(summary_insights)


# In[57]:


# Compute dynamic summary statistics for Section 6
top_state = state_txn_and_users.groupby('State')['Amount (INR)'].sum().idxmax()
top_state_amount = state_txn_and_users.groupby('State')['Amount (INR)'].sum().max()
total_txns = state_txn_and_users['Transactions'].sum()
avg_atv = state_txn_and_users['Amount (INR)'].sum() / total_txns

# Format Section 6 text output dynamically
summary_text = f"""
## Key Findings & Summary

* **Top Performing State:** {top_state} generated the highest total transaction amount at **₹{top_state_amount:,.2f}**.
* **Overall Volume:** Across all recorded periods, a total of **{total_txns:,}** transactions were completed.
* **Average Transaction Value (ATV):** The overall calculated ATV across all transactions stands at **₹{avg_atv:.2f}**.
"""

print(summary_text)


# In[58]:


# 6.3 Summary & recommendations
latest = state_txn_and_users[(state_txn_and_users.Year == 2021) & (state_txn_and_users.Quarter == 2)]
ratio = user_pop_df.set_index("State")["User_to_Pop_Ratio"]
print(f"""
Key findings
- Volume grew from {first.Transactions:,.0f} to {last.Transactions:,.0f} quarterly transactions (2018 Q1 to 2021 Q2); only 2020 Q2 declined.
- {top_state} leads by total transaction amount (INR {top_state_amount:,.0f}); overall ATV is INR {avg_atv:,.0f}.
- Highest user/population ratios: {', '.join(ratio.nlargest(3).index)}; lowest: {', '.join(ratio.nsmallest(3).index)}.
- Population (not density or area) is the main demographic driver of usage.

Recommendations
1. Prioritise user acquisition in the low-penetration states above (e.g. Meghalaya, Lakshadweep, Mizoram): the gap to leaders is large.
2. In high-volume states, focus on deepening usage (merchant and bill payments) rather than sign-ups.
3. Fix data gaps before reporting: AP 2021 Q1 amount is missing at state level, and 28 district rows lack a Code.
""")


# In[ ]:




