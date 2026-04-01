print("Enter num1:")
num1= float(input())
print("Enter num2:")
num2 = float(input())
print("Enter operation:(+,-,*,/)")
op = input()
if op == '+':
    print(f"Sum is {num1+num2}")
elif op == '-':
    print("sub is "+num1-num2)
elif op == '*':
    print("Mul is "+num1*num2)
elif op == '/':
    print("Div is "+num1/num2)
else:
    print("Wrong Entry check again")