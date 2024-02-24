import random
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def send_email_aws_ses(subject, html_content, sender_name, sender_email, to):
    ses = boto3.client('ses', region_name=settings.AWS_S3_REGION)

    email_message = {
        'Subject': {'Data': subject},
        'Body': {
            'Html': {
                'Data': html_content,
            }
        }
    }

    source = f"{sender_name} <{sender_email}>"
    destination = {
        'ToAddresses': [f"{recipient['name']} <{recipient['email']}>" for recipient in to],
    }

    try:
        response = ses.send_email(
            Source=source,
            Destination=destination,
            Message=email_message
        )

        print("Email sent! Message ID:", response['MessageId'])
        return True

    except ClientError as e:
        print(f"Error sending email: {e.response['Error']['Message']}")
        return False
