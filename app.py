import streamlit as st
import pandas as pd

# پیج سیٹ اپ
st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# گوگل شیٹ لنک
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # ڈیٹا لوڈ کرنا
    df = pd.read_csv(sheet_url)
    df = df.dropna(how="all")
    
    # کالمز اور ڈیٹا کی صفائی
    df.columns = df.columns.str.strip()
    # ID کو نمبر سے ٹیکسٹ میں بدلنا تاکہ سرچ میں مسئلہ نہ ہو
    if 'ID' in df.columns:
        df['ID'] = df['ID'].astype(str).str.replace('.0', '', regex=False).str.strip()

    st.success("✅ سسٹم کامیابی سے اپ ڈیٹ ہو گیا ہے!")

    # --- حصہ 1: مین ڈیٹا ٹیبل (ایڈٹ اور ڈیلیٹ کے لیے) ---
    st.subheader("📊 Employee Database")
    # اسٹریم لٹ کا نیا ڈیٹا ایڈیٹر جو ایڈٹ کی سہولت دیتا ہے
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    st.divider()

    # --- حصہ 2: سیلری سلپ سرچ ---
    st.subheader("🔍 Search & Print Salary Slip")
    search_query = st.text_input("ملازم کی ID لکھیں (مثال: 102)", placeholder="یہاں ID ٹائپ کریں اور Enter دبائیں...")

    if search_query:
        # سرچ کرنے کا عمل
        matched_emp = df[df['ID'] == str(search_query).strip()]
        
        if not matched_emp.empty:
            emp = matched_emp.iloc[0]
            salary_val = emp.get('Salary', emp.get('Basic', '0'))
            
            # سلپ کا ڈیزائن (unsafe_allow_html=True کے ساتھ تاکہ کوڈ نہ دکھے)
            slip_html = f"""
            <div style="background-color: white; padding: 30px; border: 2px solid #ff4b4b; border-radius: 10px; color: #333; max-width: 700px; margin: auto;">
                <div style="text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px;">
                    <h1 style="color: #ff4b4b; margin: 0;">THE EDUCATORS</h1>
                    <p style="margin: 5px 0;">Gulshan Campus III, Karachi</p>
                    <b style="background: #fdf2f2; padding: 5px 15px; border-radius: 10px;">MONTHLY SALARY SLIP</b>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 20px;">
                    <div>
                        <p><b>Name:</b> {emp.get('Name', 'N/A')}</p>
                        <p><b>Designation:</b> {emp.get('Designation', 'N/A')}</p>
                    </div>
                    <div style="text-align: right;">
                        <p><b>ID:</b> {emp.get('ID', 'N/A')}</p>
                        <p><b>CNIC:</b> {emp.get('CNIC', 'N/A')}</p>
                    </div>
                </div>
                <table style="width: 100%; margin-top: 20px; border-collapse: collapse;">
                    <tr style="background: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                        <th style="padding: 10px; text-align: left;">Description</th>
                        <th style="padding: 10px; text-align: right;">Amount (PKR)</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #eee;">Monthly Basic Salary</td>
                        <td style="padding: 10px; text-align: right; border-bottom: 1px solid #eee;">Rs. {salary_val}</td>
                    </tr>
                    <tr style="font-weight: bold; background: #fff5f5;">
                        <td style="padding: 10px;">Total Net Payable</td>
                        <td style="padding: 10px; text-align: right; color: #d32f2f;">Rs. {salary_val}</td>
                    </tr>
                </table>
                <div style="margin-top: 40px; display: flex; justify-content: space-between;">
                    <div style="border-top: 1px solid #333; width: 150px; text-align: center;">Accountant</div>
                    <div style="border-top: 1px solid #333; width: 150px; text-align: center;">Employee</div>
                </div>
            </div>
            """
            # یہاں ہم HTML کو رینڈر کر رہے ہیں تاکہ کوڈ کے بجائے ڈیزائن نظر آئے
            st.markdown(slip_html, unsafe_allow_html=True)
            st.info("💡 پرنٹ کے لیے **Ctrl + P** دبائیں۔")
        else:
            st.error("❌ اس ID کا کوئی ریکارڈ موجود نہیں ہے۔")

    # ڈاؤن لوڈ بٹن
    st.divider()
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Excel Report", data=csv, file_name='Salary_Report.csv')

except Exception as e:
    st.error(f"Error: {e}")
