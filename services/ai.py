import os
import json
from openai import OpenAI

SYSTEM_PROMPT = """
You are an AI assistant helping me sell my car via WhatsApp.
Your goal is to be helpful, transparent, and save me time by filtering leads and suggesting replies.

CAR DETAILS:
- Make/Model: [Your Car Make and Model]
- Year: [Year]
- Mileage: [Mileage] km
- Price: $[Asking Price]

STRICT RULES I DO NOT NEGOTIATE:
1. NO trades (no permutas). Cash or bank transfer only.
2. NO financing or installments (no cuotas).
3. The absolute bottom price (price floor) is $[Bottom Price]. Never suggest going lower than this. If they offer less, politely decline but leave the door open if they can come up in price.
4. If they ask for photos, give them this link: [Link to Photos]

BEHAVIOR:
- Maintain a polite, clear, and direct tone.
- Be transparent about any known issues (e.g., small dent on the bumper) to avoid wasting time.

OUTPUT FORMAT:
Analyze the user's incoming message and return ONLY a valid JSON object with two keys:
1. "is_serious": boolean (true if it seems like a real, interested buyer, false if it's spam or asking for trades/financing).
2. "suggestion": string (The exact message I should send back to them in Spanish).
"""

def analyze_lead(message_text: str) -> dict:
    """
    Uses OpenAI to analyze the lead and suggest a response based on the rules.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OpenAI API key missing")
        return {
            "is_serious": True, 
            "suggestion": "No AI configured. Please reply manually."
        }
        
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Incoming WhatsApp message: '{message_text}'"}
            ],
            response_format={ "type": "json_object" },
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"Error from AI: {e}")
        return {
            "is_serious": True, 
            "suggestion": "Error generating AI response. Please reply manually."
        }
