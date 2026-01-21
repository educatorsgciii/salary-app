import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# Page Configuration
st.set_page_config(page_title="The Educators Salary System", layout="wide")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #f8f9fa; }
    
    /* Sidebar buttons */
    .stSidebar div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        border: none;
        margin-bottom: 5px;
    }

    /* Small & Sleek Action Buttons in Table */
    .stButton > button {
        padding: 2px 10px;
        font-size: 14px;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        background-color: white;
        height: 28px;
        line-height: 1;
    }
    
    /* Hover effect for action buttons */
    .stButton > button:hover {
        border-color: #3B82F6;
        color: #3B82F6;
        background-color: #f0f7ff;
    }

    /* Table Header Styling */
    .header-style {
        font-size: 16px;
        font-weight: bold;
        color: #1E3A8A;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

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

# --- SIDEBAR ---
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

st.sidebar.markdown("### 🛠️ Control Panel")
if st.sidebar.button("📊 VIEW DASHBOARD"):
    st.session_state.page = "Dashboard"
if st.sidebar.button("➕ ADD NEW EMPLOYEE"):
    st.session_state.page = "Add New Employee"

# --- DASHBOARD ---
if st.session_state.page == "Dashboard":
    st.subheader("📊 Employee Database")
    
    if not df.empty:
        # Professional Headers
        h_cols = st.columns([0.6, 2, 2, 2, 1.5, 1.2])
        headers = ["ID", "Name", "CNIC", "Designation", "Salary", "Actions"]
        for i, h in enumerate(headers):
            h_cols[i].markdown(f'<p class="header-style">{h}</p>', unsafe_allow_html=True)

        for index, row in df.iterrows():
            cols = st.columns([0.6, 2, 2, 2, 1.5, 1.2])
            cols[0].write(row.get("ID", "-")) 
            cols[1].write(row.get("Name", "-"))
            cols[2].write(row.get("CNIC", "-"))
            cols[3].write(row.get("Designation", "-"))
            sal = row.get("Basic_Salary", row.get("Salary", 0))
            cols[4].write(f"Rs. {sal}")
            
            # Action Buttons: Tiny & Professional
            btn_col1, btn_col2 = cols[5].columns(2)
            if btn_col1.button("✏️", key=f"ed_{index}"):
                st.session_state.edit_mode = True
                st.session_state.edit_index = index
                st.session_state.edit_data = row.to_dict()
            if btn_col2.button("🗑️", key=f"dl_{index}"):
                with st.spinner("Deleting..."):
                    updated_df = df.drop(index)
                    conn.update(data=updated_df)
                    st.cache_data.clear()
                    st.rerun()

        # Edit Section
        if st.session_state.get("edit_mode"):
            st.info(f"Editing ID: {st.session_state.edit_data.get('ID')}")
            with st.form("edit_form"):
                n_name = st.text_input("Name", value=st.session_state.edit_data.get('Name'))
                n_cnic = st.text_input("CNIC", value=st.session_state.edit_data.get('CNIC'))
                n_desig = st.selectbox("Designation", ["Teacher", "Principal", "office", "Admin Staff", "Security", "Other"])
                n_sal = st.number_input("Salary", value=int(st.session_state.edit_data.get('Basic_Salary', 0)))
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Update"):
                    df.at[st.session_state.edit_index, "Name"] = n_name
                    df.at[st.session_state.edit_index, "CNIC"] = n_cnic
                    df.at[st.session_state.edit_index, "Designation"] = n_desig
                    df.at[st.session_state.edit_index, "Basic_Salary"] = n_sal
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
elif st.session_state.page == "Add New Employee":
    st.subheader("📝 Registration Form")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        cnic = st.text_input("CNIC Number")
        designation = st.selectbox("Designation", ["Teacher", "Principal", "office", "Admin Staff", "Security", "Other"])
        salary = st.number_input("Basic Salary", min_value=0)
        submit = st.form_submit_button("Save Record")

        if submit and name and cnic:
            if not df.empty and "ID" in df.columns:
                max_id = pd.to_numeric(df["ID"], errors='coerce').max()
                next_id = 101 if pd.isna(max_id) else int(max_id) + 1
            else:
                next_id = 101
            new_row = pd.DataFrame([{"ID": next_id, "Name": name, "CNIC": cnic, "Designation": designation, "Basic_Salary": salary}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.cache_data.clear()
            st.success(f"Record Saved! ID: {next_id}")
            time.sleep(1)
            st.rerun()
