import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = "maingacecilia@gmail.com"
EMAIL_PASSWORD = "lyhf uoox znzz rjpu"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

def send_email_alert(engine_id, predicted_value, threshold_min, threshold_max, recipient_email):
    try:
        msg = EmailMessage()
        msg["Subject"] = "⚠️ EGT Hot Day Margin Alert!"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email
        msg.set_content(f"""
Warning! The predicted EGT Hot Day Margin for Engine Serial Number {engine_id} has exceeded safe limits.

Predicted Value: {float(predicted_value):.2f}°C
Safe Range: {threshold_min}°C - {threshold_max}°C
Review the data for the necessary maintenance action.

Regards

Predictive Maintenance Team
""")
        
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        print(f"✅ Email sent successfully to {recipient_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication error: Check your email and password.")
    except smtplib.SMTPRecipientsRefused:
        print(f"❌ Email refused: Invalid recipient {recipient_email}")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return False
