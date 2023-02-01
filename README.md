# Telegram Listener
![Bot](https://www.techopedia.com/images/uploads/6e13a6b3-28b6-454a-bef3-92d3d5529007.jpeg)
This Telegram Bot listens to your group chat and monitors the following events: 
- An Administrator is added or removed to the group chat
- Some predefined words are mentioned in the chat

These events are being sent to your Splunk instance for further analysis. 


## Requirements
- Python 3.0+
- [Aiogram](https://github.com/aiogram/aiogram) library 
- Telegram group and bot
- API key from Telegram Bot
- Splunk 9.x

## Installation and Guide
In this script, the monitor_words handler is triggered whenever a message in the group chat contains any of the monitored words 'malicious' or 'dangerous' as an example. The handler then sends the results to Splunk using the Splunk HTTP Event Collector (HEC). The message payload is sent as JSON data in the body of the POST request. 
Note: Replace the placeholders in the script 
- API_TOKEN, 
- GROUP_ID, 
- SPLUNK_HEC_URL,
- SPLUNK_HEC_TOKEN

with your actual Telegram bot API token, group ID, Splunk HEC URL, and Splunk HEC token, respectively.
Also do not forget to install the aiogram library as stated in the requirements. 

##### Modify the predefined monitored words

In order to set the words that you want to monitor put your values in place of 'WORD_1' etc.:
```py
#### Monitoring for flag words
    @dp.message_handler(lambda message: any(word in message.text.lower() for word in ['WORD_1', 'WORD_2', 'WORD_3']))
```

## Use Cases
1.This Telegram Bot can be used in cases you want to monitor changes in the priveleged accounts of your Telegram Group. In case of some actor gains admin access and the telegram group gets compromised this approach will help to reduce the mean time to detect and respond to this kind of malicious activity. 
2.This Telegram Bot can monitor for certain words in your Telegram Group. This can be interesting to Corporate Security Teams in order to monitor for any conflicts or violations of the corporate policies between the group members. 

## Things to improve in the future releases
1. The current capabilities of this bot can be expanded. The changed in admin accounts may be monitored with more details. For example changes in the name of the admins and even the time that this admin is online to look for unusual hours of logins. Also a response capability could be added in order to block any new unaproved admins in the telegram group and send the results to splunk. The current aproved admins could be stored in a file to avoid getting this information on every run of the script. 
2. The 'words' monitoring capability could be improved by adding a response capability. For example to delete or ban a member under certain conditions and send the results to Splunk. The predefined words could be imported from a file and not hardcoded in the script. 
3. Another functionality could be added to the Telegram bot. For example an integration with Virus Total in order to check any links or files sent to the Telegram group. In this case an automated response would also benefit the Security Team. 


