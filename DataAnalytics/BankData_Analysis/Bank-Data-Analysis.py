#!/usr/bin/env python
# coding: utf-8

# In[44]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import io


# In[45]:


df = pd.read_excel(r'C:\Users\Lakshya\Bank\bank-additional-full.xlsx')


# In[46]:


# df


# In[47]:


# Select numeric columns into NumPy array
numeric_cols = [
    'age', 'duration', 'campaign', 'pdays', 'previous',
    'emp.var.rate', 'cons.price.idx', 'cons.conf.idx',
    'euribor3m', 'nr.employed'
]

data = df[numeric_cols].to_numpy()


# In[48]:


# Column index helper
col = {name: i for i, name in enumerate(numeric_cols)}


# **<h1 style="font-size:30px">Some Operations with Numpy</h1>**

# **Mean, Median, Std of Age**

# In[49]:


age = data[:, col['age']]

mean_age = np.mean(age)
median_age = np.median(age)
std_age = np.std(age)

print(mean_age)
print(median_age)
print(std_age)
# mean_age, median_age, std_age


# **Min, Max, Range of Age**

# In[50]:


min_age = np.min(age)
max_age = np.max(age)
age_range = max_age - min_age

print(min_age)
print(max_age)
print(age_range)
# min_age, max_age, age_range


# **Campaign Contact Analysis**

# In[51]:


campaign = data[:, col['campaign']]

avg_campaign = np.mean(campaign)
max_campaign = np.max(campaign)

print(avg_campaign)
print(max_campaign)
# avg_campaign, max_campaign


# **Call Duration Insights**

# In[52]:


duration = data[:, col['duration']]
mean_duration = np.mean(duration)

above_mean_pct = np.sum(duration > mean_duration) / len(duration) * 100

print(mean_duration)
print(above_mean_pct)
# mean_duration, above_mean_pct


# **Previous Campaign Impact**

# In[53]:


previous = data[:, col['previous']]

previous_contacted = previous[previous > 0]
avg_previous = np.mean(previous_contacted)

print(avg_previous)
# avg_previous


# **Euribor Rate Variability**

# In[54]:


euribor = data[:, col['euribor3m']]

variance_euribor = np.var(euribor)
std_euribor = np.std(euribor)

print(variance_euribor)
print(std_euribor)
# variance_euribor, std_euribor


# **Correlation Between Age and Duration**

# In[55]:


correlation = np.corrcoef(age, duration)[0, 1]

print(correlation)
# correlation


# **Employment vs Subscription Outcome**

# In[56]:


# Convert y column to numeric
y_numeric = np.where(df['y'] == 'yes', 1, 0)

nr_employed = data[:, col['nr.employed']]

avg_emp_yes = np.mean(nr_employed[y_numeric == 1])
avg_emp_no = np.mean(nr_employed[y_numeric == 0])

print(avg_emp_yes)
print(avg_emp_no)

# avg_emp_yes, avg_emp_no


# **Outlier Detection (Z-Score on Duration)**

# In[57]:


z_scores = (duration - np.mean(duration)) / np.std(duration)

outliers = np.sum(np.abs(z_scores) > 3)

print(outliers)
# outliers


# **Economic Indicators Comparison**

# In[58]:


cpi = data[:, col['cons.price.idx']]
cci = data[:, col['cons.conf.idx']]

mean_cpi = np.mean(cpi)
std_cpi = np.std(cpi)

mean_cci = np.mean(cci)
std_cci = np.std(cci)

print(mean_cpi)
print(std_cpi)

print(mean_cci)
print(std_cci)

# (mean_cpi, std_cpi), (mean_cci, std_cci)


# **<h1 style="font-size:30px">Some Operations with Pandas</h1>**

# **What is the subscription rate?**

# In[59]:


subscription_rate = df['y'].value_counts(normalize=True) * 100

print(subscription_rate)
# subscription_rate


# **Which job category subscribes the most?**

# In[60]:


job_subscription = df.groupby('job')['y'].value_counts(normalize=True).unstack() * 100

print(job_subscription.sort_values(by='yes', ascending=False))
# job_subscription.sort_values(by='yes', ascending=False)


