marks = int(input("Enter marks (1-100): "))

if marks < 50:
    print("Grade F")
elif 50 <= marks <= 60:
    print("Grade E")
elif 61 <= marks <= 70:
    print("Grade D")
elif 71 <= marks <= 80:
    print("Grade C")
elif 81 <= marks <= 90:
    print("Grade B")
elif 91 <= marks <= 100:
    print("Grade A")
else:
    print("Invalid input")