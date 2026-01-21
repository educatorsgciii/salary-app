import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# پیج سیٹ اپ
st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# گوگل شیٹ سے کنکشن (Secrets کے ذریعے)
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # ڈیٹا پڑھنا
    df = conn.read(ttl="0")
    df = df.dropna(how="all")
    
    st.success("✅ سسٹم کامیابی سے کنکٹ ہو گیا ہے!")

    # --- ایڈٹ اور ڈیلیٹ والا ٹیبل ---
    st.subheader("📊 Manage Employees")
    
    # یہاں 'data_editor' ہی وہ طریقہ ہے جو پنسل اور ڈیلیٹ کے بٹن فراہم کرتا ہے
    # جب آپ کسی لائن کو منتخب کریں گی تو اوپر 'Delete' کا نشان خود بخود آ جائے گا
    edited_df = st.data_editor(
        df, 
        use_container_width=True, 
        num_rows="dynamic", # اس سے نئی لائن ایڈ (Pencil) اور ڈیلیٹ (Trash) ہو سکے گی
        key="employee_editor"
    )

    # تبدیلیوں کو محفوظ کرنے کا بٹن
    if st.button("💾 Save All Changes to Google Sheet"):
        try:
            conn.update(data=edited_df)
            st.balloons()
            st.success("تبدیلیاں گوگل شیٹ میں محفوظ کر دی گئی ہیں!")
        except Exception as e:
            st.error(f"محفوظ کرنے میں مسئلہ ہوا: {e}")

    st.divider()

    # --- سیلری سلپ والا حصہ ---
    st.subheader("🔍 Search & Print Salary Slip")
    search_id = st.text_input("ملازم کی ID لکھیں:")

    if search_id:
        matched_emp = df[df['ID'].astype(str) == str(search_id).strip()]
        if not matched_emp.empty:
            emp = matched_emp.iloc[0]
            # سلپ کا ڈیزائن
            st.markdown(f"""
            <div style="border: 2px solid #ff4b4b; padding: 20px; border-radius: 10px; background-color: white;">
                <h2 style="text-align: center; color: #ff4b4b;">THE EDUCATORS</h2>
                <hr>
                <p><b>Name:</b> {emp.get('Name', '---')}</p>
                <p><b>Designation:</b> {emp.get('Designation', '---')}</p>
                <p><b>Salary:</b> Rs. {emp.get('Salary', '0')}</p>
            </div>
            """, unsafe_allow_html=True)
            st.info("پرنٹ کے لیے Ctrl + P دبائیں۔")
        else:
            st.error("اس ID کا کوئی ریکارڈ نہیں ملا۔")

except Exception as e:
    st.error("پہلے 'Secrets' والے باکس میں کوڈ ڈالیں تاکہ سسٹم کنکٹ ہو سکے۔")
    st.info(f"Technical Detail: {e}")
