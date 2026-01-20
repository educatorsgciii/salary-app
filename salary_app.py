# مینو میں نیا آپشن شامل کرنا
menu = ["📊 Dashboard", "➕ Add New Employee", "🗑️ Manage Staff"]
choice = st.sidebar.selectbox("Menu", menu)

# ... (پرانا کوڈ ویسے ہی رہے گا)

elif choice == "🗑️ Manage Staff":
    st.subheader("Remove or Edit Employee")
    if not df.empty:
        # نام منتخب کرنے کے لیے لسٹ
        names = df['Name'].tolist()
        selected_name = st.selectbox("Select Employee", names)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Delete Employee"):
                # منتخب نام کو نکال کر باقی ڈیٹا بچانا
                df = df[df['Name'] != selected_name]
                conn.update(spreadsheet=url, data=df)
                st.error(f"{selected_name} has been removed!")
                st.rerun()
        
        with col2:
            st.info("Edit feature coming soon!")
    else:
        st.write("No employees found to manage.")
