print("Welcome to the Daily Expense Tracker!")

print("\nMenu:")
print("1. Add a new expense")
print("2. View all expenses")
print("3. Calculate total and average expense")
print("4. Clear all expenses")
print("5. Exit")

lst = []

while True:
    choice = input()

    if choice == "5":
        print("Exiting the Daily Expense Tracker. Goodbye!")
        break
    elif choice == "1":
        num = float(input())
        lst.append(num)
        print("Expense added successfully!")
    elif choice == "2":
        if len(lst) == 0:
            print("No expenses recorded yet.")
        else:
            print("Your expenses:")
            for i in range(len(lst)):
                print(f"{i+1}. {lst[i]}")
    elif choice == "3":
        if len(lst) == 0:
            print("No expenses recorded yet.")
        else:
            total = sum(lst)
            avg = total/len(lst)
            print(f"Total expense: {total}")
            print(f"Average expense: {avg}")
    elif choice == "4":
        lst.clear()
        print("All expenses cleared.")
    else:
        print("Invalid choice. Please try again.")