#!/usr/bin/env python
# coding: utf-8

# In[94]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io


# In[95]:


df = pd.read_excel(r'C:\Users\Lakshya\Adult_Income_Census\adult.xlsx', na_values="?")


# In[96]:


#Replacing missing values "?" to "NaN":
df.replace("?", pd.NA, inplace=True)


# In[97]:


df.head(50)


# **<h1 style="font-size: 30px;">Some Opeartions with Numpy</h1>**

# **Convert the age column to a NumPy array and compute basic statistics**

# In[98]:


# Mean, Median, Std
ages = df['age'].to_numpy()

print("Mean:", np.mean(ages))
print("Median:", np.median(ages))
print("Std:", np.std(ages))


# **Find the percentage of people earning >50K using NumPy**

# In[99]:


income = df['income'].to_numpy()

high_income_ratio = np.mean(income == '>50K')
print("Percentage earning >50K:", high_income_ratio * 100)


# **Normalize hours.per.week using Min–Max normalization**

# In[100]:


hours = df['hours.per.week'].to_numpy()

normalized_hours = (hours - hours.min()) / (hours.max() - hours.min())

#Printing head 10 only:
print(normalized_hours[:10])


# **Detect outliers in capital.gain using Z-score**

# In[101]:


capital_gain = df['capital.gain'].to_numpy()

z_scores = (capital_gain - capital_gain.mean()) / capital_gain.std()
outliers = capital_gain[np.abs(z_scores) > 3]

#Printing head 10 only:
print("Outliers:", outliers[:10])


# **Compute correlation between age and hours.per.week**

# In[102]:


age = df['age'].to_numpy()
hours = df['hours.per.week'].to_numpy()

correlation = np.corrcoef(age, hours)[0, 1]
print("Correlation:", correlation)


# **Create a NumPy mask to filter people working more than 40 hours**

# In[103]:


mask = df['hours.per.week'].to_numpy() > 40
filtered_ages = df['age'].to_numpy()[mask]

#Printing head 10 only:
print(filtered_ages[:10])


# **Encode sex column into binary using NumPy**

# In[104]:


sex = df['sex'].to_numpy()
encoded_sex = np.where(sex == 'Male', 1, 0)

#Printing head 10 only:
print(encoded_sex[:10])


# **Calculate average age by income group using NumPy only**

# In[105]:


ages = df['age'].to_numpy()
income = df['income'].to_numpy()

avg_high = ages[income == '>50K'].mean()
avg_low = ages[income == '<=50K'].mean()

print("Avg age (>50K):", avg_high)
print("Avg age (<=50K):", avg_low)


# **Create a NumPy histogram of education.num**

# In[106]:


education_num = df['education.num'].to_numpy()

hist, bins = np.histogram(education_num, bins=10)
print("Histogram:", hist)
print("Bins:", bins)


# **Build a NumPy feature matrix (age, hours.per.week, capital.gain)**

# In[107]:


features = np.column_stack([
    df['age'].to_numpy(),
    df['hours.per.week'].to_numpy(),
    df['capital.gain'].to_numpy()
])

print(features.shape)
#Head -> 5:
print(features[:5])


# **<h1 style="font-size: 30px;">Some Opeartions with Pandas</h1>**

# **What is the average age by income group?**

# In[108]:


df.groupby('income')['age'].mean()


# **Which occupation has the highest average salary rate (>50K percentage)?**

# In[109]:


result = (
    df.groupby('occupation')['income']
      .apply(lambda x: (x == '>50K').mean())
      .sort_values(ascending=False)
)

print(result.head())


# **Count number of people per education level**

# In[110]:


df['education'].value_counts()


# **What percentage of males earn >50K?**

# In[111]:


male_high_income = df[df['sex'] == 'Male']
percentage = (male_high_income['income'] == '>50K').mean() * 100

print(percentage)


# **Find correlation between numerical features**

# In[112]:


df.corr(numeric_only=True)


# **Create a new column: income_binary (1 = >50K, 0 = <=50K)**

# In[113]:


df['income_binary'] = df['income'].map({'>50K': 1, '<=50K': 0})


# **What is the average hours worked per week by marital status?**

# In[114]:


df.groupby('marital.status')['hours.per.week'].mean()


# **Find top 5 oldest people in the dataset**

