import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# إعداداتك الخاصة
VERIFY_TOKEN = "OverBot_123"
ACCESS_TOKEN = "EAAV3Lxl8JBIBQ35fnVC1N6BSxSDxPzvqyjFfzmMGGd8IdaDvIUtV0pUZAVJyZCNkMZBbnaB3ycdnrSl1ISfGHsC24zDbAwKgonvUgdrosWZBceWkZAGvwNZAgvRSGZAxDW7F0BJZCYVcbUV5NQ3NGfchdskGygUhC3QWcXtHZBJ1kXeqo2ZC9GeXQofS1HtvB17WYOzt1ZBZBCypzgi6PKxRGAANK2FrqYAaF9Q0tZCLJBqfoZCUNZBAdcSIwBK9nX8ULAk4JfWntCpREZC4TQA5KczUKJIq"
PHONE_NUMBER_ID = "1025739520622186"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge'), 200
    return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" in value:
                    for message in value.get("messages", []):
                        from_number = message.get("from")
                        # إرسال رد تلقائي
                        send_whatsapp_message(from_number, "أهلاً نايف! استلمت رسالتك بنجاح ✅")
    return jsonify({"status": "ok"}), 200

def send_whatsapp_message(to_number, text):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to_number, "type": "text", "text": {"body": text}}
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
