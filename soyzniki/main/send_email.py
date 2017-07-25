import smtplib
from email.mime.text import MIMEText


def send_email(you, subject, message):
    me = 'site@soyzniki.ru'
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you
    s = smtplib.SMTP('soyzniki.ru', 587)
    s.connect('soyzniki.ru', 587)
    s.starttls()
    s.ehlo()
    s.login(me, 'LbvfbDbnz2Xfirb')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
