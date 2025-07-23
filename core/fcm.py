import firebase_admin
from firebase_admin import credentials, messaging
import os
import logging

# Path to your service account key file
SERVICE_ACCOUNT_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "firebase-service-account.json")

# Initialize the Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

def send_fcm_notification(token, title, body, data=None):
    try:
        logging.info(f"[FCM] Sending notification to token: {token}, title: {title}, body: {body}, data: {data}")
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            data=data or {},
        )
        response = messaging.send(message)
        logging.info(f"[FCM] Notification sent successfully: {response}")
        return response
    except Exception as e:
        logging.error(f"[FCM] Error sending notification: {e}")
        return None 