import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="The Educators Salary Pro", layout="wide")

st.title("🏫 The Educators - Smart Attendance & Salary System")

# گوگل شیٹ کا براہِ راست لنک
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# ڈیٹا لوڈ کرنے کا فنکشن
def load_data():
    try:
        df = pd.read_csv(sheet_url).dropna(how="all")
        df.columns = df.columns.str.strip()
        # ضروری کالمز اگر نہیں ہیں تو عارضی طور پر بنائیں
        cols = ['ID', 'Name', 'Designation', 'Basic_Salary', 'Absents', 'Lates', 'Half_Day', 'Advance']
        for c in cols:
            if c not in df.columns: df[c] = 0
        return df
    except:
        return pd.DataFrame(columns=['ID', 'Name', 'Designation', 'Basic_Salary', 'Absents', 'Lates', 'Half_Day', 'Advance'])

if 'main_df' not in st.session_state:
    st.session_state.main_df = load_data()

df = st.session_state.main_df

# --- نئی انٹری (Add New Employee) ---
with st.expander("➕ Add New Employee"):
    col1, col2, col3 = st.columns(3)
    n_name = col1.text_input("Name")
    n_desig = col2.text_input("Designation")
    n_basic = col3.number_input("Basic Salary", min_value=0)
    
    if st.button("Register Employee"):
        # Auto ID Generation
        last_id = 100
        if not df.empty:
            try: last_id = int(float(df['ID'].max()))
            except: last_id = 100
        
        new_row = {'ID': last_id + 1, 'Name': n_name, 'Designation': n_desig, 'Basic_Salary': n_basic, 'Absents': 0, 'Lates': 0, 'Half_Day': 0, 'Advance': 0}
        st.session_state.main_df = pd.concat([st.session_state.main_df, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"ملازم رجسٹر ہو گیا! ID: {last_id + 1}")
        st.rerun()

# --- حاضری اور حساب کتاب ---
st.subheader("📊 Attendance Sheet")
st.info("💡 نیچے ٹیبل میں حاضری درج کریں، حساب خود بخود ہو جائے گا۔")

# ڈیٹا ایڈیٹر
edited_df = st.data_editor(st.session_state.main_df, use_container_width=True, num_rows="dynamic")

# حساب کتاب کا فارمولا
calc_list = []
for index, row in edited_df.iterrows():
    basic = float(row.get('Basic_Salary', 0))
    per_day = basic / 30
    
    # رولز: 3 لایٹس پر 1 چھٹی، 2 ہاف ڈیز پر 1 چھٹی
    lates_off = math.floor(float(row.get('Lates', 0)) / 3)
    half_day_off = math.floor(float(row.get('Half_Day', 0)) / 2)
    
    total_deduction_days = float(row.get('Absents', 0)) + lates_off + half_day_off
    total_deduction_rs = total_deduction_days * per_day
    
    net_salary = basic - total_deduction_rs - float(row.get('Advance', 0))
    calc_list.append(round(net_salary))

edited_df['Net_Salary'] = calc_list

# ایکسل ڈاؤن لوڈ بٹن (کیونکہ اب ہم Secrets استعمال نہیں کر رہے)
st.divider()
csv = edited_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Updated Data (Excel)", data=csv, file_name='Salary_Report.csv')
st.info("نوٹ: ڈیٹا ایڈٹ کرنے کے بعد اسے ڈاؤن لوڈ کر کے اپنی گوگل شیٹ میں کاپی پیسٹ کر لیں۔")

# --- سیلری سلپ ---
st.subheader("🔍 Generate Salary Slip")
search_id = st.text_input("ID لکھیں:")
if search_id:
    match = edited_df[edited_df['ID'].astype(str).str.contains(str(search_id))]
    if not match.empty:
        emp = match.iloc[0]
        st.markdown(f"""
            <div style="border: 2px solid #ff4b4b; padding: 20px; border-radius: 15px; background: white; color: black; max-width: 500px; margin: auto;">
                <h2 style="text-align: center; color: #ff4b4b;">THE EDUCATORS</h2>
                <hr>
                <p><b>Name:</b> {emp['Name']} | <b>ID:</b> {emp['ID']}</p>
                <p><b>Designation:</b> {emp['Designation']}</p>
                <p><b>Total Off Days (Inc. Lates/Half):</b> {float(emp['Absents']) + math.floor(float(emp['Lates'])/3) + math.floor(float(emp['Half_Day'])/2)}</p>
                <div style="background: #fdf2f2; padding: 10px; text-align: center;">
                    <h3>Net Payable: PKR {emp['Net_Salary']}</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
