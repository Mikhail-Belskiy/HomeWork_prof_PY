import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

def format_phone(number):
    # Удалить все символы, кроме цифр, '+' и 'доб'
    cleaned_number = re.sub(r'[^\d+доб]', '', number)

    # Разделить на основной номер и добавочный, если он есть
    match = re.match(r'(\+7|8)?(\d{3})(\d{3})(\d{2})(\d{2})(?:доб\.(\d{1,4}))?', cleaned_number)

    if match:
        code = match.group(2)
        part1 = match.group(3)
        part2 = match.group(4)
        part3 = match.group(5)
        ext = match.group(6)
        
        # Форматировать основной номер
        formatted_number = f"+7({code}){part1}-{part2}-{part3}"
        
        # Добавить добавочный, если есть
        if ext:
            formatted_number += f" доб.{ext}"     
        return formatted_number

unique_entries = {}

for entry in contacts_list[1:]:
    last_name = entry[0]
    first_name = entry[1]
    surname = entry[2]
    organization = entry[3]
    position = entry[4]
    phone = entry[5]
    email = entry[6]

    # Форматирование номера
    formatted_phone = format_phone(phone)

    # Обработка Фамилии, Имени и Отчества
    if last_name and not first_name:
        names = last_name.split()
        last_name = names[0]
        first_name = names[1] if len(names) > 1 else ''
        surname = names[2] if len(names) > 2 else ''
    elif first_name and not last_name:
        names = first_name.split()
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ''
        surname = names[2] if len(names) > 2 else ''

    # Формируем ключ для уникальности
    key = (last_name, first_name)

    if key not in unique_entries:
        unique_entries[key] = [last_name, first_name, surname, organization, position, formatted_phone, email]
    else:
        # Если запись уже существует, объединяем их
        existing_entry = unique_entries[key]

        # Предпочитаем непустые значения из новой записи
        existing_entry[2] = existing_entry[2] or surname
        existing_entry[3] = existing_entry[3] or organization
        existing_entry[4] = existing_entry[4] or position
        existing_entry[5] = existing_entry[5] or formatted_phone
        existing_entry[6] = existing_entry[6] or email

sorted_unique_entries = [list(entry) for entry in unique_entries.values()]
sorted_unique_entries.insert(0, ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email'])

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(sorted_unique_entries)