import streamlit as st
import bcrypt

# Dummy user data
users = {
    "bob": b"$2b$12$6O3yS/1Ravhx1fVRFPp0QOQMDpiF0x6E3W8yab5D2xm3hDu0LcqKe",
    "bombaclat": b"$2b$12$qxQgtFYnxAF1.id9gCHoAuF5yQJDs5vmrzjFSuS0y3EpuO5cVbJNy",  # streamlit
}

def login():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users:
            hashed_pw = users[username]
            if bcrypt.checkpw(password.encode(), hashed_pw):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success("Login successful! 🎉 You can now access other pages.")
            else:
                st.error("Incorrect password ❌")
        else:
            st.error("User not found ❌")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    st.success(f"Welcome back, {st.session_state['username']}!")
    st.info("Use the sidebar to navigate to other pages.")

