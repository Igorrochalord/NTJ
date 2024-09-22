# NTJ Telegram Bot

Este é um bot do Telegram desenvolvido para fornecer serviços de desenvolvimento de sites, criação de bots, design gráfico, edição de vídeos e robótica e IA. O bot permite que os usuários se registrem, façam login e selecionem serviços.
Um projeto para estudos e demonstraçao 

## Funcionalidades

- Registro de usuários com dados como nome de usuário, nome completo, idade, nome da empresa, ramo de atuação, número de telefone e senha.
- Login de usuários registrados.
- Seleção de serviços oferecidos após login.
- Armazenamento de informações no MongoDB.

## Requisitos

Certifique-se de ter os seguintes requisitos instalados:

- Python 3.x
- MongoDB

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/NTJ-Telegram-Bot.git
Navegue até o diretório do projeto:

bash

cd NTJ-Telegram-Bot

Instale as dependências necessárias:

bash

    pip install -r requirements.txt

    Configure o seu MongoDB e certifique-se de que ele está em execução.

    Substitua o token do bot no código (bot = telebot.TeleBot('SEU_TOKEN_AQUI')) pelo token gerado pelo BotFather.

Executando o Bot

Para executar o bot, use o seguinte comando:

bash

python app/TelegramFunction.py

Contribuição
