import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import markdown
from .assistant import ask_question, summarize_text, create_study_plan

# Load API key
load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')  # Works everywhere
if not api_key:
    raise ValueError("API key missing!")

import google.generativeai as genai
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

#app = Flask(__name__, template_folder="../templates")
app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ""
    summary = ""
    plan = ""
    if request.method == 'POST':
        question = request.form.get('question')
        text = request.form.get('text')
        topic = request.form.get('topic')
        days = request.form.get('days')

        try:
            if question:
                raw_answer = ask_question(question)
                answer = markdown.markdown(raw_answer)
            if text:
                raw_summary = summarize_text(text)
                summary = markdown.markdown(raw_summary)
            if topic and days:
                raw_plan = create_study_plan(topic, days)
                plan = markdown.markdown(raw_plan)
        except Exception as e:
            answer = f"Error: {str(e)}"

    return render_template("index.html", answer=answer, summary=summary, plan=plan)

# Add this to index.py (right after your routes)
def handler(request):
    with app.app_context():
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.data.decode('utf-8')
        }

if __name__ == '__main__':
    app.run(debug=True)
