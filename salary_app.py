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
        # Header Row - Fixed columns for ID, Name, CNIC, etc.
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
            cols[0].write(index + 1) # ID pakki hai yahan
            cols[1].write(row.get("Name", "N/A"))
            cols[2].write(row.get("CNIC", "N/A"))
            cols[3].write(row.get("Designation", "N/A"))
            
            # Salary checking in different possible column names
            salary_val = row.get("Salary", row.get("Basic_Salary", 0))
            cols[4].write(f"Rs. {salary_val}")
            
            # Action Buttons in the last column
            btn_col1, btn_col2 = cols[5].columns(2)
            btn_edit = btn_col1.button("✏️", key=f"edit_{index}")
            btn_del = btn_col2.button("🗑️", key=f"del_{index}")

            # Edit Logic
            if btn_edit:
                st.session_state.edit_mode = True
                st.session_state.edit_index = index
                st.session_state.edit_data = row.to_dict()

            # Delete Logic
            if btn_del:
                updated_df = df.drop(index)
                conn.update(data=updated_df)
                st.success(f"❌ Record Deleted!")
                st.cache_data.clear()
                st.rerun()

        # Edit Form Section
        if st.session_state.get("edit_mode"):
            st.divider()
            st.subheader(f"🔄 Edit Record: {st.session_state.edit_data.get('Name', '')}")
            with st.form("edit_form"):
                en_name = st.text_input("Full Name", value=st.session_state.edit_data.get('Name', ''))
                en_cnic = st.text_input("CNIC", value=st.session_state.edit_data.get('CNIC', ''))
                
                designations = ["Teacher", "Principal", "Admin Staff", "Security", "Other"]
                current_desig = st.session_state.edit_data.get('Designation', 'Other')
                desig_idx = designations.index(current_desig) if current_desig in designations else 0
                en_desig = st.selectbox("Designation", designations, index=desig_idx)
                
                curr_sal = int(st.session_state.edit_data.get('Salary', st.session_state.edit_data.get('Basic_Salary', 0)))
                en_sal = st.number_input("Basic Salary", value=curr_sal)
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Save Changes"):
                    df.at[st.session_state.edit_index, "Name"] = en_name
                    df.at[st.session_state.edit_index, "CNIC"] = en_cnic
                    df.at[st.session_state.edit_index, "Designation"] = en_desig
                    
                    # Update salary in both possible column names for safety
                    if "Salary" in df.columns: df.at[st.session_state.edit_index, "Salary"] = en_sal
                    if "Basic_Salary" in df.columns: df.at[st.session_state.edit_index, "Basic_Salary"] = en_sal
                    
                    conn.update(data=df)
                    st.success("✅ Changes Saved Successfully!")
                    st.session_state.edit_mode = False
                    st.cache_data.clear()
                    st.rerun()
                
                if c2.form_submit_button("Cancel"):
                    st.session_state.edit_mode = False
                    st.rerun()
    else:
        st.info("No records found in cloud.")

# --- ADD NEW EMPLOYEE ---
elif choice == "Add New Employee":
    st.subheader("📝 Registration Form")
    with st.form("add_form"):
        name = st.text_input("Full Name")
        cnic = st.text_input("CNIC Number (e.g. 42101-1234567-1)")
        designation = st.selectbox("Designation", ["Teacher", "Principal", "Admin Staff", "Security", "Other"])
        salary = st.number_input("Basic Salary", min_value=0)
        submit = st.form_submit_button("Save to Cloud")

        if submit:
            if name and cnic:
                # Adding new data with all columns to keep it uniform
                new_row = pd.DataFrame([{"Name": name, "CNIC": cnic, "Designation": designation, "Salary": salary, "Basic_Salary": salary}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"✅ {name} added to the system!")
                st.balloons()
                st.rerun()
            else:
                st.warning("Name aur CNIC dono lazmi hain.")
