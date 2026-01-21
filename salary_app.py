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
        h_cols = st.columns([1, 2, 2, 2, 2, 2])
        h_cols[0].markdown("**ID**")
        h_cols[1].markdown("**Name**")
        h_cols[2].markdown("**CNIC**")
        h_cols[3].markdown("**Designation**")
        h_cols[4].markdown("**Salary**")
        h_cols[5].markdown("**Actions**")
        st.divider()

        # Data Rows
        for index, row in df.iterrows():
            cols = st.columns([1, 2, 2, 2, 2, 2])
            cols[0].write(index + 1)  # ID automatic based on row index
            cols[1].write(row.get("Name", "N/A"))
            cols[2].write(row.get("CNIC", "N/A"))
            cols[3].write(row.get("Designation", "N/A"))
            salary_val = row.get("Salary", row.get("Basic_Salary", 0))
            cols[4].write(f"Rs. {salary_val}")
            
            # Action Buttons
            btn_col1, btn_col2 = cols[5].columns(2)
            btn_edit = btn_col1.button("✏️", key=f"edit_{index}")
            btn_del = btn_col2.button("🗑️", key=f"del_{index}")

            # If Edit is clicked
            if btn_edit:
                st.session_state.edit_mode = True
                st.session_state.edit_index = index
                st.session_state.edit_data = row.to_dict()

            # If Delete is clicked
            if btn_del:
                updated_df = df.drop(index)
                conn.update(data=updated_df)
                st.success(f"❌ Record removed!")
                st.cache_data.clear()
                st.rerun()

        # Edit Form (appears below the table)
        if st.session_state.get("edit_mode"):
            st.divider()
            st.subheader(f"🔄 Editing Record")
            with st.form("edit_form"):
                en_name = st.text_input("Name", value=st.session_state.edit_data.get('Name', ''))
                en_cnic = st.text_input("CNIC", value=st.session_state.edit_data.get('CNIC', ''))
                
                designations = ["Teacher", "Principal", "Admin Staff", "Security", "Other"]
                current_desig = st.session_state.edit_data.get('Designation', 'Other')
                desig_idx = designations.index(current_desig) if current_desig in designations else 0
                en_desig = st.selectbox("Designation", designations, index=desig_idx)
                
                current_sal = int(st.session_state.edit_data.get('Salary', st.session_state.edit_data.get('Basic_Salary', 0)))
                en_sal = st.number_input("Salary", value=current_sal)
                
                c1, c2 = st.columns(2)
                save = c1.form_submit_button("Update Records")
                cancel = c2.form_submit_button("Cancel")

                if save:
                    df.at[st.session_state.edit_index, "Name"] = en_name
                    df.at[st.session_state.edit_index, "CNIC"] = en_cnic
                    df.at[st.session_state.edit_index, "Designation"] = en_desig
                    if "Salary" in df.columns: df.at[st.session_state.edit_index, "Salary"] = en_sal
                    if "Basic_Salary" in df.columns: df.at[st.session_state.edit_index, "Basic_Salary"] = en_sal
                    
                    conn.update(data=df)
                    st.success("✅ Updated!")
                    st.session_state.edit_mode = False
                    st.cache_data.clear()
                    st.rerun()
                
                if cancel:
                    st.session_state.edit_mode = False
                    st.rerun()
    else:
        st.info("No records found.")

# --- ADD NEW EMPLOYEE ---
elif choice == "Add New Employee":
    st.subheader("📝 Registration Form")
    with st.form("add_form"):
        name = st.text_input("Employee Name")
        cnic = st.text_input("CNIC Number (e.g. 42101-XXXXXXX-X)")
        designation = st.selectbox("Designation", ["Teacher", "Principal", "Admin Staff", "Security", "Other"])
        salary = st.number_input("Basic Salary", min_value=0)
        submit = st.form_submit_button("Save to Cloud")

        if submit:
            if name and cnic:
                new_entry = pd.DataFrame([{"Name": name, "CNIC": cnic, "Designation": designation, "Salary": salary, "Basic_Salary": salary}])
                updated_df = pd.concat([df, new_entry], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"✅ {name} saved successfully!")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please enter Name and CNIC.")
