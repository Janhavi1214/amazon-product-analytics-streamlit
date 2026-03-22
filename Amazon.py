import streamlit as st
import pandas as pd
import sqlite3
import matplotlib as plt
import seaborn as sns

# Streamlit Page Configuration
st.set_page_config(
    page_title="Amazon Product Analysis",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Heading
st.title("🛒 Amazon Product Data Dashboard")
st.markdown("Analyze and explore Amazon product data with interactive visualizations and insights.")

# Database connection function
@st.cache_resource
def get_connection():
    conn = sqlite3.connect("amazon_data.db")
    return conn

# SQL execution function
@st.cache_data
def execute_sql(query, params=None):
    conn = get_connection()
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    return df

# Sidebar Filters
main_categories_query = "SELECT DISTINCT main_category FROM products"
main_categories = execute_sql(main_categories_query)['main_category'].tolist()

selected_category = st.sidebar.multiselect(
    "Filter by Main Category", options=main_categories, default=main_categories
)

# Price Range Filter
min_price, max_price = st.sidebar.slider(
    "Filter by Price", min_value=0.0, max_value=5000.0, value=(0.0, 5000.0), step=1.0
)

# Rating Range Filter
min_rating, max_rating = st.sidebar.slider(
    "Filter by Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1
)

# Query the filtered data from SQLite
filtered_query = f"""
    SELECT * FROM products
    WHERE main_category IN ({','.join(['?' for _ in selected_category])})
    AND discounted_price BETWEEN ? AND ?
    AND rating BETWEEN ? AND ?
"""
filtered_data = execute_sql(
    filtered_query,
    tuple(selected_category) + (min_price, max_price, min_rating, max_rating)
)

# Main Content
st.subheader("Filtered Data Overview")
st.write(filtered_data)

# Visualizations
st.subheader("Visualizations")

# 1. Rating Distribution by Main Category
st.markdown("### Rating Distribution by Main Category")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=filtered_data, x='main_category', y='rating', ax=ax)
ax.set_title("Rating Distribution by Main Category")
ax.set_xlabel('Main Category')
ax.set_ylabel('Rating')
ax.tick_params(axis='x', rotation=90, labelsize=10)
plt.tight_layout()
st.pyplot(fig)

# 2. Top Main Categories by Average Rating
st.markdown("### Top Main Categories by Average Rating")
top_categories = (
    filtered_data.groupby('main_category')['rating']
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(top_categories['main_category'], top_categories['rating'], color='blue')
ax.set_xlabel('Main Category', fontsize=12)
ax.set_ylabel('Average Rating', fontsize=12)
ax.set_title('Top Main Categories by Average Rating', fontsize=14)
ax.tick_params(axis='x', rotation=90, labelsize=10)
plt.tight_layout()
st.pyplot(fig)

# 3. Average Discount by Main Category
st.markdown("### Average Discount by Main Category")
avg_discount = (
    filtered_data.groupby('main_category')['discount_percentage']
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=avg_discount, x='main_category', y='discount_percentage', ax=ax, palette="viridis")
ax.set_title("Average Discount by Main Category")
ax.set_xlabel("Main Category")
ax.set_ylabel("Average Discount (%)")
ax.tick_params(axis='x', rotation=90, labelsize=10)
plt.tight_layout()
st.pyplot(fig)

# 4. Rating vs. Discounted Price (Scatter Plot)
st.markdown("### Rating vs. Discounted Price")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x='discounted_price', y='rating', hue='main_category', palette="tab10", ax=ax)
ax.set_title("Rating vs. Discounted Price")
ax.set_xlabel("Discounted Price")
ax.set_ylabel("Rating")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig)

# 5. Top Products by Rating Count
st.markdown("### Top Products by Rating Count")
top_rated_products = (
    filtered_data.nlargest(10, 'rating_count')[['product_name', 'rating_count']]
    .reset_index()
)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_rated_products, y='product_name', x='rating_count', ax=ax, palette="coolwarm")
ax.set_title("Top Products by Rating Count")
ax.set_xlabel("Rating Count")
ax.set_ylabel("Product Name")
plt.tight_layout()
st.pyplot(fig)

# Trending Products Section
st.subheader("🔥 Trending Products")
trending_query = """
    SELECT product_name, rating, rating_count, discounted_price 
    FROM products 
    WHERE rating_count > 1000 
    ORDER BY rating_count DESC 
    LIMIT 5
"""
trending_data = execute_sql(trending_query)
if not trending_data.empty:
    st.write(trending_data)
else:
    st.write("No trending products found.")

# Deals of the Day Section
st.subheader("💰 Deals of the Day")
deals_query = """
    SELECT product_name, main_category, discount_percentage, discounted_price, actual_price 
    FROM products 
    WHERE discount_percentage > 50
    ORDER BY discount_percentage DESC 
    LIMIT 10
"""
deals_data = execute_sql(deals_query)

if not deals_data.empty:
    st.write(deals_data)
else:
    st.write("No deals found.")
    
