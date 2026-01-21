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
        # Header Row using markdown for bold text
        h_cols = st.columns([3, 2, 2, 2])
        h_cols[0].markdown("**Name**")
        h_cols[1].markdown("**Designation**")
        h_cols[2].markdown("**Salary**")
        h_cols[3].markdown("**Actions**")
        st.divider()

        # Data Rows
        for index, row in df.iterrows():
            cols = st.columns([3, 2, 2, 2])
            cols[0].write(row["Name"])
            cols[1].write(row["Designation"])
            # Display salary safely (checks if column is named Salary or Basic_Salary)
            salary_val = row.get("Salary", row.get("Basic_Salary", 0))
            cols[2].write(f"Rs. {salary_val}")
            
            # Action Buttons
            btn_col1, btn_col2 = cols[3].columns(2)
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
                st.success(f"❌ {row['Name']} removed!")
                st.cache_data.clear()
                st.rerun()

        # Edit Form (appears below the table)
        if st.session_state.get("edit_mode"):
            st.divider()
            st.subheader(f"🔄 Editing: {st.session_state.edit_data['Name']}")
            with st.form("edit_form"):
                new_name = st.text_input("Name", value=st.session_state.edit_data['Name'])
                
                # Check available designations
                designations = ["Teacher", "Principal", "Admin Staff", "Security", "Other"]
                current_desig = st.session_state.edit_data['Designation']
                desig_index = designations.index(current_desig) if current_desig in designations else 0
                
                new_desig = st.selectbox("Designation", designations, index=desig_index)
                
                # Get current salary
                current_sal = int(st.session_state.edit_data.get('Salary', st.session_state.edit_data.get('Basic_Salary', 0)))
                new_sal = st.number_input("Salary", value=current_sal)
                
                c1, c2 = st.columns(2)
                save = c1.form_submit_button("Update Records")
                cancel = c2.form_submit_button("Cancel")

                if save:
                    df.at[st.session_state.edit_index, "Name"] = new_name
                    df.at[st.session_state.edit_index, "Designation"] = new_desig
                    
                    # Update salary in whichever column it exists
                    if "Salary" in df.columns:
                        df.at[st.session_state.edit_index, "Salary"] = new_sal
                    if "Basic_Salary" in df.columns:
                        df.at[st.session_state.edit_index, "Basic_Salary"] = new_sal
                    
                    conn.update(data=df)
                    st.success("✅ Records Updated!")
                    st.session_state.edit_mode = False
                    st.cache_data.clear()
                    st.rerun()
                
                if cancel:
                    st.session_state.edit_mode = False
                    st.rerun()
    else:
        st.info("No records found in the cloud.")

# --- ADD NEW EMPLOYEE ---
elif choice == "Add New Employee":
    st.subheader("📝 Registration Form")
    with st.form("add_form"):
        name = st.text_input("Employee Name")
        designation = st.selectbox("Designation", ["Teacher", "Principal", "Admin Staff", "Security", "Other"])
        salary = st.number_input("Basic Salary", min_value=0)
        submit = st.form_submit_button("Save to Cloud")

        if submit:
            if name:
                # We save it under both names just to be safe with your sheet structure
                new_data = pd.DataFrame([{"Name": name, "Designation": designation, "Salary": salary, "Basic_Salary": salary}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"✅ {name} has been saved!")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please enter a name.")
