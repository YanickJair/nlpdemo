import json

with open("/etc/nlp-mail-config.json") as f:
    config = json.load(f)       

def send_mail_tls(message, fullname, user_email):
    try:
        import smtplib, ssl
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        port = config.get("MAIL_PORT")  # For starttls
        smtp_server = config.get("MAIL_SERVER")
        sender_email = config.get("MAIL_USERNAME")
        receiver_email = config.get("TO_EMAIL")
        password =config.get("MAIL_PASSWORD")
        
        SUBJECT = "NLP DEMO WEB APP - {0}".format(fullname)

        message = MIMEMultipart("alternative")
        message["Subject"] = SUBJECT
        message["From"] = sender_email
        message["To"] = receiver_email
        html = """
            <html>
                <body>
                    <p>Name: {0} </p>
                    <p>Email: {1} </p>
                    <p>Message: {2} </p>
                </body>
            </html>""".format(fullname, user_email, message)
        message.attach(MIMEText(html, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except:
        raise