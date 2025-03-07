import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Energy Efficiency Dashboard", layout="wide")

st.title("📊 Energy Efficiency Dashboard for Smart Buildings")

# File uploader
uploaded_file = st.file_uploader("📂 Energy_comsumption.csv", type="csv")

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)

    # Sidebar for filtering
    st.sidebar.header("🔍 Data Filters")
    columns = df.columns.tolist()

    # Auto-detect numerical & categorical columns
    num_columns = df.select_dtypes(include=['number']).columns.tolist()
    cat_columns = df.select_dtypes(exclude=['number']).columns.tolist()

    # Display preview and summary
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 Data Summary")
    st.write(df.describe())

    # Multi-filter selection
    st.sidebar.subheader("🔎 Filter Data")
    filters = {}
    for col in cat_columns:
        unique_values = df[col].dropna().unique()
        selected_value = st.sidebar.selectbox(f"Filter by {col}", ["All"] + list(unique_values))
        if selected_value != "All":
            filters[col] = selected_value

    # Apply filters
    filtered_df = df.copy()
    for col, value in filters.items():
        filtered_df = filtered_df[filtered_df[col] == value]

    # Display filtered data
    st.subheader("🔹 Filtered Data")
    st.dataframe(filtered_df)

    # Visualization section
    st.subheader("📈 Energy Consumption Trends")
    col1, col2, col3 = st.columns(3)

    with col1:
        x_column = st.selectbox("Select X-axis", num_columns, index=0)
    with col2:
        y_column = st.selectbox("Select Y-axis", num_columns, index=1)
    with col3:
        plot_type = st.selectbox("Select Plot Type", ["Line Chart", "Scatter Plot", "Histogram"])

    # Generate plots
    fig, ax = plt.subplots(figsize=(10, 5))
    if plot_type == "Line Chart":
        sns.lineplot(data=filtered_df, x=x_column, y=y_column, marker="o", ax=ax)
    elif plot_type == "Scatter Plot":
        sns.scatterplot(data=filtered_df, x=x_column, y=y_column, ax=ax)
    elif plot_type == "Histogram":
        sns.histplot(data=filtered_df, x=x_column, kde=True, ax=ax)

    ax.set_title(f"{plot_type} of {y_column} vs {x_column}")
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    st.pyplot(fig)

else:
    st.warning("⚠ Please upload a CSV file to begin analysis.")