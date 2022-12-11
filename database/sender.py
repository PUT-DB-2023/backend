import smtplib, ssl
from email.message import EmailMessage

class EmailSender:

    def send_email_poczta(self, random_password):

        # return new exception with method not yet implemented

        # return Exception("Method not yet implemented")

        port = 587  # For starttls
        smtp_server = "poczta.student.put.poznan.pl"
        sender_email = "jakub.p.wrobel@student.put.poznan.pl"
        receiver_email = "jakub.p.wrobel@student.put.poznan.pl"
        password = "KUBussiek1531"
        message = """\
        Subject: Hi there

        This message is sent from Python."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)


    def send_email_gmail(self, target_email, random_password):

        msg = EmailMessage()
        msg.set_content('Your new password is: {}'.format(random_password))

        msg['Subject'] = 'You have just received a new password'
        msg['From'] = "putdb2023@gmail.com"
        msg['To'] = target_email

        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("putdb2023@gmail.com", "zutwbrlimiopqovl")
        server.send_message(msg)
        server.quit()

        
sender = EmailSender()
sender.send_email_gmail("test")

