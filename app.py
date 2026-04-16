from flask import Flask, request, jsonify
import threading
import time
import requests

app = Flask(__name__)

# === YOUR LEAD MAPPING (add prospects here later) ===
mapping = {
    # Example:
    "+17622247961": {"business_name": "Zyna Pest Control", "city": "Dallas", "opening": "I called your office a little while ago and reached voicemail."},
}

@app.route('/retell-webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    caller = data.get('caller_phone_number')
    
    biz = mapping.get(caller)
    
    if biz:
        prompt = f"""You are a professional after-hours AI dispatcher for {biz['business']}, a trusted pest control company serving {biz['city']} and surrounding areas.

{biz['opening']}

Follow the core behavior exactly as defined in the base agent prompt. Be helpful and end with a soft mention of how this AI works for pest control businesses."""
    else:
        prompt = """You are a demo AI dispatcher for pest control companies in the Houston area. Ask the caller their company name, then demonstrate how you handle emergency vs routine calls professionally. At the end, explain briefly that this is a live demo of a 24/7 AI voice agent for pest control businesses."""

    return jsonify({
        "response_type": "config",
        "prompt": prompt
    })


# === Simple health check route (fixes 404 in browser) ===
@app.route('/')
def home():
    return "Pest Control Webhook is running ✅"


# === Keep-alive to prevent Render from spinning down ===
def keep_alive():
    while True:
        try:
            # Ping the health check route
            requests.get("https://pest-control-webhook.onrender.com/", timeout=10)
        except:
            pass
        time.sleep(600)  # every 10 minutes


if __name__ == '__main__':
    # Start keep-alive in background
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)