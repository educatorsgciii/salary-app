import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

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
        # Header Row
        h_cols = st.columns([0.5, 2, 2, 2, 1.5, 1.5])
        h_cols[0].markdown("**ID**")
        h_cols[1].markdown("**Name**")
        h_cols[2].markdown("**CNIC**")
        h_cols[3].markdown("**Designation**")
        h_cols[4].markdown("**Salary**")
        h_cols[5].markdown("**Actions**")
        st.divider()

        # Data Rows
        for index, row in df.iterrows():
            cols = st.columns([0.5, 2, 2, 2, 1.5, 1.5])
            # Safely get ID
            emp_id = row.get("ID", "N/A")
            cols[0].write(emp_id) 
            cols[1].write(row.get("Name", "N/A"))
            cols[2].write(row.get("CNIC", "N/A"))
            cols[3].write(row.get("Designation", "N/A"))
            
            # Show salary from whichever column exists
            salary_val = row.get("Basic_Salary", row.get("Salary", 0))
            cols[4].write(f"Rs. {salary_val}")
            
            # Action Buttons
            btn_col1, btn_col2 = cols[5].columns(2)
            btn_edit = btn_col1.button("✏️", key=f"edit_{index}")
            btn_del = btn_col2.button("🗑️", key=f"del_{index}")

            if btn_edit:
                st.session_state.edit_mode = True
                st.session_state.edit_index = index
                st.session_state.edit_data = row.to_dict()

            if btn_del:
                updated_df = df.drop(index)
                conn.update(data=updated_df)
                st.success(f"❌ Record Deleted!")
                st.cache_data.clear()
                st.rerun()

        # Edit Form Section
        if st.session_state.get("edit_mode"):
            st.divider()
            st.subheader(f"🔄 Editing ID: {st.session_state.edit_data.get('ID', 'New')}")
            with st.form("edit_form"):
                en_name = st.text_input("Name", value=st.session_state.edit_data.get('Name', ''))
                en_cnic = st.text_input("CNIC", value=st.session_state.edit_data.get('CNIC', ''))
                
                designations = ["Teacher", "Principal", "office", "Admin Staff", "Security", "Other"]
                current_desig = st.session_state.edit_data.get('Designation', 'Other')
                desig_idx = designations.index(current_desig) if current_desig in designations else 0
                en_desig = st.selectbox("Designation", designations, index=desig_idx)
                
                curr_sal = int(st.session_state.edit_data.get('Basic_Salary', st.session_state.edit_data.get('Salary', 0)))
                en_sal = st.number_input("Basic Salary", value=curr_sal)
                
                if st.form_submit_button("Update Changes"):
                    df.at[st.session_state.edit_index, "Name"] = en_name
                    df.at[st.session_state.edit_index, "CNIC"] = en_cnic
                    df.at[st.session_state.edit_index, "Designation"] = en_desig
                    if "Basic_Salary" in df.columns: df.at[st.session_state.edit_index, "Basic_Salary"] = en_sal
                    else: df.at[st.session_state.edit_index, "Salary"] = en_sal
                    
                    conn.update(data=df)
                    st.success("✅ Record Updated!")
                    st.session_state.edit_mode = False
                    st.cache_data.clear()
                    st.rerun()
    else:
        st.info("No records found.")

# --- ADD NEW EMPLOYEE ---
elif choice == "Add New Employee":
    st.subheader("📝 Registration Form")
    with st.form("add_form"):
        name = st.text_input("Employee Name")
        cnic = st.text_input("CNIC Number")
        designation = st.selectbox("Designation", ["Teacher", "Principal", "office", "Admin Staff", "Security", "Other"])
        salary = st.number_input("Basic Salary", min_value=0)
        submit = st.form_submit_button("Save to Cloud")

        if submit:
            if name and cnic:
                # SAFE ID GENERATION
                if not df.empty and "ID" in df.columns:
                    try:
                        # Find max numeric ID, ignore non-numeric stuff
                        max_id = pd.to_numeric(df["ID"], errors='coerce').max()
                        if pd.isna(max_id): next_id = 101
                        else: next_id = int(max_id) + 1
                    except:
                        next_id = 101
                else:
                    next_id = 101
                
                new_row = pd.DataFrame([{"ID": next_id, "Name": name, "CNIC": cnic, "Designation": designation, "Basic_Salary": salary}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"✅ Saved! ID Assigned: {next_id}")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please fill all fields.")
