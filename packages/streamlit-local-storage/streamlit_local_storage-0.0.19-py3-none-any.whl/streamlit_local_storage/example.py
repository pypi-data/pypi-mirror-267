import time 
import streamlit as st
from __init__ import LocalStorage
# from streamlit_local_storage import LocalStorage

st.set_page_config(layout="wide")

localStorage = LocalStorage(pause=None)
localStorage.setItem("Mike", "Farah")

result = localStorage.getItem("testing")
st.write(result)
result2 = localStorage.getItem("Jade")
st.write(result2)
result3 = localStorage.getItem("Mike")
st.write(result3)
# localStorage.deleteAll()
# result = localStorage.getItem("Eddie")
# st.write(result)


