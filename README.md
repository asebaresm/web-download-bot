# FC no-invite bot

A simple Telegram bot to download FC threads for people with no invite

# Dependencies
- virtualenv
- wkhtmltopdf (optional for image format rendering)

# Run the bot
A sequence like this should make it run:
- Check file names in `config.yml` file
- Add cookies file
- `source  environment/bin/activate.fish`
- `python run_bot.py`

# Use the bot
- `/start`     - display your `chat_id` for white/blacklisting purposes
- `/help`      - commands help
- `/get <url>` - fetch thread from FC and download it in html format
