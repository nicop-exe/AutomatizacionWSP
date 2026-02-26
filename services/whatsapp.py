import os
import requests

def send_whatsapp_message(to_number: str, message: str):
    """
    Sends a text message using Meta's Cloud API.
    """
    token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")
    
    if not token or not phone_number_id:
        print("WhatsApp credentials missing in .env")
        return False
        
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"Message sent successfully to {to_number}")
        return True
    else:
        print(f"Failed to send message: {response.text}")
        return False
