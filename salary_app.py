import streamlit as st
import pandas as pd
import os

# Excel file ka naam
FILE_NAME = "staff_data.xlsx"

# File setup
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=['ID', 'Name', 'Designation', 'Basic_Salary', 'Remaining_CL', 'Advance_Balance'])
    df.to_excel(FILE_NAME, index=False)

def load_data():
    return pd.read_excel(FILE_NAME, dtype={'ID': int}) # ID ko number mein rakhna takay calculation ho sakay

def save_data(df):
    df.to_excel(FILE_NAME, index=False)

# Page Setup
st.set_page_config(page_title="Professional Salary System", layout="wide")
st.title("📂 Salary Management System (Auto ID)")

# Data load karna
emp_df = load_data()

menu = ["📊 Dashboard", "📝 Monthly Attendance", "📈 Increment", "➕ Add New Employee", "❌ Employee Left (Remove)"]
choice = st.sidebar.selectbox("Menu", menu)

# --- 1. Dashboard ---
if choice == "📊 Dashboard":
    st.subheader("All Employees Record")
    st.dataframe(emp_df, use_container_width=True)

# --- 2. Monthly Attendance ---
elif choice == "📝 Monthly Attendance":
    st.subheader("Monthly Salary Calculation")
    if not emp_df.empty:
        selected_name = st.selectbox("Select Employee", emp_df['Name'])
        idx = emp_df.index[emp_df['Name'] == selected_name][0]
        row = emp_df.iloc[idx]
        
        col1, col2 = st.columns(2)
        with col1:
            absents = st.number_input("Absents", min_value=0)
            lates = st.number_input("Lates", min_value=0)
            halfdays = st.number_input("Half Days", min_value=0)
        with col2:
            st.info(f"Current Advance: {row['Advance_Balance']}")
            deduct_adv = st.number_input("Advance Deduction", min_value=0.0, max_value=float(row['Advance_Balance']))

        total_offs = absents + (lates // 3) + (halfdays // 2)
        curr_cl = row['Remaining_CL']
        
        if total_offs <= curr_cl:
            new_cl = curr_cl - total_offs
            unpaid = 0
        else:
            unpaid = total_offs - curr_cl
            new_cl = 0
            
        per_day = row['Basic_Salary'] / 30
        net_salary = row['Basic_Salary'] - ((unpaid * per_day) + deduct_adv)
        
        st.write(f"### This Month's Salary: {net_salary:,.0f} PKR")
        
        if st.button("Save Monthly Record"):
            emp_df.at[idx, 'Remaining_CL'] = new_cl
            emp_df.at[idx, 'Advance_Balance'] -= deduct_adv
            save_data(emp_df)
            st.success("Record updated in Excel!")
    else:
        st.warning("No employees found.")

# --- 3. Increment ---
elif choice == "📈 Increment":
    st.subheader("Apply Salary Increment (%)")
    if not emp_df.empty:
        target = st.selectbox("Select Employee", emp_df['Name'])
        percent = st.number_input("Enter Percentage (%)", min_value=0.0)
        
        if st.button("Confirm Increment"):
            idx = emp_df.index[emp_df['Name'] == target][0]
            old_sal = emp_df.at[idx, 'Basic_Salary']
            new_sal = old_sal + (old_sal * percent / 100)
            emp_df.at[idx, 'Basic_Salary'] = new_sal
            save_data(emp_df)
            st.success(f"Salary updated to {new_sal:,.0f}")

# --- 4. Add New Employee (ID Automatic Feature) ---
elif choice == "➕ Add New Employee":
    st.subheader("Add New Employee")
    
    # Auto ID Logic
    if not emp_df.empty:
        next_id = int(emp_df['ID'].max()) + 1
    else:
        next_id = 101  # Pehla employee 101 se shuru hoga
    
    st.write(f"**Assigned ID:** {next_id}") # User ko dikhayega ke konsi ID mil rahi hai
    
    with st.form("Add Form"):
        name_n = st.text_input("Full Name")
        des_n = st.text_input("Designation")
        sal_n = st.number_input("Basic Salary", min_value=0.0)
        adv_n = st.number_input("Initial Advance (if any)", min_value=0.0)
        
        if st.form_submit_button("Save Employee"):
            new_row = pd.DataFrame([{
                'ID': next_id, 
                'Name': name_n, 
                'Designation': des_n, 
                'Basic_Salary': sal_n, 
                'Remaining_CL': 10, 
                'Advance_Balance': adv_n
            }])
            emp_df = pd.concat([emp_df, new_row], ignore_index=True)
            save_data(emp_df)
            st.success(f"New employee {name_n} added with ID {next_id}!")
            st.rerun()

# --- 5. Remove Employee ---
elif choice == "❌ Employee Left (Remove)":
    st.subheader("Remove Employee from System")
    if not emp_df.empty:
        delete_name = st.selectbox("Select Employee who left", emp_df['Name'])
        st.warning(f"Are you sure you want to remove {delete_name}?")
        
        if st.button("Permanently Remove"):
            emp_df = emp_df[emp_df['Name'] != delete_name]
            save_data(emp_df)
            st.success(f"{delete_name} removed.")
            st.rerun()