import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title="Data Visualizer", page_icon="📊", layout="wide")

# CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2196F3;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<div class="main-header">📊 Data Visualizer</div>', unsafe_allow_html=True)

# Navigation
menu = st.sidebar.radio("Choose an Option", ["🔢 Array Analyzer", "📁 CSV File Analyzer"])

# --- ARRAY ANALYZER ---
if menu == "🔢 Array Analyzer":
    st.markdown('<div class="section-header">Array Analyzer</div>', unsafe_allow_html=True)

    rows = st.number_input("Rows", 1, 20, 3)
    cols = st.number_input("Columns", 1, 20, 3)

    df_array = pd.DataFrame(np.zeros((rows, cols)))
    edited_df = st.data_editor(df_array, use_container_width=True, key="array_editor")

    if st.button("Generate Heatmap"):
        array = edited_df.to_numpy()
        st.dataframe(array, use_container_width=True)

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(array, annot=True, cmap='viridis', ax=ax)
        ax.set_title("Heatmap of Input Array")
        st.pyplot(fig, use_container_width=True)

# --- CSV ANALYZER ---
elif menu == "📁 CSV File Analyzer":
    st.markdown('<div class="section-header">CSV File Analyzer</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully!")
            
            if df.isnull().sum().sum() > 0:
                st.warning("Null values detected. Choose how to handle them:")
                method = st.radio("Null Handling Method", ["Drop Rows", "Forward Fill", "Backward Fill", "Do Nothing"])

                if method == "Drop Rows":
                    df = df.dropna()
                elif method == "Forward Fill":
                    df = df.fillna(method='ffill')
                elif method == "Backward Fill":
                    df = df.fillna(method='bfill')

            st.subheader("Data Preview")
            st.dataframe(df.head(), use_container_width=True)

            option = st.selectbox("Select Analysis Type", ["Basic Info", "Head/Tail", "Statistics", "Visualizations"])

            if option == "Basic Info":
                st.text("Data Info:")
                st.text(df.info())
                st.text("Shape: {} rows, {} columns".format(*df.shape))
                st.dataframe(df.describe(), use_container_width=True)

            elif option == "Head/Tail":
                st.subheader("Top Rows")
                st.dataframe(df.head(), use_container_width=True)
                st.subheader("Bottom Rows")
                st.dataframe(df.tail(), use_container_width=True)

            elif option == "Statistics":
                num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if not num_cols:
                    st.warning("No numeric columns available.")
                else:
                    st.dataframe(df[num_cols].describe().T, use_container_width=True)

            elif option == "Visualizations":
                num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(num_cols) < 2:
                    st.warning("At least 2 numeric columns are required.")
                else:
                    viz = st.multiselect("Select Visualizations", ["Scatter Plot", "Bar Chart", "Line Plot", "Pie Chart", "Correlation Heatmap"])

                    if "Scatter Plot" in viz:
                        x = st.selectbox("X-axis", num_cols, index=0)
                        y = st.selectbox("Y-axis", num_cols, index=1)
                        fig, ax = plt.subplots()
                        sns.scatterplot(data=df, x=x, y=y, ax=ax)
                        ax.set_title(f"Scatter Plot: {x} vs {y}")
                        st.pyplot(fig, use_container_width=True)

                    if "Bar Chart" in viz:
                        bar_col = st.selectbox("Column for Bar Chart", num_cols)
                        fig, ax = plt.subplots()
                        df[bar_col].value_counts().head(10).plot(kind='bar', ax=ax)
                        ax.set_title(f"Bar Chart: {bar_col}")
                        st.pyplot(fig, use_container_width=True)

                    if "Line Plot" in viz:
                        fig, ax = plt.subplots()
                        df[num_cols].plot(ax=ax)
                        ax.set_title("Line Plot of Numeric Columns")
                        st.pyplot(fig, use_container_width=True)

                    if "Pie Chart" in viz:
                        pie_col = st.selectbox("Column for Pie Chart", num_cols)
                        fig, ax = plt.subplots()
                        df[pie_col].value_counts().head(5).plot.pie(autopct="%1.1f%%", ax=ax)
                        ax.set_ylabel("")
                        ax.set_title(f"Pie Chart: {pie_col}")
                        st.pyplot(fig, use_container_width=True)

                    if "Correlation Heatmap" in viz:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
                        ax.set_title("Correlation Heatmap")
                        st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
