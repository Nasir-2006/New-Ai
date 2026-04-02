print("----------Bismillah----------")
name = input("Please Enter Name: ")
city = input("Please Enter City Name: ")
print(f"Hello {name.strip().title()} From {city.title()}")
nick = (name.strip()[0:3]+city[-1].lower())
print(nick.lower())
items = input("Enter List Items with(-):")
new_Item = items.replace("-"," ")
clean = new_Item.split(" ")
try:
    bil = int(input("Enter total Bill:"))
    total = bil*0.90
    print(f"Total is {total:.2f}")
except:
    print("Enter Correct Bill:")

print("------CUSTOMER RECEIPT------")
print(f"CUSTUMER NAME:   {name.title()}")
print(f"CUSTOMER ID:     {nick}")
print(f"Purchased Item:  {', '.join(clean).upper()}")
print("----------------------------------------")
print(f"Total Bill (with 10% Discount): {total}")
print("----------------------------------------")