# In[115]:


df.sort_values('age', ascending=False).head(5)


# **Pivot table: average age by sex and income**

# In[116]:


pd.pivot_table(
    df,
    values='age',
    index='sex',
    columns='income',
    aggfunc='mean'
)


# **Identify the country with highest proportion of >50K earners**

# In[117]:


country_income = (
    df.groupby('native.country')['income']
      .apply(lambda x: (x == '>50K').mean())
      .sort_values(ascending=False)
)

print(country_income.head())


# **<h1 style="font-size:30px">Some Operations with Matplotlib</h1>**

# **Plot age distribution (Histogram)**

# In[118]:


plt.hist(df['age'], bins=20)
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.title("Age Distribution")
plt.show()


# **Bar chart of income distribution**

# In[119]:


income_counts = df['income'].value_counts()

plt.bar(income_counts.index, income_counts.values)
plt.xlabel("Income")
plt.ylabel("Count")
plt.title("Income Distribution")
plt.show()


# **Boxplot of hours.per.week by income group**

# In[120]:


groups = [
    df[df['income'] == '<=50K']['hours.per.week'],
    df[df['income'] == '>50K']['hours.per.week']
]

plt.boxplot(groups, tick_labels=['<=50K', '>50K'])
plt.title("Hours per Week by Income")
plt.show()


# **Scatter plot: age vs hours.per.week**

# In[121]:


plt.scatter(df['age'], df['hours.per.week'])
plt.xlabel("Age")
plt.ylabel("Hours per Week")
plt.title("Age vs Working Hours")
plt.show()


# **Line plot: Average age by education.num**

# In[122]:


avg_age = df.groupby('education.num')['age'].mean()

plt.plot(avg_age.index, avg_age.values)
plt.xlabel("Education Number")
plt.ylabel("Average Age")
plt.title("Average Age by Education Level")
plt.show()


# **Pie chart of gender distribution**

# In[123]:


gender_counts = df['sex'].value_counts()

plt.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%')
plt.title("Gender Distribution")
plt.show()


# **Bar chart: Top 10 occupations**

# In[124]:


top_occ = df['occupation'].value_counts().head(10)

plt.barh(top_occ.index, top_occ.values)
plt.title("Top 10 Occupations")
plt.xlabel("Count")
plt.show()


# **Histogram comparing capital.gain for income groups**

# In[125]:


plt.hist(df[df['income'] == '<=50K']['capital.gain'], bins=30, alpha=0.5)
plt.hist(df[df['income'] == '>50K']['capital.gain'], bins=30, alpha=0.5)
plt.legend(['<=50K', '>50K'])
plt.title("Capital Gain Comparison")
plt.show()


# **Correlation heatmap (using Matplotlib only)**

# In[126]:


corr = df.corr(numeric_only=True)

plt.imshow(corr, cmap='coolwarm')
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Correlation Heatmap")
plt.show()


# **Stacked bar chart: Income by sex**

# In[127]:


income_sex = pd.crosstab(df['sex'], df['income'])

income_sex.plot(kind='bar', stacked=True)
plt.title("Income by Sex")
plt.ylabel("Count")
plt.show()


# **<h1 style="font-size:30px">Dashboard Script</h1>**

# In[136]:


# Census_dashboard_pro.py

# =====================================================
# ---------------- Load & Prepare Data ---------------
# =====================================================

