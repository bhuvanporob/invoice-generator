import streamlit as st
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from io import BytesIO
from num2words import num2words
import pandas as pd

st.title("📅 Step 3: Generate & Download Invoice")

# Check previous steps
if "invoice_data" not in st.session_state or "products" not in st.session_state or len(st.session_state.products) == 0:
    st.warning("Please complete Step 1 and Step 2 before generating the invoice.")
    st.stop()

products = st.session_state.products
invoice = st.session_state.invoice_data

# --- Subtotal Calculation ---
subtotal = sum(p["amount"] for p in products)

# --- User Inputs for Final Adjustments ---
st.header("📊 Final Adjustments")

freight = st.number_input("Freight Charges", value=0.0, step=0.1)
round_off = st.number_input("Round Off on Sales (±)", value=0.0, step=0.1)
discount = st.number_input("Discount on Sales", value=0.0, step=0.1)

final_total = round(subtotal + freight + round_off - discount, 2)
amount_words = num2words(final_total, to='cardinal', lang='en_IN').upper() + " ONLY"

# --- Product Preview ---
st.subheader("📦 Product List Preview")
df = pd.DataFrame(products)
df.index = range(1, len(df) + 1)
st.dataframe(df[["product_name", "product_code", "hsn", "uom", "qty", "rate", "amount"]].style.format({
    "rate": "₹{:.2f}",
    "amount": "₹{:.2f}"
}))

# --- Generate Excel ---
if st.button("📄 Generate Invoice"):
    wb = load_workbook("sample invoice.xlsx")
    ws = wb.active

    # --- Replace Header Placeholders ---
    replacements = {
        "{invoice number}": invoice["invoice_number"],
        "{date}": invoice["invoice_date"].strftime("%d-%m-%Y"),
        "{Buyer name}": invoice["buyer_name"],
        "{Address}": invoice["buyer_address"],
        "{Consignee details}": invoice["consignee_details"],
        "{Consingee Address}": invoice["consignee_address"],
        "{INCO terms}": invoice["inco_terms"],
        "{Payment terms}": invoice["payment_terms"],
        "{PO no}": invoice["po_number"],
        "{PO date}": invoice["po_date"].strftime("%d-%m-%Y"),
        "{final destination}": invoice["final_destination"],
        "{final discharge}": invoice["final_discharge"],
        "{Contact person}": invoice["contact_person"],
        "{emailid}": invoice["email_id"],
        "{Contact details}": invoice["contact_details"],
        "{remarks}": invoice["remarks"]
    }

    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                for key, value in replacements.items():
                    if key in cell.value:
                        cell.value = cell.value.replace(key, str(value))

    # --- Insert Products ---
    start_row = None
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and "{product 1}" in cell.value:
                start_row = cell.row
                break
        if start_row:
            break

    if not start_row:
        st.error("Template does not contain product placeholder `{product 1}`.")
        st.stop()

    for idx, product in enumerate(products):
        sr = idx + 1
        row_num = start_row + idx * 2

        # Row 1: Product Name
        ws.insert_rows(row_num)
        ws.cell(row=row_num, column=1, value=sr)
        ws.merge_cells(start_row=row_num, start_column=2, end_row=row_num, end_column=6)
        ws.cell(row=row_num, column=2, value=product["product_name"])

        # Row 2: Product Code + HSN + other details
        ws.insert_rows(row_num + 1)
        desc = f'Product Code: {product["product_code"]}   HSN Code: {product["hsn"]}'
        ws.cell(row=row_num + 1, column=2, value=desc)
        ws.cell(row=row_num + 1, column=3, value=product["uom"])
        ws.cell(row=row_num + 1, column=4, value=product["qty"])
        ws.cell(row=row_num + 1, column=5, value=product["rate"])
        ws.cell(row=row_num + 1, column=6, value=product["amount"])

    # Remove the original placeholder row
    ws.delete_rows(start_row + len(products) * 2)

    # --- Replace Summary Fields ---
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                label = cell.value.upper()
                if "SUB -TOTAL" in label:
                    ws.cell(row=cell.row, column=cell.column + 1, value=subtotal)
                elif "FREIGHT" in label:
                    ws.cell(row=cell.row, column=cell.column + 1, value=freight)
                elif "ROUND OFF" in label:
                    ws.cell(row=cell.row, column=cell.column + 1, value=round_off)
                elif "DISCOUNT" in label:
                    ws.cell(row=cell.row, column=cell.column + 1, value=discount)
                elif "TOTAL AMOUNT" in label:
                    ws.cell(row=cell.row, column=cell.column + 1, value=final_total)

    # Replace {Amount in words}
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and "{Amount in words}" in cell.value:
                cell.value = cell.value.replace("{Amount in words}", amount_words)

    # --- Export Excel ---
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    st.success("✅ Invoice successfully generated!")

    st.download_button(
        label="📅 Download Invoice Excel",
        data=output,
        file_name=f"Invoice_{invoice['invoice_number']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
