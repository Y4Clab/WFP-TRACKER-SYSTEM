import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail.backends.base import BaseEmailBackend
from django.template.loader import render_to_string
from dotenv import dotenv_values
from jinja2 import Environment, FileSystemLoader

config = dotenv_values(".env")

class CustomEmailBackend(BaseEmailBackend):
    
    def __init__(self, email_messages, html_template):
        self.email_messages = email_messages
        self.html_template = html_template
    
    @classmethod
    def send_messages(cls, email_messages,html_template):
        EMAIL_HOST = config['EMAIL_HOST']
        EMAIL_PASSWORD = config['EMAIL_HOST_PASSWORD']
        EMAIL_USER = config['EMAIL_HOST_USER']
        EMAIL_PORT = config['EMAIL_PORT']
        EMAIL_USE_TLS = config['EMAIL_USE_TLS']
        DEFAULT_FROM_EMAIL = config['DEFAULT_FROM_EMAIL']
                
        html_content = render_to_string(html_template, {'data': email_messages})
        
        # Create a Jinja2 environment with the HTML template
        env = Environment(loader=FileSystemLoader(html_template))
        template = env.from_string(html_content)

        # Render the template with the provided context
        rendered_template = template.render({'data': email_messages})
    
        # Create a multipart message and set the headers
        msg = MIMEMultipart()
        msg['From'] = DEFAULT_FROM_EMAIL
        msg['To'] = email_messages['receiver_details']
        msg['Subject'] = email_messages['subject']

        # Attach the rendered HTML content as the email body
        msg.attach(MIMEText(rendered_template, 'html'))
        
        # Create a secure SSL/TLS connection to the SMTP server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        # server.set_debuglevel(1)
        if EMAIL_USE_TLS=="True":
            server.starttls()

        # Login to the email account
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        # Send the email
        server.sendmail(DEFAULT_FROM_EMAIL, email_messages['receiver_details'], msg.as_string())

        # Disconnect from the server
        server.quit()

        return True