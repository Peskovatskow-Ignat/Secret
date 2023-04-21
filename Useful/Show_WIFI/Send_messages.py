from Show_pointPassword import main
import smtplib
import os

email = os.environ["your_email"]
password = os.environ["send_passwd"]
send_email = os.environ["email"]

sender_email = send_email
sender_password = password
recipient_email = email
subject = "Show Password on Wi-Fi point"
email_text = main()

message = f"From: {sender_email}\nTo: {recipient_email}\nSubject: {subject}\n\n{email_text}"

with smtplib.SMTP_SSL("smtp.yandex.ru", 465) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email,
                    message.format(sender_email, recipient_email, subject, email_text).encode("utf-8"))
