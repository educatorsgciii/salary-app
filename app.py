import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# Direct Google Sheet Link (Public CSV Export)
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Reading Data from Sheet
    df = pd.read_csv(sheet_url)
    df = df.dropna(how="all") # Remove empty rows
    
    st.success("✅ ڈیٹا کامیابی سے لوڈ ہو گیا ہے!")
    
    # --- Display Dashboard ---
    st.subheader("📊 ملازمین کا ریکارڈ")
    st.dataframe(df, use_container_width=True)
    
    # --- Salary Slip Generation Logic ---
    st.divider()
    st.subheader("📄 Generate Salary Slip")
    
    if not df.empty:
        # Select Employee from List
        employee_names = df['Name'].tolist()
        selected_emp = st.selectbox("ملازم کا نام منتخب کریں", employee_names)
        
        # Get details for selected employee
        emp_data = df[df['Name'] == selected_emp].iloc[0]
        
        # Display Slip Preview
        st.info(f"سیلری سلپ برائے: **{selected_emp}**")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Designation:** {emp_data.get('Designation', 'N/A')}")
            st.write(f"**ID:** {emp_data.get('ID', 'N/A')}")
        with col2:
            st.write(f"**CNIC:** {emp_data.get('CNIC', 'N/A')}")
            # Yahan ap mazeed salary components (Basic, Net) add kar sakte hain
            
        # Download Excel Button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Record (Excel)",
            data=csv,
            file_name='Educators_Salary_Report.csv',
            mime='text/csv',
        )
    else:
        st.warning("شیٹ میں کوئی ڈیٹا موجود نہیں ہے۔")

except Exception as e:
    st.error(f"کنکشن میں مسئلہ ہے: {e}")
    st.info("براہِ کرم اسکرین ریفریش کریں یا گٹ ہب کوڈ چیک کریں۔")
