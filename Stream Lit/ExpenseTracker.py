import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💸 Advanced Expense Tracker")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.sidebar.header("🔎 Filter Expenses")
filter_category = st.sidebar.selectbox(
    "Select category to filter", ["All", "Food", "Transport", "Shopping", "Bills", "Others"]
)

# Add expense
st.subheader("➕ Add New Expense")

with st.form("expense_form"):
    desc = st.text_input("Description")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=0.5)
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Others"])
    date_input = st.date_input("Date", date.today())

    submit = st.form_submit_button("Add Expense")

    if submit and desc and amount > 0:
        st.session_state.expenses.append({
            "Date": date_input,
            "Description": desc,
            "Category": category,
            "Amount": amount
        })
        st.success("✅ Expense added successfully!")

# Convert to DataFrame
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)

    # Filter by category
    if filter_category != "All":
        df = df[df["Category"] == filter_category]

    st.subheader("📋 Expense Table")
    st.dataframe(df, use_container_width=True)

    # Show total
    total = df["Amount"].sum()
    st.markdown(f"### 💰 Total Expense: ₹{total:.2f}")

    # Download CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "expenses.csv", "text/csv")
else:
    st.info("No expenses to display.")
