#source https://www.courier.com/blog/three-ways-to-send-emails-using-python-with-code-tutorials/
import smtplib 
try: 
    #Create your SMTP session 
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 

   #Use TLS to add security 
    smtp.starttls() 

    #User Authentication 
    smtp.login("sender_email_id","sender_email_id_password")

    #Defining The Message 
    message = "Message_you_need_to_send" 

    #Sending the Email
    smtp.sendmail("sender_email_id", "receiyer_email_id",message) 

    #Terminating the session 
    smtp.quit() 
    print ("Email sent successfully!") 

except Exception as ex: 
    print("something went wrong...")
