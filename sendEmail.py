import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
# from config_reader import ConfigReader



class EmailSender():
    with open('config.json', 'r') as c:
        params = json.load(c)['params']

    def send_email_to_user(self, user_email, message, city_name):
        try:
            self.message = str(message)
            # self.message = "total confirm cases in {} are {}".format(city_name, self.message)
            self.user_email = user_email

            # instance of MIMEMultipart
            self.msg = MIMEMultipart()

            # storing the senders email address
            self.msg['From'] = self.params['gmail_user']

            # storing the receivers email address
            # self.msg['To'] = ",".join(user_email)
            self.msg['To'] = self.user_email


            # storing the subject
            self.msg['Subject'] = self.params['EMAIL_SUBJECT']

            # string to store the body of the mail
            #body = "This will contain attachment"
            body=self.message

            # attach the body with the msg instance
            self.msg.attach(MIMEText(body))


            # instance of MIMEBase and named as p
            self.p = MIMEBase('application', 'octet-stream')


            # creates SMTP session
            self.smtp = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            self.smtp.starttls()

            # Authentication
            self.smtp.login(self.msg['From'], self.params['gmail_pass'])

            # Converts the Multipart msg into a string
            self.text = self.msg.as_string()
            print(self.text)

            # sending the mail
            self.smtp.sendmail(self.msg['From'], self.msg['To'], self.text)


            # terminating the session
            self.smtp.quit()
        except Exception as e:
            print('the exception is '+str(e))
# email_user = 'neerajbafila@gmail.com'
# ob = EmailSender()
# from templates.CallExternalApi import  CallExternalApi
# o = CallExternalApi()
# ll = o.featch_district_data('Nagpur')
# conf= ll['confirmed']
# conf = "total confirm cases in Nagpur are "+ str(conf)
# ob.send_email_to_student(email_user, conf)