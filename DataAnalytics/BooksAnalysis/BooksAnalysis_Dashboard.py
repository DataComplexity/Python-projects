#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
import seaborn as sns
import streamlit as st
import io


# In[2]:


df = pd.read_csv(r'C:\Users\Lakshya\Documents\Data_Sets\books.csv')


# In[3]:


print(df.columns.tolist())


# In[4]:


df.head(10)


# In[5]:


print(df['Publication_Date'].dtypes)


# In[6]:


df['Publication_Date'] = df['Publication_Date'].astype(str).str.replace('/', '-', regex=False)
df['Publication_Date'] = pd.to_datetime(df['Publication_Date'], dayfirst=False, errors='coerce')
df['Publication_Date'] = df['Publication_Date'].dt.strftime('%d-%m-%Y')


# In[7]:


#Remove extra column with NaN values.
# df = df.drop(columns=['Unnamed: 12'])


# In[8]:


print(df['Publication_Date'])


# In[9]:


# df


# In[10]:


# Convert necessary columns to numeric types
df['Average_Rating'] = pd.to_numeric(df['Average_Rating'], errors='coerce')
df['Ratings_Count'] = pd.to_numeric(df['Ratings_Count'], errors='coerce')
df['Num_Pages'] = pd.to_numeric(df['Num_Pages'], errors='coerce')


# **<h1 style="font-size: 30px;">Some Opeartions with Numpy</h1>**

# **Count of non-missing values:**

# In[11]:


print(df['Average_Rating'].count())


# **Minimum and Maximum values:**

# In[12]:


print("Minimum Pages: ", df['Num_Pages'].min())

df['Num_Pages'] = pd.to_numeric(df['Num_Pages'], errors='coerce')
print("Maximum Pages: ", df['Num_Pages'].max())


# **Filter Books with Num_Pages in a Certain Range (100-500):**

# In[13]:


# df[np.logical_and(df['Num_Pages'] >= 100, df['Num_Pages'] <= 500)]


# **Find Index of Book with Maximum Text Reviews:**

# In[14]:


print(np.argmax(df['Text_Reviews_Count'].values))


# **Get Mean and Std Dev of Ratings:**

# In[15]:


print(np.mean(df['Average_Rating']), np.std(df['Average_Rating']))


# **Rating Tier Assignment:**

# In[16]:


df['Average_Rating'] = pd.to_numeric(df['Average_Rating'], errors='coerce')
def assign_rating_tiers(ratings):
    # Define bin edges and matching labels
    bins = np.array([0, 3.0, 4.0, 4.5, np.inf])  # 4 bins → 4 categories
    labels = np.array(['Poor', 'Average', 'Good', 'Excellent'])

    # Start with "Unknown" by default
    tiers = np.full(ratings.shape, 'Unknown', dtype=object)

    # Find non-NaN values to apply binning
    valid_mask = ~np.isnan(ratings)
    valid_ratings = ratings[valid_mask]

    # Digitize and map to labels safely
    bin_indices = np.digitize(valid_ratings, bins) - 1
    tiers[valid_mask] = labels[bin_indices]

    return tiers

# Apply to your dataset
df['Rating_Tier'] = assign_rating_tiers(df['Average_Rating'].values)
print(df['Rating_Tier'])


# **Find Books with Extreme Pages or Ratings:**

# In[17]:


def detect_outliers(arr, threshold=1):
    z_scores = (arr - np.nanmean(arr)) / np.nanstd(arr)
    return np.abs(z_scores) > threshold

df['Is_Page_Outlier'] = detect_outliers(df['Num_Pages'].values)
df['Is_Rating_Outlier'] = detect_outliers(df['Average_Rating'].values)
print(df['Is_Rating_Outlier'].head(50))


# **Create a Book Score:**

# In[18]:


def min_max_normalize(array):
    min_val = np.nanmin(array)
    max_val = np.nanmax(array)
    if max_val - min_val == 0:
        return np.zeros_like(array)  # avoid division by zero
    return (array - min_val) / (max_val - min_val)

def compute_score(ratings, counts, pages):
    # Normalize all features
    norm_r = min_max_normalize(ratings)
    norm_c = min_max_normalize(counts)
    norm_p = min_max_normalize(pages)

    # Weighted score: favor rating & popularity more than length
    score = (0.5 * norm_r) + (0.4 * norm_c) + (0.1 * norm_p)
    return score

