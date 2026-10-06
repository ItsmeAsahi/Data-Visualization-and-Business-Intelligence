import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Page Configuration ---
st.set_page_config(page_title="E-Commerce Intelligence", page_icon="📈", layout="wide")

# --- 2. Synthetic Data Generator ---
@st.cache_data
def generate_synthetic_data():
    """Generates a fallback e-commerce dataset."""
    np.random.seed(42)
    data = {
        'CustomerID': range(1, 201),
        'Total_Spend': np.random.uniform(20, 3000, 200).round(2),
        'Category': np.random.choice(['Electronics', 'Apparel', 'Home & Garden', 'Beauty', 'Sports'], 200, p=[0.35, 0.25, 0.2, 0.1, 0.1]),
        'Website_Visits': np.random.randint(1, 100, 200)
    }
    return pd.DataFrame(data)

# --- 3. Sidebar: Data Upload & Column Mapping ---
st.sidebar.title("⚙️ Data Configuration")
uploaded_file = st.sidebar.file_uploader("Upload CSV Data", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
else:
    df = generate_synthetic_data()
    st.sidebar.info("Demo Data Loaded. Upload a CSV for custom analysis.")

# Detect column types
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

if not numeric_cols or not categorical_cols:
    st.error("Dataset must contain at least one numeric and one text column.")
    st.stop()

st.sidebar.markdown("### 📊 Map Your Data")
st.sidebar.markdown("Tell the dashboard how to read your file:")

# User defines which columns represent which e-commerce concepts
val_col = st.sidebar.selectbox("Revenue/Spend Column:", numeric_cols, index=0)
cat_col = st.sidebar.selectbox("Segment/Category Column:", categorical_cols, index=0)
eng_col = st.sidebar.selectbox("Engagement Column (e.g., Visits):", numeric_cols, index=min(1, len(numeric_cols)-1))

# --- 4. Main Dashboard UI ---
st.title("📈 E-Commerce Performance Overview")
st.markdown("Analyze revenue distribution, customer engagement, and segment viability.")

# Calculate core metrics
total_revenue = df[val_col].sum()
avg_order_value = df[val_col].mean()
top_category = df.groupby(cat_col)[val_col].sum().idxmax()
top_cat_revenue = df.groupby(cat_col)[val_col].sum().max()
top_cat_percentage = (top_cat_revenue / total_revenue) * 100

# Top KPI Cards
st.markdown("### Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Revenue", f"${total_revenue:,.2f}")
kpi2.metric("Average Value per Customer", f"${avg_order_value:,.2f}")
kpi3.metric("Top Performing Segment", str(top_category), f"{top_cat_percentage:.1f}% of Total Revenue")

st.markdown("---")

# --- 5. Analysis Section 1: Revenue Distribution (Graph + Theory + % Breakdown) ---
st.subheader("1. Category Revenue Distribution")

col_theory1, col_graph1 = st.columns([1, 1.5])

with col_theory1:
    st.info("**Business Theory: The Pareto Principle (80/20 Rule)**")
    st.write(
        "In e-commerce, revenue is rarely distributed evenly across categories. "
        "Understanding **Category Contribution** identifies 'cash cow' products. "
        "Capital allocation for marketing and inventory should be weighted toward these high-yield segments."
    )
    
    # Calculate and display dynamic percentages
    st.write("**Segment Breakdown:**")
    category_totals = df.groupby(cat_col)[val_col].sum().sort_values(ascending=False)
    for cat, val in category_totals.items():
        pct = (val / total_revenue) * 100
        st.markdown(f"- **{cat}:** {pct:.1f}% (${val:,.0f})")

with col_graph1:
    # Donut Chart for Percentages
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    colors = sns.color_palette('pastel')[0:len(category_totals)]
    ax1.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%', 
            colors=colors, startangle=90, pctdistance=0.85, 
            wedgeprops=dict(width=0.4, edgecolor='w'))
    ax1.set_title(f"Revenue Contribution by {cat_col}", fontsize=12)
    st.pyplot(fig1)

st.markdown("---")

# --- 6. Analysis Section 2: Engagement vs Conversion ---
st.subheader("2. Customer Engagement vs. Spend Value")

col_graph2, col_theory2 = st.columns([1.5, 1])

with col_graph2:
    # Scatter Plot
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=eng_col, y=val_col, hue=cat_col, data=df, palette='Set2', alpha=0.7, ax=ax2)
    
    # Calculate trendline
    z = np.polyfit(df[eng_col].dropna(), df[val_col].dropna(), 1)
    p = np.poly1d(z)
    plt.plot(df[eng_col], p(df[eng_col]), "r--", alpha=0.5, label="Trendline")
    
    plt.title(f"Correlation: {eng_col} vs {val_col}")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    st.pyplot(fig2)

with col_theory2:
    st.info("**Business Theory: Intent vs. Browsing Behavior**")
    st.write(
        "This scatter plot maps user engagement against final spend. "
        "A steep positive trendline indicates highly engaged users are converting well. "
    )
    
    # Dynamic insight based on data
    correlation = df[eng_col].corr(df[val_col])
    st.write("**Current Data Insight:**")
    if correlation > 0.5:
        st.success(f"**Strong Positive Correlation ({correlation:.2f}):** Higher engagement strongly drives higher spend.")
    elif correlation > 0.1:
        st.warning(f"**Weak Correlation ({correlation:.2f}):** Engagement leads to some sales, but many visitors might be 'window shopping'.")
    else:
        st.error(f"**Poor Correlation ({correlation:.2f}):** More visits do not equate to higher spend. Investigate site friction or pricing.")