from datetime import datetime
import pandas as pd
import streamlit as st

# Initialize session storage
def init_storage():
    if "entries" not in st.session_state:
        st.session_state.entries = []

# Add a new meal
def add_meal(meal_name, calories, ingredients, meal_date):
    st.session_state.entries.append({
        "Meal": meal_name,
        "Calories": calories,
        "Ingredients": ingredients,
        "Date": meal_date.strftime("%Y-%m-%d"),
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Get all meals
def get_all_meals():
    return pd.DataFrame(st.session_state.entries)

# Filter meals by date
def filter_meals_by_date(df, date):
    return df[df["Date"] == date.strftime("%Y-%m-%d")]

# Get summary data
def get_summary(df):
    df["Calories"] = df["Calories"].astype(float)
    return df.groupby("Date")["Calories"].sum().reset_index()

# Get total calories
def get_total_calories(df):
    return df["Calories"].sum()

