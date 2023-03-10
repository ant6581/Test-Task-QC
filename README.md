# Telegram Listener
![Bot](https://publicapi.dev/images/logos/core.telegram.org.png)

This Telegram Bot listens to your group chat and monitors the following events: 
- When an Administrator is added or removed from the group chat
- When some predefined words are mentioned in the chat

These events are being sent to your Splunk instance for further analysis. 


## Requirements
- Python 3.0+
- [Aiogram](https://github.com/aiogram/aiogram) library 
- Telegram group and bot
- API key from Telegram Bot
- Splunk 9.x

## Installation and Guide
1. Clone the repository 
2. Install the requirements 
3. Create a Splunk HTTP Event Collector
4. Replace the API_TOKEN, GROUP_ID, SPLUNK_HEC_URL, SPLUNK_HEC_TOKEN with your values, make any other configurations for you needs

##### Modify the predefined monitored words

In order to set the words that you want to monitor put your values in place of 'WORD_1' etc.:
```py
#### Monitoring for flag words
    @dp.message_handler(lambda message: any(word in message.text.lower() for word in ['WORD_1', 'WORD_2', 'WORD_3']))
```

## Use Cases
1. This Telegram Bot can be used in cases you want to monitor changes in the privileged accounts of your Telegram Group. In case of some actor gains admin access and the telegram group gets compromised this approach will help to reduce the mean time to detect and respond to this kind of malicious activity. 
2. This Telegram Bot can monitor for certain words in your Telegram Group. This can be interesting to Corporate Security Teams in order to monitor for any conflicts or violations of the corporate policies between the group members. 

## What to improve in the future releases
1. The changes in admin accounts can be monitored with more details. For example changes in the name of the admins or the time that this admin is online to look for unusual hours of logins. Also a response capability could be added in order to block any new unapproved admins in the telegram group and send the results to splunk. The current aproved admins could be stored in a file to avoid getting this information on every run of the script. 
2. The 'words' monitoring capability could be improved by adding a response capability. For example to delete or ban a member under certain conditions and send the results to Splunk. The predefined words could be imported from a file and not hardcoded in the script. 
3. Another functionality could be added to the Telegram bot. For example an integration with Virus Total in order to check any links or files sent to the Telegram group. In this case an automated response would also benefit the Security Team. 

## Comment for QC
I had no prior experience in working with Splunk and Python before this task and it was easier for me to use the aiogram library instead of the official Telegram API. Also ChatGPT helped me to generate some parts of the script. Still, I am eager to work as a SOC Engineer, learn python and everything related to automation of detection & response. 

