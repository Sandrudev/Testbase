import streamlit as st
import telebot

# Telegram bot credentials
BOT_TOKEN = '5660590671:AAHboouGd0fFTpdjJSZpTfrtLyWsK1GM2JE'
CHANNEL_ID = '-1002173127202'

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Функция отправки сообщения в Telegram канал
def send_message_to_channel(message):
    bot.send_message(CHANNEL_ID, message)

# Функция проверки логина и пароля в телеграм-канале
def check_login_password(login, password):
    updates = bot.get_updates()
    for update in updates:
        if update.message and update.message.chat.id == int(CHANNEL_ID):
            text = update.message.text
            if f"Login: {login}, Password: {password}" in text:
                return True
    return False

# UI приложения
st.title("Регистрация и Авторизация")

# Выбор между регистрацией и авторизацией
choice = st.selectbox("Выберите действие", ["Регистрация", "Авторизация"])

if choice == "Регистрация":
    st.subheader("Регистрация")
    login = st.text_input("Введите логин")
    password = st.text_input("Введите пароль", type="password")
    
    if st.button("Зарегистрироваться"):
        if login and password:
            # Отправка данных в телеграм-канал
            message = f"Login: {login}, Password: {password}"
            send_message_to_channel(message)
            st.success("Вы успешно зарегистрировались!")
        else:
            st.error("Пожалуйста, введите логин и пароль.")

elif choice == "Авторизация":
    st.subheader("Авторизация")
    login = st.text_input("Введите логин")
    password = st.text_input("Введите пароль", type="password")
    
    if st.button("Войти"):
        if check_login_password(login, password):
            st.success("Вы успешно вошли в систему!")
        else:
            st.error("Неверный логин или пароль.")
