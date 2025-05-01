import streamlit as st
from datetime import datetime, date
import pandas as pd

# Initialize session state
if "entries" not in st.session_state:
    st.session_state.entries = []

# Title
st.title("🥗 Calorie Tracker App")

# Sidebar navigation
menu = st.sidebar.radio("Go to", ["Add Meal", "View Log", "Summary"])

# Add Meal Page
if menu == "Add Meal":
    st.header("🍽️ Add a Meal")

    with st.form("meal_form"):
        meal_name = st.text_input("Meal Name")
        calories = st.number_input("Calories", min_value=0, step=1)
        ingredients = st.text_area("Ingredients (comma-separated)")
        meal_date = st.date_input("Date", date.today())
        submit = st.form_submit_button("Add Meal")

        if submit and meal_name:
            st.session_state.entries.append({
                "Meal": meal_name,
                "Calories": calories,
                "Ingredients": ingredients,
                "Date": meal_date.strftime("%Y-%m-%d"),
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.success(f"Added {meal_name} ({calories} kcal)")

# View Log Page
elif menu == "View Log":
    st.header("📋 View Meal Log")

    if not st.session_state.entries:
        st.info("No meals added yet.")
    else:
        df = pd.DataFrame(st.session_state.entries)
        st.dataframe(df)

        filter_date = st.date_input("Filter by Date (optional)", date.today())
        if filter_date:
            filtered_df = df[df["Date"] == filter_date.strftime("%Y-%m-%d")]
            st.subheader(f"Meals on {filter_date}")
            st.dataframe(filtered_df)

# Summary Page
elif menu == "Summary":
    st.header("📊 Calorie Summary")

    if not st.session_state.entries:
        st.info("No data available.")
    else:
        df = pd.DataFrame(st.session_state.entries)
        df["Calories"] = df["Calories"].astype(float)
        summary = df.groupby("Date")["Calories"].sum().reset_index()
        st.subheader("Total Calories Per Day")
        st.bar_chart(summary.rename(columns={"Calories": "Calories"}).set_index("Date"))

        total = df["Calories"].sum()
        st.metric("Total Calories Logged", f"{total:.0f} kcal")

