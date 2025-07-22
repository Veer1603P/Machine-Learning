import streamlit as st
import pandas as pd
from datetime import datetime

# App Config
st.set_page_config("Zomato Next-Level", layout="wide")
st.title("🍽️ Zomato - Next Level App")

# Sample in-memory restaurant & menu data
restaurants = [
    {"id": 1, "name": "Foodie King", "location": "Mumbai"},
    {"id": 2, "name": "Spicy Hub", "location": "Delhi"},
    {"id": 3, "name": "Urban Bites", "location": "Bangalore"},
]

menu = [
    {"restaurant_id": 1, "name": "Pizza", "price": 250, "category": "Meals", "veg": True, "image": "https://source.unsplash.com/400x300/?pizza"},
    {"restaurant_id": 1, "name": "Cold Coffee", "price": 100, "category": "Drinks", "veg": True, "image": "https://source.unsplash.com/400x300/?cold-coffee"},
    {"restaurant_id": 2, "name": "Burger", "price": 120, "category": "Meals", "veg": False, "image": "https://source.unsplash.com/400x300/?burger"},
    {"restaurant_id": 2, "name": "Chai", "price": 30, "category": "Drinks", "veg": True, "image": "https://source.unsplash.com/400x300/?chai"},
    {"restaurant_id": 3, "name": "Gulab Jamun", "price": 60, "category": "Desserts", "veg": True, "image": "https://source.unsplash.com/400x300/?gulab-jamun"},
]

# Convert to DataFrames
rest_df = pd.DataFrame(restaurants)
menu_df = pd.DataFrame(menu)

# Session State Initialization
if "username" not in st.session_state:
    st.session_state.username = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "orders" not in st.session_state:
    st.session_state.orders = []

# Login Section
if not st.session_state.username:
    st.subheader("👤 Login")
    username = st.text_input("Enter your name")
    if st.button("Login") and username.strip():
        st.session_state.username = username.strip()
        st.success(f"Welcome, {st.session_state.username}!")
    st.stop()

# Sidebar - Logged In Info
st.sidebar.markdown(f"👤 **{st.session_state.username}**")
if st.sidebar.button("🔄 Logout"):
    st.session_state.username = None
    st.session_state.cart = []
    st.experimental_rerun()

# Restaurant Selection
st.subheader("🏬 Choose a Restaurant")
selected_rest = st.selectbox("Select Restaurant", rest_df["name"])
rest_id = rest_df[rest_df["name"] == selected_rest]["id"].values[0]

# Sidebar Filters
st.sidebar.header("🔍 Filters")
category_filter = st.sidebar.selectbox("Category", ["All", "Meals", "Drinks", "Desserts"])
veg_only = st.sidebar.checkbox("Veg Only", value=False)
search_query = st.sidebar.text_input("Search")

# Filter Menu
filtered = menu_df[menu_df["restaurant_id"] == rest_id]
if category_filter != "All":
    filtered = filtered[filtered["category"] == category_filter]
if veg_only:
    filtered = filtered[filtered["veg"] == True]
if search_query:
    filtered = filtered[filtered["name"].str.contains(search_query, case=False)]

# Menu Display
st.subheader(f"📜 Menu - {selected_rest}")
if filtered.empty:
    st.info("No items match your filters.")
else:
    for i, row in filtered.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {row['name']}")
                st.markdown(f"{'🟢 Veg' if row['veg'] else '🔴 Non-Veg'} | ₹{row['price']} | {row['category']}")
                qty = st.number_input(f"Qty for {row['name']}", min_value=0, max_value=10, key=row['name'])
                if qty > 0:
                    st.session_state.cart.append({
                        "restaurant": selected_rest,
                        "item": row["name"],
                        "qty": qty,
                        "price": row["price"]
                    })
            with col2:
                st.image(row["image"], width=130)

# Cart
if st.session_state.cart:
    st.markdown("---")
    st.subheader("🛒 Cart")
    cart_df = pd.DataFrame(st.session_state.cart)
    cart_df["total"] = cart_df["qty"] * cart_df["price"]
    st.table(cart_df[["item", "qty", "price", "total"]])
    total = cart_df["total"].sum()
    st.markdown(f"### 💰 Total: ₹{total}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Place Order"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for order in st.session_state.cart:
                st.session_state.orders.append({
                    "user": st.session_state.username,
                    "restaurant": order["restaurant"],
                    "item": order["item"],
                    "qty": order["qty"],
                    "price": order["price"],
                    "timestamp": now
                })
            st.session_state.cart = []
            st.success("Order placed successfully! 🚀")

    with col2:
        if st.button("🗑️ Clear Cart"):
            st.session_state.cart = []
            st.info("Cart cleared.")

# Order History
st.markdown("---")
st.subheader("📦 Order History")
user_orders = [o for o in st.session_state.orders if o["user"] == st.session_state.username]
if user_orders:
    history_df = pd.DataFrame(user_orders)
    st.dataframe(history_df[["timestamp", "restaurant", "item", "qty", "price"]])
else:
    st.info("No orders placed yet.")
