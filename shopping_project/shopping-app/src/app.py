"""Streamlit app for the shopping app.

Run with:
    streamlit run src/app.py
"""
import streamlit as st
from src.utils.database import get_connection
import sqlite3
import subprocess
from pathlib import Path


def get_products():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_product(name, description, price, stock):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
        (name, description, price, stock),
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def create_order(product_id, user_id, quantity, total_price):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO orders (product_id, user_id, quantity, total_price) VALUES (?, ?, ?, ?)",
        (product_id, user_id, quantity, total_price),
    )
    conn.commit()
    oid = cur.lastrowid
    conn.close()
    return oid


def add_review(product_id, user_name, rating, comment):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO reviews (product_id, user_name, rating, comment) VALUES (?, ?, ?, ?)",
        (product_id, user_name, rating, comment),
    )
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid


def main():
    st.title("Shopping App (Streamlit)")

    st.header("Products")
    try:
        products = get_products()
    except sqlite3.DatabaseError as e:
        st.error("SQLite error: file is not a database or database is corrupted.")
        st.code(str(e))
        st.write("Close any editors or DB viewers that have `data/store.db` open, then recreate the DB.")
        if st.button("Recreate DB from schema"):
            # run the initializer script using the current Python executable and force overwrite
            # `parents[1]` is the shopping-app folder (one level up from src)
            script = Path(__file__).resolve().parents[1] / "create_store_db.py"
            try:
                import sys
                res = subprocess.run([sys.executable, str(script), "--force"], capture_output=True, text=True)
                if res.returncode == 0:
                    st.success("Recreated DB successfully — reload the app")
                else:
                    st.error("Failed to recreate DB")
                    st.text(res.stdout)
                    st.text(res.stderr)
            except Exception as ex:
                st.exception(ex)
        return

    if products:
        st.table(products)
    else:
        st.write("No products yet.")

    with st.expander("Add product"):
        name = st.text_input("Name")
        description = st.text_area("Description")
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        stock = st.number_input("Stock", min_value=0, format="%d")
        if st.button("Add product"):
            pid = add_product(name, description, price, stock)
            st.success(f"Product added with id {pid}")

    st.header("Create order")
    if products:
        product_options = {p['id']: p for p in products}
        selected = st.selectbox("Select product", options=list(product_options.keys()), format_func=lambda x: f"{product_options[x]['name']} (id {x})")
        qty = st.number_input("Quantity", min_value=1, value=1)
        user_id = st.number_input("User id", min_value=1, value=1)
        total = product_options[selected]['price'] * qty
        st.write(f"Total: {total:.2f}")
        if st.button("Place order"):
            oid = create_order(selected, user_id, qty, total)
            st.success(f"Order created: {oid}")
    else:
        st.write("Add a product first to place orders.")

    st.header("Add review")
    if products:
        r_product = st.selectbox("Product for review", options=list(product_options.keys()), format_func=lambda x: f"{product_options[x]['name']} (id {x})", key="rprod")
        user_name = st.text_input("Your name", key="rname")
        rating = st.slider("Rating", min_value=1, max_value=5, value=5)
        comment = st.text_area("Comment", key="rcomment")
        if st.button("Submit review"):
            rid = add_review(r_product, user_name, rating, comment)
            st.success(f"Review submitted: {rid}")
    else:
        st.write("Add a product first to leave reviews.")


if __name__ == "__main__":
    main()