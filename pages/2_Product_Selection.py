import streamlit as st
import pandas as pd

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🚫 You must log in to view this page.")
    st.stop()


st.write(f"Hello, {st.session_state['username']}! You have access to this secure page.")

st.title("📦 Step 2: Select Products")

# Load product list from file (do only once)
@st.cache_data
def load_products():
    df = pd.read_excel("product list.xlsx")
    df.columns = df.columns.str.lower().str.strip()
    df.fillna("", inplace=True)
    return df

product_df = load_products()

# Ensure required columns are present
required_cols = {"product name", "product code", "hsn code", "uom", "price"}
if not required_cols.issubset(set(product_df.columns)):
    st.error("❌ 'product list.xlsx' must contain columns: Product Name, Product Code, HSN Code, UOM, Price")
    st.stop()

# Initialize session state list for added products
if "products" not in st.session_state:
    st.session_state.products = []

with st.form("add_product_form"):
    st.subheader("➕ Add Product")

    product_names = product_df["product name"].tolist()
    selected_name = st.selectbox("Select Product Name", product_names)

    if selected_name:
        product_row = product_df[product_df["product name"] == selected_name].iloc[0]
        product_code = product_row["product code"]
        hsn = product_row["hsn code"]
        uom = product_row["uom"] or "UNITS"
        rate = float(product_row["price"])
    else:
        st.stop()

    col1, col2 = st.columns(2)
    with col1:
        qty = st.number_input("Quantity", min_value=0.0, step=1.0)
    with col2:
        st.markdown(f"**Rate:** ${rate:.2f}")

    submitted = st.form_submit_button("✅ Add to Invoice")

    if submitted and qty > 0:
        amount = round(qty * rate, 2)
        st.session_state.products.append({
            "product_name": selected_name,
            "product_code": product_code,
            "hsn": hsn,
            "uom": uom,
            "qty": qty,
            "rate": rate,
            "amount": amount
        })
        st.success(f"Added {selected_name} (Qty: {qty}) to invoice.")
    elif submitted:
        st.error("Quantity must be greater than 0.")

# --- Show Added Products ---
if st.session_state.products:
    st.subheader("🧾 Products Added")
    df = pd.DataFrame(st.session_state.products)
    st.dataframe(df[["product_name", "product_code", "hsn", "uom", "qty", "rate", "amount"]].style.format({
        "rate": "${:.2f}",
        "amount": "${:.2f}"
    }))
