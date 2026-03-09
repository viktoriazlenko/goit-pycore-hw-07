from main import (
    add_contact,
    change_username_phone,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)
from main_classes import AddressBook
from datetime import datetime, timedelta

book = AddressBook()

print(add_contact(["John", "1234567890"], book))
print(add_contact(["John", "5555555555"], book))
print(show_phone(["John"], book))

print(change_username_phone(["John", "1234567890", "1112223333"], book))
print(show_phone(["John"], book))

print(add_birthday(["John", (datetime.today() + timedelta(days=2)).strftime("%d.%m.%Y")], book))
print(show_birthday(["John"], book))

print(show_all([], book))
print(birthdays([], book))