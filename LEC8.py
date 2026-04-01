

# 1. ARITHMETIC OPERATORS
# Used to perform mathematical calculations
a = 15
b = 4

print("--- Arithmetic Operators ---")
print("Addition (+):", a + b)           # Adds two operands
print("Subtraction (-):", a - b)        # Subtracts right operand from left
print("Multiplication (*):", a * b)     # Multiplies two operands
print("Division (/):", a / b)           # Returns a float result (3.75)
print("Modulus (%):", a % b)            # Returns the remainder (3)
print("Floor Division (//):", a // b)   # Returns the quotient as integer (3)
print("Exponentiation (**):", a ** b)   # Performs 'a' to the power of 'b' (15^4)

# 2. COMPARISON OPERATORS
# Used to compare two values; always returns a Boolean (True/False)
x = 10
y = 20

print("\n--- Comparison Operators ---")
print("Equal to (==):", x == y)         # True if values are equal
print("Not equal to (!=):", x != y)     # True if values are not equal
print("Less than (<):", x < y)          # True if left is smaller than right
print("Greater than (>):", x > y)       # True if left is larger than right
print("Less than or equal (<=):", x <= 10) # True if left is smaller or equal
print("Greater than or equal (>=):", y >= 30) # True if left is larger or equal

# 3. LOGICAL OPERATORS
# Used to combine conditional statements
is_student = True
has_passed = False

print("\n--- Logical Operators ---")
# 'and' returns True only if BOTH statements are true
print("Logical AND:", is_student and has_passed) 

# 'or' returns True if at least ONE statement is true
print("Logical OR:", is_student or has_passed)

# 'not' reverses the result (True becomes False and vice versa)
print("Logical NOT:", not is_student)