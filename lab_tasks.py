def get_int_input(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid whole number.")


def calculate_grade(marks):
    if marks < 50:
        return "F"
    if marks <= 60:
        return "E"
    if marks <= 70:
        return "D"
    if marks <= 80:
        return "C"
    if marks <= 90:
        return "B"
    return "A"


def factorial(number):
    result = 1
    for i in range(2, number + 1):
        result *= i
    return result


def fibonacci_series(count):
    sequence = []
    a, b = 0, 1
    for _ in range(count):
        sequence.append(a)
        a, b = b, a + b
    return sequence


def task_student_grade_calculator():
    marks = get_int_input("Enter marks (1-100): ")
    if marks < 1 or marks > 100:
        print("Invalid marks. Please enter a value from 1 to 100.")
        return

    grade = calculate_grade(marks)
    print(f"Grade: {grade}")


def task_factorial_calculator():
    number = get_int_input("Enter a number to calculate factorial: ")
    if number < 0:
        print("Factorial is not defined for negative numbers.")
        return

    print(f"Factorial of {number} is {factorial(number)}")


def task_fibonacci_series():
    terms = get_int_input("Enter number of terms for Fibonacci series: ")
    if terms <= 0:
        print("Please enter a positive number of terms.")
        return

    sequence = fibonacci_series(terms)
    print("Fibonacci series:", ", ".join(str(item) for item in sequence))


def main():
    while True:
        print("\nLab Tasks Menu")
        print("1. Student Grade Calculator")
        print("2. Factorial Calculator")
        print("3. Fibonacci Series")
        print("0. Exit")

        choice = input("Choose a task (0-3): ").strip()

        if choice == "1":
            task_student_grade_calculator()
        elif choice == "2":
            task_factorial_calculator()
        elif choice == "3":
            task_fibonacci_series()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select from 0 to 3.")


if __name__ == "__main__":
    main()