import gspread
from google.oauth2.service_account import Credentials

# Авторизация в Google Таблицах
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('budget')

# Функция для ввода суммы с проверкой на числовое значение
def input_amount(prompt):
    while True:
        amount = input(prompt)
        if amount.isdigit():
            return int(amount)
        else:
            print("Введите сумму в виде числа.")

# Приветственное сообщение
print("Цель проекта: помочь управлять финансами")

# Ввод доходов
print("Введите планируемые доходы:")
income_categories = {
    "1": "Зарплата",
    "2": "Иные доходы"
}
income = {"Нал": 0, "Карта": 0}
for key, category in income_categories.items():
    amount = input_amount(f"Введите сумму для категории '{category}': ")
    income_source = input(f"Добавить сумму к 'Нал' или 'Карта'? ").strip().lower()
    while income_source not in ["нал", "карта"]:
        print("Выберите 'Нал' или 'Карта'.")
        income_source = input(f"Добавить сумму к 'Нал' или 'Карта'? ").strip().lower()
    income[income_source] += amount

# Ввод расходов
print("Заполните планируемые расходы:")
expense_categories = {
    "1": "Еда",
    "2": "Здоровье",
    "3": "Одежда",
    "4": "Путешествия",
    "5": "Моя мечта"
}
expenses = {}
while True:
    for key, category in expense_categories.items():
        amount = input_amount(f"Введите сумму для категории '{category}': ")
        expenses[category] = amount
    add_more = input("Хотите добавить еще категории расходов (Да/Нет)? ").strip().lower()
    if add_more != "да":
        break

# Подсчет остатка средств и прогноза
total_income = sum(income.values())
total_expense = sum(expenses.values())
forecast = {}
for category, amount in expenses.items():
    forecast[category] = (total_income - total_expense) * (amount / total_expense)

# Запись данных в Google Таблицы
row = ["Категория расходов", "План на месяц", "Факт потрачено", "Осталось потратить", "Прогноз на конец месяца"]
sheet.append_row(row)
for category in expense_categories.values():
    row = [category, expenses[category], 0, 0, forecast[category]]
    sheet.append_row(row)

print("Данные успешно записаны в таблицу.")

