import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="The Educators Salary System", layout="wide")

# بٹن ڈیزائن
st.markdown("""
    <style>
    div.stButton > button { border: none !important; background-color: transparent !important; font-size: 20px !important; }
    div.stButton > button:hover { color: #ff4b4b !important; }
    .slip-box { border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background-color: white; color: black; max-width: 500px; margin: auto; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 The Educators - Salary Management System")

# گوگل شیٹ سے کنکشن
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl="0").dropna(how="all")
    df.columns = df.columns.str.strip()

    if 'main_df' not in st.session_state:
        st.session_state.main_df = df

    current_df = st.session_state.main_df

    # --- مکمل ایڈٹ فارم (Sidebar) ---
    if 'edit_idx' in st.session_state:
        idx = st.session_state.edit_idx
        row = current_df.loc[idx]
        st.sidebar.subheader(f"📝 Full Edit: {row.get('Name', 'Record')}")
        
        # تمام تفصیلات بدلنے کے خانے
        new_name = st.sidebar.text_input("Name", str(row.get('Name', '')))
        new_desig = st.sidebar.text_input("Designation", str(row.get('Designation', '')))
        new_salary = st.sidebar.text_input("Salary Amount", str(row.get('Salary', '0')))
        
        if st.sidebar.button("✅ Update in App"):
            st.session_state.main_df.at[idx, 'Name'] = new_name
            st.session_state.main_df.at[idx, 'Designation'] = new_desig
            st.session_state.main_df.at[idx, 'Salary'] = new_salary
            del st.session_state.edit_idx
            st.rerun()
        
        if st.sidebar.button("❌ Cancel"):
            del st.session_state.edit_idx
            st.rerun()

    # --- مین ٹیبل ---
    st.subheader("📊 Employee Records")
    h = st.columns([1, 2, 2, 2, 1, 1])
    headers = ["ID", "Name", "Designation", "Salary", "Edit", "Del"]
    for i, txt in enumerate(headers): h[i].write(f"**{txt}**")

    st.divider()

    for index, row in current_df.iterrows():
        c = st.columns([1, 2, 2, 2, 1, 1])
        c[0].write(str(row.get('ID', '---')).replace('.0', ''))
        c[1].write(row.get('Name', '---'))
        c[2].write(row.get('Designation', '---'))
        c[3].write(str(row.get('Salary', '0')))
        
        if c[4].button("📝", key=f"edit_{index}"):
            st.session_state.edit_idx = index
            st.rerun()
        
        if c[5].button("🗑️", key=f"del_{index}"):
            st.session_state.main_df = current_df.drop(index)
            st.rerun()

    st.divider()
    
    # گوگل شیٹ میں مستقل محفوظ کرنے کا بٹن
    if st.button("💾 SAVE CHANGES TO GOOGLE SHEET"):
        with st.spinner("ڈیٹا اپ ڈیٹ ہو رہا ہے..."):
            conn.update(data=st.session_state.main_df)
            st.success("✅ گوگل شیٹ میں تمام تفصیلات محفوظ ہو گئی ہیں!")
            st.balloons()

    # --- سرچ اور سلپ ---
    st.subheader("🔍 Search & Print Slip")
    s_id = st.text_input("ID لکھیں:")
    if s_id:
        match = current_df[current_df['ID'].astype(str).str.contains(str(s_id))]
        if not match.empty:
            emp = match.iloc[0]
            st.markdown(f"""
                <div class="slip-box">
                    <h2 style="text-align:center; color:#ff4b4b;">THE EDUCATORS</h2>
                    <hr>
                    <p><b>Name:</b> {emp.get('Name')} | <b>ID:</b> {s_id}</p>
                    <p><b>Designation:</b> {emp.get('Designation')}</p>
                    <h3 style="background:#fdf2f2; padding:10px; text-align:center;">Net Salary: PKR {emp.get('Salary')}</h3>
                </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error("کنکشن کا مسئلہ: براہِ کرم Secrets دوبارہ چیک کریں۔")
