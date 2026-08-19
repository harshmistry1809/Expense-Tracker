import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    description TEXT,
    amount REAL
)
""")
conn.commit()

print("===================================")
print("   Welcome to Expense Tracker")
print("===================================")

while True:
    print("\n------ MENU ------")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Total Expense")
    print("4. Delete Expense")
    print("5. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    # Add Expense
    if choice == 1:
        date = input("Enter Date (DD-MM-YYYY): ")
        category = input("Enter Category (Food/Travel/etc): ")
        description = input("Enter Description: ")

        try:
            amount = float(input("Enter Amount: "))
        except ValueError:
            print("Invalid amount.")
            continue

        cursor.execute(
            """
            INSERT INTO expenses(date, category, description, amount)
            VALUES (?, ?, ?, ?)
            """,
            (date, category, description, amount)
        )

        conn.commit()
        print("Expense Added Successfully!")

    # View All Expenses
    elif choice == 2:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        if not expenses:
            print("No expenses found.")
        else:
            print("\n-------------------------------")
            print("ID | Date | Category | Description | Amount")
            print("-------------------------------")

            for expense in expenses:
                print(
                    f"{expense[0]} | {expense[1]} | "
                    f"{expense[2]} | {expense[3]} | ₹{expense[4]}"
                )

    # View Total Expense
    elif choice == 3:
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0]

        if total is None:
            total = 0

        print(f"\nTotal Expense = ₹{total}")

    # Delete Expense
    elif choice == 4:
        expense_id = input("Enter Expense ID to delete: ")

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Expense Deleted Successfully!")
        else:
            print("Expense ID not found.")

    # Exit
    elif choice == 5:
        print("Thank you for using Expense Tracker!")
        conn.close()
        break

    else:
        print("Invalid Choice.")