# **Does marital status affect subscription?**

# In[61]:


marital_analysis = pd.crosstab(df['marital'], df['y'], normalize='index') * 100

print(marital_analysis)
# marital_analysis


# **Average Age of Subscribers vs Non-Subscribers**

# In[62]:


age_analysis = df.groupby('y')['age'].mean()
print(age_analysis)
# age_analysis


# **Which month had the highest subscriptions?**

# In[63]:


month_analysis = pd.crosstab(df['month'], df['y'])

print(month_analysis.sort_values(by='yes', ascending=False))
# month_analysis.sort_values(by='yes', ascending=False)


# **Education vs Subscription Rate**

# In[64]:


education_analysis = pd.crosstab(df['education'], df['y'], normalize='index') * 100
education_analysis.sort_values(by='yes', ascending=False)


# **Does call duration impact subscription?**

# In[65]:


duration_analysis = df.groupby('y')['duration'].mean()
print(duration_analysis)
# duration_analysis


# **Campaign Efficiency**

# In[66]:


#(Average contacts required before subscription)

campaign_efficiency = df.groupby('y')['campaign'].mean()
print(campaign_efficiency)
# campaign_efficiency


# **Economic Factors Impact**

# In[67]:


economic_impact = df.groupby('y')[['euribor3m', 'emp.var.rate']].mean()
print(economic_impact)
# economic_impact


# **Correlation Matrix (Numeric Features)**

# In[68]:


correlation_matrix = df.corr(numeric_only=True)
print(correlation_matrix)
# correlation_matrix


# **Top 5 Age Groups with Highest Subscription**

# In[69]:


df['age_group'] = pd.cut(df['age'], bins=[15,25,35,45,55,65,100])
age_group_analysis = pd.crosstab(df['age_group'], df['y'], normalize='index') * 100
age_group_analysis.sort_values(by='yes', ascending=False)


# **Day of Week Performance**

# In[70]:


day_analysis = pd.crosstab(df['day_of_week'], df['y'], normalize='index') * 100
day_analysis.sort_values(by='yes', ascending=False)


# **<h1 style="font-size:30px">Some Operations with Matplotlib</h1>**

# **Plot Age Distribution (Histogram)**

# In[71]:


plt.figure()
plt.hist(df['age'], bins=20)
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.title("Age Distribution")
plt.show()


# **Subscription Count (Bar Chart)**

# In[72]:


counts = df['y'].value_counts()

plt.figure()
plt.bar(counts.index, counts.values)
plt.xlabel("Subscription")
plt.ylabel("Count")
plt.title("Subscription Count")
plt.show()


# **Average Duration by Subscription**

# In[73]:


avg_duration = df.groupby('y')['duration'].mean()

plt.figure()
plt.bar(avg_duration.index, avg_duration.values)
plt.xlabel("Subscription")
plt.ylabel("Average Duration")
plt.title("Avg Call Duration by Subscription")
plt.show()


# **Campaign Contacts Distribution**

# In[74]:


plt.figure()
plt.hist(df['campaign'], bins=20)
plt.xlabel("Number of Contacts")
plt.ylabel("Frequency")
plt.title("Campaign Contact Distribution")
plt.show()


# **Monthly Subscription Trend**

# In[75]:


monthly = pd.crosstab(df['month'], df['y'])['yes']

plt.figure()
plt.plot(monthly.index, monthly.values)
plt.xlabel("Month")
plt.ylabel("Subscriptions")
plt.title("Monthly Subscriptions")
plt.xticks(rotation=45)
plt.show()


# **Job Category vs Subscriptions**

# In[76]:


job_sub = pd.crosstab(df['job'], df['y'])['yes']

plt.figure()
plt.bar(job_sub.index, job_sub.values)
plt.xlabel("Job")
plt.ylabel("Subscriptions")
plt.title("Subscriptions by Job")
plt.xticks(rotation=90)
plt.show()


# **Correlation Heatmap (Using Matplotlib Only)**

# In[77]:


corr = df.corr(numeric_only=True)

