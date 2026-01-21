import streamlit as st
import pandas as pd

st.set_page_config(page_title="The Educators Salary System", layout="wide")

# بٹنوں کو سادہ بنانے کے لیے CSS
st.markdown("""
    <style>
    div.stButton > button {
        border: none !important;
        background-color: transparent !important;
        color: inherit !important;
        padding: 0px !important;
        font-size: 20px !important;
    }
    div.stButton > button:hover { color: #ff4b4b !important; }
    .salary-slip {
        border: 2px solid #ff4b4b; padding: 30px; border-radius: 15px;
        background-color: white; color: black; max-width: 600px; margin: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 The Educators - Salary Management System")

# ڈیٹا لوڈ کرنا
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv(sheet_url).dropna(how="all")
        st.session_state.df.columns = st.session_state.df.columns.str.strip()
    except:
        st.error("شیٹ لوڈ نہیں ہو سکی۔")

df = st.session_state.df

# --- ایڈٹ فارم (سائیڈ بار) ---
if 'editing_index' in st.session_state:
    idx = st.session_state.editing_index
    row = df.loc[idx]
    st.sidebar.subheader(f"📝 Edit: {row['Name']}")
    new_salary = st.sidebar.text_input("Salary", str(row.get('Salary', row.get('Basic_Salary', '0'))))
    if st.sidebar.button("✅ Update Record"):
        st.session_state.df.at[idx, 'Salary'] = new_salary
        del st.session_state.editing_index
        st.rerun()

# --- ریکارڈ ٹیبل ---
st.subheader("📊 Employee Records")
h = st.columns([1, 2, 2, 2, 1, 1])
headers = ["ID", "Name", "Designation", "Salary", "Edit", "Del"]
for i, head in enumerate(headers): h[i].write(f"**{head}**")

st.divider()

for index, row in df.iterrows():
    c = st.columns([1, 2, 2, 2, 1, 1])
    # ID کو صاف دکھانا (102.0 کے بجائے 102)
    emp_id = str(row['ID']).replace('.0', '')
    c[0].write(emp_id)
    c[1].write(row['Name'])
    c[2].write(row['Designation'])
    # تنخواہ اگر nan ہو تو 0 دکھانا
    salary_display = row.get('Salary', row.get('Basic_Salary', '0'))
    c[3].write(salary_display if pd.notna(salary_display) else "0")
    
    if c[4].button("📝", key=f"e_{index}"):
        st.session_state.editing_index = index
        st.rerun()
    if c[5].button("🗑️", key=f"d_{index}"):
        st.session_state.df = df.drop(index)
        st.rerun()

# --- سلپ سرچ (مسئلہ حل شدہ) ---
st.divider()
st.subheader("🔍 Generate Salary Slip")
search_id = st.text_input("ملازم کی ID لکھیں (مثال: 102):")

if search_id:
    # سرچ کو بہتر بنایا تاکہ 102 اور 102.0 دونوں میچ ہوں
    df['ID_str'] = df['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()
    matched = df[df['ID_str'] == str(search_id).strip()]
    
    if not matched.empty:
        emp = matched.iloc[0]
        final_salary = emp.get('Salary', emp.get('Basic_Salary', '0'))
        
        st.markdown(f"""
            <div class="salary-slip">
                <div style="text-align: center;">
                    <h2 style="color: #ff4b4b; margin:0;">THE EDUCATORS</h2>
                    <p style="margin:0;">Gulshan Campus III</p>
                    <hr>
                    <h4 style="text-decoration: underline;">MONTHLY SALARY SLIP</h4>
                </div>
                <table style="width: 100%; margin-top: 20px;">
                    <tr><td><b>Name:</b> {emp['Name']}</td><td style="text-align: right;"><b>ID:</b> {search_id}</td></tr>
                    <tr><td><b>Designation:</b> {emp['Designation']}</td><td style="text-align: right;"><b>CNIC:</b> {emp.get('CNIC', '---')}</td></tr>
                </table>
                <div style="background: #fdf2f2; padding: 15px; margin-top: 20px; text-align: center; border-radius: 10px;">
                    <span style="font-size: 20px; font-weight: bold;">Net Salary: PKR {final_salary}</span>
                </div>
                <div style="margin-top: 50px; display: flex; justify-content: space-between; font-size: 12px;">
                    <p style="border-top: 1px solid #000; width: 150px; text-align: center;">Accountant Signature</p>
                    <p style="border-top: 1px solid #000; width: 150px; text-align: center;">Employee Signature</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.info("🖨️ پرنٹ کے لیے **Ctrl + P** دبائیں۔")
    else:
        st.error("❌ اس ID کا کوئی ریکارڈ نہیں ملا۔")

st.download_button("📥 Download Excel", data=df.to_csv(index=False).encode('utf-8'), file_name='Salary_Report.csv')
