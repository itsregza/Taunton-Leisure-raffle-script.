# Taunton-Leisure-raffle-script.
Simple script i made to mass enter their giveaway type raffles

# How it works?
- Emails are entered into emails.csv
- Capsolver key is entered in config.json
- Entry script is ran from entry.py. It runs 1 entry at a time. There is a sleep time between entries which can be manually adjusted from current "time.sleep(random.uniform(120, 180))"
- All entries receive confirmation email.
# Requirements
- The script uses https://github.com/bogdanfinn/tls-client/ for the request session. This is stored in a py "vendor" folder. You can remove this load if you just want to use the https://github.com/FlorianREGAZ/Python-Tls-Client version.
