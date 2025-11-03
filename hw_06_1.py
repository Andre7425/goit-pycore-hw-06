

from collections import UserDict

# --- Базовий клас для полів ---
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# --- Клас для імені (обов'язкове) ---
class Name(Field):
    # Поки що не додаємо логіки, лише наслідуємо
    pass

# --- Клас для телефону з валідацією ---
class Phone(Field):
    def __init__(self, value):
        # Перевірка на 10 цифр
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Телефон має складатися рівно з 10 цифр.")
        # ініціалізація з батьківського класу
        super().__init__(value)

# --- Клас для запису контакту ---
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []  # Список об'єктів Phone

    def add_phone(self, phone_str):
        """
        Додає новий телефон до запису.
        Телефонна валідація відбувається при створенні об'єкта Phone.
        """
        try:
            phone = Phone(phone_str)
            self.phones.append(phone)
        except ValueError as e:
            print(f"Помилка при додаванні телефону: {e}")

    def find_phone(self, phone_str):
        """
        Шукає об'єкт Phone за його рядковим представленням (номером).
        Повертає об'єкт Phone або None, якщо не знайдено.
        """
        for phone in self.phones:
            if phone.value == phone_str:
                return phone
        return None

    def remove_phone(self, phone_str):
        """
        Видаляє телефон зі списку за його номером.
        """
        phone_to_remove = self.find_phone(phone_str)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            print(f"Телефон {phone_str} не знайдено для видалення.")

    def edit_phone(self, old_phone_str, new_phone_str):
        """
        Редагує телефон. Знаходить старий номер та замінює його на новий.
        """
        # Спочатку валідуємо новий номер
        try:
            new_phone = Phone(new_phone_str)
        except ValueError as e:
            print(f"Помилка при редагуванні: {e}")
            return  # Зупиняємо виконання, якщо новий номер невалідний

        # Шукаємо та замінюємо старий
        found = False
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone_str:
                self.phones[i] = new_phone
                found = True
                break
        
        if not found:
            print(f"Старий телефон {old_phone_str} не знайдено.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# --- Клас Адресної Книги ---
class AddressBook(UserDict):
    def add_record(self, record: Record):
        """
        Додає запис (record) до self.data.
        Ключем є ім'я контакту (рядок), значенням — об'єкт Record.
        """
        name_key = record.name.value
        self.data[name_key] = record

    def find(self, name: str):
        """
        Знаходить запис за іменем (name).
        Повертає об'єкт Record або None, якщо не знайдено.
        """
        return self.data.get(name)

    def delete(self, name: str):
        """
        Видаляє запис за іменем (name).
        """
        if name in self.data:
            del self.data[name]
        else:
            print(f"Контакт з іменем {name} не знайдено.")


# --- КОД ДЛЯ ПЕРЕВІРКИ ---


if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print("--- Всі записи ---")
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print("\n--- John після редагування ---")
    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    print("\n--- Пошук телефону 5555555555 у John ---")
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Спроба додати невалідний номер
    print("\n--- Спроба додати невалідний номер ---")
    john.add_phone("123") # Виведе помилку валідації

    # Видалення запису Jane
    book.delete("Jane")
    print("\n--- Всі записи після видалення Jane ---")
    for name, record in book.data.items():
        print(record)