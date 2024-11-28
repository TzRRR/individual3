from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Configure OpenAI API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    email_draft = None
    if request.method == "POST":
        purpose = request.form.get("purpose")
        tone = request.form.get("tone")
        additional_details = request.form.get("details")
        
        # Generate prompt for LLM
        prompt = f"""
        Write a professional email for the following scenario:
        - Purpose: {purpose}
        - Tone: {tone}
        - Additional Details: {additional_details}
        """

        try:
            # Use OpenAI's chat model
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Switch to the supported model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates professional emails."},
                    {"role": "user", "content": f"Generate an email for the following: Purpose: {purpose}, Tone: {tone}, Additional Details: {additional_details}"}
                ],
                max_tokens=200,
                temperature=0.7
            )
            email_draft = response['choices'][0]['message']['content'].strip()
        except Exception as e:
            email_draft = f"Error generating email: {e}"

    return render_template("index.html", email_draft=email_draft)

if __name__ == "__main__":
    app.run(debug=True)
