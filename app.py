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
    div.stButton > button:hover {
        color: #ff4b4b !important;
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 The Educators - Salary Management System")

# ڈیٹا لوڈ کرنا
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv(sheet_url).dropna(how="all")
        st.session_state.df.columns = st.session_state.df.columns.str.strip()
    except:
        st.error("شیٹ لوڈ نہیں ہو سکی۔")

df = st.session_state.df

# --- ایڈٹ کرنے کا فارم ---
if 'editing_index' in st.session_state:
    idx = st.session_state.editing_index
    row = df.loc[idx]
    st.sidebar.subheader(f"📝 Edit Record: {row['Name']}")
    new_name = st.sidebar.text_input("Name", row['Name'])
    new_desig = st.sidebar.text_input("Designation", row['Designation'])
    new_salary = st.sidebar.text_input("Salary", str(row['Salary']))
    
    if st.sidebar.button("✅ Update Now"):
        st.session_state.df.at[idx, 'Name'] = new_name
        st.session_state.df.at[idx, 'Designation'] = new_desig
        st.session_state.df.at[idx, 'Salary'] = new_salary
        del st.session_state.editing_index
        st.rerun()
    if st.sidebar.button("❌ Cancel"):
        del st.session_state.editing_index
        st.rerun()

# --- ریکارڈ ٹیبل ---
st.subheader("📊 Employee Records")
h1, h2, h3, h4, h5, h6 = st.columns([1, 2, 2, 2, 1, 1])
h1.write("**ID**"); h2.write("**Name**"); h3.write("**Designation**"); h4.write("**Salary**"); h5.write("**Edit**"); h6.write("**Del**")

st.divider()

for index, row in df.iterrows():
    c1, c2, c3, c4, c5, c6 = st.columns([1, 2, 2, 2, 1, 1])
    c1.write(row['ID'])
    c2.write(row['Name'])
    c3.write(row['Designation'])
    c4.write(row['Salary'])
    
    # بغیر باکس والا ایڈٹ بٹن
    if c5.button("📝", key=f"ed_{index}"):
        st.session_state.editing_index = index
        st.rerun()
    
    # بغیر باکس والا ڈیلیٹ بٹن
    if c6.button("🗑️", key=f"de_{index}"):
        st.session_state.df = df.drop(index)
        st.rerun()

# --- سیلری سلپ اور سرچ ---
st.divider()
search_id = st.text_input("🔍 Search by ID to Print Slip:")
if search_id:
    matched = df[df['ID'].astype(str) == str(search_id).strip()]
    if not matched.empty:
        emp = matched.iloc[0]
        st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: white; color: black; max-width: 500px;">
                <h3 style="text-align: center; color: #ff4b4b;">THE EDUCATORS</h3>
                <p><b>Name:</b> {emp['Name']} | <b>ID:</b> {emp['ID']}</p>
                <p><b>Designation:</b> {emp['Designation']}</p>
                <h4 style="color: green;">Net Salary: Rs. {emp['Salary']}</h4>
            </div>
        """, unsafe_allow_html=True)
        st.info("Print with Ctrl + P")

# ڈاؤن لوڈ ایکسل
st.download_button("📥 Download Excel", data=df.to_csv(index=False).encode('utf-8'), file_name='Salary_Report.csv')
