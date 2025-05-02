from flask import Flask, request, jsonify
import openai
import json
from flask_cors import CORS
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Load menu
with open("menu.json", "r") as f:
    menu = json.load(f)

# Load restaurant info
with open("restaurant_info.json", "r") as f:
    info = json.load(f)

# Format restaurant info as a readable string
restaurant_info = f"""
Restaurant Name: {info['name']}
Phone: {info['phone']}
Address: {info['address']}
Hours: {info['hours']}
Reservations: {info['reservations']}
Website: {info['website']}
"""

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    prompt = f"""
You are a friendly AI assistant for a restaurant. Use the following restaurant information and menu to answer the user's question clearly and helpfully.

{restaurant_info}

Menu:
{json.dumps(menu, indent=2)}

User: {user_input}
Assistant:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        reply = response.choices[0].message["content"]
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
