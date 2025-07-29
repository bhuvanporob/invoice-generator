import streamlit as st
import datetime

st.set_page_config(page_title="Invoice Generator", layout="wide")
st.title("📄 Excel Invoice Generator")

# Sidebar Form
with st.sidebar.form("invoice_form"):
    st.subheader("📌 Invoice Info")
    invoice_number = st.text_input("Invoice Number")
    invoice_date = st.date_input("Invoice Date", value=datetime.date.today())
    
    st.subheader("🧾 Buyer Info")
    buyer_name = st.text_input("Buyer Name")
    buyer_address = st.text_area("Buyer Address (can span multiple lines)")

    st.subheader("🏢 Consignee Info")
    consignee_details = st.text_input("Consignee Name")
    consignee_address = st.text_area("Consignee Address (can span multiple lines)")

    st.subheader("🚢 Shipment & Order Info")
    inco_terms = st.text_input("INCO Terms")
    payment_terms = st.text_input("Payment Terms")
    po_number = st.text_input("Purchase Order Number")
    po_date = st.date_input("Purchase Order Date", value=datetime.date.today())
    final_destination = st.text_input("Final Destination")
    final_discharge = st.text_input("Final Discharge Port")

    st.subheader("📞 Contact Info")
    contact_person = st.text_input("Contact Person")
    email_id = st.text_input("Email ID")
    contact_details = st.text_input("Phone/Mobile No.")

    st.subheader("📝 Other")
    remarks = st.text_area("Remarks (can span multiple lines)")

    submitted = st.form_submit_button("Proceed to Product Selection")
