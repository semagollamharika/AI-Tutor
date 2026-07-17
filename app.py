!pip -q install google-genai gradio

import os
import gradio as gr
from google import genai

# Read API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are a StudyMate AI, a highly intelligent tutor and educational assistant.

Instructions:
- Answer study-related questions clearly and accurately.
- Explain concepts in simple and easy-to-understand language.
- Provide step-by-step explanations whenever appropriate.
- Use examples to improve understanding.
- If programming code is requested, provide complete and well-commented code.
- Explain code line by line if requested.
- Present information using headings, bullet points, or tables whenever helpful.
- If solving numerical problems, show all calculation steps.
- If multiple solutions exist, explain the best one first.
- If you are unsure of an answer, clearly state that instead of guessing.
- Maintain a polite, friendly, and professional tone.
- Format every response neatly for easy reading.
"""

# Create chat session
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "system_instruction": SYSTEM_PROMPT
    }
)

def respond(message, history):
    global chat
    response = chat.send_message(message)
    return response.text

def clear_chat():
    global chat

    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )

    return [], ""

with gr.Blocks(title="AI Study Tutor") as demo:

    gr.Markdown("# 📚 StudyMate AI")
    gr.Markdown("Ask any study-related question.")

    chatbot = gr.ChatInterface(
        fn=respond
    )

    clear_btn = gr.Button("🗑️ Clear Chat")

    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot.chatbot, chatbot.textbox]
    )

demo.launch()
