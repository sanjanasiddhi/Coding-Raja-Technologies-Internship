import csv
from datetime import datetime

income = 0
expenses = []
categories = {}

def add_income():
    global income
    amount = float(input("Enter your total income amount: "))
    income += amount

def add_expense():
    global expenses, categories
    category = input("Please choose the valid category (Food, Medicals, Cloth, Rent, Entertainment): ").lower()
    if category not in categories:
        categories[category] = 0
    amount = float(input(f"Enter cost for {category}: "))
    if amount < 0:
        print("Enter the correct amount")
    else:
        timestamp = datetime.now().strftime('%Y-%m-%d')  
        expenses.append((timestamp, category, amount))
        categories[category] += amount

def analyze_spending_over_time():
    global expenses
    time_period = input("Enter the time period to analyze (weekly, monthly): ").lower()
    expenses_over_time = {}
    for _, category, amount in expenses:
        if category not in expenses_over_time:
            expenses_over_time[category] = {}
        
        if time_period == "weekly":
            time_key = datetime.strptime(_, '%Y-%m-%d').strftime('%Y-%W')
        elif time_period == "monthly":
            time_key = datetime.strptime(_, '%Y-%m-%d').strftime('%Y-%m')
        else:
            print("Invalid time period.")
            return
        
        if time_key not in expenses_over_time[category]:
            expenses_over_time[category][time_key] = 0
        
        expenses_over_time[category][time_key] += amount
    print(f"{'Category':<15} {'Time Period':<15} {'Total Spending':<15}")
    print("-" * 45)
    for category, data in expenses_over_time.items():
        for time_period, total_spending in data.items():
            print(f"{category:<15} {time_period:<15} ${total_spending:<15.2f}")
            
def view_expenses():
    global expenses, categories
    if not expenses:
        print("No expenses added yet.")
    else:
        print("Expenses by Category:")
        highest_expense_category = max(categories, key=categories.get)
        for category, amount in categories.items():
            print(f"\t- {category}: ${amount:.2f}")
        print(f"\nCategory with highest expenses: {highest_expense_category} (${categories[highest_expense_category]:.2f})")



def view_budget():
    global income, expenses
    total_expense_amount = sum(amount for _, _, amount in expenses)
    remaining_budget = income - total_expense_amount
    print("Budget Summary:")
    print(f"- Total Income: ${income:.2f}")
    print(f"- Total Expenses: ${total_expense_amount:.2f}")
    print(f"- Remaining Budget: ${remaining_budget:.2f}")


def save_data():
    global income, expenses
    with open("budget_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Income", income])
        writer.writerow(["Categories"])
        for category, amount in categories.items():
            writer.writerow([category, amount])
        writer.writerow(["Expenses"])
        writer.writerows(expenses)
    print("Budget data saved successfully to CSV!")

def load_data():
    global income, expenses, categories
    try:
        with open("budget_data.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            income = float(next(reader)[1])
            next(reader)  
            categories = {}
            
            for row in reader:
                if row[0] == "Expenses":
                    break
                categories[row[11
                               ]] = float(row[1])
                next(reader)
            expenses = list(next(reader))  
            expenses = [(category, float(amount)) for category, amount in zip(*expenses[1:])]
            print("Budget data loaded successfully from CSV!")
    except FileNotFoundError:
        print("No budget data found.")
    except (IOError, csv.Error) as e:
        print(f"Error loading budget data: {e}")

def main():
    while True:
        print("My Budget Tracker:")
        print("1. Add Total Income")
        print("2. Add Your Expenses")
        print("3. Analyze Spending Over Time")
        print("4. View Total Expenses")
        print("5. View Remaining Budget")
        print("6. Save and Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            analyze_spending_over_time()
        elif choice == "4":
            view_expenses()
        elif choice == "5":
            view_budget()
        elif choice == "6":
            save_data()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
