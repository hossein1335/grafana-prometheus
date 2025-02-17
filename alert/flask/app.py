import logging
from flask import Flask, request
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.json

    username = ''
    password = ''
    domain = 'pdn'
    to = 'phone-number,phone-number'
    text = data['alerts'][0]['annotations']['summary']  

    url = 'https://sms.com/api/sms/v1'
    params = {
        'username': username,
        'password': password,
        'domain': domain,
        'service': 'enqueue',
        'from': '00745532',
        'to': to,
        'text': text
    }

    try:
        response = requests.get(url, params=params)

        app.logger.debug(f"SMS API Response status: {response.status_code}")
        app.logger.debug(f"SMS API Response text: {response.text}")

        if response.status_code == 200:
            return 'SMS sent successfully', 200
        else:
            return f'Failed to send SMS: {response.text}', response.status_code

    except Exception as e:
        app.logger.error(f"sms Error occurred: {e}")
        return 'sms Internal Server Error', 500

@app.route('/send-bale', methods=['POST'])
def send_bale():

    data=request.json
    text_bale = data['alerts'][0]['annotations']['summary']
    chat_id="4957097031"

    url_bale = 'https://tapi.bale.ai/bot199:9kOurEgoMeEVNRP/sendMessage'
    params_bale= {
        'chat_id': chat_id,
        'text' : text_bale
    }
    
    try:

        response_bale = requests.post(url_bale, params=params_bale)

        app.logger.debug(f"bale API Response status: {response_bale.status_code}")
        app.logger.debug(f"bale API Response text: {response_bale.text}")
    
        if response_bale.status_code == 200:
            return 'bale sent successfully', 200
        else:
            return f'failed to send bale: {response_bale.text}', response_bale.status_code

    except Exception as e:
        app.logger.error(f"bale Error occurred: {e}")
        return 'bale Internal Server Error', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


