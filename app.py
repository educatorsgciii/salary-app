import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Setup
st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# Establish Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch Data
try:
    df = conn.read(ttl="0")
    df = df.dropna(how="all")
    
    if not df.empty:
        st.subheader("📊 Employee Database")
        # Displaying the data in a simple table
        st.dataframe(df, use_container_width=True)
    else:
        st.info("ریکارڈ میں ابھی کوئی ڈیٹا موجود نہیں ہے۔")
except Exception as e:
    st.error(f"کنکشن میں مسئلہ ہے: {e}")
