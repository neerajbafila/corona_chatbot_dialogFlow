from flask import Flask, request, make_response
from flask_cors import cross_origin
import os
from flask_mail import Mail
import json
from logger import logger
from flask_mail import Mail
from templates.sendEmail import  EmailSender



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
@app.route('/webhook', methods=['POST', 'GET'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)

    # response variable
    print(req)

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


@app.route('/processRequest', methods=['POST'])
def processRequest(req):

    session_id = req.get('responseId')

    result = req.get('queryResult')
    parameters = result.get("parameters")
    user_name = parameters.get('user_name')
    city_name = parameters.get('geo-city')
    user_email = parameters.get('user_email')
    print(user_email)
    from_name = params['gmail_user']
    intent = result.get("intent").get('displayName')

    if intent == 'covid-19_BasicInfo':

        # mail.send_message(sender=from_name, recipients=user_email,
        #                   body="Hello this is testing")

        email_message = "Kindly find below details"
        email_sender = EmailSender()
        email_sender.send_email_to_student(user_email, email_message)
        fulfillmentText = "We have sent the course syllabus and other relevant details to you via email." \
                          " An email has been" \
                          " sent to the Support Team with your contact information, you'll be " \
                          "contacted soon. Do you have further queries?"
        return {
            "fulfillmentText": fulfillmentText
        }


if __name__ == '__main__':
    # app.run(debug=True)

    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')


