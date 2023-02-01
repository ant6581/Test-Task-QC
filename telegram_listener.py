import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
import requests
import json
 
 
API_TOKEN = os.environ.get('BOT_TOKEN', '5809652131:AAFK5tQeG9Ww1OYi-_TyFXhyUOI8L1m_-s0')
GROUP_ID = os.environ.get('GROUP_ID', '-1001628491781')
 
# Enter the URL for your Splunk HEC endpoint
SPLUNK_HEC_URL = 'http://10.10.1.75:8088/services/collector'
 
# Enter the Splunk HEC token
SPLUNK_HEC_TOKEN = '1949df5e-e7bf-412d-a4b2-bb81c9cac75b'
 
# Configure logging
logging.basicConfig(level=logging.INFO)
 
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
 
# Store the current administrators
current_administrators = []
 
async def check_administrators(group_id):
    """
    Check for changes in the list of administrators in a group.
    """
    global current_administrators
 
    # Get the current administrators
    administrators = await bot.get_chat_administrators(group_id)
 
    # Store the new administrators
    new_administrators = [admin.user for admin in administrators]
 
    # Check for new administrators
    new_admins = set(new_administrators) - set(current_administrators)
    if new_admins:
        message = "New administrator(s) have been added to the group: \n"
        for admin in new_admins:
            message += f"{admin.full_name} ({admin.username})\n"
        await bot.send_message(GROUP_ID, message)
      # Send the update to Splunk
        payload = json.dumps({
            "sourcetype": "telegram_group",
            "event": message,
            "fields":{
			"admin_username": admin.username,
 			"admin_full_name": admin.full_name,
                        "action": "added"}
        })

        headers = {
            'Authorization': 'Splunk ' + SPLUNK_HEC_TOKEN
        }
        response = requests.post(SPLUNK_HEC_URL, headers=headers, data=payload)
        print(response.text)
 
    # Check for removed administrators
    removed_admins = set(current_administrators) - set(new_administrators)
    if removed_admins:
        message = "An administrator(s) have been removed from the group: \n"
        for admin in removed_admins:
            message += f"{admin.full_name} ({admin.username})\n"
        await bot.send_message(GROUP_ID, message)
      # Send the update to Splunk
      # Send the update to Splunk
        payload = json.dumps({
            "sourcetype": "telegram_group",
            "event": message,
            "fields":{
                        "admin_username": admin.username,
                        "admin_full_name": admin.full_name,
                        "action": "removed"}

        })
 
        headers = {
            'Authorization': 'Splunk ' + SPLUNK_HEC_TOKEN
        }
        response = requests.post(SPLUNK_HEC_URL, headers=headers, data=payload)
        print(response.text)
 
    # Update the current administrators
    current_administrators = new_administrators
 
async def scheduled_check(wait_time):
    """
    Schedule regular checks for changes in the administrators.
    """
    while True:
        await check_administrators(GROUP_ID)
        await asyncio.sleep(wait_time)

#### Monitoring for flag words
@dp.message_handler(lambda message: any(word in message.text.lower() for word in ['malicious', 'dangerous']))
async def monitor_words(message: types.Message):
    headers = {
        'Authorization': f'Splunk {SPLUNK_HEC_TOKEN}',
        'Content-Type': 'application/json'
    }

    payload = {
        "sourcetype": "telegram-group-update",
        "event": "A flag word has been detected in the Group Chat",
        "fields":{
        "flag_word": message.text,
        "sender": message.from_user.full_name}
    }
    response = requests.post(SPLUNK_HEC_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f'Failed to send data to Splunk: {response.text}')
    else:
        print(f'Successfully sent data to Splunk: {message.text}')


 
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_check(5))
    executor.start_polling(dp, skip_updates=True)
