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
        prompt = f"""You are a professional after-hours AI dispatcher for {biz['business']}, a trusted pest control company serving {biz['city']} and surrounding areas.

{biz['opening']}

Speak calmly, confidently, and helpfully. Use natural conversation.

Core rules:
- Always greet immediately: "Thanks for calling {biz['business']}. We're closed right now, but I can help you right away."
- Ask if this is an emergency (rodents, termites, bed bugs, wasps, etc.).
- Handle emergency and routine calls properly.
- At the end, briefly mention: "By the way, this is exactly how our AI voice agent works for pest control companies 24/7."

Be empathetic and sound human."""
    else:
        prompt = """You are a demo AI dispatcher for pest control companies in the Houston area. Ask the caller their company name, then demonstrate how you handle emergency vs routine calls professionally. At the end, explain briefly that this is a live demo of a 24/7 AI voice agent for pest control businesses."""

    return jsonify({
        "response_type": "config",
        "prompt": prompt
    })


@app.route('/')
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