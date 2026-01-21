import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# کنکشن قائم کرنا
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # ڈیٹا پڑھنا (بغیر کسی ایرر کے)
    df = conn.read(ttl="0")
    df = df.dropna(how="all")
    df.columns = df.columns.str.strip()

    # خودکار کالم مینجمنٹ: اگر ID کا کالم نہیں ہے تو اسے شامل کریں
    if 'ID' not in df.columns:
        st.warning("⚠️ آپ کی شیٹ میں 'ID' کا کالم نہیں تھا، میں نے اسے عارضی طور پر شامل کر دیا ہے۔")
        df.insert(0, 'ID', range(101, 101 + len(df)))

    if 'main_df' not in st.session_state:
        st.session_state.main_df = df

    st.success("✅ سسٹم کامیابی سے گوگل شیٹ سے منسلک ہے!")

    # --- ڈیٹا ایڈیٹر (جہاں سے آپ ایڈٹ اور ڈیلیٹ کریں گی) ---
    st.subheader("📊 ملازمین کا ریکارڈ (براہِ راست ایڈٹ کریں)")
    st.info("💡 آپ کسی بھی خانے پر کلک کر کے اسے بدل سکتی ہیں اور نئی لائن بھی جوڑ سکتی ہیں۔")
    
    edited_df = st.data_editor(st.session_state.main_df, use_container_width=True, num_rows="dynamic")

    # جادوئی سیو بٹن
    if st.button("💾 SAVE CHANGES TO GOOGLE SHEET"):
        with st.spinner("ڈیٹا گوگل شیٹ میں محفوظ ہو رہا ہے..."):
            conn.update(data=edited_df)
            st.session_state.main_df = edited_df
            st.success("🎉 زبردست! تمام تبدیلیاں اور نئے کالمز گوگل شیٹ میں اپ ڈیٹ ہو گئے ہیں۔")
            st.balloons()

    st.divider()

    # --- سرچ اور سلپ جنریٹر ---
    st.subheader("🔍 Search & Print Slip")
    search_id = st.text_input("ملازم کی ID لکھیں:")
    
    if search_id:
        # آئی ڈی میچ کرنا
        match = edited_df[edited_df['ID'].astype(str).str.contains(str(search_id))]
        if not match.empty:
            emp = match.iloc[0]
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background-color: white; color: black; max-width: 500px; margin: auto;">
                    <h2 style="text-align: center; color: #ff4b4b;">THE EDUCATORS</h2>
                    <p style="text-align: center;">Salary Slip</p>
                    <hr>
                    <p><b>Name:</b> {emp.get('Name', '---')}</p>
                    <p><b>ID:</b> {emp.get('ID', '---')}</p>
                    <h3 style="color: green; text-align: center;">Net Salary: PKR {emp.get('Salary', emp.get('Basic', '0'))}</h3>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("ریکارڈ نہیں ملا۔")

except Exception as e:
    st.error("❌ کنکشن میں اب بھی مسئلہ ہے۔")
    st.info(f"Technical Reason: {e}")
    st.warning("مشورہ: Secrets میں 'private_key' کو دوبارہ کاپی پیسٹ کریں، شاید کوئی لفظ رہ گیا ہے۔")
