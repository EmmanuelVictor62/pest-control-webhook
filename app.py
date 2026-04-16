from flask import Flask, request, jsonify
import threading
import time
import requests

app = Flask(__name__)

# === YOUR LEAD MAPPING ===
mapping = {
    # Add more leads here
    "+17622247961": {
        "business": "Zyna Pest Control",      # ← Changed to "business"
        "city": "Dallas",
    },
}


@app.route('/retell-webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    caller = data.get('caller_phone_number')
    
    biz = mapping.get(caller)
    
    if biz:
        # Override the prompt WITH the variables included
        custom_prompt = f"""You are a professional after-hours AI dispatcher for {biz['business']}, a trusted pest control company serving {biz['city']} and surrounding areas. You answer calls when the office is closed. Speak calmly, confidently, and helpfully — like an experienced dispatcher. Use natural conversation, not a rigid script.

Core rules:
- Always start with: "Thanks for calling {biz['business']} Pest Control. We're closed right now, but I can help you right away."
- Ask: "Is this an emergency, like rodents in the kitchen, termites, bed bugs, wasps, or something else urgent?"
- If emergency: "I understand — this sounds important. I'll make sure our on-call technician contacts you within 15 minutes. May I have your name, phone number, and a quick description of the issue?"
- If routine (inspection, quote, follow-up): "Great, I'll schedule a callback from our team first thing tomorrow morning. What's your name and best phone number?"
- Confirm details and end positively: "Got it, [name]. Someone from {biz['business']} will reach out shortly. Thank you for calling — we take pest problems seriously."
- Never promise instant on-site arrival (liability). Never say "we'll be there in X minutes."
- Keep the entire call under 60–90 seconds for the demo.
- At the very end of the call, after helping, add briefly: "By the way, this is exactly how our AI voice agent works for pest control companies 24/7. Would you like to hear more about setting this up for your real phone number?"

Be empathetic with emergencies. Sound human — use contractions, short pauses if natural."""

        return jsonify({
            "response_type": "config",
            "prompt": custom_prompt,
            "dynamic_variables": {
                "business_name": biz['business'],
                "city": biz['city']
            }
        })

def home():
    return "Pest Control Webhook is running ✅"


# Keep-alive
def keep_alive():
    while True:
        try:
            requests.get("https://pest-control-webhook.onrender.com/", timeout=10)
        except:
            pass
        time.sleep(600)

if __name__ == '__main__':
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)