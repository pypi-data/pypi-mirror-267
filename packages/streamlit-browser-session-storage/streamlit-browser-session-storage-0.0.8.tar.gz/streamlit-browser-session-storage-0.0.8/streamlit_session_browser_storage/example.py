import streamlit as st
from __init__ import SessionStorage
# from streamlit_local_storage import sessionStorage

st.set_page_config(layout="wide")

sessionS = SessionStorage() 
sessionS.setItem("King", "KAdel")

result = sessionS.getItem("King")
st.write(result)

sessionS.deleteItem("King")
result = sessionS.getItem("King")
st.write(result)

st.write(sessionS.getAll()  )
