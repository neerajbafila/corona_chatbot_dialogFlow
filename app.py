from flask import Flask, request, make_response
from flask_cors import cross_origin
import os
from flask_mail import Mail
import json
from logger import logger
from flask_mail import Mail
# from templates.sendEmail import EmailSender
# from templates.CallExternalApi import CallExternalApi
from sendEmail import EmailSender
from CallExternalApi import CallExternalApi


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

def featch_data(temp):
    active = []
    confirmed = []
    for i in temp.keys():
        if i == 'active':
            active.append(temp['active'])
        if i == 'confirmed':
            confirmed.append(temp['confirmed'])
    return active, confirmed


@app.route('/processRequest', methods=['POST'])
def processRequest(req):

    session_id = req.get('responseId')

    result = req.get('queryResult')
    parameters = result.get("parameters")
    user_name = parameters.get('user_name')
    city_name = parameters.get('city_name')
    user_email = parameters.get('user_email')
    state_name = parameters.get('state_name')
    # print(user_email)
    from_name = params['gmail_user']
    intent = result.get("intent").get('displayName')
    print(intent)


    if intent == 'covid-19_StateInfo':

        call_external_api = CallExternalApi()

        temp = call_external_api.featch_state_data(state_name)
        active, confirmed = featch_data(temp)
        print(active)
        print(confirmed)
        fulfillmentText = "{} has {} active cases and {} confirm cases ".format(state_name, active[0], confirmed[0])
        email_message = fulfillmentText
        print(fulfillmentText)
        email_sender = EmailSender()
        email_sender.send_email_to_user(user_email, email_message, state_name)

        return {
            "fulfillmentText": fulfillmentText
        }

    if intent == 'covid-19_DistrictInfo':



        call_external_api = CallExternalApi()

        fulfillmentText = call_external_api.featch_district_data(city_name)
        fulfillmentText = "total confirm cases in {} are {}".format(city_name, fulfillmentText['confirmed'])
        email_message = fulfillmentText
        email_sender = EmailSender()
        email_sender.send_email_to_user(user_email, email_message, city_name)

        return {
            "fulfillmentText": fulfillmentText
        }


if __name__ == '__main__':
    # app.run(debug=True)

    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')


