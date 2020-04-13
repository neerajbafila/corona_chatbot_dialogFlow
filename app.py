from flask import Flask, request, make_response
from flask_mail import Mail
import json
from logger import logger
from flask_mail import Mail


app = Flask(__name__)
with open('config.json', 'r') as c:
    params = json.load(c)['params']

app.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    # MAIL_USE_TLS=True,
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_pass'])
)

mail = Mail(app)


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@app.route('/', methods=['POST', 'GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # response variable

    res = processRequest(req)


def processRequest(req):

    session_id = req.get('responseId')

    result = session_id.get('queryResult')
    user_name = result.get('user_name')
    city_name = result.get('geo-city')
    user_email = result.get('user_email')
    from_name = params['gmail_user']
    intent = result.get('displayName')

    if intent == 'covid-19 _BasicInfo':

        mail.send_message(sender=from_name, recipients=user_email,
                          body="Hello this is testing")
        return ("testing")


if __name__ == '__main__':
    app.run()
    # port = int(os.getenv('PORT', 5000))
    # print("Starting app on port %d" % port)
    # app.run(debug=False, port=port, host='0.0.0.0')


