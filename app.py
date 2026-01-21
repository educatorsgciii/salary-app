import streamlit as st
import pandas as pd

# پیج سیٹ اپ
st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# شیٹ کا آئی ڈی اور لنک
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
# براہِ راست ایکسل فارمیٹ میں ڈیٹا اٹھانا
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # ڈیٹا لوڈ کرنا
    df = pd.read_csv(sheet_url)
    df = df.dropna(how="all")
    
    # کالمز کی صفائی
    df.columns = df.columns.str.strip()
    if 'ID' in df.columns:
        df['ID'] = df['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()

    st.success("✅ سسٹم کامیابی سے بحال ہو گیا ہے!")

    # --- ایڈٹ اور ڈیلیٹ کے لیے ٹیبل ---
    st.subheader("📊 Manage Employee Records")
    st.info("💡 کسی بھی خانے پر ڈبل کلک کر کے ایڈٹ کریں، یا لائن سلیکٹ کر کے ڈیلیٹ دبائیں۔")
    
    # اسٹریم لٹ کا ایڈیٹر جو آپ کو ایڈٹ اور ڈیلیٹ کی سہولت دیتا ہے
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

    # ایکسل ڈاؤن لوڈ بٹن
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Updated Excel", data=csv, file_name='Updated_Salary_Report.csv')

    st.divider()

    # --- سیلری سلپ والا حصہ ---
    st.subheader("🔍 Search & Print Salary Slip")
    search_query = st.text_input("ملازم کی ID لکھیں:")

    if search_query:
        matched = edited_df[edited_df['ID'] == str(search_query).strip()]
        if not matched.empty:
            emp = matched.iloc[0]
            st.markdown(f"""
            <div style="border: 2px solid #ff4b4b; padding: 30px; border-radius: 10px; background-color: white; color: black;">
                <h2 style="text-align: center; color: #ff4b4b; margin: 0;">THE EDUCATORS</h2>
                <p style="text-align: center; margin: 5px 0;">Gulshan Campus III</p>
                <hr>
                <table style="width: 100%;">
                    <tr><td><b>Name:</b> {emp.get('Name', '---')}</td><td style="text-align: right;"><b>ID:</b> {emp.get('ID', '---')}</td></tr>
                    <tr><td><b>Designation:</b> {emp.get('Designation', '---')}</td><td style="text-align: right;"><b>CNIC:</b> {emp.get('CNIC', '---')}</td></tr>
                </table>
                <br>
                <div style="background: #f8f9fa; padding: 10px; font-size: 20px; text-align: center;">
                    <b>Net Salary: Rs. {emp.get('Salary', emp.get('Basic', '0'))}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.info("🖨️ پرنٹ کے لیے Ctrl + P دبائیں۔")

except Exception as e:
    st.error(f"کنکشن میں مسئلہ ہے: {e}")
