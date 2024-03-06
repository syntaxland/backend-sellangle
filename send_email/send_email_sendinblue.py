import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import base64 
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def send_email_sendinblue(subject, html_content, to):
    try:
        # Email Sending API Config
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        sender_name = settings.EMAIL_SENDER_NAME
        sender_email = settings.EMAIL_HOST_USER
        sender = {"name": sender_name, "email": sender_email}

        # Sending email
        print(f"\nSending email with subject: {subject} ...")
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject
        )

        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent successfully with subject: {subject}")
        return True
    except ApiException as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_email_with_attachment_sendinblue(subject, html_content, to, attachment_data=None, attachment_name="attachment.pdf"):
    try:
        # Email Sending API Config
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        sender_name = settings.EMAIL_SENDER_NAME
        sender_email = settings.EMAIL_HOST_USER
        sender = {"name": sender_name, "email": sender_email}

        # Sending email
        print(f"\nSending email with subject: {subject} ...")
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject
        )

        # Attach the PDF to the email if provided
        if attachment_data:
            encoded_attachment = base64.b64encode(attachment_data).decode('utf-8')
            pdf_attachment = sib_api_v3_sdk.SendSmtpEmailAttachment(
                content=encoded_attachment,
                name=attachment_name 
            )
            send_smtp_email.attachment = [pdf_attachment]

        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent successfully with subject: {subject}")
        return True
    except ApiException as e:
        print(f"Error sending email: {str(e)}")
        return False
