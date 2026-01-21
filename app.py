import streamlit as st
import pandas as pd

# پیج سیٹ اپ
st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# گوگل شیٹ کا لنک
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # ڈیٹا لوڈ کرنا
    df = pd.read_csv(sheet_url)
    df = df.dropna(how="all")
    
    st.success("✅ ڈیٹا کامیابی سے لوڈ ہو گیا ہے!")
    
    # ڈیش بورڈ دکھانا
    st.subheader("📊 ملازمین کا ریکارڈ")
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # --- سیلری سلپ جنریٹ کرنے کا حصہ ---
    st.subheader("📄 Generate Salary Slip")
    
    if not df.empty:
        # ملازم کا انتخاب
        employee_names = df['Name'].tolist()
        selected_emp = st.selectbox("ملازم کا نام منتخب کریں", employee_names)
        
        # منتخب ملازم کا ڈیٹا نکالنا
        emp_data = df[df['Name'] == selected_emp].iloc[0]
        
        # سیلری سلپ کا ڈیزائن (HTML/CSS کے ساتھ)
        slip_html = f"""
        <div style="border: 2px solid #333; padding: 25px; border-radius: 5px; background-color: white; color: black; font-family: sans-serif;">
            <div style="text-align: center;">
                <h2 style="margin: 0;">THE EDUCATORS</h2>
                <p style="margin: 5px 0;">Gulshan Campus III</p>
                <h4 style="text-decoration: underline;">MONTHLY SALARY SLIP</h4>
            </div>
            <br>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 5px;"><b>Employee Name:</b> {selected_emp}</td>
                    <td style="padding: 5px;"><b>ID:</b> {emp_data.get('ID', '---')}</td>
                </tr>
                <tr>
                    <td style="padding: 5px;"><b>Designation:</b> {emp_data.get('Designation', '---')}</td>
                    <td style="padding: 5px;"><b>CNIC:</b> {emp_data.get('CNIC', '---')}</td>
                </tr>
            </table>
            <hr>
            <table style="width: 100%;">
                <tr style="background-color: #f2f2f2;">
                    <th style="text-align: left; padding: 10px;">Description</th>
                    <th style="text-align: right; padding: 10px;">Amount (Rs.)</th>
                </tr>
                <tr>
                    <td style="padding: 10px;">Basic Salary</td>
                    <td style="text-align: right; padding: 10px;">{emp_data.get('Salary', '0')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px;">Allowances</td>
                    <td style="text-align: right; padding: 10px;">0</td>
                </tr>
                <tr style="border-top: 1px solid #333;">
                    <td style="padding: 10px;"><b>Total Payable</b></td>
                    <td style="text-align: right; padding: 10px;"><b>{emp_data.get('Salary', '0')}</b></td>
                </tr>
            </table>
            <br><br>
            <div style="display: flex; justify-content: space-between;">
                <p style="border-top: 1px solid #333; width: 200px; text-align: center;">Accountant Signature</p>
                <p style="border-top: 1px solid #333; width: 200px; text-align: center;">Employee Signature</p>
            </div>
        </div>
        """
        
        # سلپ دکھانا
        st.markdown(slip_html, unsafe_allow_html=True)
        
        # پرنٹ بٹن
        st.info("💡 سلپ پرنٹ کرنے کے لیے اپنے کی بورڈ سے **Ctrl + P** دبائیں اور اسے PDF کے طور پر سیو کر لیں۔")

        # ایکسل ڈاؤن لوڈ بٹن
        st.divider()
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
