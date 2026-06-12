def display_menu():
    print("Contact Book Menu:")
    print("1. Add Contact")
    print("2. View Contact")
    print("3. Edit Contact")
    print("4. Delete Contact")
    print("5. List All Contacts")
    print("6. Exit")
    num = int(input())
    return num

def add_contact(contact_book):
    name = input() 
    
    if name in contact_book:
        print("Contact already exists!")
        return
    else:
        phone = input()
        email = input()
        address = input()
        contact_book[name] = {
            "phone": phone,
            "email": email,
            "address": address
        }
        print("Contact added successfully!")
    
def view_contact(contact_book):
        name = input()
        if name not in contact_book:
            print("Contact not found!")
        else:
            print(f"Name: {name}")
            print(f"Phone: {contact_book[name]['phone']}")
            print(f"Email: {contact_book[name]['email']}")
            print(f"Address: {contact_book[name]['address']}")
def edit_contact(contact_book):
    name = input()
    if name not in contact_book:
        print("Contact not found!")
    else:
        phone = input()
        email = input()
        address = input()
        if phone != '':
            contact_book[name]['phone'] = phone
            
        if email != '':
            contact_book[name]['email'] = email
            
        if address != '':
            contact_book[name]['address'] = address
        print("Contact updated successfully!")
def delete_contact(contact_book):
    name = input()
    if name in contact_book:
        del contact_book[name]
        print("Contact deleted successfully!")
    else:
        print("Contact not found!")
def list_all_contacts(contact_book):
    if len(contact_book)==0:
        print("No contacts available.")
    else:
        for name,info in contact_book.items():
            print(f"Name: {name}")
            print(f"Phone: {info.get('phone')}")
            print(f"Email: {info.get('email')}")
            print(f"Address: {info.get('address')}")
            print("")

contact_book = {}
while(True):
    choice = int(display_menu())
    if choice == 1:
        add_contact(contact_book)
    elif choice == 2:
        view_contact(contact_book)
    elif choice == 3:
        edit_contact(contact_book)
    elif choice == 4:
        delete_contact(contact_book)
    elif choice == 5:
        list_all_contacts(contact_book)
    elif choice == 6:
        break
    else:
        print("Invalid choice.Please try again.")