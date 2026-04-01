#Task 1
# dost = { "Nasir":"Mango",
#     "Ehtisham" :  "Cherry",
#     "Asdaq":"Guavava",
#     "Sadain":"Apple",
#     "Mubasher":"Watermelon"
# }
# print(dost.keys())
# print("--------------------")
# print(dost.values())
# print("---------------------")
# print(dost.items())
# Task2
dic = {
    "Chair":"Kursi",
    "Water":"Pani",
    "Air":"Hawa",
    "Lake":"Jheel",
    "Airplane":"Jahaz"
}
print("Enter English word:(Chair,Water,Air,Lake,Airplane)")
name = input()
tran = dic.get(name)
if tran:
    print(f"{name} ka matlab he {tran} ")
else:
    print("No Translation available")
