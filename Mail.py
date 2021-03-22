import smtplib, ssl, getpass, requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
res = requests.get('https://www.bnr.ro/nbrfxrates.xml')
soup = BeautifulSoup(res.content, 'html.parser')
page = soup.find('cube')
rate_currency = page.find('rate',{'currency':'EUR'}).text
port = 465
password = getpass.getpass("Password: ")
value = rate_currency
sender_email = "Vlad.Radutoiu99@gmail.com"
receiver_email = "alexandru.vilcea@smartouch.ro"
message = MIMEMultipart("alternative")
message["Subject"] = "Schimb valutar"
message["From"] = sender_email
message["To"] = receiver_email
text = """\
Curs RON-EURO: """
html = """\
<html>
  <body>
   <p>Curs RON_EURO :{value}</p>
  </body>
</html>
"""
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)
context = ssl.create_default_context()
for i in range(5):
    res = requests.get('https://www.bnr.ro/nbrfxrates.xml')
    soup = BeautifulSoup(res.content, 'html.parser')
    page = soup.find('cube')
    rate_currency = page.find('rate',{'currency':'EUR'}).text
    value = rate_currency
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
        server.login("Vlad.Radutoiu99@gmail.com",password)
        server.sendmail(sender_email, receiver_email,message.as_string().format(value=value))
    time.sleep(60)