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
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 The Educators - Salary Management System")

# ڈیٹا لوڈ کرنا
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

if 'df' not in st.session_state:
    try:
        raw_df = pd.read_csv(sheet_url).dropna(how="all")
        raw_df.columns = raw_df.columns.str.strip()
        # ID اور تنخواہ کو صاف کرنا
        if 'ID' in raw_df.columns:
            raw_df['ID'] = raw_df['ID'].astype(str).str.replace('.0', '', regex=False)
        st.session_state.df = raw_df
    except:
        st.error("شیٹ لوڈ نہیں ہو سکی۔")

df = st.session_state.df

# --- ایڈٹ فارم (سائیڈ بار) میں تفصیلات لانا ---
if 'editing_index' in st.session_state:
    idx = st.session_state.editing_index
    if idx in df.index:
        row = df.loc[idx]
        st.sidebar.subheader(f"📝 Edit: {row.get('Name', 'Unknown')}")
        
        # یہاں ہم یقینی بنا رہے ہیں کہ پرانی قیمتیں نظر آئیں
        old_salary = str(row.get('Salary', row.get('Basic_Salary', '0')))
        if old_salary == 'nan': old_salary = "0"
            
        new_salary = st.sidebar.text_input("New Salary Amount:", value=old_salary)
        
        if st.sidebar.button("✅ Update Now"):
            st.session_state.df.at[idx, 'Salary'] = new_salary
            st.session_state.df.at[idx, 'Basic_Salary'] = new_salary # دونوں کالمز اپ ڈیٹ کریں
            del st.session_state.editing_index
            st.rerun()
        
        if st.sidebar.button("❌ Cancel"):
            del st.session_state.editing_index
            st.rerun()

# --- ریکارڈ ٹیبل ---
st.subheader("📊 Employee Records")
h = st.columns([1, 2, 2, 2, 1, 1])
for i, head in enumerate(["ID", "Name", "Designation", "Salary", "Edit", "Del"]):
    h[i].write(f"**{head}**")

st.divider()

for index, row in df.iterrows():
    c = st.columns([1, 2, 2, 2, 1, 1])
    c[0].write(row.get('ID', '---'))
    c[1].write(row.get('Name', '---'))
    c[2].write(row.get('Designation', '---'))
    
    # تنخواہ دکھانا
    s_val = row.get('Salary', row.get('Basic_Salary', '0'))
    c[3].write(s_val if pd.notna(s_val) else "0")
    
    if c[4].button("📝", key=f"edit_btn_{index}"):
        st.session_state.editing_index = index
        st.rerun()
    if c[5].button("🗑️", key=f"del_btn_{index}"):
        st.session_state.df = df.drop(index)
        st.rerun()

# --- سیلری سلپ جنریٹر ---
st.divider()
st.subheader("🔍 Search & Generate Slip")
search_id = st.text_input("ملازم کی ID لکھیں:")

if search_id:
    # سرچ کو مضبوط بنانا
    matched = df[df['ID'].astype(str).str.strip() == str(search_id).strip()]
    
    if not matched.empty:
        emp = matched.iloc[0]
        f_salary = emp.get('Salary', emp.get('Basic_Salary', '0'))
        if pd.isna(f_salary): f_salary = "0"
        
        st.markdown(f"""
            <div class="salary-slip">
                <h2 style="text-align: center; color: #ff4b4b;">THE EDUCATORS</h2>
                <p style="text-align: center;">Gulshan Campus III</p>
                <hr>
                <p><b>Employee Name:</b> {emp.get('Name', '---')}</p>
                <p><b>ID:</b> {search_id} | <b>Designation:</b> {emp.get('Designation', '---')}</p>
                <div style="background: #fdf2f2; padding: 15px; text-align: center; font-size: 20px;">
                    <b>Total Salary: PKR {f_salary}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("اس ID کا کوئی ملازم نہیں ملا۔")
