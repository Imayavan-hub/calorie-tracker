import streamlit as st
from datetime import date
import backend as bk

# Initialize backend session
bk.init_storage()

# UI
st.title("🥗 Calorie Tracker App")

menu = st.sidebar.radio("Go to", ["Add Meal", "View Log", "Summary"])

# Add Meal
if menu == "Add Meal":
    st.header("🍽️ Add a Meal")
    with st.form("meal_form"):
        name = st.text_input("Meal Name")
        cal = st.number_input("Calories", min_value=0, step=1)
        ing = st.text_area("Ingredients")
        meal_date = st.date_input("Date", date.today())
        submit = st.form_submit_button("Add Meal")

        if submit and name:
            bk.add_meal(name, cal, ing, meal_date)
            st.success(f"Added {name} ({cal} kcal)")

# View Log
elif menu == "View Log":
    st.header("📋 View Meal Log")
    df = bk.get_all_meals()
    if df.empty:
        st.info("No meals added yet.")
    else:
        st.dataframe(df)
        filter_date = st.date_input("Filter by Date (optional)", date.today())
        filtered_df = bk.filter_meals_by_date(df, filter_date)
        st.subheader(f"Meals on {filter_date}")
        st.dataframe(filtered_df)

# Summary
elif menu == "Summary":
    st.header("📊 Calorie Summary")
    df = bk.get_all_meals()
    if df.empty:
        st.info("No data to show.")
    else:
        summary = bk.get_summary(df)
        st.bar_chart(summary.set_index("Date"))
        st.metric("Total Calories Logged", f"{bk.get_total_calories(df):.0f} kcal")

