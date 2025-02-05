import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def send_email(to_email: str, subject: str, body: str, file_path: str):
    msg = MIMEMultipart()    #kreiranje instance za mail poruku
    msg['From'] = 'i.stojic02@gmail.com'
    msg['To'] = to_email
    msg['Subject'] = subject

    body_part = MIMEText(body, 'plain')   #kreira se objek sa sadrzajem maila
    msg.attach(body_part)   #dodavanje 

    with open(file_path, 'rb') as attachment:
        part = MIMEText(attachment.read(), 'base64', 'utf-8')     #cita se cijeli sadrzaj filea kodira file u base64
        part.add_header('Content-Disposition', 'attachment', filename=file_path)
        msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('i.stojic02@gmail.com', '')
            server.sendmail(msg['From'], msg['To'], msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
