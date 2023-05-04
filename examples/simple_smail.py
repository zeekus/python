import smtplib
from email.mime.text import MIMEText

sender = 'sender@tld'
receivers = ['receiver1@tld', 'receiver2@tld']
body_of_email = 'The body of the email'
msg = MIMEText(body_of_email, 'plain')
# html_body_of_email = '<h1>The html body of the email</h1>'
# msg = MIMEText(html_body_of_email, 'html')
msg['Subject'] = 'The Subject'
msg['From'] = sender
msg['To'] = ','.join(receivers)

s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
s.login(user = 'username', password = 'password')
s.sendmail(sender, receivers, msg.as_string())
s.quit()
