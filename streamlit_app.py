import streamlit as st

st.set_page_config(page_title="Invoice Generator", layout="centered")

st.title("🧾 Invoice Generator Web App")

st.markdown("""
Welcome to the **Invoice Generator App**!  
This tool helps you create professional Excel-based invoices using a predefined template.

---

### 🔄 Workflow

1. **Step 1: Enter Invoice Details**  
   Fill out billing and shipping information, PO numbers, payment terms, etc.

2. **Step 2: Select Products**  
   Choose products from a dropdown (with auto-filled HSN, price, and UOM), and enter quantities.

3. **Step 3: Review & Download Invoice**  
   Preview your invoice details and download the final Excel file, fully formatted and ready to send.

---

### 🚀 Get Started

Use the **navigation menu on the left** to begin with **Step 1: Invoice Details**.

You can come back to this screen any time.

""")
