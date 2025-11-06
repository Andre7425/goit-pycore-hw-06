

from collections import UserDict

# --- Базовий клас для полів ---


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# --- Клас для імені ---


class Name(Field):
    # Поки що не додаємо логіки, лише наслідуємо
    pass

# --- Клас для телефону з валідацією ---


class Phone(Field):
    def __init__(self, value):
        # Перевірка на 10 цифр.
        # ValueError "прокинеться" нагору, якщо валідація не пройде.
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
        Валідація відбувається в класі Phone.
        Повертає створений об'єкт Phone.
        """
        # (Зауваження 2) Видалено try-except.
        # Якщо phone_str невалідний, клас Phone сам "прокине" ValueError.
        phone = Phone(phone_str)
        self.phones.append(phone)
        return phone  # (Зауваження 1) Повертаємо об'єкт

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
        Повертає True, якщо видалення успішне, False - якщо телефон не знайдено.
        """
        # (Зауваження 4) Використовуємо find_phone
        phone_to_remove = self.find_phone(phone_str)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
            return True  # (Зауваження 1) Повертаємо результат
        return False  # (Зауваження 1) Повертаємо результат

    def edit_phone(self, old_phone_str, new_phone_str):
        """
        Редагує телефон. Знаходить старий номер та замінює його на новий.
        Повертає True, якщо редагування успішне, False - якщо старий тел. не знайдено.
        Якщо новий номер невалідний, "прокине" ValueError.
        """
        # (Зауваження 2, 3) Валідація нового номера.
        # Якщо new_phone_str невалідний, Phone() "прокине" ValueError.
        new_phone = Phone(new_phone_str)

        # (Зауваження 4) Використовуємо find_phone
        old_phone_obj = self.find_phone(old_phone_str)

        if old_phone_obj:
            # Знаходимо індекс старого об'єкта та замінюємо його
            index = self.phones.index(old_phone_obj)
            self.phones[index] = new_phone
            return True  # (Зауваження 1) Повертаємо результат

        # (Зауваження 1) Повертаємо результат
        return False

    def __str__(self):
        return (f"Contact name: {self.name.value}, "
                f"phones: {'; '.join(p.value for p in self.phones)}")

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
        Повертає True, якщо видалення успішне, False - якщо запис не знайдено.
        """
        if name in self.data:
            del self.data[name]
            return True  # (Зауваження 1) Повертаємо результат
        return False  # (Зауваження 1) Повертаємо результат


# --- КОД ДЛЯ ПЕРЕВІРКИ (оновлений) ---
# Тепер цей код відповідає за обробку помилок та спілкування з користувачем

if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    try:
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
    except ValueError as e:
        print(f"Помилка при додаванні телефону John: {e}")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    try:
        jane_record.add_phone("9876543210")
        book.add_record(jane_record)
    except ValueError as e:
        print(f"Помилка при додаванні телефону Jane: {e}")

    # Виведення всіх записів у книзі
    print("--- Всі записи ---")
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    try:
        if john.edit_phone("1234567890", "1112223333"):
            print(f"\nТелефон для {john.name.value} успішно змінено.")
        else:
            print(f"\nТелефон 1234567890 не знайдено у {john.name.value}.")
    except ValueError as e:
        print(f"\nПомилка редагування: {e}")  # Спрацює, якщо новий номер невалідний

    print("\n--- John після редагування ---")
    print(john)

    # Пошук конкретного телефону у записі John
    print("\n--- Пошук телефону 5555555555 у John ---")
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    # Спроба додати невалідний номер (тепер з try-except)
    print("\n--- Спроба додати невалідний номер ---")
    try:
        john.add_phone("123")
    except ValueError as e:
        print(f"Помилка! {e}")  # Коректна обробка помилки

    # Видалення запису Jane
    print("\n--- Видалення Jane ---")
    if book.delete("Jane"):
        print("Запис 'Jane' успішно видалено.")
    else:
        print("Запис 'Jane' не знайдено.")

    print("\n--- Всі записи після видалення Jane ---")
    for name, record in book.data.items():
        print(record)