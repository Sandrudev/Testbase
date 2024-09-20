import streamlit as st
import json
import os
import hashlib

USER_DATA_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                if os.path.getsize(USER_DATA_FILE) == 0:
                    return {}
                users = json.load(file)
                return users
        except json.JSONDecodeError:
            return {}
    return {}

def save_users(users):
    try:
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        st.error(f"Ошибка при сохранении данных: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):
    users = load_users()
    if username in users:
        st.error("Пользователь уже существует!")
        return False
    users[username] = hash_password(password)
    save_users(users)
    st.success("Регистрация успешна!")
    return True

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

st.title("Регистрация и авторизация")

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

if st.button("Показать данные из JSON"):
    users = load_users()
    st.write(users)
