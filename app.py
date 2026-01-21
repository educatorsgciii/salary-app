import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Educators Salary Pro", layout="wide")

st.title("🏫 The Educators - Smart Attendance & Salary System")

# گوگل شیٹ کا لنک (CSV فارمیٹ میں)
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# ڈیٹا لوڈ کرنا
if 'main_df' not in st.session_state:
    try:
        df = pd.read_csv(sheet_url).dropna(how="all")
        df.columns = df.columns.str.strip()
        st.session_state.main_df = df
    except:
        st.session_state.main_df = pd.DataFrame(columns=['ID', 'Name', 'Designation', 'Basic_Salary', 'Absents', 'Lates', 'Half_Day', 'Advance'])

df = st.session_state.main_df

# --- نئی انٹری (Add New Employee) ---
with st.expander("➕ Add New Employee"):
    c1, c2, c3 = st.columns(3)
    n_name = c1.text_input("Name")
    n_desig = c2.text_input("Designation")
    n_basic = c3.number_input("Basic Salary", min_value=0)
    
    if st.button("Register Now"):
        # Auto ID Generation
        last_id = 100
        if not df.empty and 'ID' in df.columns:
            try: last_id = int(float(df['ID'].max()))
            except: last_id = 100
        
        new_row = {'ID': last_id + 1, 'Name': n_name, 'Designation': n_desig, 'Basic_Salary': n_basic, 'Absents': 0, 'Lates': 0, 'Half_Day': 0, 'Advance': 0}
        st.session_state.main_df = pd.concat([st.session_state.main_df, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"ملازم رجسٹر ہو گیا! ID: {last_id + 1}")
        st.rerun()

# --- حاضری ٹیبل ---
st.subheader("📊 Attendance Sheet")
edited_df = st.data_editor(st.session_state.main_df, use_container_width=True, num_rows="dynamic")

# حساب کتاب (Calculations)
calc_results = []
for index, row in edited_df.iterrows():
    try:
        basic = float(row.get('Basic_Salary', 0))
        per_day = basic / 30
        
        # رولز: 3 لایٹس = 1 آف، 2 ہاف ڈیز = 1 آف
        l_off = math.floor(float(row.get('Lates', 0)) / 3)
        h_off = math.floor(float(row.get('Half_Day', 0)) / 2)
        
        total_days = float(row.get('Absents', 0)) + l_off + h_off
        net = basic - (total_days * per_day) - float(row.get('Advance', 0))
        calc_results.append(round(net))
    except:
        calc_results.append(0)

edited_df['Net_Salary'] = calc_results

# ڈیٹا محفوظ کرنا (Download)
st.divider()
csv_data = edited_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Excel Report", data=csv_data, file_name='Monthly_Salary.csv')
st.info("نوٹ: ڈیٹا یہاں ایڈٹ کرنے کے بعد اسے ڈاؤن لوڈ کر کے اپنی گوگل شیٹ میں ایک بار پیسٹ کر لیں۔")

# --- سیلری سلپ ---
st.subheader("🔍 Generate Salary Slip")
search_id = st.text_input("ملازم کی ID لکھیں:")
if search_id:
    match = edited_df[edited_df['ID'].astype(str).str.contains(str(search_id).strip())]
    if not match.empty:
        emp = match.iloc[0]
        st.markdown(f"""
            <div style="border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background: white; color: black; max-width: 500px; margin: auto;">
                <h2 style="text-align: center; color: #ff4b4b;">THE EDUCATORS</h2>
                <hr>
                <p><b>Name:</b> {emp['Name']} | <b>ID:</b> {emp['ID']}</p>
                <p><b>Designation:</b> {emp['Designation']}</p>
                <div style="background: #fdf2f2; padding: 15px; text-align: center;">
                    <h3>Net Payable: PKR {emp['Net_Salary']}</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
