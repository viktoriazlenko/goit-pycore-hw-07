'''
This is a simple assistant bot that can manage contacts. 
 It allows you to add, change, and show contacts, as well as exit the program.
 The bot recognizes the following commands:
 - "hello": The bot will greet you and ask how it can help you.
 - "add [name] [phone]": The bot will add a new contact with the provided name and phone number.
 - "change [name] [phone]": The bot will update the phone number of an existing contact with the provided name.
 - "phone [name]": The bot will show the phone number of the contact with the provided name.
 - "all": The bot will show all contacts in the contact list.
 - "close" or "exit": The bot will say goodbye and exit the program.
''' 
 
from main_classes import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            if func.__name__ in ["add_contact", "change_username_phone"]:
                return "Give me name and phone please."
            return "Invalid input."
        except KeyError:
            return "Contact not found."
        except IndexError:
            if func.__name__ == "show_phone":
                return "Give me user name please."
            return "Invalid input."

    return inner


def say_hello(args, book): #The function takes a list of arguments and a dictionary of contacts, and simply returns a greeting message asking how the bot can help the user.
    return "How can I help you?"

def parse_input(user_input): #The function takes a user input string, splits it into a command and its arguments, and returns the command in lowercase along with the arguments as a list.
    parts = user_input.split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.strip().lower(), args

@input_error 
def add_contact(args, book):   #The function takes a list of arguments and a dictionary of contacts, tries to add a new contact to the dictionary using the provided name and phone number, and returns a message indicating whether the contact was added successfully, if the contact already exists, or if there was an error with the input.
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error 
def change_username_phone(args, book):  #The function takes a list of arguments and a dictionary of contacts, tries to update the phone number of an existing contact in the dictionary using the provided name and new phone number, and returns a message indicating whether the contact was updated successfully or if there was an error with the input.
    name, old_phone, new_phone = args
    record = book.find(name)

    if record is None:
        raise KeyError("Contact not found.")

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book): #The function takes a list of arguments and a dictionary of contacts, tries to retrieve the phone number of a contact from the dictionary using the provided name, and returns the phone number if the contact is found or a message indicating that the contact was not found if it is not in the dictionary.
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    return "; ".join(phone.value for phone in record.phones)

@input_error
def show_all(args, book): #The function takes a list of arguments and a dictionary of contacts, checks if there are any contacts in the dictionary, and returns a formatted string of all contacts and their phone numbers if there are any, or a message indicating that no contacts were found if the dictionary is empty.
    if book:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "No contacts found."
    
@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    return str(record.birthday) if record.birthday else "No birthday set."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()

    if upcoming:
        return "Upcoming birthdays:\n" + "\n".join(f"{record['name']}: {record['congratulation_date']}"for record in upcoming)
    else:        
        return "No upcoming birthdays found."
    


def main():
    book = AddressBook()
    commands = {
        "hello": say_hello,
        "add": add_contact,
        "change": change_username_phone,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays
        
    }


    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command == "":
            continue

        elif command in ["close", "exit"]:
            print("Good bye!")
            break

        handler = commands.get(command)

        if handler: 
            print(handler(args, book))
        
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()




