#!/usr/bin/python
#file: aws_email_function.py
#description: send email using aws sasl - not the most reliable

import smtplib, ssl #for email 

def send_email_warning(sasl_user,sasl_pass,sent_from,sent_to,subject,sent_body):
  email_text = """\
From: %s
To: %s
Subject: %s
%s
""" % (sent_from, ", ".join(sent_to), subject, sent_body)
  # my_from=("From: <" + smail + ">\n")
  # my_to=("To: <" + rmail + ">\n")
  # Subject=("Subject: warning message\n\n")
  # message=(str(my_from) + str(my_to) + str(Subject) + str(warn_message) ) #created the header and message info
  # print(message)

  smtp_server = "email-smtp.us-east-1.amazonaws.com"
  context = ssl.create_default_context()
  try:
      server = smtplib.SMTP(smtp_server,587,context )
      server.connect(smtp_server)
      server.starttls(context=context) # Secure the connection
      server.login(sasl_user,sasl_pass)
      server.sendmail(sent_to,sent_from,email_text)

  except Exception as e:
    print ("error: %s" % e ) 
  finally:
    server.quit() 



sasl_user="BKIAVVANJJNTLSMPNFZG"                 #an example not a valid one
sasl_pass="SOme1cxCJbk9MqWxVK7in/ABZZZZAABBBBAA" #an example not valid
subject="some subject"
warn_message="This is a warning"

sent_from="sender@myhost.com"
send_to="receiver@myhost.com"
send_email_warning(sasl_user,sasl_pass,sent_from,send_to,subject,warn_message)

