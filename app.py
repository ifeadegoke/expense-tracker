import streamlit as st 
import json
import os
from datetime import date

DATA_FILE = "expense.json"

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent= 4)


st.title("💰Expense Tracker & Decision Maker")
st.markdown("----")


expenses = load_expenses()


st.subheader("➕Add New Expense")


category = st.selectbox("Category", ["Food", "Transport", "Data", "Shopping", "Other"])
description = st.text_input("Description")
amount = st.number_input("Amount (#)", min_value=0.00, format="%.2f")

if st.button("Add Expense"):
    if description and amount > 0:
        new_expense = {
            "category" : category, 
            "description" : description,
            "amount":amount,
            "date": str(date.today())
        }
        expenses.append(new_expense)
        save_expenses(expenses)
        st.success("✅ Expense Added Sucessfully!")
    else:
        st.error("⚠️ Please Fill in Description and Amount")
        

st.markdown("----")
st.subheader("🗒️ Your Expenses")


if expenses:
    total = 0
    for i, e in enumerate(expenses, 1):
        col1, col2 = st.columns([5, 1])
    with col1:    
        expense_date = e.get('date', 'No date')
        st.write(f"{i}.**[{e['category']}]** {e['description']} - NGN{e['amount']:,.2f}  \n📅 {expense_date}")
    with col2:
        if st.button("🗑️", key = f"delete_{i}"):
            expenses.pop(i - 1)
            save_expenses(expenses)
            st.rerun()

    total += e['amount']


    st.markdown("----")
    st.metric("💸 Total Spent", f"#{total:,.1f}")


else:
    st.info("No expenses recorded yet!")


st.markdown("----")
st.subheader("🎯 Set Your Budget")

budget = st.number_input("Set Monthly Budget (NGN)", min_value=0.0, format="%.2f")


if budget > 0:
    total_spent = sum(e['amount'] for e in expenses)
    remaining = budget - total_spent
    percentage = (total_spent/budget) * 100


    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Budget", f"NGN{budget:,.2f}")
    with col2:
        st.metric("💸 Spent", f"NGN{total_spent:,.2f}")
    with col3:
        st.metric("🏦 Remaining", f"NGN{remaining:,.2f}")


    st.progress(min(percentage / 100, 1.0))


    if percentage >= 100:
        st.error("🚨 You have exceeded your budget!")
    elif percentage >= 80:
        st.warning('⚠️ You are close to your budget limit!')
    else:
        st.success("✅ You are within your budget!")


st.markdown("----")
st.subheader("🗑️ Clear Expense History ")

if 'confirm_clear' not in st.session_state:
    st.session_state.confirm_clear = False


if st.button("Clear All Expenses"):
    st.session_state.confirm_clear = True


if st.session_state.confirm_clear:
    st.warning("⚠️ Are you sure you want to delete all Expenses? ")

    col1, col2, = st.columns(2)

    with col1:
        if st.button("✅ Yes, Clear Everything"):
            save_expenses([])
            st.session_state.confirm_clear = False
            st.success("✅ All Expenses Cleared")
            st.rerun()

    with col2:
        if st.button("❌ No, Go Back"):
            st.session_state.confirm_clear = False
            st.rerun()
            