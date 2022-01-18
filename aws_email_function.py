#!/usr/bin/python
#file: aws_email_function.py
#description: send email using aws sasl 

def send_email_warning(sasl_user=my_sasl_id,sasl_pass=my_sasl_pass,smail,rmail,warn_message):
  my_from=("From: <" + smail + ">\n")
  my_to=("To: <" + rmail + ">\n")
  Subject=("Subject: warning message\n\n")
  message=(str(my_from) + str(my_to) + str(Subject) + str(warn_message) )
  print(message)

  smtp_server = "email-smtp.us-east-1.amazonaws.com"
  context = ssl.create_default_context()
  try:
      server = smtplib.SMTP(smtp_server,587,context )
      server.connect(smtp_server)
      server.starttls(context=context) # Secure the connection
      server.login(sasl_user, sasl_password)
      server.sendmail(smail,rmail, message)

  except Exception as e:
    print ("error: %s" % e ) 
  finally:
    server.quit() 



sasl_id="BKIAVVANJJNTLSMPNFZG"
sasl_pass="SOme1cxCJbk9MqWxVK7in/ABZZZZAABBBBAA"
warn_message="This is a warning"

smail="sender@myhost.com"
rmail="receiver@myhost.com"
send_email_warning(sasl_id,sasl_pass,smail,rmail,warn_message)
