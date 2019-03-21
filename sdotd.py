# !python 3
import datetime
import email.message
import smtplib
import sys

import bs4
import requests

from config import password
from config import emailAddress
from config import smtpLibrary
from config import smtpPort

url = 'https://www.musiciansfriend.com/stupid'
res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

feature = soup.select('.feature-title')[0].select('h2')[0].text
feature = feature.replace('\n', ' ')
feature = feature.replace(u'\xa0', '').encode('utf-8')

oldPrice = soup.select('.regular-price')[0].text
oldPrice = oldPrice.replace('\n', '')
oldPrice = oldPrice.replace(u'\xa0', ' ').encode('utf-8')

newPrice = soup.select('.feature-price')[0].text
newPrice.replace('\n', '')
newPrice = newPrice.replace(u'\xa0', ' ').encode('utf-8')

emailContent = """
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </head>
        <body>
        
        Item:  """ + str(feature.decode()) + """<br/>
        Was:  """ + str(oldPrice.decode()) + """<br/>
        Now: """ + str(newPrice.decode()) + """<br/>
        
        <br/><br/>
        <a href='https://www.musiciansfriend.com/stupid'>Link</a>
        
        </body></html>
"""

subject = "Stupid Deal of the Day " + datetime.datetime.now().strftime("%m-%d-%y %H:%M%p")
msg = email.message.Message()
msg['SUBJECT'] = subject
msg['From'] = emailAddress
msg['To'] = emailAddress
msg.add_header('Content-Type', 'text/html')
msg.set_payload(emailContent)

# start the sending of emails
try:
    smtpObj = smtplib.SMTP(smtpLibrary, smtpPort)
except smtplib.SMTPException as e:
    smtpObj.quit()
    sys.exit()

smtpObj.ehlo()
smtpObj.starttls()

try:
    smtpObj.login(emailAddress, password)
    smtpObj.send_message(msg)
except smtplib.SMTPAuthenticationError as e:
    smtpObj.quit()

sys.exit()