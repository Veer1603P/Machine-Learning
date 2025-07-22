import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="CSV DATA VISUALIZER")
st.title("REAL TIME DATA VISUALIZER")

st.sidebar.header("Step 1: Upload your dataset")
upload_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if upload_file:
    df = pd.read_csv(upload_file)
    st.success("File Uploaded Successfully")
    
    st.subheader("Data Preview")
    st.dataframe(df.head(10))

    st.sidebar.header("Step 2: Select columns")
    numeric_cols = df.select_dtypes(include='number').columns.to_list()
    
    selected_cols = st.sidebar.multiselect("Choose numeric columns to visualize", numeric_cols)
    

    if selected_cols:
        st.subheader("Visualization")
        chart_type = st.selectbox("Choose your chart type:", ["Bar chart", "Line chart", "Box chart", "Heatmap chart"])

        if chart_type == "Line chart":
            st.line_chart(df[selected_cols])
            
        elif chart_type == "Bar chart":
            st.bar_chart(df[selected_cols])

        elif chart_type == "Box chart":
            fig, ax = plt.subplots()
            df[selected_cols].plot(kind='box', ax=ax)
            st.pyplot(fig)

        elif chart_type == "Heatmap chart":
            fig, ax = plt.subplots()
            sns.heatmap(df[selected_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

    st.sidebar.header("Step 3: Filter Data (Optional)")
    for col in df.select_dtypes(include='object').columns:
        if st.sidebar.checkbox(f"Filter by {col}"):
            unique_vals = df[col].unique().tolist()
            selected_vals = st.sidebar.selectbox(f"Choose {col}",unique_vals)
            df=df[df[col]==selected_vals]
    st.download_button("Download the filtered CSV",data=df.to_csv(index=False),file_name="filtered_data.csv")

else:
    st.warning("Please do upload 1 file to visualize it.")