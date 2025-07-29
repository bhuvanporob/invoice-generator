import streamlit as st
import datetime

st.title("📌 Step 1: Enter Invoice & Buyer Info")

st.markdown("Please fill in all required details for the invoice.")

# Invoice Details
st.header("🧾 Invoice Details")
invoice_number = st.text_input("Invoice Number")
invoice_date = st.date_input("Invoice Date", value=datetime.date.today())

# Buyer Info
st.header("🏢 Buyer Information")
buyer_name = st.text_input("Buyer Name")
buyer_address = st.text_area("Buyer Address (multi-line supported)")

# Consignee Info
st.header("🏬 Consignee Information")
consignee_details = st.text_input("Consignee Name")
consignee_address = st.text_area("Consignee Address")

# Shipment & Order Info
st.header("🚚 Shipment & Purchase Info")
po_number = st.text_input("Purchase Order Number")
po_date = st.date_input("PO Date", value=datetime.date.today())
inco_terms = st.text_input("INCO Terms")
payment_terms = st.text_input("Payment Terms")
final_destination = st.text_input("Final Destination")
final_discharge = st.text_input("Final Discharge Port")

# Contact Details
st.header("📞 Contact Info")
contact_person = st.text_input("Contact Person")
email_id = st.text_input("Email ID")
contact_details = st.text_input("Phone No.")

# # Remarks
# st.header("📝 Remarks")
# remarks = st.text_area("Any Remarks")

# Save in session
if st.button("Save & Continue"):
    st.session_state.invoice_data = {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "buyer_name": buyer_name,
        "buyer_address": buyer_address,
        "consignee_details": consignee_details,
        "consignee_address": consignee_address,
        "po_number": po_number,
        "po_date": po_date,
        "inco_terms": inco_terms,
        "payment_terms": payment_terms,
        "final_destination": final_destination,
        "final_discharge": final_discharge,
        "contact_person": contact_person,
        "email_id": email_id,
        "contact_details": contact_details,
        # "remarks": remarks,
    }
    st.success("✅ Details saved. Please go to the next page: *Product Selection*")
