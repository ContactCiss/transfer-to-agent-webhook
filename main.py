from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Dial
import urllib

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "✅ Webhook is actief!"

@app.route("/transfer", methods=["POST"])
def transfer_to_agent():
    data = request.get_json(silent=True) or request.form
    print("📩 Binnenkomend request:")
    print(data)

    phone_number = data.get("phone_number", "+31884114114")
    print(f"📞 Doorschakelen naar: {phone_number}")

    response = VoiceResponse()
    dial = Dial()
    dial.number(phone_number)
    response.append(dial)

    return Response(str(response), mimetype="text/xml")

@app.route("/routes", methods=["GET"])
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        url = urllib.parse.unquote(str(rule))
        output.append(f"{url:30s} | {methods}")
    return "<pre>" + "\n".join(output) + "</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
