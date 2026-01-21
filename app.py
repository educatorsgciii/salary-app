import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🏫 The Educators Salary Record")

# کنکشن بنانے کی کوشش
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    st.write("### آپ کا تمام ریکارڈ نیچے موجود ہے:")
    st.dataframe(df) # سادہ ٹیبل میں ڈیٹا دکھانا
except Exception as e:
    st.error(f"کنکشن میں مسئلہ ہے، براہ کرم پیج ریفریش کریں یا requirements چیک کریں۔")
