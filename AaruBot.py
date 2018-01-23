from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/webhook',methods=['GET'])
def verify():
    print request.data
    VERIFY_TOKEN = 'Aaru'
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    print mode, token, challenge
    if mode and token :
        if mode == 'subscribe' and token == VERIFY_TOKEN :
            return challenge,200
        else :
            return 'Forbidden',403
    return 'Hello world'

@app.route('/webhook',methods= ['POST'])
def webhook():
    body = request.get_json()
    print body
    if body['object'] == 'page' :
        for entry in body['entry']:
            webhook_event = entry['messaging'][0]
            return 'EVENT_RECEIVED',200
    else :
        return 404

if __name__ == '__main__':
    app.run()
