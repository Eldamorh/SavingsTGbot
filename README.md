## Sumary

This Python project is a Telegram bot using telebot and Django that contains user information and performs a simple function of calculating savings.
Each user can have savings of different types and amounts. Savings can be added, viewed and deleted.

The bot name in Telegram is @arsenii_malko_bot (https://t.me/arsenii_malko_bot)

## Installation

1. Clone this project `git clone https://github.com/Eldamorh/SavingsTGbot.git`
2. Make sure you have python3 and pip installed
3. Install requirements file `pip install -r requirements.txt`
4. Edit .env_prod file and add your Bot Token and Django Secret Key and paste this file to .env `cat .env_prod > .env`
5. Make migrations `python3 manage.py makemigrations`

Now everything is ready to run. Bot and Server are running seperately. 
To run server use this command `python3 manage.py runserver`. Server can be used to mannualy edit tables in admin panel
To start bot use `python3 manage.py startbot`.

