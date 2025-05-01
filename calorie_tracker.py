import streamlit as st
from datetime import datetime, date
import pandas as pd
import db
import auth
import sqlite3

db.init_db()

# One-time admin creation (for dev only — remove after use)
if st.sidebar.button("Create Admin"):
    created = auth.register_backend("admin", "admin123", role="admin")
    if created:
        st.success("Admin account created. Username: admin, Password: admin123")
    else:
        st.warning("Admin already exists.")

if st.session_state.get("logged_in"):
    st.sidebar.subheader("Logged in as: " + st.session_state["username"])

    role = db.get_user_role(st.session_state["user_id"])
    st.sidebar.info(f"Role: {role}")

    if role == "admin":
        st.sidebar.success("Admin Access")
        if st.sidebar.button("View All Entries"):
            all_entries = db.get_all_entries()
            st.write("### All User Entries")
            for username, food, calories, timestamp in all_entries:
                st.write(f"👤 {username} | 🍽️ {food} | 🔥 {calories} cal | 🕒 {timestamp}")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    page = st.sidebar.radio("Auth", ["Login", "Register"])
    if page == "Login":
        auth.login()
    elif page == "Register":
        st.subheader("Create New Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            if username and password:
                success = auth.register(username, password)
                if success:
                    st.success("User registered successfully!")
                else:
                    st.error("Username already exists.")
            else:
                st.warning("Please enter both username and password.")

else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    menu = st.sidebar.radio("Menu", ["Add Meal", "View Log", "Summary", "Logout"])

    if menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()

    if menu == "Add Meal":
        st.header("➕ Add Meal")
        with st.form("meal_form"):
            meal = st.text_input("Meal Name")
            cal = st.number_input("Calories", min_value=0)
            ing = st.text_area("Ingredients")
            dt = st.date_input("Date", date.today())
            submitted = st.form_submit_button("Add Meal")
            if submitted and meal:
                db.insert_meal(st.session_state.user_id, meal, cal, ing, dt.strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                st.success("Meal added!")

    if menu == "View Log":
        st.header("📋 Your Meal Log")
        all_meals = db.get_meals(st.session_state.user_id)
        if all_meals:
            df = pd.DataFrame(all_meals, columns=["ID", "User ID", "Meal", "Calories", "Ingredients", "Date", "Timestamp"])
            st.dataframe(df)
            filter_date = st.date_input("Filter by Date", date.today())
            filtered = db.get_meals_by_date(st.session_state.user_id, filter_date.strftime("%Y-%m-%d"))
            if filtered:
                st.subheader(f"Meals on {filter_date}")
                st.dataframe(pd.DataFrame(filtered, columns=["ID", "User ID", "Meal", "Calories", "Ingredients", "Date", "Timestamp"]))
            else:
                st.info("No meals on this date.")
        else:
            st.info("No data found.")

    if menu == "Summary":
        st.header("📊 Calorie Summary")
        summary = db.get_summary(st.session_state.user_id)
        if summary:
            df = pd.DataFrame(summary, columns=["Date", "Total Calories"])
            st.bar_chart(df.set_index("Date"))
            st.metric("Total Calories", f"{db.get_total_calories(st.session_state.user_id):.0f} kcal")
        else:
            st.info("No summary available.")