plt.figure()
plt.imshow(corr)
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Correlation Matrix")
plt.show()


# **Age vs Duration (Scatter Plot)**

# In[78]:


plt.figure()
plt.scatter(df['age'], df['duration'])
plt.xlabel("Age")
plt.ylabel("Duration")
plt.title("Age vs Call Duration")
plt.show()


# **Economic Indicator Trend (Line Plot)**

# In[79]:


plt.figure()
plt.plot(df['euribor3m'])
plt.xlabel("Index")
plt.ylabel("Euribor Rate")
plt.title("Euribor Rate Variation")
plt.show()


# **Subscription by Age Group (Bar Chart)**

# In[80]:


df['age_group'] = pd.cut(df['age'], bins=[15,25,35,45,55,65,100])

age_group = pd.crosstab(df['age_group'], df['y'])['yes']

plt.figure()
plt.bar(age_group.index.astype(str), age_group.values)
plt.xlabel("Age Group")
plt.ylabel("Subscriptions")
plt.title("Subscriptions by Age Group")
plt.xticks(rotation=45)
plt.show()


# **<h1 style="font-size:30px">Dashboard Script</h1>**

# In[82]:

# =====================================================
# DATA LOADING
# =====================================================

@st.cache_data
def load_data(path):
    df = pd.read_excel(path)
    return df

df = load_data(r"C:\Users\Lakshya\Bank\bank-additional-full.xlsx")

# =====================================================
# ---------------- Sidebar Filters --------------------
# =====================================================

st.sidebar.header("🔎 Filters")

jobs = ["All"] + sorted(df['job'].dropna().unique().tolist())
selected_job = st.sidebar.selectbox("Job", jobs)

education = ["All"] + sorted(df['education'].dropna().unique().tolist())
selected_edu = st.sidebar.selectbox("Education", education)

age_range = st.sidebar.slider("Age Range",
                              int(df['age'].min()),
                              int(df['age'].max()),
                              (25, 60))

# Apply filters
filtered_df = df.copy()
if selected_job != "All":
    filtered_df = filtered_df[filtered_df['job'] == selected_job]

if selected_edu != "All":
    filtered_df = filtered_df[filtered_df['education'] == selected_edu]

filtered_df = filtered_df[
    filtered_df['age'].between(age_range[0], age_range[1])
]

# =====================================================
# HEADER & KPI BLOCK
# =====================================================

st.title("Bank Marketing Campaign — Executive Analytics Dashboard")

total_records = len(filtered_df)
subscription_rate = (filtered_df["y"] == "yes").mean() * 100
avg_age = filtered_df["age"].mean()
avg_duration = filtered_df["duration"].mean()
avg_contacts = filtered_df["campaign"].mean()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Records", f"{total_records:,}")
c2.metric("Subscription Rate (%)", f"{subscription_rate:.2f}")
c3.metric("Avg Age", f"{avg_age:.1f}")
c4.metric("Avg Call Duration", f"{avg_duration:.1f}")
c5.metric("Avg Campaign Contacts", f"{avg_contacts:.2f}")

# =====================================================
# DATA EXPORT
# =====================================================

csv_buffer = io.StringIO()
filtered_df.to_csv(csv_buffer, index=False)

st.download_button(
    "Download Filtered Dataset",
    csv_buffer.getvalue(),
    "bank_filtered.csv",
    "text/csv"
)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "Statistical Engine (NumPy)",
    "Business Intelligence (Pandas)",
    "Visual Analytics (Matplotlib)"
])

# =====================================================
# TAB 1 — NUMPY ENGINE
# =====================================================