df['Book_Score'] = compute_score(df['Average_Rating'].values,
                                 df['Ratings_Count'].values,
                                 df['Num_Pages'].values)

df['Book_Score'] = (df['Book_Score'] * 10).round(2)
print(df['Book_Score'])


# **Find Books Closest to a Target Rating:**

# In[19]:


def get_closest_books(target, n=5):
    diffs = np.abs(df['Average_Rating'].values - target)
    indices = np.argsort(diffs)[:n]
    return df.iloc[indices]

closest_books = get_closest_books(4.3)
# closest_books


# In[20]:


# Define rolling average function
def rolling_avg_rating(arr, window=5):
    return np.convolve(arr, np.ones(window)/window, mode='same')


# **Rolling Average Rating:**

# In[21]:


# 1. Create a copy sorted by Publication_Date
df_sorted = df.sort_values('Publication_Date')

# 2. Compute rolling average rating on sorted data
rolling = rolling_avg_rating(df_sorted['Average_Rating'].fillna(0).values)
print(rolling)

# 3. Assign back to original DataFrame using index alignment
df['Rolling_Avg_Rating'] = pd.Series(rolling, index=df_sorted.index).sort_index()


# **<p style="font-size: 30px;">Some Operations with Pandas<p>**

# **Top Authors by Number of Books:**

# In[22]:


print(df['Authors'].value_counts().head(10))


# **Top Rated Books (Min 1000 ratings):**

# In[23]:


top_rated = df[df['Ratings_Count'] > 1000].sort_values(by='Average_Rating', ascending=False).head(10)
# print(top_rated)
# top_rated


# **Group by Publisher and get average rating:**

# In[24]:


publisher_avg = df.groupby('Publisher')['Average_Rating'].mean().sort_values(ascending=False).head(10)
print(publisher_avg)


# **Convert Publication_Date to datetime format:**

# In[25]:


df['Publication_Date'] = pd.to_datetime(df['Publication_Date'], errors='coerce', dayfirst=True)
print(df['Publication_Date'].dtype)


# **Number of Books per Year:**

# In[26]:


df['Year'] = df['Publication_Date'].dt.year
books_per_year = df['Year'].value_counts().sort_index()
print(books_per_year)


# **Books with Missing Data:**

# In[27]:


print(df.isnull().sum())


# **Average Page Count by Language:**

# In[28]:


df.groupby('Language_Code')['Num_Pages'].mean().sort_values(ascending=False)


# **Group-Aware Ranking Within Publisher:**

# In[29]:


df['Publisher_Rank'] = df.groupby('Publisher')['Book_Score'].rank(ascending=False, method='dense')
print(df['Publisher_Rank'])


# **Multi-Condition Filtering Using .query() for Readability:**

# In[30]:


high_quality_books = df.query(
    "Average_Rating >= 4.3 and Ratings_Count > 10000 and Num_Pages.between(200, 800)"
)
# print(high_quality_books)
# high_quality_books


# **<p style="font-size: 30px">Some Operations with Matplotlib<p>**

# **Compare values across categories (e.g., books, authors):**

# In[31]:


# Bar Plot:

top_books = df.nlargest(10, 'Book_Score')
plt.figure(figsize=(10, 6))
plt.barh(top_books['Title'], top_books['Book_Score'], color='skyblue')
plt.xlabel("Book Score")
plt.title("Top 10 Books by Score")
plt.gca().invert_yaxis()  # Highest at top
plt.tight_layout()
plt.show()


# **Distribution of a numeric feature (e.g., ratings, pages):**

# In[32]:


# Histogram:

plt.hist(df['Average_Rating'].dropna(), bins=20, edgecolor='black', color='lightgreen')
plt.xlabel("Average Rating")
plt.ylabel("Number of Books")
plt.title("Distribution of Book Ratings")
plt.show()


# **Trend over time (e.g., average rating by publication date):**

# In[33]:


# Line Plot:

