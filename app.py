import streamlit as st
import pandas as pd

st.set_page_config(page_title="The Educators Salary System", layout="wide")

st.title("🏫 The Educators - Salary Management System")

# گوگل شیٹ لنک
sheet_id = "13eYpH7tTx-SCDkCVRFzq5Ar7QXccXoLBIRfsmvufp3Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# ڈیٹا لوڈ کرنا
if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv(sheet_url).dropna(how="all")
        st.session_state.df.columns = st.session_state.df.columns.str.strip()
    except:
        st.error("شیٹ لوڈ نہیں ہو سکی۔")

df = st.session_state.df

# --- مین ٹیبل جس میں ایڈٹ اور ڈیلیٹ بٹن ہوں گے ---
st.subheader("📊 Employee Records")

# ٹیبل کے ہیڈر
cols = st.columns([1, 2, 2, 2, 1, 1])
cols[0].write("**ID**")
cols[1].write("**Name**")
cols[2].write("**Designation**")
cols[3].write("**Salary**")
cols[4].write("**Edit**")
cols[5].write("**Delete**")

st.divider()

# ہر لائن کے لیے بٹن بنانا
for index, row in df.iterrows():
    c1, c2, c3, c4, c5, c6 = st.columns([1, 2, 2, 2, 1, 1])
    c1.write(row['ID'])
    c2.write(row['Name'])
    c3.write(row['Designation'])
    c4.write(row['Salary'])
    
    # پنسل (Edit) والا بٹن
    if c5.button("📝", key=f"edit_{index}"):
        st.info(f"آپ {row['Name']} کا ڈیٹا ایڈٹ کر رہے ہیں۔ (یہ فیچر ابھی منسلک ہو رہا ہے)")
    
    # ڈسٹ بن (Delete) والا بٹن
    if c6.button("🗑️", key=f"del_{index}"):
        st.session_state.df = df.drop(index)
        st.rerun()

st.divider()

# --- سیلری سلپ سرچ ---
st.subheader("🔍 Search & Print Salary Slip")
search_id = st.text_input("ملازم کی ID لکھیں:")

if search_id:
    matched = df[df['ID'].astype(str) == str(search_id).strip()]
    if not matched.empty:
        emp = matched.iloc[0]
        slip_html = f"""
        <div style="border: 2px solid #ff4b4b; padding: 20px; border-radius: 10px; background-color: white; color: black; max-width: 600px; margin: auto;">
            <h2 style="text-align: center; color: #ff4b4b;">THE EDUCATORS</h2>
            <hr>
            <p><b>Name:</b> {emp['Name']}</p>
            <p><b>ID:</b> {emp['ID']}</p>
            <p><b>Designation:</b> {emp['Designation']}</p>
            <h3 style="color: green;">Salary: Rs. {emp['Salary']}</h3>
        </div>
        """
        st.markdown(slip_html, unsafe_allow_html=True)
        st.info("پرنٹ کے لیے Ctrl + P دبائیں۔")

# ایکسل ڈاؤن لوڈ
st.divider()
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Updated Excel", data=csv, file_name='Salary_Report.csv')
