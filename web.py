import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def email(receiver_email,content):
    sender_email = "weberwebercode@gmail.com"
    port = 465  # For SSL
    password ='yourpassword'
    subject = "This is an warning email from monitorning system"
    body = "Warning: "+content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    filename = "plot.jpg"


    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    # Create a secure SSL context
    context = ssl.create_default_context()
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()



    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("weberwebercode@gmail.com", password)
        server.sendmail(sender_email, receiver_email, text)
