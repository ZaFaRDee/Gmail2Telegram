import imaplib
import email
from email.header import decode_header
import time
from data import config
from loader import bot
import asyncio
from drawer import Setup
from aiogram import types
from aiogram.types import InputMediaPhoto
from datetime import datetime
import pytz
import re




async def main(algorithm, date, tickers=None, ticker=None):
    hour_minutes = date.split(',')[0]
    parsed_date = datetime.strptime(hour_minutes, "%H:%M")

    if ticker:
        web = Setup(ticker=ticker)
        web.init()
        path = web.screenshot()
        web.close_browser()
        text = f"<b>Ticker:</b> {ticker}\n" \
               f"\n<b>Algorithm:</b> {algorithm}\n" \
               f"\n<b>Date:</b> {date}"
        with open(path, 'rb') as photo:
            message = await bot.send_photo(chat_id=config.main_user, photo=photo, caption=text)
    else:
        # try:
        media_group = []
        print(tickers)
        for ticker in tickers:
            ticker = ticker.strip()
            web = Setup(ticker=ticker)
            web.init()
            path = web.screenshot()
            print(path)
            web.close_browser()
            media_group.append(
                types.InputMediaPhoto(media=open(path, 'rb')),
            )
        text = f"<b>Ticker:</b> {ticker}\n" \
               f"\n<b>Algorithm:</b> {algorithm}\n" \
               f"\n<b>Date:</b> {date}"
        message = await bot.send_media_group(chat_id=config.main_user, media=media_group)
        await bot.edit_message_caption(chat_id=config.main_user, message_id=message[0].message_id, caption=text)



# IMAP settings
imap_server = 'imap.gmail.com'
imap_port = 993
imap_username = config.email
imap_password = config.password

while True:
    # Connect to the IMAP server
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(imap_username, imap_password)

    imap.select('inbox')  # You can choose a different mailbox if needed
    # Search for unread emails
    status, email_ids = imap.search(None, f'(UNSEEN FROM "{config.sender_email}")')
    # Iterate through email IDs and retrieve email content
    for email_id in email_ids[0].split():
        EMAIL_ID = email_id
        status, email_data = imap.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]

        # Parse the raw email content
        msg = email.message_from_bytes(raw_email)
        # Get email headers (subject, from, date)
        subject, _ = decode_header(msg["Subject"])[0]
        from_, _ = decode_header(msg.get("From"))[0]
        date, _ = decode_header(msg.get("Date"))[0]

        print(f"Subject: {subject}")
        print(f"From: {from_}")
        print(f"Date: {date}\n")
        try:
            date_string_cleaned = re.sub(r'\([^)]*\)', '', date).strip()
            # Convert the input date and time to a datetime object
            dt_object = datetime.strptime(date_string_cleaned, "%a, %d %b %Y %H:%M:%S %z")


            # Convert the datetime object to the target time zone (Uzbekistan Time)
            uzbek_timezone = pytz.timezone('Asia/Tashkent')
            converted_dt = dt_object.astimezone(uzbek_timezone)

            # Format the converted datetime object
            formatted_date = converted_dt.strftime("%H:%M, %d-%b, %Y")
        except:formatted_date = date
        print("\n__________________")

        if config.sender_email in str(from_):
            message = str(subject).strip()
            if "Alert: New symbol:" in message:
                ticker, algorithm = message.replace("Alert: New symbol:", '').replace("was added to", '%%').split("%%")
                asyncio.run(main(algorithm, formatted_date, ticker=ticker))
            else:
                tickers, algorithm = message.replace("Alert: New symbols:", '').replace("were added to", '%%').replace("""were
             added to""", "%%").split("%%")
                tickers = tickers.split(',')
                asyncio.run(main(algorithm, formatted_date, tickers=tickers))
            continue

    # Close the IMAP connection
    imap.logout()
    time.sleep(10)


    
