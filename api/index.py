import os
from flask import Flask, render_template, request, jsonify
import markdown
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Load and validate API key
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable missing!")

# Configure Gemini (do this once at startup)
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Import assistant functions after Flask app creation
from .assistant import ask_question, summarize_text, create_study_plan

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = summary = plan = ""
    if request.method == 'POST':
        try:
            if (question := request.form.get('question')):
                answer = markdown.markdown(ask_question(question))
            if (text := request.form.get('text')):
                summary = markdown.markdown(summarize_text(text))
            if (topic := request.form.get('topic')) and (days := request.form.get('days')):
                plan = markdown.markdown(create_study_plan(topic, days))
        except Exception as e:
            answer = f"Error: {str(e)}"

    return render_template("index.html", answer=answer, summary=summary, plan=plan)

# Vercel serverless handler (REQUIRED)
def handler(event, context):
    with app.app_context():
        # Convert Vercel event to Flask request
        from flask.wrappers import Request
        flask_request = Request.from_values(
            path=event['path'],
            method=event['httpMethod'],
            headers=event['headers'],
            query_string=event.get('queryStringParameters', {}),
            data=event.get('body', '')
        )
        
        # Process request
        response = app.full_dispatch_request(flask_request)
        
        # Return Vercel-compatible response
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }

# Local development guard
if __name__ == '__main__':
    app.run(debug=True)
    