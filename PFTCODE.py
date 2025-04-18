import csv
import datetime

# File to store transactions
FILENAME = "finance_tracker.csv"

# Initialize the file 
def initialize_file():
    try:
        with open(FILENAME, mode="x", newline="") as file:
            writer = csv.writer(file)
            # Write headers
            writer.writerow(["Date", "Type", "Category", "Amount", "Description"])
    except FileExistsError:
        pass  # File already exists

# Add a transaction
def add_transaction():
    transaction_type = input("Enter type (Income/Expense): ").strip().title()
    if transaction_type not in ["Income", "Expense"]:
        print("Invalid type. Please enter 'Income' or 'Expense'")
        return

    category = input("Enter category (e.g., Food, Rent, Salary etc...): ").strip()
    try:
        amount = float(input("Enter amount (in RS): "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    description = input("Enter description (optional): ").strip()
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not date:
        date = datetime.date.today().isoformat()
    else:
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")
            return

    # Save transaction to file
    with open(FILENAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, transaction_type, category, amount, description])

    print("Transaction added successfully!")

# View transactions
def view_transactions():
    print("\nTransactions:")
    print(f"{'Date':<12}{'Type':<16}{'Category':<15}{'Amount':<12}{'Description'}")
    print("-" * 60)
    try:
        with open(FILENAME, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"{row['Date']:<12}{row['Type']:<16}{row['Category']:<15}RS{float(row['Amount']):<10.2f}{row['Description']}")
    except FileNotFoundError:
        print("No transactions found. Add some first.")

# Summarize by category and calculate remaining balance
def summarize_by_category():
    categories = {}
    total_income = 0
    total_expenses = 0

    try:
        with open(FILENAME, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = row["Category"]
                amount = float(row["Amount"])
                if row["Type"] == "Income":
                    total_income += amount
                elif row["Type"] == "Expense":
                    total_expenses += amount
                    amount = -amount
                categories[category] = categories.get(category, 0) + amount

        print("\nCategory Summary:")
        for category, total in categories.items():
            print(f"{category}: RS{total:.2f}")

        # Remaining balance
        remaining_balance = total_income - total_expenses
        print("\nTotal Income: RS{:.2f}".format(total_income))
        print("Total Expenses: RS{:.2f}".format(total_expenses))
        print("Remaining Balance: RS{:.2f}".format(remaining_balance))
    except FileNotFoundError:
        print("No transactions found. Add some first.")

# Main menu
def main():
    initialize_file()
    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Summarize by Category")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            summarize_by_category()
        elif choice == "4":
            print("Thank you for using the finance tracker!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ =='__main__':
  main()