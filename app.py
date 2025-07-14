from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")

    prompt = f"""
You are a legal assistant chatbot specialized in global vehicle regulations such as FMVSS and ECE.
Answer the following question based on the latest known regulations. Include the regulation name (e.g., FMVSS 111), the requirement (e.g., 2 seconds), and the regulation date or version if available.

Question: {user_question}
Answer:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about vehicle safety regulations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        answer = response['choices'][0]['message']['content'].strip()
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'answer': f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
