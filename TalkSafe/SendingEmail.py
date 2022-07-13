import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def SendEmail(contacts):
    subject = 'ALERT! PERSON IN DANGER!'
    from_addr = 'testias536@gmail.com'
    body = 'User is in DANGER!'

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ", ".join(contacts)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('testias536@gmail.com', 'clphrtrraqtgjorl')
    MsgText = msg.as_string()
    s.sendmail(from_addr, contacts, MsgText)
    s.quit()


def SendGPS(lat, lon, contacts):
    subject = 'User GPS Active'
    from_addr = 'testias536@gmail.com'
    body = 'User latitude: ' + lat + ', longitude: ' + lon

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ", ".join(contacts)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('testias536@gmail.com', 'clphrtrraqtgjorl')
    MsgText = msg.as_string()
    s.sendmail(from_addr, contacts, MsgText)
    s.quit()
