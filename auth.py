# auth.py
import streamlit as st
import db

def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id = db.validate_user(username, password)
        if user_id:
            st.success(f"Welcome back, {username}!")
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.username = username
        else:
            st.error("Invalid username or password.")

def register():
    st.subheader("📝 Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Register"):
        success = db.insert_user(new_username, new_password)
        if success:
            st.success("Registered successfully! Please log in.")
        else:
            st.error("Username already exists.")
