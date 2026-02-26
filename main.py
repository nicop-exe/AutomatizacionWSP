import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from services.whatsapp import send_whatsapp_message
from services.ai import analyze_lead
from services.sheets import log_lead

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory storage for pending approvals (in reality, you'd use a DB like SQLite for persistence)
pending_responses = []


@app.get("/")
def read_root():
    return {"status": "Car Seller Agent is running"}

# --- WHATSAPP WEBHOOK --- 
@app.get("/webhook")
def verify_webhook(request: Request):
    """
    Meta uses this endpoint to verify your webhook URL.
    """
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "mi_token_secreto_personalizado")
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == verify_token:
            print("Webhook verified successfully!")
            return int(challenge)
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
    return {"message": "Invalid request"}


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Meta sends incoming WhatsApp messages here.
    """
    body = await request.json()
    
    # 1. Parse incoming message
    try:
        if body.get("object"):
            entry = body["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            
            if "messages" in value:
                message = value["messages"][0]
                contact = value["contacts"][0]
                
                phone_number = message["from"]
                name = contact["profile"]["name"]
                text = message["text"]["body"]
                
                print(f"New message from {name} ({phone_number}): {text}")
                
                # 2. Send to AI
                ai_result = analyze_lead(text)
                suggestion = ai_result.get("suggestion", "No recommendation")
                is_serious = ai_result.get("is_serious", True)
                
                # 3. Log to Sheets
                log_lead(name, phone_number, text, is_serious)
                
                # 4. Save for manual approval
                pending_responses.append({
                    "id": len(pending_responses) + 1,
                    "name": name,
                    "phone_number": phone_number,
                    "incoming_message": text,
                    "suggested_reply": suggestion
                })

            return {"status": "success"}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error"}


# --- DASHBOARD ---
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(request: Request):
    """
    Local dashboard to approve or edit messages before sending.
    """
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "pending_responses": pending_responses}
    )

@app.post("/approve/{response_id}")
async def approve_response(response_id: int):
    """
    Endpoint called from the dashboard to approve and send a message.
    """
    global pending_responses
    response_to_send = next((r for r in pending_responses if r["id"] == response_id), None)
    
    if not response_to_send:
        raise HTTPException(status_code=404, detail="Response not found")
        
    # Send the message via WhatsApp API
    print(f"Sending message to {response_to_send['phone_number']}: {response_to_send['suggested_reply']}")
    send_whatsapp_message(response_to_send["phone_number"], response_to_send["suggested_reply"])
    
    # Remove from pending list
    pending_responses = [r for r in pending_responses if r["id"] != response_id]
    
    return {"status": "Sent successfully"}
