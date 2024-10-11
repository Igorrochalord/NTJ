import telebot
from telebot import types
import pymongo
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# Conexão com o MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['bot_database']
users_collection = db['usuarios']

# Substitua pelo seu token
bot = telebot.TeleBot('7169792732:AAFCZC67pW0fKRaWhZdYH0tkQ-RPsJsiIVM')

# Dicionário temporário para armazenar dados do usuário e sessão
temp_user_data = {}
logged_users = {}  # Armazenará os usuários logados com base no chat_id

# Função para exibir o menu inicial
def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Registrar")
    item2 = types.KeyboardButton("Login")
    markup.add(item1, item2)
    
    bot.send_message(chat_id, "Bem-vindo! Escolha uma opção:", reply_markup=markup)

# Função para exibir o menu de serviços (após login)
def show_service_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Botões de serviços
    item1 = types.KeyboardButton("Desenvolvimento de Sites")
    item2 = types.KeyboardButton("Criação de Bots")
    item3 = types.KeyboardButton("Design Gráfico")
    item4 = types.KeyboardButton("Edição de Vídeos")
    item5 = types.KeyboardButton("Robótica e IA")
    back = types.KeyboardButton("Voltar ao Menu Principal")

    markup.add(item1, item2, item3, item4, item5, back)
    
    bot.send_message(chat_id, "Selecione um serviço:", reply_markup=markup)

# Função para o comando /start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_photo(message.chat.id, open('/home/igor-rocha/NTJ/TelegramBot/images/Logo.webp', 'rb'))
    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao carregar imagem: {str(e)}")
    show_main_menu(message.chat.id)

# Função para lidar com mensagens gerais
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    if message.text == "Registrar":
        bot.send_message(chat_id, "Digite seu nome de usuário:")
        bot.register_next_step_handler(message, process_username)
    elif message.text == "Login":
        bot.send_message(chat_id, "Digite seu nome de usuário:")
        bot.register_next_step_handler(message, login_username)
    elif message.text == "Voltar ao Menu Principal":
        show_main_menu(chat_id)
    
    # Somente após login, processa os serviços
    elif message.text in ["Desenvolvimento de Sites", "Criação de Bots", "Design Gráfico", "Edição de Vídeos", "Robótica e IA"]:
        if chat_id in logged_users:
            user = users_collection.find_one({"username": logged_users[chat_id]})
            if user:
                users_collection.update_one({"username": user['username']}, {"$push": {"escolhas": message.text}})
                bot.send_message(chat_id, f"Você selecionou: {message.text}. Aqui está como fazemos:\n\n[Detalhes do serviço aqui]")
                bot.send_message(chat_id, "Sua escolha foi registrada.")
            else:
                bot.send_message(chat_id, "Erro ao encontrar usuário.")
        else:
            bot.send_message(chat_id, "Você precisa fazer login para acessar os serviços.")
            show_main_menu(chat_id)
    else:
        bot.send_message(chat_id, "Opção inválida. Use o menu para escolher.")

# Função para registrar o usuário
def process_username(message):
    temp_user_data['username'] = message.text
    bot.send_message(message.chat.id, "Digite seu nome completo:")
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    temp_user_data['nome'] = message.text
    bot.send_message(message.chat.id, "Digite sua idade:")
    bot.register_next_step_handler(message, process_age)

def process_age(message):
    temp_user_data['idade'] = message.text
    bot.send_message(message.chat.id, "Digite o nome da sua empresa:")
    bot.register_next_step_handler(message, process_company)

def process_company(message):
    temp_user_data['empresa'] = message.text
    bot.send_message(message.chat.id, "Qual é o ramo da sua empresa?")
    bot.register_next_step_handler(message, process_business_area)

# Adicionar step handler para processar o telefone
def process_business_area(message):
    temp_user_data['ramo'] = message.text
    bot.send_message(message.chat.id, "Digite seu número de telefone:")
    bot.register_next_step_handler(message, process_phone)

def process_phone(message):
    temp_user_data['telefone'] = message.text
    bot.send_message(message.chat.id, "Digite uma senha:")
    bot.register_next_step_handler(message, process_password)

def process_password(message):
    try:
        temp_user_data['senha'] = generate_password_hash(message.text)
        users_collection.insert_one(temp_user_data)
        bot.send_message(message.chat.id, "Registro concluído com sucesso! Agora faça o login.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ocorreu um erro ao registrar: {str(e)}")
    finally:
        temp_user_data.clear()
        show_main_menu(message.chat.id)

# Fluxo de login
def login_username(message):
    temp_user_data['username'] = message.text
    bot.send_message(message.chat.id, "Digite sua senha:")
    bot.register_next_step_handler(message, login_password)

def login_password(message):
    chat_id = message.chat.id
    username = temp_user_data['username']
    senha = message.text
    
    user = users_collection.find_one({"username": username})
    if user and check_password_hash(user.get('senha', ''), senha):
        # Enviar uma imagem após login bem-sucedido
        try:
            bot.send_photo(chat_id, open('/home/igor-rocha/NTJ/TelegramBot/images/banner_insta.webp', 'rb'))
        except Exception as e:
            bot.send_message(chat_id, f"Erro ao carregar imagem: {str(e)}")
        bot.send_message(chat_id, f"Bem-vindo, {user['nome']}!")
        logged_users[chat_id] = username  # Armazena o username logado com base no chat_id
        show_service_menu(chat_id)  # Exibir menu de serviços após login bem-sucedido
    else:
        bot.send_message(chat_id, "Usuário ou senha incorretos. Tente novamente.")
        show_main_menu(chat_id)  # Voltar ao menu inicial se o login falhar
    
    temp_user_data.clear()

# Iniciar o bot
bot.infinity_polling()