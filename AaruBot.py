from flask import Flask, request
from pymessenger import Bot
from modules.greet import *
from modules.jokes import *
from modules.feedback import *
from modules.news import *
from modules.wiki import *
from modules.quotes import *
from modules.songs import *


app = Flask(__name__)
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
SRCDIR = os.path.dirname(os.path.abspath(__file__))
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
bot = Bot(PAGE_ACCESS_TOKEN,base_url= 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN))

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
                print(messaging_event)

                if messaging_event['message']:
                    if messaging_event['message']['text']:
                        query = messaging_event['message']['text']
                        handleMessage(sender_id, query)

                    elif messaging_event['postback']:
                        query = messaging_event['postback']['payload']
                        handlePostback(sender_id, query)
            return 'SEND_OK',200
    else :
        return 404

def handleMessage(sender_PSID, msg):
    print(msg)
    txt = msg.split(' ',1)
    fin_resp = ''
    if txt[0] == '/jokes':
        fin_resp = get_jokes()
    elif txt[0] == '/bugs':
        if len(txt) != 1:
            bug(txt[1])
            bot.send_text_message(sender_PSID, txt[1])
            fin_resp="Thanks for the help"
        else:
            fin_resp = "Please use following format\n/bugs Bug-Issue"
    elif txt[0] == '/suggestions':
        if len(txt) != 1:
            suggestions(txt[1])
            bot.send_text_message(sender_PSID, txt[1])
            fin_resp = "Thanks for the input"
        else:
            fin_resp= "Please use following format\n/suggestions Your-Suggestion"
    elif txt[0] == '/memes':
        print(SRCDIR)
        path = os.path.join(SRCDIR,'meme.jpg')
        resp = get_memes()
        if resp=="done":
            bot.send_image(sender_PSID, path)
    elif txt[0] == '/bugdata':
        fin_resp = getBugData()
    elif txt[0] == '/sugdata':
        fin_resp= getSuggestionData()
    elif txt[0] == '/short':
        if len(txt) != 1:
            fin_resp= "Shortened URL : "+shorten_url(txt[1])
        else:
            fin_resp= "Please use following format\n/short LONGURL"
    elif txt[0] == '/news':
        fin_resp= get_news()
        for i in range(3):
            bot.send_text_message(sender_PSID, fin_resp[i])
        bot.send_button_message(sender_PSID,buttons=[{
            "type": "postback",
            "title": "Yes",
            "payload": "yes"}],
            text= 'Want more ??')
        fin_resp=''
    elif txt[0] == '/wiki':
        if len(txt) != 1:
            fin_resp=get_wiki(txt[1])
        else:
            fin_resp = "Please use following format\n/wiki Query"
    elif txt[0] == '/quotes':
        fin_resp = get_quotes()
    elif txt[0] == '/contact':
        if len(txt)!=1:
            bot.send_text_message(1295205007247180,"Contact message from "+str(sender_PSID))
            fin_resp = "You will be contacted soon"
        else:
            fin_resp = "No message provided"
    elif txt[0].lower() in ['hi','hello','hey']:
        fin_resp = 'Hi \nLets have fun :D'
    elif txt[0].lower() in ['thanks','bye','love']:
        fin_resp = "Bubyee :D"
    elif txt[0] == '/lyrics':
        if len(txt)!=1:
            fin_resp = find_lyrics(txt[1])
            for i in fin_resp[:3]:
                bot.send_text_message(sender_PSID,i.split('\n')[0]+"\nby "+i.split('\n')[1])
            buttons = [
                {
                    "type": "postback",
                    "title": "Download 1st option",
                    "payload": fin_resp[0].split('\n')[2]
                },
                {
                    "type": "postback",
                    "title": "Download 2nd option",
                    "payload": fin_resp[1].split('\n')[2]
                },
                {
                    "type": "postback",
                    "title": "Download 3rd option",
                    "payload": fin_resp[2].split('\n')[2]
                }
            ]
            bot.send_button_message(sender_PSID, "Choose to get lyrics",buttons)
            fin_resp=''
        else:
            fin_resp = "Please provide songname"
    elif txt[0] == '/song':
        if len(txt)!=1:
            fin_resp = find_song(txt[1])
            for i in fin_resp[:3]:
                bot.send_text_message(sender_PSID, i)
            buttons = [
                {
                    "type": "postback",
                    "title": "Download 1st option",
                    "payload": fin_resp[0]+' song'
                },
                {
                    "type": "postback",
                    "title": "Download 2nd option",
                    "payload": fin_resp[1]+' song'
                },
                {
                    "type": "postback",
                    "title": "Download 3rd option",
                    "payload": fin_resp[2]+' song'
                }
            ]
            bot.send_button_message(sender_PSID, "Select song to download", buttons)
            fin_resp = ''
    else:
        ## Type is unknown
        fin_resp = welcome()
    if fin_resp != '':
        bot.send_text_message(sender_PSID, fin_resp)
    return "Ok"


def handlePostback(sender_PSID, rcv_postback):
    print(rcv_postback)
    bot.send_text_message(sender_PSID, 'In handle postback')
    # if rcv_postback== "morenews":
    #     bot.answerCallbackQuery(callback_query_id=query_id, text='Loading More News')
    #     response = get_news()[2:]
    #     bot.sendMessage(from_id, random.choice(response))
    #
    #     keyboardNews = InlineKeyboardMarkup(inline_keyboard=[
    #         [InlineKeyboardButton(text='More News', callback_data="morenews")]
    #     ])
    #     bot.sendMessage(chat_id=from_id, text="Click below for more", reply_markup=keyboardNews)
    # else:
    #     query, type = query_data.split(' ')
    #     if type == 'song':
    #         bot.answerCallbackQuery(callback_query_id=query_id, text="Fetching your song")
    #         name = download_song(query_data.split(' ')[0])
    #         bot.answerCallbackQuery(callback_query_id=query_id, text="Donwloading your song")
    #         song = open(name, 'rb')
    #         bot.sendAudio(chat_id=from_id, audio=song)
    #         song.close()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug= True)
