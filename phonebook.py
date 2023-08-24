"""Данная программа может отображать телефонный справочник, сохранять новые записи, искать по фамилии.
Управление можно осуществлять вводом цифры соответствующего действия.
Сохранить можно следующие данные:
    фамилия, имя, отчество, название организации, телефон рабочий, телефон личный (сотовый)
Программа принимает записи в формате UTF-8. 
"""

import os


class Entry:
    """Class for entry"""

    def __init__(
        self,
        last_name: str,
        first_name: str,
        middle_name: str,
        company_name: str,
        work_phone: str,
        personal_phone: str,
    ):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.company_name = company_name
        self.work_phone = work_phone
        self.personal_phone = personal_phone


class Phonebook:
    """Class for Phonebook"""

    def __init__(self, filename: str):
        self.filename = filename
        self.entries = []
        self.load_entries()

    def load_entries(self):
        """open phonebook file and load entries"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(";")
                    entry = Entry(*data)
                    self.entries.append(entry)

    def save_entries(self):
        """save entries with semicolon formatting"""
        with open(self.filename, "w", encoding="utf") as file:
            for entry in self.entries:
                line = ";".join(
                    [
                        entry.last_name,
                        entry.first_name,
                        entry.middle_name,
                        entry.company_name,
                        entry.work_phone,
                        entry.personal_phone,
                    ]
                )
                file.write(line + "\n")

    def display_entries(self, page_size=10):
        """display entries in terminal"""
        total_entries = len(self.entries)
        total_pages = (total_entries + page_size - 1) // page_size

        page = 1
        while True:
            start_idx = (page - 1) * page_size
            end_idx = min(start_idx + page_size, total_entries)
            print(
                "\n___ Phonebook Entries - Page {} of {} ___".format(page, total_pages)
            )
            for idx in range(start_idx, end_idx):
                entry = self.entries[idx]
                print(
                    "Name: {} {} {}".format(
                        entry.last_name, entry.first_name, entry.middle_name
                    )
                )
                print("Сompany: {}".format(entry.company_name))
                print("Work Phone: {}".format(entry.work_phone))
                print("Personal Phone: {}".format(entry.personal_phone))
                print("_" * 40)
            print("Page {} of {}".format(page, total_pages))

            if total_pages > 1:
                command = input(
                    "Enter 'n' for next page, 'p' for previous page, or any other key to exit: "
                )
                if command.lower() == "n":
                    page = min(page + 1, total_pages)
                elif command.lower() == "p":
                    page = max(page - 1, 1)
                else:
                    break
            else:
                input("Press Enter to exit...")
                break

    def add_entry(self, entry: Entry):
        self.entries.append(entry)
        self.save_entries()

    def find_entries(self, **kwargs):
        found_entries = []
        for entry in self.entries:
            match = True
            for key, value in kwargs.items():
                if getattr(entry, key, None) != value:
                    match = False
                    break
            if match:
                found_entries.append(entry)

        return found_entries


# Create the phonebook instance
phonebook = Phonebook("phonebook.txt")

# Main loop
while True:
    print("\n=== Phonebook Menu ===")
    print("1. Display Entries")
    print("2. Add Entry")
    print("3. Search Entries")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        phonebook.display_entries()
    elif choice == "2":
        # creating new entry
        last_name = input("Last Name: ")
        first_name = input("First Name: ")
        middle_name = input("Middle Name: ")
        company_name = input("Company: ")
        work_phone = input("Work Phone: ")
        personal_phone = input("Personal Phone: ")
        new_entry = Entry(
            last_name, first_name, middle_name, company_name, work_phone, personal_phone
        )
        phonebook.add_entry(new_entry)
        print("Entry added successfully!")
    elif choice == "3":
        search_last_name = input("Search by Last Name: ")
        found_entries = phonebook.find_entries(last_name=search_last_name)
        if found_entries:
            print("\n___ Found Entries ___")
            for idx, entry in enumerate(found_entries, start=1):
                print(
                    "{}. {} {} {}\n    company: {}\n    work phone: {}, personal phone: {}".format(
                        idx,
                        entry.last_name,
                        entry.first_name,
                        entry.middle_name,
                        entry.company_name,
                        entry.work_phone,
                        entry.personal_phone,
                    )
                )
        else:
            print("No entries found.")
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please choose a valid option.")

print("Goodbye!")
