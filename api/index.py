import os
from flask import Flask, render_template, request, jsonify
import markdown
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Configure Gemini (must be outside handler)
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable missing!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Import assistant functions
try:
    from .assistant import ask_question, summarize_text, create_study_plan
except ImportError:
    from assistant import ask_question, summarize_text, create_study_plan

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

# Vercel Serverless Adapter (REQUIRED)
def vercel_handler(req):
    with app.request_context(req.environ):
        try:
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }

# Local development
if __name__ == '__main__':
    app.run(debug=True)