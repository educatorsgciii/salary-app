import streamlit as st
import pandas as pd

# پیج سیٹ اپ
st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 The Educators - Salary Management System")

# گوگل شیٹ لنک
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    df = df.dropna(how="all")
    # کالمز کے ناموں کو صاف کرنا (تاکہ اسپیس کا مسئلہ نہ ہو)
    df.columns = df.columns.str.strip()
    
    st.success("✅ ڈیٹا کامیابی سے اپ ڈیٹ ہو گیا ہے!")
    
    st.subheader("📊 ملازمین کا ریکارڈ")
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    st.subheader("🔍 Search & Generate Salary Slip")

    if not df.empty:
        # ID سے سرچ کرنے کا خانہ
        search_id = st.text_input("ملازم کی ID لکھیں (مثال: 101)", "")

        if search_id:
            # ID میچ کرنا (نمبر یا ٹیکسٹ دونوں صورتوں میں)
            matched_emp = df[df['ID'].astype(str) == str(search_id)]
            
            if not matched_emp.empty:
                emp_data = matched_emp.iloc[0]
                
                # سیلری نکالنا (اگر کالم کا نام Salary ہے)
                basic_salary = emp_data.get('Salary', emp_data.get('Basic Salary', '0'))
                
                # خوبصورت سلپ ڈیزائن
                slip_design = f"""
                <div style="background-color: white; padding: 40px; border: 1px solid #ddd; border-radius: 15px; max-width: 700px; margin: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); color: #333;">
                    <div style="text-align: center; border-bottom: 3px solid #ff4b4b; padding-bottom: 10px;">
                        <h1 style="margin: 0; color: #ff4b4b; letter-spacing: 2px;">THE EDUCATORS</h1>
                        <p style="margin: 5px 0; font-size: 16px;">Gulshan Campus III, Karachi</p>
                        <h3 style="margin: 10px 0; background: #eee; display: inline-block; padding: 5px 20px; border-radius: 5px;">MONTHLY SALARY SLIP</h3>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 30px; font-size: 15px;">
                        <div>
                            <p><b>Employee Name:</b> <span style="color: #555;">{emp_data.get('Name', '---')}</span></p>
                            <p><b>Designation:</b> <span style="color: #555;">{emp_data.get('Designation', '---')}</span></p>
                        </div>
                        <div style="text-align: right;">
                            <p><b>ID No:</b> <span style="color: #555;">{emp_data.get('ID', '---')}</span></p>
                            <p><b>CNIC:</b> <span style="color: #555;">{emp_data.get('CNIC', '---')}</span></p>
                        </div>
                    </div>
                    <table style="width: 100%; margin-top: 30px; border-collapse: collapse; font-size: 16px;">
                        <tr style="background-color: #ff4b4b; color: white;">
                            <th style="padding: 12px; text-align: left; border-radius: 5px 0 0 5px;">Description</th>
                            <th style="padding: 12px; text-align: right; border-radius: 0 5px 5px 0;">Amount (PKR)</th>
                        </tr>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 15px;">Basic Salary</td>
                            <td style="padding: 15px; text-align: right;">Rs. {basic_salary}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 15px;">Allowances / Bonus</td>
                            <td style="padding: 15px; text-align: right;">Rs. 0</td>
                        </tr>
                        <tr style="background-color: #f9f9f9; font-weight: bold; font-size: 18px;">
                            <td style="padding: 15px;">Net Payable Amount</td>
                            <td style="padding: 15px; text-align: right; color: #2e7d32;">Rs. {basic_salary}</td>
                        </tr>
                    </table>
                    <div style="margin-top: 60px; display: flex; justify-content: space-between;">
                        <div style="border-top: 1px solid #333; width: 180px; text-align: center; padding-top: 5px; font-size: 14px;">Accountant Signature</div>
                        <div style="border-top: 1px solid #333; width: 180px; text-align: center; padding-top: 5px; font-size: 14px;">Employee Signature</div>
                    </div>
                </div>
                """
                st.markdown(slip_design, unsafe_allow_html=True)
                st.info("💡 سلپ پرنٹ کرنے کے لیے **Ctrl + P** دبائیں")
            else:
                st.error("❌ اس ID کا کوئی ملازم نہیں ملا۔")
        else:
            st.info("اوپر ملازم کی ID لکھ کر سرچ کریں۔")

    # ایکسل ڈاؤن لوڈ بٹن
    st.divider()
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download All Records (Excel)", data=csv, file_name='Salary_Records.csv', mime='text/csv')

except Exception as e:
    st.error(f"Error: {e}")
