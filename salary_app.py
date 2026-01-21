import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# Page Configuration
st.set_page_config(page_title="The Educators Salary System", layout="wide")

# --- CUSTOM CSS FOR DARK SIDEBAR & CLEAN ICONS ---
st.markdown("""
    <style>
    /* 1. Dark Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #111827 !important; /* Dark Grey/Blue */
    }
    
    /* 2. Sidebar Icons and Text Color */
    [data-testid="stSidebar"] section[flex-direction="column"] {
        color: white !important;
    }

    /* Sidebar Buttons Styling */
    .stSidebar div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #1E3A8A; /* Professional Blue */
        color: white;
        font-weight: bold;
        border: none;
        margin-bottom: 10px;
    }
    
    .stSidebar div.stButton > button:hover {
        background-color: #3B82F6;
        color: white;
    }

    /* 3. Transparent Action Icons (No Box, No Border) */
    .stButton > button {
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        color: #4B5563 !important; /* Grey color for icons */
        padding: 0px !important;
        font-size: 20px !important;
        height: auto !important;
        width: auto !important;
        transition: 0.2s;
    }
    
    .stButton > button:hover {
        transform: scale(1.3);
        color: #ef4444 !important; /* Red on hover for delete/edit */
    }

    /* Table Header Styling */
    .header-style {
        font-size: 16px;
        font-weight: bold;
        color: #1E3A8A;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 8px;
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

# --- SIDEBAR NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

st.sidebar.markdown("<h2 style='color: white; text-align: center;'>Menu</h2>", unsafe_allow_html=True)
if st.sidebar.button("📊 VIEW DASHBOARD"):
    st.session_state.page = "Dashboard"
if st.sidebar.button("➕ ADD NEW EMPLOYEE"):
    st.session_state.page = "Add New Employee"

st.sidebar.divider()
st.sidebar.markdown(f"<p style='color: #9CA3AF; text-align: center;'>Active: {st.session_state.page}</p>", unsafe_allow_html=True)

# --- DASHBOARD PAGE ---
if st.session_state.page == "Dashboard":
    st.subheader("📊 Employee Database")
    
    if not df.empty:
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

        if st.session_state.get("edit_mode"):
            st.info(f"Editing: {st.session_state.edit_data.get('Name')}")
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

# --- ADD NEW EMPLOYEE PAGE ---
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
            st.success(f"Saved! ID: {next_id}")
            time.sleep(1)
            st.rerun()
