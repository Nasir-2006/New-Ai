dic = {"Apple": "Seeb"}
while True:
    print("-----Dictionary project-----")
    print("1-Word Add karna\n2-Word remove karna\n3-Word Update karna\n4-Exit\n5-View Dictionary")
    try:
        num = int(input("Enter your option: (1,2,3,4,5)\n"))
    except ValueError:
        print("Please enter option between 1-5")
    
    if num == 1 :
        
        print('Pass')
        word = input("Enter English Word:")
        trans = input("Enter Urdu of Word:")
        

        dic[word] = trans
        print(f"-----{word} and meaning {trans} Added Successfully🎆-----")
        
    elif num == 2:
        
        print("Pass")
        word = input("Enter English Word😁:")
        if word in dic:
            dic.pop(word)
            print("Congrgulation word Founded😍")
            print(f"-----{word} Removed Successfully!🎆-----")
        else:
            print("Word is not in DICTIONARY😒")
        
        
    elif num == 3:
        
        print("Pass")
        word = input("Enter English word to be updated:")
        if word in dic:
            print("Word already Exists!")
        trans = input("Enter new meaning:")
        dic[word] = trans
        print(dic)
    elif num == 4:
        break
    elif num == 5:
        print("----------")
        for word,meaning in dic.items():
            print(f"{word} --> {meaning}")

        print("----------")