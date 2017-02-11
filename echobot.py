import time
import json
import requests
import urllib


TOKEN = '320053880:AAH-nr-2Je_tgUpaPm4GIyMnHk0iIloNzEU'
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)


# collect url
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


# parse url
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


# collects messages sent to the bot every 100 seconds
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
# dont show any messages with smaller ids
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


# collect last mesage sent to the bot
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


# sends the message contained in text to chat_id
def send_message(text, chat_id):
	text = urllib.parse.quote_plus(text)
	url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
	get_url(url)


# return highest id of all recieved updates
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# repeat every message sent to the bot
def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


# infinite loop
# collect last sent text and echo it back, check every 0.5 seconds
def main():
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
