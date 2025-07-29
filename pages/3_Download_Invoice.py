import streamlit as st
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.pagebreak import Break
from io import BytesIO
from num2words import num2words
import pandas as pd
from openpyxl.styles import Font, Border, Side

bold_font = Font(name="Arial", bold=True)
italic_font = Font(name="Calibri", italic=True)
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
thin_border_lower = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    bottom=Side(style='thin')
)


st.title("Step 3: Generate & Download Invoice")

# Check previous steps
if "invoice_data" not in st.session_state or "products" not in st.session_state or len(st.session_state.products) == 0:
    st.warning("Please complete Step 1 and Step 2 before generating the invoice.")
    st.stop()

products = st.session_state.products
invoice = st.session_state.invoice_data

# --- Subtotal Calculation ---
subtotal = sum(p["amount"] for p in products)

# --- User Inputs for Final Adjustments ---
st.header("Final Adjustments")

freight = st.number_input("Freight Charges", value=0.0, step=0.1)
round_off = round(subtotal, 0)
discount = st.number_input("Discount on Sales", value=0.0, step=0.1)

final_total = round(freight + round_off - discount,0)
amount_words = num2words(final_total, to='cardinal', lang='en_IN').upper() + " ONLY"

# --- Product Preview ---
st.subheader("Product List Preview")
df = pd.DataFrame(products)
df.index = range(1, len(df) + 1)
st.dataframe(df[["product_name", "product_code", "hsn", "uom", "qty", "rate", "amount"]].style.format({
    "rate": "₹{:.2f}",
    "amount": "₹{:.2f}"
}))

# --- Generate Excel ---
if st.button("Generate Invoice"):
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
        # "{remarks}": invoice["remarks"]
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

        # Insert two new rows for each product
        ws.insert_rows(row_num)
        ws.insert_rows(row_num + 1)

        # Row 1: Sr. No, UOM, QTY, Rate, Amount — Bold + Border
        for col, val in zip([2, 4, 5, 6, 7], [sr, product["uom"], product["qty"], product["rate"], product["amount"]]):
            cell = ws.cell(row=row_num, column=col, value=val)
            cell.font = bold_font
            cell.border = thin_border

        # Row 2: Product Code & HSN — Italics + Border
        desc = f'Product Code: {product["product_code"]}   HSN Code: {product["hsn"]}'
        desc_cell = ws.cell(row=row_num + 1, column=3, value=desc)
        desc_cell.font = italic_font
        desc_cell.border = thin_border

        # Also apply border to the rest of the merged columns in row_num + 1
        for col in [2, 4, 5, 6, 7]:
            cell = ws.cell(row=row_num + 1, column=col)
            cell.border = thin_border_lower

        # Product name in Row 1, Column 3 (Product Description)
        name_cell = ws.cell(row=row_num, column=3, value=product["product_name"])
        # name_cell.font = Font(name="Arial",bold=True)  # Bold
        # name_cell.border = thin_border

        # Description in Row 2, Column 3
        desc = f'Product Code: {product["product_code"]}   HSN Code: {product["hsn"]}'
        desc_cell = ws.cell(row=row_num + 1, column=3, value=desc)
        # desc_cell.font = Font(name="Calibri", italic=True)  # Italic and border
        # desc_cell.border = thin_border

        # Merge Sr. No, UOM, QTY, Rate, Amount across the two rows
        for col in [2, 4, 5, 6, 7]:  # Adjusted to match correct column indexes (B-G)
            ws.merge_cells(start_row=row_num, start_column=col, end_row=row_num + 1, end_column=col)

        # Fill merged values in top row (columns B-G = 2-7)
        # Sr. No
        cell = ws.cell(row=row_num, column=2, value=sr)
        # cell.font = bold_font
        # cell.border = thin_border

        # UOM
        cell = ws.cell(row=row_num, column=4, value=product["uom"])
        # cell.font = bold_font
        # cell.border = thin_border

        # QTY
        cell = ws.cell(row=row_num, column=5, value=product["qty"])
        # cell.font = bold_font
        # cell.border = thin_border

        # Rate
        cell = ws.cell(row=row_num, column=6, value=product["rate"])
        # cell.font = bold_font
        # cell.border = thin_border

        # Amount
        cell = ws.cell(row=row_num, column=7, value=product["amount"])
        # cell.font = bold_font
        # cell.border = thin_border

    # Remove the original placeholder row
    ws.delete_rows(start_row + len(products) * 2)

    # --- Adjust Page Break Based on Product Count ---
    base_page_break = 40
    product_rows = len(products) * 2
    new_page_break = base_page_break + product_rows

    ws.row_breaks.append(Break(id=new_page_break))

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

    st.success("Invoice successfully generated!")

    st.download_button(
        label="Download Invoice Excel",
        data=output,
        file_name=f"Invoice_{invoice['invoice_number']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
