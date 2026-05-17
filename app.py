import streamlit as st
from database import init_db, validate_user

init_db()

st.set_page_config(page_title="Hello World App", page_icon="👋", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


def login_screen():
    st.title("Login")
    st.markdown("---")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
        elif validate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.caption("Default credentials — username: **admin** | password: **admin123**")


def home_screen():
    st.title("Hello, World!")
    st.markdown("---")
    st.success(f"Welcome back, **{st.session_state.username}**!")
    st.markdown("## Hello World")
    st.write("You are successfully logged in. This message is powered by a SQLite backend.")

    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()


if st.session_state.logged_in:
    home_screen()
else:
    login_screen()
