# Event search bot

This bot is built with **Aiogram** and **Selenium**. It finds current events from an event listing website and allows users to select events by **category**, **date**, and **location**. 

Selenium is used to scrape up-to-date event data, while Aiogram handles the bot's interaction and state management.

The bot's interaction flow is handled in `bot.py`.
The bot's core logicis implemented in the `EventBot` class located in `bot_class.py`.