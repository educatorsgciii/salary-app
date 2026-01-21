import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import math

st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# گوگل شیٹ کنکشن
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl="0").dropna(how="all")
    df.columns = df.columns.str.strip()

    # ضروری کالمز اگر نہیں ہیں تو بنا دیں
    required_cols = ['ID', 'Name', 'Designation', 'Basic_Salary', 'Presents', 'Absents', 'Lates', 'Half_Day', 'Advance', 'Net_Salary']
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    if 'main_df' not in st.session_state:
        st.session_state.main_df = df

    # --- حصہ 1: نئی انٹری (Add New Employee) ---
    with st.expander("➕ Add New Employee"):
        col1, col2, col3 = st.columns(3)
        new_name = col1.text_input("Name")
        new_desig = col2.text_input("Designation")
        new_basic = col3.number_input("Basic Salary", min_value=0)
        
        if st.button("Register Employee"):
            # خودکار ID جنریٹ کرنا (آخری ID میں 1 پلس کرنا)
            last_id = 100
            if not st.session_state.main_df.empty:
                try:
                    last_id = int(float(st.session_state.main_df['ID'].max()))
                except: last_id = 100
            
            new_row = {
                'ID': last_id + 1, 'Name': new_name, 'Designation': new_desig,
                'Basic_Salary': new_basic, 'Presents': 0, 'Absents': 0, 
                'Lates': 0, 'Half_Day': 0, 'Advance': 0, 'Net_Salary': 0
            }
            st.session_state.main_df = pd.concat([st.session_state.main_df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"ملازم رجسٹر ہو گیا! ID: {last_id + 1}")
            st.rerun()

    # --- حصہ 2: حاضری اور حساب کتاب ---
    st.subheader("📊 Attendance & Salary Calculation")
    
    # ڈیٹا ایڈیٹر (جہاں آپ حاضری ڈالیں گی)
    edited_df = st.data_editor(st.session_state.main_df, use_container_width=True, num_rows="dynamic")

    # حساب کتاب کا فارمولا (Calculations)
    for index, row in edited_df.iterrows():
        basic = float(row['Basic_Salary'])
        per_day_sal = basic / 30 # ایک دن کی تنخواہ
        
        # 3 لایٹس پر ایک چھٹی
        lates_off = math.floor(float(row['Lates']) / 3)
        # 2 ہاف ڈیز پر ایک چھٹی
        half_day_off = math.floor(float(row['Half_Day']) / 2)
        
        # کل کٹوتیاں (Absents + Lates Off + Half Day Off)
        total_offs = float(row['Absents']) + lates_off + half_day_off
        deduction = total_offs * per_day_sal
        
        # نیٹ سیلری (Basic - Deductions - Advance)
        net = basic - deduction - float(row['Advance'])
        edited_df.at[index, 'Net_Salary'] = round(net)

    # سیو بٹن
    if st.button("💾 SAVE ALL DATA TO GOOGLE SHEET"):
        conn.update(data=edited_df)
        st.session_state.main_df = edited_df
        st.success("تمام حاضری اور حساب کتاب گوگل شیٹ میں سیو ہو گیا ہے!")
        st.balloons()

    st.divider()

    # --- حصہ 3: سرچ اور سیلری سلپ ---
    st.subheader("🔍 Generate Salary Slip")
    search_id = st.text_input("ملازم کی ID لکھیں:")
    if search_id:
        match = edited_df[edited_df['ID'].astype(str).str.contains(str(search_id))]
        if not match.empty:
            emp = match.iloc[0]
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; padding: 20px; border-radius: 15px; background-color: white; color: black; max-width: 600px; margin: auto;">
                    <h2 style="text-align: center; color: #ff4b4b;">THE EDUCATORS</h2>
                    <hr>
                    <p><b>Name:</b> {emp['Name']} | <b>ID:</b> {emp['ID']}</p>
                    <p><b>Designation:</b> {emp['Designation']}</p>
                    <p><b>Lates:</b> {emp['Lates']} (Deducted: {math.floor(float(emp['Lates'])/3)} days)</p>
                    <p><b>Half Days:</b> {emp['Half_Day']} (Deducted: {math.floor(float(emp['Half_Day'])/2)} days)</p>
                    <p><b>Advance:</b> Rs. {emp['Advance']}</p>
                    <h3 style="background: #fdf2f2; padding: 10px; text-align: center;">Net Payable: PKR {emp['Net_Salary']}</h3>
                </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error("کنکشن کا مسئلہ: براہِ کرم چیک کریں کہ گوگل شیٹ Editor پر شیئر ہے۔")
    st.info(f"Error: {e}")
