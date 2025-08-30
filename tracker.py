import streamlit as st
import json
import os
from datetime import date
#defining categories and the file to store the data
categories = ["Food", "Transport", "Shopping", "Bills", "Fun", "Other"]
data_file = "my_expenses.json"

def load_expenses():
    """Load expenses from file"""
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    """Save expenses to file"""
    with open(data_file, 'w') as f:
        json.dump(expenses, f)

def add_expense(expenses, date_str, amount, category, description):
    """Add new expense"""
    expense = {
        'date': date_str,
        'amount': amount,
        'category': category,
        'description': description
    }
    expenses.append(expense)
    return expenses

def calculate_total(expenses):
    """Calculate total spending"""
    total = 0
    for expense in expenses:
        total += expense['amount']
    return total

def get_category_totals(expenses):
    """Calculate spending by category"""
    category_money = {}
    for expense in expenses:
        category = expense['category']
        if category in category_money:
            category_money[category] += expense['amount']
        else:
            category_money[category] = expense['amount']
    return category_money

def show_expenses_table(expenses):
    """Show expenses in a simple table"""
    if not expenses:
        st.write("No expenses yet!")
        return

    st.write("**Your Expenses:**")
    for i, expense in enumerate(expenses):
        st.write(f"{i+1}. {expense['date']} - {expense['description']} - ₹{expense['amount']} ({expense['category']})")

def main():
    st.title("💰 My Expense Tracker")
    st.write("Keep track of your daily expenses!")

    # Load expenses are retrived here
    expenses = load_expenses()

    # Sidebar menu
    st.sidebar.header("Menu")
    page = st.sidebar.selectbox("Choose:", ["Add Expense", "View Expenses", "Summary"])

    # Adding Expense Page
    if page == "Add Expense":
        st.header("➕ Add New Expense")

        # giving input form
        expense_date = st.date_input("Date:", value=date.today())
        amount = st.number_input("Amount (₹):", min_value=1, value=100)
        category = st.selectbox("Category:", categories)
        description = st.text_input("What did you buy?", placeholder="e.g., Lunch, Bus ticket")

        # Add button
        if st.button("Add Expense"):
            if description:
                expenses = add_expense(expenses, str(expense_date), amount, category, description)
                save_expenses(expenses)
                st.success(f"Added ₹{amount} for {description}!")
                st.balloons()
            else:
                st.error("Please write what you bought!")

    # Creating Expenses Page to view
    elif page == "View Expenses":
        st.header("📋 All Expenses")

        if expenses:
            # Show total first
            total = calculate_total(expenses)
            st.metric("Total Spent", f"₹{total}")

            # Filter by category
            selected_category = st.selectbox("Filter by category:", ["All"] + categories)

            # Show filtered expenses
            if selected_category == "All":
                show_expenses_table(expenses)
            else:
                filtered = [exp for exp in expenses if exp['category'] == selected_category]
                show_expenses_table(filtered)

            # Code for deleting last expense 
            if st.button("🗑️ Delete Last Expense"):
                if expenses:
                    deleted = expenses.pop()
                    save_expenses(expenses)
                    st.success(f"Deleted: {deleted['description']}")
                    st.experimental_rerun()
        else:
            st.info("No expenses yet. Add some expenses first!")

    # Everything is summarized here  
    elif page == "Summary":
        st.header("📊 Spending Summary")

        if expenses:
            # Basic stats
            total_spent = calculate_total(expenses)
            num_expenses = len(expenses)
            average = total_spent / num_expenses if num_expenses > 0 else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("Total", f"₹{total_spent}")
            col2.metric("Count", num_expenses)
            col3.metric("Average", f"₹{average:.0f}")

            # Category breakdown
            st.subheader("💳 Spending by Category")
            category_totals = get_category_totals(expenses)

            for category, amount in category_totals.items():
                percentage = (amount / total_spent) * 100
                st.write(f"**{category}:** ₹{amount} ({percentage:.1f}%)")
                st.progress(percentage / 100)

            # for showing recent expenses
            st.subheader("🕐 Recent Expenses")
            recent = expenses[-5:]  # Last 5 expenses
            for expense in reversed(recent):
                st.write(f"• {expense['date']} - {expense['description']} - ₹{expense['amount']}")

        else:
            st.info("Add some expenses first to see summary!")

    # Shows quick stats here in slidebar
    if expenses:
        st.sidebar.markdown("---")
        st.sidebar.write("**Quick Stats:**")
        st.sidebar.write(f"Total: ₹{calculate_total(expenses)}")
        st.sidebar.write(f"Expenses: {len(expenses)}")

        # Defining code that will find the most expensive expense of user
        max_expense = max(expenses, key=lambda x: x['amount'])
        st.sidebar.write(f"Biggest: ₹{max_expense['amount']}")

if __name__ == "__main__":
    main()
