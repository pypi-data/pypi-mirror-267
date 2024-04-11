# Third-party Libraries
import smtplib
from email.message import EmailMessage
from lytils.surfshark import Surfshark


class Email:
    def __init__(self, smtp, credentials, surfshark_path: str = "", notify: str = ""):
        """
        :param smtp dict:
            Expects 'server' key (ex. 'smtp.example.com')
            Expects 'port' key (default: 587)
        :param credentials dict:
            Expects 'email' key; email used to send the email
            Expects 'password' key; password for sender's email
        :param notify string:
            Instead of having to pass a recipient email to
            send_email every time, you can declare a default
            email, and use notify() to send email to that recipient
        """
        self.__smtp = smtp

        # Set port by default if not specified
        if "port" not in smtp:
            self.__smtp["port"] = 587

        self.__surfshark = None
        if surfshark_path:
            self.__surfshark = Surfshark(surfshark_path)

        self.__creds = credentials
        self.__notify = notify
        self.__server = None

    def start_server(self):
        # Kill surfshark as it blocks email SMTP and Selenium connections
        self.__surfshark.kill()
        # Connect to the SMTP server
        self.__server = smtplib.SMTP("smtp.gmail.com", 587)
        # self.__server = smtplib.SMTP(smtp['server'], smtp['port'])
        # self.__server.ehlo()
        self.__server.starttls()
        self.__server.login(self.__creds["email"], self.__creds["password"])

    def send_email(self, recipient, subject, message):
        # Create the email
        msg = EmailMessage()
        msg.set_content(message)
        msg["subject"] = subject
        msg["to"] = recipient
        msg["from"] = self.__creds["email"]

        # Send the email
        self.__server.sendmail(self.__creds["email"], recipient, msg.as_string())

    def notify(self, subject, message):
        if self.__notify:
            self.send_email(self.__notify, subject, message)

    def quit(self):
        if self.__server:
            self.__server.quit()

            # Restart surfshark to stay safe
            if self.__surfshark:
                self.__surfshark.start()
