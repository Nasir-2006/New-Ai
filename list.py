# # Q1
# dost = ["Ali", "Saad", "Hassan", "Usman", "Bilal"]
# print(dost[0],dost[-1])
# # Q2
# numbers = [10, 20, 30]
# numbers.append(40)
# print(numbers)
# numbers.remove(40)
# print(numbers)
# # Q3
# alphabets = ['A', 'B', 'C', 'D', 'E']
# alphabets[2] = 'Z'
# print(alphabets[1 : 4])
# # Q4
# ginti = [1, 2, 4, 5]
# ginti.insert(2, 3)
# print(ginti)
# # Q5
# items = ["Apple", "Banana", "Cherry", "Date"]
# items[0],items[-1] = items[-1],items[0]
# print(items)
# # var = items.pop(2)
# # print(var)
# ----------------------------------------------------
# list = []
# print("Enter your 3 favourite Movies Name:")
# for i in range(3):
#     movie=input(str())
#     list.append(movie)
# print(list)
# ----------------------------------------------------
# list = [1,2,3,2,1]
# if list == list[::-1]:
#     print("Palindrom List")
# else:
#     print("No it is Not")
# -----------------------------------------------------
list = ["C","A","A","D"]
print(list.count("A"))
list.sort()
print(list)