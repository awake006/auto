import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr

from api.log import console_logger


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(excel, email):
    msg = MIMEMultipart()
    msg['From'] = _format_addr('test_team <%s>' % email.get("from"))
    msg['To'] = _format_addr('en <%s>' % email.get("to_address"))
    msg['Subject'] = "Interface test report"
    content = MIMEText("Latest interface test report", 'plain', 'utf-8')
    msg.attach(content)
    basename = os.path.basename(excel)
    fp = open(excel, 'rb')
    att = MIMEApplication(fp.read())
    att["Content-Type"] = 'application/octet-stream'
    att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', basename))
    msg.attach(att)

    server = smtplib.SMTP(email.get("smtp_server"), 25)
    server.set_debuglevel(1)
    server.login(email.get("from"), email.get("password"))
    server.sendmail(email.get("from"), [email.get("to_address")], msg.as_string())
    server.quit()
    console_logger.info('Mail sent successfully')
