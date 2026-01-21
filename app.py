import streamlit as st
import pandas as pd

st.title("🏫 The Educators Salary Record")

# اپنی گوگل شیٹ کا پبلک لنک یہاں ڈالیں
sheet_url = "https://docs.google.com/spreadsheets/d/آپ_کی_شیٹ_کا_آئی_ڈی/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    st.write("### آپ کا تمام ریکارڈ نیچے موجود ہے:")
    st.dataframe(df)
except Exception as e:
    st.error("براہ کرم گوگل شیٹ کا لنک چیک کریں یا اسے 'Anyone with the link' پر شیئر کریں۔")
