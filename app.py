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
    
    # ڈیٹا کی صفائی (تاکہ سرچ میں مسئلہ نہ ہو)
    df.columns = df.columns.str.strip()
    df['ID'] = df['ID'].astype(str).str.strip().str.replace('.0', '', regex=False)
    
    st.success("✅ ڈیٹا کامیابی سے اپ ڈیٹ ہو گیا ہے!")
    
    # ملازمین کا ریکارڈ دکھانا
    with st.expander("📊 تمام ملازمین کا ریکارڈ دیکھیں"):
        st.dataframe(df, use_container_width=True)
    
    st.divider()
    st.subheader("🔍 Search Employee & Print Salary Slip")

    # سرچ کے لیے ان پٹ
    search_query = st.text_input("ملازم کی ID لکھیں (مثال: 104)", placeholder="یہاں ID ٹائپ کریں...")

    if search_query:
        # سرچ کرنے کا بہتر طریقہ
        matched_emp = df[df['ID'] == str(search_query).strip()]
        
        if not matched_emp.empty:
            emp_data = matched_emp.iloc[0]
            
            # سلپ کا پروفیشنل ڈیزائن
            slip_html = f"""
            <div style="background-color: white; padding: 30px; border: 2px solid #ff4b4b; border-radius: 10px; max-width: 800px; margin: auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333;">
                <div style="text-align: center; border-bottom: 2px solid #eee; padding-bottom: 15px;">
                    <h1 style="color: #ff4b4b; margin: 0;">THE EDUCATORS</h1>
                    <p style="margin: 5px 0; color: #666;">Gulshan Campus III, Karachi</p>
                    <div style="background: #fdf2f2; display: inline-block; padding: 5px 30px; border-radius: 20px; font-weight: bold; margin-top: 10px;">MONTHLY SALARY SLIP</div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-top: 25px;">
                    <div style="line-height: 1.8;">
                        <p><b>Employee Name:</b> {emp_data.get('Name', 'N/A')}</p>
                        <p><b>Designation:</b> {emp_data.get('Designation', 'N/A')}</p>
                    </div>
                    <div style="text-align: right; line-height: 1.8;">
                        <p><b>Employee ID:</b> <span style="color: #ff4b4b;">{emp_data.get('ID', 'N/A')}</span></p>
                        <p><b>CNIC:</b> {emp_data.get('CNIC', 'N/A')}</p>
                    </div>
                </div>

                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <thead>
                        <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                            <th style="padding: 12px; text-align: left;">Description</th>
                            <th style="padding: 12px; text-align: right;">Amount (PKR)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 15px;">Basic Salary / Total Monthly</td>
                            <td style="padding: 15px; text-align: right; font-weight: bold;">Rs. {emp_data.get('Salary', '0')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 15px;">Allowances / Bonus</td>
                            <td style="padding: 15px; text-align: right;">Rs. 0</td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr style="background-color: #fff5f5; font-size: 1.2em; font-weight: bold;">
                            <td style="padding: 15px; border-top: 2px solid #ff4b4b;">Net Payable</td>
                            <td style="padding: 15px; text-align: right; border-top: 2px solid #ff4b4b; color: #d32f2f;">Rs. {emp_data.get('Salary', '0')}</td>
                        </tr>
                    </tfoot>
                </table>

                <div style="margin-top: 50px; display: flex; justify-content: space-between;">
                    <div style="text-align: center; border-top: 1px solid #999; width: 200px; padding-top: 5px;">Accountant Signature</div>
                    <div style="text-align: center; border-top: 1px solid #999; width: 200px; padding-top: 5px;">Employee Signature</div>
                </div>
            </div>
            """
            st.markdown(slip_html, unsafe_allow_html=True)
            st.info("🖨️ سلپ پرنٹ کرنے کے لیے **Ctrl + P** دبائیں اور اسے PDF کے طور پر محفوظ کر لیں۔")
        else:
            st.error(f"❌ ID '{search_query}' کا کوئی ملازم نہیں ملا۔")

    # ڈاؤن لوڈ بٹن
    st.divider()
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download All Records (Excel)", data=csv, file_name='Salary_Report.csv', mime='text/csv')

except Exception as e:
    st.error(f"Error: {e}")
