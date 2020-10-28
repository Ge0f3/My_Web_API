
import requests
import json
from flask import request
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from services.config import RequiredConstants as RC


class ServiceLayer:

    @staticmethod
    def send_email(data):
        message = Mail(
            from_email='geo.geofe@icloud.com',
            to_emails='geoffrey.geofe@gmail.com',
            subject="Howdy !! Website Email Enquiry",
            html_content="""<html>
                            <head></head>
                            <body>
                            <h1>Email Enquiry from Ultrasoft.io</h1>
                            <p> Contacted Person - {} </p>
                            <p> Email Address - {} </p>
                            <p> Message - {} </p>
                            </body>
                            </html>
                                        """.format(data['name'], data['email'], data['msg'])
        )
        gretting_message = Mail(
            from_email='geo.geofe@icloud.com',
            to_emails=data['email'],
            subject="Howdy !! Thanks for Email Enquiry",
            html_content="""<html>
                            <head></head>
                            <body>
                            <h1>Thank you for your Email Enquiry </h1>
                            <p> I am Geoffrey :). Thank you for visiting my website https://geoffrey.works. I will be in touch with you shortly.</p>
                            <p>Thanks,<br/>Geoffrey<br/>https://geoffrey.works</p>
                
                            </body>
                            </html>
                                        """
        )
        sg = SendGridAPIClient(RC.SENDGRID_API_KEY)
        response = sg.send(message)
        response_two = sg.send(gretting_message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return response
