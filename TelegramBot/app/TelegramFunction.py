import telebot
from telebot import types

# Substitua pelo seu token
bot = telebot.TeleBot('7169792732:AAFCZC67pW0fKRaWhZdYH0tkQ-RPsJsiIVM')

# Função para o comando /start
@bot.message_handler(commands=['start'])
def start(message):
    # Enviando uma foto de boas-vindas
    with open('/home/igor-rocha/NTJ/TelegramBot/images/banner_insta.webp', 'rb') as foto:
        bot.send_photo(message.chat.id, foto, caption="Bem-vindo à NTJ! Aqui estão nossos serviços.")

    # Criando o teclado personalizado
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Nossos Serviços")
    item2 = types.KeyboardButton("Contato")
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, "Escolha o serviço:", reply_markup=markup)

# Função para lidar com as opções do menu
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Nossos Serviços":
        # Criar teclado com os serviços
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Desenvolvimento de Sites")
        item2 = types.KeyboardButton("Criação de Bots")
        item3 = types.KeyboardButton("Design Gráfico")
        item4 = types.KeyboardButton("Edição de Vídeos")
        item5 = types.KeyboardButton("Robótica e Inteligência Artificial")
        back = types.KeyboardButton("Voltar ao Menu Principal")
        markup.add(item1, item2, item3, item4, item5, back)
        
        bot.send_message(message.chat.id, "Selecione um serviço:", reply_markup=markup)
    
    elif message.text == "Desenvolvimento de Sites":
        bot.send_message(message.chat.id, (
            "Você selecionou: Desenvolvimento de Sites. Aqui está como fazemos:\n\n"
            "1. **Planejamento**: Entendemos suas necessidades e objetivos para criar um site que atenda suas expectativas.\n"
            "2. **Design**: Criamos o layout e a identidade visual do seu site, focando na usabilidade e na estética.\n"
            "3. **Desenvolvimento**: Implementamos o site utilizando as melhores práticas de codificação e tecnologias adequadas.\n"
            "4. **Testes**: Realizamos testes rigorosos para garantir que o site funcione perfeitamente em todos os dispositivos.\n"
            "5. **Lançamento**: Publicamos o site e garantimos que ele esteja otimizado para mecanismos de busca.\n"
            "6. **Suporte e Manutenção**: Oferecemos suporte contínuo e manutenção para garantir que seu site permaneça atualizado e funcional."
        ))
    
    elif message.text in ["Criação de Bots", "Design Gráfico", "Edição de Vídeos", "Robótica e Inteligência Artificial"]:
        bot.send_message(message.chat.id, f"Você selecionou: {message.text}. Aqui estão mais informações sobre esse serviço...")  # Adicione informações específicas aqui
    
    elif message.text == "Contato":
        bot.send_message(message.chat.id, "Você pode entrar em contato pelo e-mail: contato@ntj.com")
    
    elif message.text == "Voltar ao Menu Principal":
        start(message)

# Iniciar o bot
bot.infinity_polling()
