import json
import os


DATA_FILE = "expense.json"

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent= 4)


def add_expense(expenses):
    category = input("category (food/transport/data/other): ").strip().lower()
    description = input("Description: ").strip()
    amount = float(input('Amount (#): '))

    expense = {
        "category": category,
        "description": description, 
        "amount" : amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense saved! \n")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet \n")
        return
    print("\n ------ YOUR EXPENSES------")
    total = 0
    for i, e in enumerate(expenses, 1):
        print(f"{i}. [{e['category']}] {e['description']} - #{e['amount']:,.2f}")
        total += e['amount']
    print(f"\nTOTAL SPENT: #{total:,.2f}\n")


def main():
    expenses = load_expenses()

    while True: 
        print("   EXPENSE TRACKER   ")
        print("1. Add Expenses")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("choose an option; ").strip()

        if choice =="1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            print(" Have a Nice Day")
            break
        else:
            print("Invalid option, try again.\n")


main()