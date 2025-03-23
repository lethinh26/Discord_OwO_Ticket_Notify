# Discord OwO Ticket Notify

## Important Note
This code has been intentionally restricted to minimize the risk of being detected by Discord. Since it is a self-bot, it only runs and logs notifications in the console. However, self-bots violate Discord’s Terms of Service, which can lead to account termination. If you want to unlock the full potential of this bot, consider using the dedicated bot version that I have prepared: [Discord_OwO_Ticket_Notify_Bot](https://github.com/lethinh26/Discord_OwO_Ticket_Notify_Bot).

## Author
**Creator:** lethinh26

## Introduction
Discord OwO Ticket Notify is a self-bot that monitors the #seller-ads channel in the Support OwO server for stock-related messages. If someone posts a message indicating they are selling a ticket, the bot extracts relevant stock information and stores it in a MongoDB database. This allows for real-time tracking of ticket availability.

## Features
- Monitors messages in a specified channel for stock updates.
- Extracts and stores stock information from messages.
- Updates stock details if messages are edited.
- Removes stock records if messages are deleted.

## Installation
### Requirements
Ensure you have Python installed, then install the necessary dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies
- `pymongo==4.10.1`
- `git+https://github.com/dolfies/discord.py-self.git`

## Configuration
1. Clone the repository:
   ```bash
   git clone https://github.com/lethinh26/Discord_OwO_Ticket_Notify.git
   cd Discord_OwO_Ticket_Notify
   ```
2. Configure the bot by modifying the following variables in the script:
   ```python
   OWO_TICKET_CHANNEL = 822972235996201021  # This is the channel id seller-ads DO NOT EDIT
   TOKEN = ""  # Your Discord self-bot token
   ```
3. Start the bot:
   ```bash
   python main.py
   ```

## Disclaimer
This bot operates as a self-bot, which violates Discord's Terms of Service. Use it at your own risk.

