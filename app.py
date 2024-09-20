import streamlit as st
import json
import os
import hashlib

# Путь к JSON-файлу для хранения пользователей (файл должен находиться в той же директории, что и исполняемый файл)
USER_DATA_FILE = 'users.json'

# Функция для загрузки пользователей из файла
def load_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                # Если файл пуст, вернем пустой словарь
                if os.path.getsize(USER_DATA_FILE) == 0:
                    return {}
                users = json.load(file)
                return users
        except json.JSONDecodeError:
            # Если файл пуст или содержит некорректные данные, инициализируем его как пустой словарь
            return {}
    return {}

# Функция для сохранения пользователей в файл
def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)  # Форматированный JSON для удобства чтения

# Функция для хеширования паролей
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Функция для регистрации нового пользователя
def register(username, password):
    users = load_users()
    if username in users:
        st.error("Пользователь уже существует!")
        return False
    users[username] = hash_password(password)
    save_users(users)
    st.success("Регистрация успешна!")
    return True

# Функция для авторизации пользователя
def login(username, password):
    users = load_users()
    if username not in users:
        st.error("Неверное имя пользователя!")
        return False
    if users[username] != hash_password(password):
        st.error("Неверный пароль!")
        return False
    st.success(f"Добро пожаловать, {username}!")
    return True

# Интерфейс Streamlit
st.title("Регистрация и авторизация")

# Выбор между регистрацией и авторизацией
choice = st.sidebar.selectbox("Выберите действие", ["Авторизация", "Регистрация"])

if choice == "Регистрация":
    st.subheader("Регистрация нового пользователя")
    new_username = st.text_input("Введите имя пользователя")
    new_password = st.text_input("Введите пароль", type='password')
    new_password_confirm = st.text_input("Подтвердите пароль", type='password')

    if st.button("Зарегистрироваться"):
        if new_password == new_password_confirm:
            register(new_username, new_password)
        else:
            st.error("Пароли не совпадают!")
else:
    st.subheader("Авторизация")
    username = st.text_input("Введите имя пользователя")
    password = st.text_input("Введите пароль", type='password')

    if st.button("Войти"):
        login(username, password)

# Тест чтения и записи
if st.button("Показать данные из JSON"):
    users = load_users()
    st.write(users)