with tab1:

    st.subheader("Core Statistical Metrics")

    numeric_cols = [
        'age', 'duration', 'campaign', 'pdays', 'previous',
        'emp.var.rate', 'cons.price.idx', 'cons.conf.idx',
        'euribor3m', 'nr.employed'
    ]

    data = filtered_df[numeric_cols].to_numpy()
    col = {name: i for i, name in enumerate(numeric_cols)}

    age = data[:, col["age"]]
    duration = data[:, col["duration"]]
    euribor = data[:, col["euribor3m"]]

    stats_df = pd.DataFrame({
        "Metric": ["Mean Age", "Median Age", "Std Age",
                   "Mean Duration", "Duration Outliers (Z>3)",
                   "Age-Duration Correlation",
                   "Euribor Variance"],
        "Value": [
            np.mean(age),
            np.median(age),
            np.std(age),
            np.mean(duration),
            np.sum(np.abs((duration - np.mean(duration)) / np.std(duration)) > 3),
            np.corrcoef(age, duration)[0, 1],
            np.var(euribor)
        ]
    })

    st.dataframe(stats_df, use_container_width=True)

# =====================================================
# TAB 2 — PANDAS BUSINESS INTELLIGENCE
# =====================================================

with tab2:

    st.subheader("Subscription Performance Analysis")

    subscription_table = (
        filtered_df["y"]
        .value_counts(normalize=True) * 100
    )
    st.dataframe(subscription_table)

    st.subheader("Subscription Rate by Job")
    job_analysis = (
        pd.crosstab(filtered_df["job"], filtered_df["y"], normalize="index") * 100
    ).sort_values(by="yes", ascending=False)
    st.dataframe(job_analysis)

    st.subheader("Education Impact")
    edu_analysis = (
        pd.crosstab(filtered_df["education"], filtered_df["y"], normalize="index") * 100
    ).sort_values(by="yes", ascending=False)
    st.dataframe(edu_analysis)

    st.subheader("Economic Indicators vs Subscription")
    econ_analysis = (
        filtered_df.groupby("y")[["euribor3m", "emp.var.rate"]].mean()
    )
    st.dataframe(econ_analysis)

    st.subheader("Correlation Matrix")
    st.dataframe(filtered_df.corr(numeric_only=True))

# =====================================================
# TAB 3 — FULL MATPLOTLIB ANALYTICS
# =====================================================

with tab3:

    st.subheader("Age Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_df["age"], bins=25)
    ax.set_xlabel("Age")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Subscription Count")
    fig, ax = plt.subplots()
    counts = filtered_df["y"].value_counts()
    ax.bar(counts.index, counts.values)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Average Duration by Subscription")
    fig, ax = plt.subplots()
    avg_duration = filtered_df.groupby("y")["duration"].mean()
    ax.bar(avg_duration.index, avg_duration.values)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Campaign Contacts Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_df["campaign"], bins=30)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Monthly Subscription Trend")
    monthly = pd.crosstab(filtered_df["month"], filtered_df["y"])["yes"]
    fig, ax = plt.subplots()
    ax.plot(monthly.index, monthly.values)
    ax.set_xticklabels(monthly.index, rotation=45)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Subscriptions by Job")
    job_sub = pd.crosstab(filtered_df["job"], filtered_df["y"])["yes"]
    fig, ax = plt.subplots()
    ax.bar(job_sub.index, job_sub.values)
    ax.set_xticklabels(job_sub.index, rotation=90)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Correlation Heatmap (Matplotlib Native)")
    corr = filtered_df.corr(numeric_only=True)
    fig, ax = plt.subplots()
    cax = ax.imshow(corr)
    plt.colorbar(cax)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticklabels(corr.columns)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Age vs Call Duration")
    fig, ax = plt.subplots()
    ax.scatter(filtered_df["age"], filtered_df["duration"], alpha=0.4)
    ax.set_xlabel("Age")
    ax.set_ylabel("Duration")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Euribor Rate Trend")
    fig, ax = plt.subplots()
    ax.plot(filtered_df["euribor3m"].values)
    ax.set_ylabel("Euribor 3M")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Subscription by Age Group")
    filtered_df["age_group"] = pd.cut(
        filtered_df["age"],
        bins=[15, 25, 35, 45, 55, 65, 100]
    )

    age_group = pd.crosstab(filtered_df["age_group"], filtered_df["y"])["yes"]

    fig, ax = plt.subplots()
    ax.bar(age_group.index.astype(str), age_group.values)
    ax.set_xticklabels(age_group.index.astype(str), rotation=45)
    st.pyplot(fig)
    plt.close(fig)