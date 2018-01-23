from flask import Flask, request
import os
from pymessenger import Bot, Element

app = Flask(__name__)
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/',methods=['GET'])
def verify():
    print(request.data)
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    print(mode, token, challenge)
    if mode and token :
        if mode == 'subscribe' and token ==  VERIFY_TOKEN:
            return challenge,200
        else :
            return 'Forbidden',403

@app.route('/',methods= ['POST'])
def webhook():
    body = request.get_json()
    print(body)
    if body['object'] == 'page' :
        entries = body['entry']
        for entry in entries :

            messaging = entry['messaging']
            for messaging_event in messaging:

                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                print(sender_id, recipient_id)

                if messaging_event['message']:
                    # HANDLE NORMAL MESSAGES HERE
                    if messaging_event['message']['text']:
                        query = messaging_event['message']['text']
                        handleMessage(sender_id, query)

            return 'SEND_OK',200
    else :
        return 404

def handleMessage(sender_PSID, rcv_msg):
    resp = 'The message you sent is {}'.format(rcv_msg)
    elements = []
    buttons = [{
                "type": "postback",
                "title": "Yes!",
                "payload": "yes",
              },
              {
                "type": "postback",
                "title": "No!",
                "payload": "no",
              }]
    element = Element(title="test", subtitle="subtitle", buttons= buttons)
    elements.append(element)
    callSendAPI(sender_PSID, elements)

def handlePostback(sender_PSID, rcv_postback):
    resp = 'The message you sent is {}'.format(rcv_postback)
    callSendAPI(sender_PSID, resp)

def callSendAPI(sender_PSID, response):
    bot.send_text_message(sender_PSID, response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug= True)
