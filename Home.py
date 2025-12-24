import streamlit as st
from hashing import generate_hash, is_valid_hash
from app_model.db import get_connection
from app_model.users import add_user, get_user


conn = get_connection()

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.title("Welcome To The Cyber Incidents Main Page 🏠!")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False



tab_login, tab_register = st.tabs(["Login Staus", "Register"])

with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        user = get_user(conn, login_username)

        if user is None:
            st.error("User not found.")
        else:
            id, user_name, user_hash, role = user

            if is_valid_hash(login_password, user_hash):
                st.session_state["logged_in"] = True
                st.session_state["username"] = user_name
                st.session_state["role"] = role
                st.success(f"Welcome {user_name}!")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Incorrect password.")



with tab_register:
    st.subheader("Register New Account")

    register_username = st.text_input("New Username", key="register_username")
    register_password = st.text_input("Password", type="password", key="register_password")
    register_role = st.selectbox("Role", ["user", "admin"], key="register_role")

    if st.button("Register"):
        if register_username == "" or register_password == "":
            st.error("Please fill in all fields")
        else:
            hash_password = generate_hash(register_password)
            add_user(conn, register_username, hash_password, register_role)
            st.success("Registration successful! Please now log in.")





