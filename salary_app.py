import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Page Setup
st.set_page_config(page_title="The Educators Salary System", layout="wide")
st.title("📂 Salary Management System (Live Cloud)")

# Google Sheet URL
url = "https://docs.google.com/spreadsheets/d/13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y/edit?usp=sharing"

# Connection setup with direct handling
conn = st.connection("gsheets", type=GSheetsConnection)

def load_live_data():
    return conn.read(spreadsheet=url, ttl="0")

df = load_live_data()

menu = ["📊 Dashboard", "➕ Add New Employee", "🗑️ Manage Staff"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "📊 Dashboard":
    st.subheader("Live Employee Records")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records found in the Google Sheet.")

elif choice == "➕ Add New Employee":
    st.subheader("Add New Employee")
    next_id = int(df['ID'].max()) + 1 if not df.empty else 101
    
    with st.form("add_form"):
        name = st.text_input("Full Name")
        des = st.text_input("Designation")
        sal = st.number_input("Basic Salary", min_value=0)
        
        if st.form_submit_button("Save to Cloud"):
            new_row = pd.DataFrame([{"ID": next_id, "Name": name, "Designation": des, "Basic_Salary": sal, "Remaining_CL": 10, "Advance_Balance": 0}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            # Direct Update Method
            try:
                conn.update(spreadsheet=url, data=updated_df)
                st.success(f"{name} has been saved!")
                st.rerun()
            except Exception as e:
                st.error("Connection Refused. Please check Google Sheet Share settings.")