df_date = df.sort_values('Publication_Date')
plt.plot(df_date['Publication_Date'], df_date['Average_Rating'], marker='o', linestyle='-')
plt.xlabel("Publication Date")
plt.ylabel("Average Rating")
plt.title("Rating Trend Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# **Relationship between two variables (e.g., rating vs. popularity):**

# In[34]:


# Scatter Plot:

plt.scatter(df['Average_Rating'], df['Ratings_Count'], alpha=0.5)
plt.xlabel("Average Rating")
plt.ylabel("Ratings Count")
plt.title("Rating vs Popularity")
plt.grid(True)
plt.show()


# **Proportion of languages, publishers, etc:**

# In[35]:


# Pie Chart: 

lang_counts = df['Language_Code'].value_counts().head(5)
plt.pie(lang_counts, labels=lang_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Top 5 Languages Used")
plt.axis('equal')
plt.show()


# **Distribution + outliers in ratings or page numbers:**

# In[36]:


# Box Plot:

plt.boxplot(df['Num_Pages'].dropna())
plt.title("Page Count Distribution")
plt.ylabel("Number of Pages")
plt.grid(True)
plt.show()


# **Detect numeric feature relationships:**

# In[37]:


#Heatmap (Correlation Matrix):

numeric_cols = ['Average_Rating', 'Ratings_Count', 'Num_Pages', 'Book_Score']
plt.figure(figsize=(8, 6))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Between Numeric Features")
plt.show()


# **Compare grouped categories (e.g., rating tiers by language):**

# In[38]:


#Stacked Bar Plot:

tier_lang = pd.crosstab(df['Language_Code'], df['Rating_Tier'])

tier_lang.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set3')
plt.title("Rating Tiers by Language")
plt.ylabel("Book Count")
plt.xlabel("Language")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# **Top 10 Books:**

# In[39]:


# Horizontal Bar Chart:

top_books = df.nlargest(10, 'Book_Score')
plt.barh(top_books['Title'], top_books['Book_Score'], color='coral')
plt.xlabel("Score")
plt.title("Top 10 Books")
plt.tight_layout()
plt.gca().invert_yaxis()
plt.show()


# **Compare trends (e.g., ratings vs decayed ratings):**

# In[40]:


# Multi-Line Plot:

# Ensure publication date is parsed
df['Publication_Date'] = pd.to_datetime(df['Publication_Date'], errors='coerce', dayfirst=True)

# Compute age in years (from today)
df['Book_Age_Years'] = (datetime.now() - df['Publication_Date']).dt.days / 365

# Apply a simple decay: newer books keep more of their rating
decay_factor = 0.02  # adjust this to control decay strength
df['Decayed_Rating'] = df['Average_Rating'] * np.exp(-decay_factor * df['Book_Age_Years'])


df_sorted = df.sort_values('Publication_Date')

plt.plot(df_sorted['Publication_Date'], df_sorted['Average_Rating'], label='Original Rating')
plt.plot(df_sorted['Publication_Date'], df_sorted['Decayed_Rating'], label='Decayed Rating', linestyle='--')
plt.xlabel("Publication Date")
plt.ylabel("Rating")
plt.title("Original vs Decayed Ratings Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# **Compare average scores per group:**

# In[41]:


# Bar Plot by Group (Author or Publisher):

top_authors = df.groupby('Authors')['Book_Score'].mean().nlargest(10)

top_authors.plot(kind='bar', color='slateblue')
plt.ylabel("Average Score")
plt.title("Top 10 Authors by Average Book Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# **Smooth version of histogram:**

# In[42]:


# Kernel Density Plot:

df['Average_Rating'].plot(kind='kde')
plt.title("KDE of Average Ratings")
plt.xlabel("Rating")
plt.grid(True)
plt.show()


# **Scatter plot with size as third variable:**

# In[43]:


# Bubble Plot:

plt.scatter(
    df['Average_Rating'], 
    df['Ratings_Count'], 
    s=df['Num_Pages'] / 10,  # bubble size
    alpha=0.5
)
plt.xlabel("Rating")
plt.ylabel("Ratings Count")
plt.title("Rating vs Popularity (Bubble Size = Page Count)")
plt.grid(True)
plt.show()


# **Subplots (Multiple Graphs Together):**

# In[44]:


fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Histogram
axs[0].hist(df['Average_Rating'].dropna(), bins=20, color='lightblue')
axs[0].set_title("Rating Distribution")

# Boxplot
axs[1].boxplot(df['Num_Pages'].dropna())
axs[1].set_title("Page Count")

plt.tight_layout()
plt.show()


# **<h1 style="font-size: 30px">Dashboard Script</h1>**

# In[45]:


# books_dashboard.py

# ---------------- NumPy Functions ---------------- #
def assign_rating_tiers(ratings):
    bins = np.array([0, 3.0, 4.0, 4.5, np.inf])
    labels = np.array(['Poor', 'Average', 'Good', 'Excellent'])
    tiers = np.full(ratings.shape, 'Unknown', dtype=object)
    valid_mask = ~np.isnan(ratings)
    valid_ratings = ratings[valid_mask]
    bin_indices = np.digitize(valid_ratings, bins) - 1
    tiers[valid_mask] = labels[bin_indices]
    return tiers

def detect_outliers(arr, threshold=1):
    # handle constant arrays or all-nan arrays gracefully
    if np.nanstd(arr) == 0 or np.all(np.isnan(arr)):
        return np.zeros_like(arr, dtype=bool)
    z_scores = (arr - np.nanmean(arr)) / np.nanstd(arr)
    return np.abs(z_scores) > threshold

def min_max_normalize(array):
    min_val = np.nanmin(array)
    max_val = np.nanmax(array)
    if np.isnan(min_val) or np.isnan(max_val) or max_val - min_val == 0:
        return np.zeros_like(array)
    return (array - min_val) / (max_val - min_val)

def compute_score(ratings, counts, pages):
    # convert to numpy arrays and handle NaNs
    r = np.array(ratings, dtype=float)
    c = np.array(counts, dtype=float)
    p = np.array(pages, dtype=float)
    norm_r = min_max_normalize(r)
    norm_c = min_max_normalize(c)
    norm_p = min_max_normalize(p)
    score = (0.5 * norm_r) + (0.4 * norm_c) + (0.1 * norm_p)
    return np.round(score * 10, 2)

def get_closest_books(df, target, n=5):
    # returns n books with average rating closest to target
    if 'Average_Rating' not in df.columns:
        return pd.DataFrame()
    diffs = np.abs(df['Average_Rating'].values - target)
    indices = np.argsort(diffs)[:n]
    return df.iloc[indices]

def rolling_avg_rating(arr, window=10):
    a = np.array(arr, dtype=float)
    if len(a) == 0:
        return a
    if len(a) < window or window <= 1:
        # fallback to simple mean smoothing
        kernel = np.ones(len(a)) / len(a)
        return np.convolve(np.nan_to_num(a), kernel, mode='same')
    kernel = np.ones(window) / window
    return np.convolve(np.nan_to_num(a), kernel, mode='same')

# ---------------- Load Data ---------------- #
# @st.cache_data
def load_data(path=r"C:\Users\Lakshya\Documents\Data_Sets\books.csv"):
    df = pd.read_csv(path, encoding='utf-8', low_memory=False)
    # remove any Unnamed junk columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Convert types safely
    df['Publication_Date'] = pd.to_datetime(df['Publication_Date'], errors='coerce', dayfirst=True)
    df['Average_Rating'] = pd.to_numeric(df['Average_Rating'], errors='coerce')
    df['Ratings_Count'] = pd.to_numeric(df['Ratings_Count'], errors='coerce')
    df['Text_Reviews_Count'] = pd.to_numeric(df['Text_Reviews_Count'], errors='coerce')
    df['Num_Pages'] = pd.to_numeric(df['Num_Pages'], errors='coerce')

    # Sort and reset
    df = df.sort_values('Publication_Date').reset_index(drop=True)

    # NumPy features
    df['Rating_Tier'] = assign_rating_tiers(df['Average_Rating'].values)
    df['Is_Page_Outlier'] = detect_outliers(df['Num_Pages'].values)
    df['Is_Rating_Outlier'] = detect_outliers(df['Average_Rating'].values)
    df['Book_Score'] = compute_score(df['Average_Rating'].values,
                                     df['Ratings_Count'].values,
                                     df['Num_Pages'].values)
    df['Rolling_Avg_Rating'] = rolling_avg_rating(df['Average_Rating'].fillna(0).values)
    return df

# ---------------- Sidebar / Filters ---------------- #
st.sidebar.header("🔎 Filters")

# language choices with 'All' option
languages = sorted(df['Language_Code'].dropna().unique().tolist())
languages = ["All"] + languages
lang = st.sidebar.selectbox("Language", languages, index=0)

# safe year bounds
years_series = df['Publication_Date'].dropna().dt.year
if len(years_series) == 0:
    min_year, max_year = 1900, datetime.now().year
else:
    min_year = int(years_series.min())
    max_year = int(years_series.max())
default_start = max(min_year, max_year - 15)
year_range = st.sidebar.slider("Publication Year Range", min_year, max_year, (default_start, max_year))

# extra interactive selectors
min_rating = st.sidebar.slider("Minimum Average Rating", 0.0, 5.0, 0.0, step=0.1)
min_ratings_count = st.sidebar.number_input("Minimum Ratings Count", min_value=0, value=0, step=100)

# Apply filters to create filtered_df
filtered_df = df.copy()
if lang != "All":
    filtered_df = filtered_df[filtered_df['Language_Code'] == lang]
filtered_df = filtered_df[filtered_df['Publication_Date'].dt.year.between(year_range[0], year_range[1])]
filtered_df = filtered_df[filtered_df['Average_Rating'].fillna(0) >= min_rating]
filtered_df = filtered_df[filtered_df['Ratings_Count'].fillna(0) >= min_ratings_count]

# ---------------- Header / KPIs ---------------- #
st.title("📚 Book Analytics Dashboard")

# show raw data toggle
if st.checkbox("Show Raw Data (top 5 rows)"):
    st.dataframe(df.head())

col1, col2, col3 = st.columns(3)
col1.metric("Total Books (filtered)", len(filtered_df))
col2.metric("Avg Rating (filtered)", round(filtered_df['Average_Rating'].mean() if not filtered_df.empty else 0, 2))
top_pub = filtered_df['Publisher'].mode()[0] if (not filtered_df.empty and 'Publisher' in filtered_df.columns and len(filtered_df['Publisher'].dropna())>0) else "N/A"
col3.metric("Top Publisher (filtered)", top_pub)

# quick download button for CSV
csv_buffer = io.StringIO()
filtered_df.to_csv(csv_buffer, index=False)
st.download_button("📥 Download CSV", csv_buffer.getvalue(), file_name="books.csv", mime="text/csv")

# ---------------- Tabs ---------------- #
tab1, tab2, tab3 = st.tabs(["⚡ NumPy Operations", "📑 Pandas Operations", "📊 Visual Analytics"])

# =====================================================
# ---------------- NumPy Based Visuals ----------------
# =====================================================
with tab1:
    st.header("NumPy-based Insights (filtered data)")

    # Top 10 Books by Average Rating (filtered)
    st.subheader("Top 10 Books by Average Rating")
    if filtered_df.empty:
        st.info("No data for selected filters.")
    else:
        top_books = filtered_df.nlargest(10, 'Average_Rating').dropna(subset=['Average_Rating'])
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(top_books['Title'].astype(str), top_books['Average_Rating'], color='skyblue')
        ax.invert_yaxis()
        ax.set_xlabel("Average Rating")
        ax.set_title("Top 10 Books by Average Rating")
        plt.tight_layout()
        st.pyplot(fig)

    # Top 10 Books by Book Score
    st.subheader("Top 10 Books by Book Score")
    if filtered_df.empty:
        st.info("No data for selected filters.")
    else:
        top_score_books = filtered_df.nlargest(10, 'Book_Score').dropna(subset=['Book_Score'])
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.barh(top_score_books['Title'].astype(str), top_score_books['Book_Score'], color='salmon')
        ax2.invert_yaxis()
        ax2.set_xlabel("Book Score")
        ax2.set_title("Top 10 Books by Book Score")
        plt.tight_layout()
        st.pyplot(fig2)

    # Rating Tier Distribution
    st.subheader("Rating Tiers Distribution")
    if filtered_df.empty:
        st.info("No data for selected filters.")
    else:
        rating_tier_counts = filtered_df['Rating_Tier'].value_counts()
        st.bar_chart(rating_tier_counts)

    # Outlier Summary
    st.subheader("Outlier Summary")
    st.write(f"Number of Page Outliers (filtered): {int(filtered_df['Is_Page_Outlier'].sum())}")
    st.write(f"Number of Rating Outliers (filtered): {int(filtered_df['Is_Rating_Outlier'].sum())}")

    # Rolling Average Rating Over Time
    st.subheader("Rolling Average Rating Over Time")
    if filtered_df.empty or filtered_df['Publication_Date'].dropna().empty:
        st.info("No publication-date data to show rolling average.")
    else:
        rolling_df = filtered_df.sort_values('Publication_Date')
        st.line_chart(rolling_df.set_index('Publication_Date')['Rolling_Avg_Rating'])

# =====================================================
# ---------------- Pandas Based Ops -------------------
# =====================================================
with tab2:
    st.header("Pandas Operations (filtered data)")

    st.subheader("Top Authors by Number of Books")
    if filtered_df.empty:
        st.info("No data for selected filters.")
    else:
        st.write(filtered_df['Authors'].value_counts().head(10))

    st.subheader("Top Rated Books (Min 1000 Ratings)")
    top_rated = filtered_df[filtered_df['Ratings_Count'] > 1000].sort_values(by='Average_Rating', ascending=False).head(10)
    st.write(top_rated[['Title', 'Authors', 'Average_Rating', 'Ratings_Count']])

    st.subheader("Average Rating by Publisher")
    publisher_avg = filtered_df.groupby('Publisher')['Average_Rating'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(publisher_avg)

    st.subheader("Books per Year")
    # create Year column if not exists
    filtered_df['Year'] = filtered_df['Publication_Date'].dt.year
    books_per_year = filtered_df['Year'].value_counts().sort_index()
    st.line_chart(books_per_year)

    st.subheader("Books with Missing Data (full dataset)")
    st.write(df.isnull().sum())

    st.subheader("Average Page Count by Language")
    avg_pages = filtered_df.groupby('Language_Code')['Num_Pages'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(avg_pages)

    # Group-aware ranking within publisher
    if 'Book_Score' in filtered_df.columns and 'Publisher' in filtered_df.columns:
        filtered_df['Publisher_Rank'] = filtered_df.groupby('Publisher')['Book_Score'].rank(ascending=False, method='dense')
        st.subheader("Publisher Rank (sample)")
        st.write(filtered_df[['Title', 'Publisher', 'Book_Score', 'Publisher_Rank']].head(10))

    # Example of multi-condition filtering using .query()
    st.subheader("High Quality Books (example query)")
    try:
        high_quality_books = filtered_df.query(
            "Average_Rating >= 4.3 and Ratings_Count > 10000 and Num_Pages.between(200, 800)"
        )
        st.write(high_quality_books[['Title', 'Authors', 'Average_Rating', 'Ratings_Count', 'Num_Pages']].head(10))
    except Exception:
        st.info("Query had no results or was invalid for filtered data.")

# =====================================================
# --------------- Matplotlib / Seaborn Ops -----------
# =====================================================
with tab3:
    st.header("Matplotlib & Seaborn Visual Analytics (filtered data)")

    # Top 10 Books by Score
    st.subheader("Top 10 Books by Score")
    if filtered_df.empty:
        st.info("No data for selected filters.")
    else:
        top_books_score = filtered_df.nlargest(10, 'Book_Score').dropna(subset=['Book_Score'])
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(top_books_score['Title'].astype(str), top_books_score['Book_Score'], color='coral')
        ax.invert_yaxis()
        ax.set_xlabel("Score")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # Distribution of Ratings (histogram)
    st.subheader("Distribution of Ratings")
    fig, ax = plt.subplots()
    ax.hist(filtered_df['Average_Rating'].dropna(), bins=20, edgecolor='black', color='lightgreen')
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Number of Books")
    st.pyplot(fig)
    plt.close(fig)

    # Rating Trend Over Time
    st.subheader("Rating Trend Over Time")
    if filtered_df['Publication_Date'].dropna().empty:
        st.info("No publication date data for trend.")
    else:
        df_date = filtered_df.sort_values('Publication_Date')
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_date['Publication_Date'], df_date['Average_Rating'], marker='o', linestyle='-')
        ax.set_xlabel("Publication Date")
        ax.set_ylabel("Average Rating")
        fig.autofmt_xdate()
        st.pyplot(fig)
        plt.close(fig)

    # Rating vs Popularity (scatter)
    st.subheader("Rating vs Popularity")
    fig, ax = plt.subplots()
    ax.scatter(filtered_df['Average_Rating'], filtered_df['Ratings_Count'], alpha=0.5)
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Ratings Count")
    st.pyplot(fig)
    plt.close(fig)

    # Top 5 Languages Used (Pie)
    st.subheader("Top 5 Languages Used (Pie)")
    lang_counts = filtered_df['Language_Code'].value_counts().head(5)
    if lang_counts.empty:
        st.info("No language data.")
    else:
        fig, ax = plt.subplots()
        ax.pie(lang_counts, labels=lang_counts.index, autopct='%1.1f%%', startangle=140)
        ax.set_title("Top 5 Languages Used")
        ax.axis('equal')
        st.pyplot(fig)
        plt.close(fig)

    # Page Count Distribution (Boxplot)
    st.subheader("Page Count Distribution (Boxplot)")
    fig, ax = plt.subplots()
    ax.boxplot(filtered_df['Num_Pages'].dropna())
    ax.set_ylabel("Number of Pages")
    st.pyplot(fig)
    plt.close(fig)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    numeric_cols = ['Average_Rating', 'Ratings_Count', 'Num_Pages', 'Book_Score']
    corr_df = filtered_df[numeric_cols].dropna(how='all')
    if corr_df.shape[0] < 2:
        st.info("Not enough numeric data for correlation heatmap.")
    else:
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_df.corr(), annot=True, cmap='coolwarm', ax=ax3)
        st.pyplot(fig3)
        plt.close(fig)

    # Rating Tiers by Language (Stacked Bar)
    st.subheader("Rating Tiers by Language (Stacked Bar)")
    try:
        tier_lang = pd.crosstab(filtered_df['Language_Code'], filtered_df['Rating_Tier'])
        fig, ax = plt.subplots(figsize=(10, 6))
        tier_lang.plot(kind='bar', stacked=True, ax=ax, colormap='Set3')
        ax.set_ylabel("Book Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)
    except Exception:
        st.info("Not enough data to build stacked bar.")

    # Original vs Decayed Ratings Over Time
    st.subheader("Original vs Decayed Ratings Over Time")
    if filtered_df['Publication_Date'].dropna().empty:
        st.info("No publication dates for decay plot.")
    else:
        df = filtered_df.copy()
        df['Book_Age_Years'] = (datetime.now() - df['Publication_Date']).dt.days / 365
        decay_factor = 0.02
        df['Decayed_Rating'] = df['Average_Rating'] * np.exp(-decay_factor * df['Book_Age_Years'])
        df_sorted = df.sort_values('Publication_Date')
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_sorted['Publication_Date'], df_sorted['Average_Rating'], label='Original Rating')
        ax.plot(df_sorted['Publication_Date'], df_sorted['Decayed_Rating'], label='Decayed Rating', linestyle='--')
        ax.legend()
        fig.autofmt_xdate()
        st.pyplot(fig)
        plt.close(fig)

    # Top 10 Authors by Average Book Score
    st.subheader("Top 10 Authors by Average Book Score")
    try:
        top_authors = filtered_df.groupby('Authors')['Book_Score'].mean().nlargest(10)
        fig, ax = plt.subplots(figsize=(10, 4))
        top_authors.plot(kind='bar', ax=ax, color='slateblue')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)
    except Exception:
        st.info("Not enough data for top authors plot.")

    # KDE of Average Ratings
    st.subheader("KDE of Average Ratings")
    if filtered_df['Average_Rating'].dropna().empty:
        st.info("No ratings available for KDE.")
    else:
        fig, ax = plt.subplots()
        filtered_df['Average_Rating'].plot(kind='kde', ax=ax)
        st.pyplot(fig)
        plt.close(fig)

    # Bubble Plot: Rating vs Popularity (Bubble Size = Page Count)
    st.subheader("Bubble Plot: Rating vs Popularity (Bubble Size = Page Count)")
    fig, ax = plt.subplots()
    ax.scatter(filtered_df['Average_Rating'], filtered_df['Ratings_Count'], s=filtered_df['Num_Pages'].fillna(0) / 10, alpha=0.5)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Ratings Count")
    st.pyplot(fig)
    plt.close(fig)

    # Histogram + Boxplot Subplots
    st.subheader("Histogram + Boxplot Subplots")
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].hist(filtered_df['Average_Rating'].dropna(), bins=20, color='lightblue')
    axs[0].set_title("Rating Distribution")
    axs[1].boxplot(filtered_df['Num_Pages'].dropna())
    axs[1].set_title("Page Count")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# In[46]:


# import unicodedata

# chars = ["鋼", "之", "鍊", "金", "術", "師"]

# for c in chars:
#     print(c, hex(ord(c)), unicodedata.name(c))


# In[ ]:





# In[ ]:




