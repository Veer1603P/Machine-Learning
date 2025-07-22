import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Main Panel Widget App", layout="centered")

st.sidebar.title("User Info")
name = st.sidebar.text_input("Enter your name:")

st.title("Interactive Streamlit Widgets")

if name:
    st.header(f"Welcome, {name} 👋")
else:
    st.header("Welcome, Guest 👋")

st.markdown("""
This app places **all interaction widgets in the main panel**, except for the name input.
Try the checkboxes, select your preferred language, and enjoy the interactive plot!
""")

st.subheader("Choose a Greeting:")
hello = st.checkbox("Hello")
hi = st.checkbox("Hi")
welcome = st.checkbox("Welcome")

if hello:
    st.success("Hello!")
if hi:
    st.success("Hi!")
if welcome:
    st.success("Welcome!")
if not (hello or hi or welcome):
    st.info("No greeting selected.")

st.subheader("Select Your Preferred Language:")
language = st.radio("Languages", ["Python", "React", "Java"])
if language == "Python":
    st.write("🐍 Python is great for data science and automation.")
elif language == "React":
    st.write("⚛️ React is awesome for frontend development.")
else:
    st.write("☕ Java is widely used in enterprise applications.")

st.subheader("Select Your Age:")
age = st.slider("Age", 18, 60, 25)
if age < 21:
    st.warning("You're quite young!")
elif age < 40:
    st.write("You're in your prime.")
else:
    st.write("Age is just a number.")

st.subheader("Want to see a plot?")
show_plot = st.checkbox("Yes, show me a sample plot!")
if show_plot:
    fig, ax = plt.subplots()
    ax.plot([4,3,2,1], [1, 20, 25, 23], marker='o')
    ax.set_title("Sample Line Plot")
    st.pyplot(fig)

st.subheader("Click the Button Below")
if st.button("Click Me!"):
    st.balloons()
    if name:
        st.success(f"Thanks, {name}! You clicked the button.")
    else:
        st.success("You clicked the button!")

st.caption("© 2025 Main Panel Widget App")
st.c