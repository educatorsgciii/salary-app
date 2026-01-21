import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# Page Configuration
st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# Establish Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch Data
try:
    df = conn.read(ttl="0")
    df = df.dropna(how="all")
except Exception as e:
    st.error(f"Error reading data: {e}")
    df = pd.DataFrame()

# Sidebar Menu
menu = ["Dashboard", "Add New Employee"]
choice = st.sidebar.selectbox("Main Menu", menu)

# --- DASHBOARD ---
if choice == "Dashboard":
    st.subheader("📊 Employee Database")
    
    if not df.empty:
        h_cols = st.columns([0.5, 2, 2, 2, 1.5, 1.5])
        h_cols[0].markdown("**ID**")
        h_cols[1].markdown("**Name**")
        h_cols[2].markdown("**CNIC**")
        h_cols[3].markdown("**Designation**")
        h_cols[4].markdown("**Salary**")
        h_cols[5].markdown("**Actions**")
        st.divider()

        for index, row in df.iterrows():
            cols = st.columns([0.5, 2, 2, 2, 1.5, 1.5])
            cols[0].write(row.get("ID", "N/A")) 
            cols[1].write(row.get("Name", "N/A"))
            cols[2].write(row.get("CNIC", "N/A"))
            cols[3].write(row.get("Designation", "N/A"))
            salary_val = row.get("Basic_Salary", row.get("Salary", 0))
            cols[4].write(f"Rs. {salary_val}")
            
            btn_col1, btn_col2 = cols[5].columns(2)
            if btn_col1.button("✏️", key=f"edit_{index}"):
                st.session_state.edit_mode = True
                st.session_state.edit_index = index
                st.session_state.edit_data = row.to_dict()
            if btn_col2.button("🗑️", key=f"del_{index}"):
                with st.spinner("Removing record..."):
                    updated_df = df.drop(index)
                    conn.update(data=updated_df)
                    st.cache_data.clear()
                    st.rerun()

        if st.session_state.get("edit_mode"):
            st.divider()
            with st.form("edit_form"):
                st.info(f"Editing: {st.session_state.edit_data.get('Name')}")
                en_name = st.text_input("Name", value=st.session_state.edit_data.get('Name', ''))
                en_cnic = st.text_input("CNIC", value=st.session_state.edit_data.get('CNIC', ''))
                en_desig = st.selectbox("Designation", ["Teacher", "Principal", "office", "Admin Staff", "Security", "Other"], index=0)
                en_sal = st.number_input("Salary", value=int(st.session_state.edit_data.get('Basic_Salary', 0)))
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Update"):
                    with st.spinner("Updating..."):
                        df.at[st.session_state.edit_index, "Name"] = en_name
                        df.at[st.session_state.edit_index, "CNIC"] = en_cnic
                        df.at[st.session_state.edit_index, "Designation"] = en_desig
                        df.at[st.session_state.edit_index, "Basic_Salary"] = en_sal
                        conn.update(data=df)
                        st.session_state.edit_mode = False
                        st.cache_data.clear()
                        st.rerun()
                if c2.form_submit_button("Cancel"):
                    st.session_state.edit_mode = False
                    st.rerun()
    else:
        st.info("No records found.")

# --- ADD NEW EMPLOYEE ---
elif choice == "Add New Employee":
    st.subheader("📝 Registration Form")
    
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        cnic = st.text_input("CNIC Number")
        designation = st.selectbox("Designation", ["Teacher", "Principal", "office", "Admin Staff", "Security", "Other"])
        salary = st.number_input("Basic Salary", min_value=0)
        submit = st.form_submit_button("Save to Cloud")

        if submit:
            if name and cnic:
                with st.spinner("Connecting to Cloud..."):
                    # ID Logic
                    if not df.empty and "ID" in df.columns:
                        max_id = pd.to_numeric(df["ID"], errors='coerce').max()
                        next_id = 101 if pd.isna(max_id) else int(max_id) + 1
                    else:
                        next_id = 101
                    
                    new_row = pd.DataFrame([{"ID": next_id, "Name": name, "CNIC": cnic, "Designation": designation, "Basic_Salary": salary}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.cache_data.clear()
                    st.success(f"Record Saved Successfully. ID: {next_id}")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("Please fill all required fields.")
