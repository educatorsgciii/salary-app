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
    # ttl="0" is important to get fresh data every time
    df = conn.read(ttl="0")
    df = df.dropna(how="all")
except Exception as e:
    st.error(f"Error reading data: {e}")
    df = pd.DataFrame()

# Sidebar Menu
menu = ["Dashboard", "Add New Employee", "Delete Employee"]
choice = st.sidebar.selectbox("Main Menu", menu)

# --- DASHBOARD ---
if choice == "Dashboard":
    st.subheader("📊 Employee Database")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
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
                new_data = pd.DataFrame([{"Name": name, "Designation": designation, "Salary": salary}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"✅ {name} has been saved!")
                st.balloons()
            else:
                st.warning("Please enter a name.")

# --- DELETE EMPLOYEE ---
elif choice == "Delete Employee":
    st.subheader("🗑️ Delete Records")
    if not df.empty:
        # Create a clean list of names
        names_list = df["Name"].unique().tolist()
        
        # Add a placeholder so it doesn't auto-select the first name
        names_list.insert(0, "Choose an employee...")
        
        selected_employee = st.selectbox("Which employee do you want to remove?", names_list)
        
        if selected_employee != "Choose an employee...":
            st.warning(f"Are you sure you want to delete {selected_employee}?")
            if st.button("Confirm Delete"):
                # Remove the selected row
                updated_df = df[df["Name"] != selected_employee]
                conn.update(data=updated_df)
                st.success(f"❌ {selected_employee} has been removed from cloud!")
                st.cache_data.clear() # This clears the old data from memory
    else:
        st.info("No employees available to delete.")
