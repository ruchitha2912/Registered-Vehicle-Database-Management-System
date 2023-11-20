import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
from main import admin_details, user_details, authenticate_admin, authenticate_user

show_pages([
    Page("login.py", "Login"),
    Page("admin.py", "Admin"),
    Page("user.py", "User")
])


def login():

    st.set_page_config(
        page_title="AutoMate",
        page_icon="🚗",
        layout="centered",
    )
    st.header('AutoMate: Registered Vehicle Management System')
    st.subheader('Login')

    login_id = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login', key='login_credentials_button,'):
            # st.success("Login Successful!")
            if login_id == 'admin':
                admin_details[login_id] = password
                if authenticate_admin(login_id, password):
                    st.success('Admin Login Successful!')
                    switch_page('admin')
                else:
                    st.error('Invalid login credentials, Try Again!')
            else:
                user_details[login_id] = password
                if authenticate_user(login_id, password):
                    st.success('User Login Successful!')
                    switch_page('user')
                else:
                    st.error('Invalid login credentials, Try Again!')


if __name__ == '__main__':
    login()
