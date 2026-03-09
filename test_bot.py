import unittest
from datetime import datetime, timedelta

from main import (
    add_contact,
    change_username_phone,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)
from main_classes import AddressBook, Record, Name, Phone, Birthday


class TestFields(unittest.TestCase):
    def test_name_valid(self):
        name = Name("John")
        self.assertEqual(name.value, "John")

    def test_name_invalid_empty(self):
        with self.assertRaises(ValueError):
            Name("")

    def test_phone_valid(self):
        phone = Phone("1234567890")
        self.assertEqual(phone.value, "1234567890")

    def test_phone_invalid_letters(self):
        with self.assertRaises(ValueError):
            Phone("12345abcde")

    def test_phone_invalid_length(self):
        with self.assertRaises(ValueError):
            Phone("12345")

    def test_birthday_valid(self):
        birthday = Birthday("15.08.1990")
        self.assertEqual(str(birthday), "15.08.1990")

    def test_birthday_invalid_format(self):
        with self.assertRaises(ValueError):
            Birthday("1990-08-15")


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")

    def test_add_phone(self):
        self.record.add_phone("1234567890")
        self.assertEqual(len(self.record.phones), 1)
        self.assertEqual(self.record.phones[0].value, "1234567890")

    def test_remove_phone(self):
        self.record.add_phone("1234567890")
        self.record.remove_phone("1234567890")
        self.assertEqual(len(self.record.phones), 0)

    def test_edit_phone(self):
        self.record.add_phone("1234567890")
        self.record.edit_phone("1234567890", "1112223333")
        self.assertEqual(self.record.phones[0].value, "1112223333")

    def test_edit_phone_not_found(self):
        with self.assertRaises(ValueError):
            self.record.edit_phone("0000000000", "1112223333")

    def test_find_phone(self):
        self.record.add_phone("1234567890")
        result = self.record.find_phone("1234567890")
        self.assertEqual(result, "1234567890")

    def test_find_phone_not_found(self):
        with self.assertRaises(ValueError):
            self.record.find_phone("9999999999")

    def test_add_birthday(self):
        self.record.add_birthday("15.08.1990")
        self.assertIsNotNone(self.record.birthday)
        self.assertEqual(str(self.record.birthday), "15.08.1990")


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        self.john = Record("John")
        self.john.add_phone("1234567890")
        self.book.add_record(self.john)

    def test_add_record(self):
        self.assertIn("John", self.book.data)

    def test_find_existing(self):
        found = self.book.find("John")
        self.assertEqual(found.name.value, "John")

    def test_find_missing(self):
        self.assertIsNone(self.book.find("Jane"))

    def test_delete_existing(self):
        self.book.delete("John")
        self.assertNotIn("John", self.book.data)

    def test_delete_missing(self):
        with self.assertRaises(KeyError):
            self.book.delete("Jane")

    def test_get_upcoming_birthdays(self):
        # робимо birthday на 3 дні вперед
        future_date = (datetime.today() + timedelta(days=3)).strftime("%d.%m.%Y")
        self.john.add_birthday(future_date)

        upcoming = self.book.get_upcoming_birthdays()

        self.assertTrue(len(upcoming) >= 1)
        self.assertEqual(upcoming[0]["name"], "John")
        self.assertIn("congratulation_date", upcoming[0])


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()

    def test_add_contact_new(self):
        result = add_contact(["John", "1234567890"], self.book)
        self.assertEqual(result, "Contact added.")
        self.assertIn("John", self.book.data)

    def test_add_contact_existing(self):
        add_contact(["John", "1234567890"], self.book)
        result = add_contact(["John", "5555555555"], self.book)
        self.assertEqual(result, "Contact updated.")
        self.assertEqual(len(self.book.data["John"].phones), 2)

    def test_change_username_phone(self):
        add_contact(["John", "1234567890"], self.book)
        result = change_username_phone(
            ["John", "1234567890", "1112223333"], self.book
        )
        self.assertEqual(result, "Contact updated.")
        self.assertEqual(self.book.data["John"].phones[0].value, "1112223333")

    def test_show_phone(self):
        add_contact(["John", "1234567890"], self.book)
        add_contact(["John", "5555555555"], self.book)
        result = show_phone(["John"], self.book)
        self.assertEqual(result, "1234567890; 5555555555")

    def test_show_all(self):
        add_contact(["John", "1234567890"], self.book)
        add_contact(["Jane", "5555555555"], self.book)
        result = show_all([], self.book)
        self.assertIn("Contact name: John", result)
        self.assertIn("Contact name: Jane", result)

    def test_add_birthday_handler(self):
        add_contact(["John", "1234567890"], self.book)
        result = add_birthday(["John", "15.08.1990"], self.book)
        self.assertEqual(result, "Birthday added.")

    def test_show_birthday_handler(self):
        add_contact(["John", "1234567890"], self.book)
        add_birthday(["John", "15.08.1990"], self.book)
        result = show_birthday(["John"], self.book)
        self.assertEqual(result, "15.08.1990")

    def test_birthdays_handler(self):
        add_contact(["John", "1234567890"], self.book)
        future_date = (datetime.today() + timedelta(days=2)).strftime("%d.%m.%Y")
        add_birthday(["John", future_date], self.book)

        result = birthdays([], self.book)

        self.assertIn("Upcoming birthdays:", result)
        self.assertIn("John", result)


if __name__ == "__main__":
    unittest.main()