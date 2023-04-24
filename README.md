# Daily 20000

## What is this

This is a small application where users can subsribe to an email bot that asks ChatGPT Who is on the 20000 huf bill every day and sends out the answer in email each day.

## Setup

1. Clone the repo
2. Create a subscribedUsers.json file with an empty array.
3. Setup your `OPENAI_API_KEY`, `DAILY20000PWD`, `DAILY20000UNAME`, `DAILY20000_PATH` enviroment variables
4. Setup a cron job for sendMail.py for whenever you want to send the messages out
5. Start subscriptionService.py

>> Since 2022 Google has made changes to their security policy, so if you use gmail as your mail server you will need to add 2FA and generate an app password
