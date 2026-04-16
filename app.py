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
        return jsonify({
            "response_type": "config",
            "prompt": None,                    # Let the base agent prompt handle it
            "dynamic_variables": {
                "business_name": biz['business'],
                "city": biz['city']
            }
        })
    else:
        # Generic fallback
        return jsonify({
            "response_type": "config",
            "prompt": """You are a demo AI dispatcher for pest control companies in the Houston area...""",
            "dynamic_variables": {}
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