'''
AddressBook
│
└── data (dict)
    ├── "John" → Record
    │            ├── name → Name
    │            │            └── value = "John"
    │            ├── phones → [Phone, Phone]
    │            │            ├── value = "1234567890"
    │            │            └── value = "5555555555"
    │            └── birthday → Birthday or None
    │                           └── value = datetime(...)
    │
    └── "Jane" → Record
                 ├── name → Name
                 ├── phones → [Phone]
                 └── birthday → None

'''

from collections import UserDict
from datetime import datetime, timedelta

class Field:  
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value


class Name(Field):
    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        super().__init__(name)


class Phone(Field):
    def __init__(self, value):
        # delegate validation through the property setter
        # (Field doesn't know about phone-specific rules)
        self.value = value

    @property
    def value(self):
            return self.__value
        
    @value.setter
    def value(self, value):

        if not isinstance(value, str):
            raise ValueError("Phone number must be a string of 10 digits.")
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if len(value) != 10:
            raise ValueError("Phone number must be a string of 10 digits.")
            
        self.__value = value

class Birthday(Field):
    def __init__(self, value):
        
        if not isinstance(value, str):
            raise ValueError("Birthday must be a string in the format DD.MM.YYYY")
            
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        super().__init__(date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Phone number not found.")
    

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        raise ValueError("Phone number not found.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)



class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found.")

    def get_upcoming_birthdays(self):    
        today = datetime.today().date() 
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_this_year = record.birthday.value.replace(year=today.year) 

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_difference = (birthday_this_year - today).days
    
            if 0 <= days_difference <= 7:
                this_week_birthday = birthday_this_year
                if this_week_birthday.weekday() >= 5:  # If birthday falls on Saturday (5) or Sunday (6)
                    this_week_birthday += timedelta(days=(7 - this_week_birthday.weekday()))  # Move to next Monday

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": this_week_birthday.strftime("%d.%m.%Y") 
                })  
        return upcoming


        