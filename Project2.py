dic = {}
def add_student(dic):
        roll=int(input("Enter roll Number:"))
        name=input("Enter name:")
        com = int(input("Enter Computer Marks:"))
        phy = int(input("Enter Physics Marks:"))
        chem = int(input("Enter Chemistry Marks:"))
        lis = [com,phy,chem]
        dic[roll] = {
              "Name":name,
              "Marks":lis
        }

def  Report_Card(dic):
      roll = int(input("Enter roll number:"))
      try:
            if roll in dic.keys():
                  print("Roll number Exist's😊")
                  avg = sum(dic[roll]['Marks']) / 3
                  grade = ("A" if avg >= 80 else
                  "B" if avg >=70 else 
                  "C" if avg >=60 else
                  "D" if avg >=50 else 
                  "F")
            print("-----Report Card-----")
            print(f"Name:{dic[roll]['Name']}")
            print(f"Roll Number:{roll}")
            print(f"Average:{avg:.2f}")
            print(f"Grade:{grade}")
            print("--------😊😊--------")

      except:
           print("Sorry, Roll-Number could not be found.")
def Show_All(dic):
      for roll,info in dic.items():
            print(f"{roll} ---> {info}")

while True:
    print("-----Welcome to Student Management System-----")
    print("1-Add Student")
    print("2-Student Result Card")
    print("3-Show Results of all")
    opt = int(input())
    if opt == 1:
          add_student(dic)
          print(dic)
    elif opt == 2:
          Report_Card(dic)
    elif opt == 3:
          Show_All(dic)
    else:
          print("Sorry somrthing is wrong!")
        
