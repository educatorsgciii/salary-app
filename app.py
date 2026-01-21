import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="The Educators Salary System", layout="wide")

# بٹنوں کا ڈیزائن
st.markdown("""
    <style>
    div.stButton > button { border: none !important; background-color: transparent !important; font-size: 20px !important; }
    div.stButton > button:hover { color: #ff4b4b !important; }
    .slip-box { border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background-color: white; color: black; max-width: 600px; margin: auto; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 The Educators - Salary Management System")

# گوگل شیٹ سے کنکشن (Secrets لازمی ہیں)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # ڈیٹا پڑھنا
    df = conn.read(ttl="0").dropna(how="all")
    df.columns = df.columns.str.strip()
    
    # اگر سیشن میں ڈیٹا نہیں ہے تو لوڈ کریں
    if 'main_df' not in st.session_state:
        st.session_state.main_df = df

    working_df = st.session_state.main_df

    # --- ایڈٹ فنکشن ---
    if 'edit_idx' in st.session_state:
        idx = st.session_state.edit_idx
        row = working_df.loc[idx]
        st.sidebar.subheader(f"📝 Edit: {row.get('Name', 'Record')}")
        
        # تمام موجودہ کالمز کے لیے ان پٹ بنائیں
        updated_data = {}
        for col in working_df.columns:
            updated_data[col] = st.sidebar.text_input(f"Change {col}", str(row[col]))
        
        if st.sidebar.button("✅ Update in App"):
            for col, val in updated_data.items():
                st.session_state.main_df.at[idx, col] = val
            del st.session_state.edit_idx
            st.rerun()

    # --- مین ڈسپلے ---
    st.subheader("📊 Employee Database")
    
    # ہیڈرز
    cols = st.columns(list(range(len(working_df.columns) + 2)))
    for i, col_name in enumerate(working_df.columns):
        cols[i].write(f"**{col_name}**")
    cols[-2].write("**Edit**")
    cols[-1].write("**Del**")

    # ڈیٹا لائنز
    for index, row in working_df.iterrows():
        c = st.columns(list(range(len(working_df.columns) + 2)))
        for i, col_name in enumerate(working_df.columns):
            c[i].write(str(row[col_name]))
        
        if c[-2].button("📝", key=f"ed_{index}"):
            st.session_state.edit_idx = index
            st.rerun()
        
        if c[-1].button("🗑️", key=f"de_{index}"):
            st.session_state.main_df = working_df.drop(index)
            st.rerun()

    st.divider()
    
    # --- گوگل شیٹ میں سیو کرنے کا جادوئی بٹن ---
    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("💾 SAVE ALL CHANGES TO GOOGLE SHEET"):
        with st.spinner("گوگل شیٹ اپ ڈیٹ ہو رہی ہے..."):
            conn.update(data=st.session_state.main_df)
            st.success("✅ مبارک ہو! تمام تبدیلیاں گوگل شیٹ میں محفوظ ہو گئی ہیں۔")
            st.balloons()

    # --- سیلری سلپ سرچ ---
    st.subheader("🔍 Generate Salary Slip")
    search_id = st.text_input("ملازم کی ID لکھیں:")
    if search_id:
        # آئی ڈی کالم چیک کریں
        id_col = 'ID' if 'ID' in working_df.columns else working_df.columns[0]
        match = working_df[working_df[id_col].astype(str).str.contains(str(search_id))]
        
        if not match.empty:
            emp = match.iloc[0]
            st.markdown(f"""
                <div class="slip-box">
                    <h2 style="text-align:center; color:#ff4b4b;">THE EDUCATORS</h2>
                    <hr>
                    <p><b>Name:</b> {emp.get('Name', '---')} | <b>Designation:</b> {emp.get('Designation', '---')}</p>
                    <div style="background:#fdf2f2; padding:15px; text-align:center; font-size:20px;">
                        <b>Net Salary: PKR {emp.get('Salary', emp.get('Basic', '0'))}</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("ریکارڈ نہیں ملا۔")

except Exception as e:
    st.error("سسٹم کنکٹ نہیں ہو سکا۔ براہِ کرم چیک کریں کہ Secrets صحیح ہیں اور گوگل شیٹ Editor پر شیئر ہے۔")
    st.info(f"Error details: {e}")