@st.cache_data
def load_data(path=r'C:\Users\Lakshya\Adult_Income_Census\adult.xlsx'):
    df = pd.read_excel(path, na_values="?")

    # Drop missing rows for clean analytics
    df.dropna(inplace=True)

    # Convert numeric columns
    numeric_cols = [
        "age", "fnlwgt", "education.num",
        "capital.gain", "capital.loss", "hours.per.week"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Feature engineering
    df["income_binary"] = df["income"].map({">50K": 1, "<=50K": 0})

    # Age bands
    df["age.band"] = pd.cut(
        df["age"],
        bins=[17, 25, 35, 45, 55, 65, 100],
        labels=["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
    )

    return df


df = load_data()

# =====================================================
# ---------------- Sidebar Filters -------------------
# =====================================================

st.sidebar.header("🔎 Global Filters")

income_option = st.sidebar.selectbox("Income", ["All", "<=50K", ">50K"])
sex_option = st.sidebar.selectbox("Gender", ["All"] + sorted(df["sex"].unique()))

age_min, age_max = int(df["age"].min()), int(df["age"].max())
age_range = st.sidebar.slider("Age Range", age_min, age_max, (25, 60))

# Apply filters
filtered_df = df.copy()

# Create age bands
bins = [0, 25, 35, 45, 55, 65, 100]
labels = ["0-25", "26-35", "36-45", "46-55", "56-65", "65+"]
filtered_df["age_band"] = pd.cut(filtered_df["age"], bins=bins, labels=labels)

if income_option != "All":
    filtered_df = filtered_df[filtered_df["income"] == income_option]

if sex_option != "All":
    filtered_df = filtered_df[filtered_df["sex"] == sex_option]

filtered_df = filtered_df[
    filtered_df["age"].between(age_range[0], age_range[1])
]

# =====================================================
# ---------------- Header & KPIs ---------------------
# =====================================================

st.title("👥 Adult Census — Income Analytics")

total_records = len(filtered_df)
income_rate = filtered_df["income_binary"].mean() * 100 if total_records > 0 else 0
avg_hours = filtered_df["hours.per.week"].mean()
avg_age = filtered_df["age"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", total_records)
col2.metric("High Income %", f"{income_rate:.2f}%")
col3.metric("Avg Hours/Week", f"{avg_hours:.2f}")
col4.metric("Avg Age", f"{avg_age:.2f}")

# Download
csv_buffer = io.StringIO()
filtered_df.to_csv(csv_buffer, index=False)
st.download_button("📥 Download Filtered Data",
                   csv_buffer.getvalue(),
                   "filtered_adult.csv",
                   "text/csv")

# =====================================================
# ---------------- Tabs ------------------------------
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Demographics",
    "🎓 Education & Work",
    "🌍 Geographic",
    "📈 Advanced Analytics"
])

# =====================================================
# ---------------- Tab 1: Demographics ---------------
# =====================================================

with tab1:

    st.subheader("Age Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_df["age"], bins=20)
    ax.set_xlabel("Age")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Income Probability by Age Band")
    age_income = (
        filtered_df.groupby("age_band", observed=False)["income_binary"]
        .mean()
        .sort_index()
    )

    fig, ax = plt.subplots()
    ax.bar(age_income.index.astype(str), age_income.values)
    ax.set_ylabel("Probability of >50K")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Gender vs Income")
    gender_income = (
        filtered_df.groupby("sex")["income_binary"]
        .mean()
    )
    st.bar_chart(gender_income)

# =====================================================
# ---------------- Tab 2: Education & Work -----------
# =====================================================

with tab2:

    st.subheader("Income Rate by Education Level")
    edu_income = (
        filtered_df.groupby("education")["income_binary"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(edu_income.index, edu_income.values)
    ax.invert_yaxis()
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Income Rate by Occupation")
    occ_income = (
        filtered_df.groupby("occupation")["income_binary"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(occ_income)

    st.subheader("Workclass Distribution")
    workclass_counts = filtered_df["workclass"].value_counts()
    st.bar_chart(workclass_counts)

# =====================================================
# ---------------- Tab 3: Geographic ------------------
# =====================================================

with tab3:

    st.subheader("Top Countries by High Income Rate")

    country_income = (
        filtered_df.groupby("native.country")["income_binary"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(country_income.index, country_income.values)
    ax.invert_yaxis()
    st.pyplot(fig)
    plt.close(fig)

# =====================================================
# ---------------- Tab 4: Advanced Analytics ---------
# =====================================================

with tab4:

    st.subheader("Correlation Heatmap")

    numeric_df = filtered_df.select_dtypes(include=np.number)

    if numeric_df.shape[0] > 1:
        corr = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Not enough numeric data.")

    st.subheader("Age vs Hours Worked")

    fig, ax = plt.subplots()
    ax.scatter(filtered_df["age"],
               filtered_df["hours.per.week"],
               alpha=0.4)
    ax.set_xlabel("Age")
    ax.set_ylabel("Hours per Week")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Statistical Summary")
    st.dataframe(filtered_df.describe())


# In[141]:


# jupyter nbconvert --to script notebook.ipynb


# In[ ]:




