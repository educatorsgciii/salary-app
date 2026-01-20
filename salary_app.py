import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Page Setup
st.set_page_config(page_title="The Educators Salary System", layout="wide")
st.title("📂 Salary Management System (Online Sheets)")

# Google Sheet Connection
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y/edit?usp=sharing"

# Data load karna
df = conn.read(spreadsheet=url)

# Sidebar Menu
menu = ["📊 Dashboard", "➕ Add New Employee", "🗑️ Manage Staff"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "📊 Dashboard":
    st.subheader("Live Employee Records")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No records found. Please add an employee.")
    st.link_button("View Full Google Sheet", url)

elif choice == "➕ Add New Employee":
    st.subheader("Add New Employee")
    if not df.empty:
        next_id = int(df['ID'].max()) + 1
    else:
        next_id = 101
    
    st.write(f"**Assigned ID:** {next_id}")
    with st.form("Add Form"):
        name = st.text_input("Full Name")
        des = st.text_input("Designation")
        sal = st.number_input("Basic Salary", min_value=0)
        if st.form_submit_button("Save to Google Sheets"):
            new_row = pd.DataFrame([{"ID": next_id, "Name": name, "Designation": des, "Basic_Salary": sal, "Remaining_CL": 10, "Advance_Balance": 0}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=url, data=updated_df)
            st.success(f"{name} added successfully!")
            st.rerun()

elif choice == "🗑️ Manage Staff":
    st.subheader("Remove or Edit Employee")
    if not df.empty:
        selected_name = st.selectbox("Select Employee to Remove", df['Name'].tolist())
        if st.button("🗑️ Delete Employee Now"):
            updated_df = df[df['Name'] != selected_name]
            conn.update(spreadsheet=url, data=updated_df)
            st.warning(f"{selected_name} has been removed from records.")
            st.rerun()
    else:
        st.write("No employees available to manage.")
