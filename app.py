from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# --- 1. SETUP FLASK APP ---
app = Flask(__name__)
# This allows your web page to talk to this server
CORS(app)

# --- 2. CONFIGURE YOUR GEMINI API KEY ---
try:
    # Replace "YOUR_API_KEY_HERE" with your actual key
    genai.configure(api_key="AIzaSyDdAX_59Xw6_gkNv1Yhnef-ehIqb_pub2o")
except Exception as e:
    print(f"CRITICAL ERROR: Could not configure Gemini API. {e}")


# --- 3. DEFINE THE AI MODEL'S PERSONALITY (System Prompt) ---
SYSTEM_PROMPT = """
You are MindCompanion, a gentle and supportive journaling guide. The user is interacting with you through the chat interface of their digital journal.
Your goals are:
1.  Always respond with warmth, empathy, and validation. Never be judgmental.
2.  Your tone should be kind and encouraging.
3.  Do NOT give advice or medical diagnoses. You are a listener, not a therapist.
4.  Engage in a continuous, natural conversation. Ask gentle, open-ended follow-up questions to help the user explore their thoughts more deeply.
5.  Keep your responses thoughtful but not excessively long.
"""

# --- 4. CREATE THE API ENDPOINT FOR CHAT ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    history = data.get('history', []) 

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        chat_session = model.start_chat(history=history or [
            {'role': 'user', 'parts': [SYSTEM_PROMPT]},
            {'role': 'model', 'parts': ["Of course. I am ready to listen with warmth and empathy."]}
        ])
        
        response = chat_session.send_message(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"ERROR calling Gemini API: {e}")
        return jsonify({"error": "Failed to get response from AI"}), 500

# --- 5. RUN THE FLASK SERVER ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)