# Webpage downloader no-account bot

A simple Telegram bot to download threads/webpages locked behind a private site
that require an account. Just add a cookie!

# Dependencies
- virtualenv (self-contained environment)
- wkhtmltopdf (experimental and very optional for downloading html as image)

# Run the bot
A sequence like this should make it run:
- Check file names in `config.yml` file
- Add cookies DB file
- `source  environment/bin/activate.fish`
- `python run_bot.py`

# Use the bot
- `/start`     - display your `chat_id` for white/blacklisting purposes
- `/help`      - commands help
- `/get <url>` - fetch thread from FC and download it in html format

# Feature backlog
- User white-listing
    - https://stackoverflow.com/a/41054788
- [done] Get all the thread pages
- [done] Validate URLs for `/get` command
- [done]Get specific thread pages
