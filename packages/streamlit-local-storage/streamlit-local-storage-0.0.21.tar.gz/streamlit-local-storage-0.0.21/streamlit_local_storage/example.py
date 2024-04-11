# import time 
# import streamlit as st
# from __init__ import LocalStorage
# # from streamlit_local_storage import LocalStorage

# st.set_page_config(layout="wide")

# localStorage = LocalStorage(pause=None)
# localStorage.setItem("Mike", "Farah")

# result = localStorage.getItem("testing")
# st.write(result)
# result2 = localStorage.getItem("Jade")
# st.write(result2)
# result3 = localStorage.getItem("Mike")
# st.write(result3)
# # localStorage.deleteAll()
# # result = localStorage.getItem("Eddie")
# # st.write(result)



import streamlit as st
from streamlit_cookies_controller import CookieController

st.set_page_config('Cookie QuickStart', '🍪', layout='wide')

controller = CookieController()

# Set a cookie
with st.container(height=1):
    st.html("<style>div[height='1']{display:none;}</style>")
    controller.set('cookie_name', 'testing')
st.write(st.session_state)

with st.container(height=1):
    st.html("<style>div[height='1']{display:none;}</style>")
# Get all cookies
    cookies = controller.getAll()
st.write(cookies)


# Get a cookie
cookie = controller.get('cookie_name')
st.write(cookie)

with st.container(height=1):
    st.html("<style>div[height='1']{display:none;}</style>")
# Remove a cookie
    controller.remove('cookie_name')
st.write(st.session_state)