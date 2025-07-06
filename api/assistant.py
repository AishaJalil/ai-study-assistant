import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

api_key = os.environ.get('GEMINI_API_KEY')  # Works everywhere
if not api_key:
    raise ValueError("API key missing!")

# Safety check
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables!")

# Configure Gemini API
genai.configure(api_key=api_key)

# Initialize model
model = genai.GenerativeModel("models/gemini-1.5-flash")  # Note full model path

# Function: Ask a question
def ask_question(question: str) -> str:
    prompt = f"Answer this student question clearly and briefly:\n\n{question}"
    response = model.generate_content([prompt])
    return response.text.strip()

# Function: Summarize given text
def summarize_text(text: str) -> str:
    prompt = f"Summarize the following content in simple terms for a student:\n\n{text}"
    response = model.generate_content([prompt])
    return response.text.strip()

# Function: Create a study plan
def create_study_plan(subject, days):
    prompt = f"Create a {days}-day study plan to master {subject}. Return the plan in HTML list format."
    response = model.generate_content([prompt])
    return response.text.strip()
