import os
import re
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL_NAME = "llama-3.3-70b-versatile"
MAX_HISTORY_TURNS = 20
MAX_TOKENS = 1024
TEMPERATURE = 0.7

SYSTEM_PROMPT = (
    "You are Aria, a brilliant and warm AI assistant. "
    "Be helpful, clear, and concise. "
    "Never use **, ##, *, __, ~~~, or markdown bullet points. "
    "Use plain numbered lists when needed. Write clean paragraphs. "
    "Remember the full conversation and refer to it naturally."
)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
body, .gradio-container {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: #0f0f13 !important;
}
.gradio-container {
    max-width: 820px !important;
    margin: 0 auto !important;
}
#chatbot {
    background: #16161f !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 16px !important;
}
#send-btn {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-weight: 600 !important;
}
#clear-btn, #retry-btn {
    background: #1e1e2e !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
}
footer { display: none !important; }
"""


def clean_response(text):
    text = re.sub(r"\*{1,3}", "", text)
    text = re.sub(r"#{1,6}\s?", "", text)
    text = re.sub(r"_{1,2}", "", text)
    text = re.sub(r"`{1,3}", "", text)
    text = re.sub(r"~~", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chat(user_message, history):
    if not user_message.strip():
        return history, ""

    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history[-MAX_HISTORY_TURNS:]:
        msgs.append({"role": turn["role"], "content": turn["content"]})
    msgs.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME, messages=msgs,
            max_tokens=MAX_TOKENS, temperature=TEMPERATURE, top_p=0.9,
        )
        reply = clean_response(response.choices[0].message.content)
    except Exception as e:
        err = str(e)
        if "api_key" in err.lower() or "authentication" in err.lower():
            reply = "API key error: Check your GROQ_API_KEY in .env file."
        elif "rate_limit" in err.lower():
            reply = "Rate limit reached. Please wait and try again."
        else:
            reply = f"Error: {err}"

    history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": reply},
    ]
    return history, ""


def retry(history):
    if len(history) < 2:
        return history
    last_user = history[-2]["content"]
    history = history[:-2]
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history[-MAX_HISTORY_TURNS:]:
        msgs.append({"role": turn["role"], "content": turn["content"]})
    msgs.append({"role": "user", "content": last_user})
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME, messages=msgs,
            max_tokens=MAX_TOKENS, temperature=TEMPERATURE,
        )
        reply = clean_response(response.choices[0].message.content)
    except Exception as e:
        reply = f"Error: {str(e)}"
    return history + [
        {"role": "user", "content": last_user},
        {"role": "assistant", "content": reply},
    ]


EXAMPLES = [
    "Hello! What can you help me with?",
    "Explain quantum computing simply.",
    "Write a short poem about the night sky.",
    "3 tips for staying focused while studying.",
    "Tell me something amazing about space.",
    "Help me write a professional email.",
]


def build_ui():
    with gr.Blocks(title="Aria AI Assistant") as demo:

        gr.HTML("""
        <div style="text-align:center; padding:32px 0 20px;">
            <div style="font-size:2rem; font-weight:700;
                background:linear-gradient(135deg,#a78bfa,#60a5fa,#f472b6);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                margin-bottom:6px;">
                &#10022; Aria
            </div>
            <div style="color:#94a3b8; font-size:0.88rem;">
                Your intelligent AI assistant &mdash; powered by Llama 3.3 70B via Groq
            </div>
        </div>
        """)

        chatbot = gr.Chatbot(
            elem_id="chatbot",
            label="",
            height=460,
            show_label=False,
        )

        with gr.Row():
            msg_input = gr.Textbox(
                placeholder="Ask me anything...",
                show_label=False,
                scale=9,
                container=False,
                lines=1,
                max_lines=4,
            )
            send_btn = gr.Button("Send", elem_id="send-btn", scale=1, variant="primary")

        with gr.Row():
            clear_btn = gr.Button("Clear Chat", elem_id="clear-btn", size="sm")
            retry_btn = gr.Button("Retry Last", elem_id="retry-btn", size="sm")

        gr.Examples(
            examples=EXAMPLES,
            inputs=msg_input,
            label="Quick prompts",
        )

        gr.HTML('<div style="text-align:center;color:#2a2a3a;font-size:0.72rem;padding:16px 0;">Aria &bull; Groq API &bull; llama-3.3-70b-versatile</div>')

        msg_input.submit(chat, inputs=[msg_input, chatbot], outputs=[chatbot, msg_input])
        send_btn.click(chat, inputs=[msg_input, chatbot], outputs=[chatbot, msg_input])
        retry_btn.click(retry, inputs=[chatbot], outputs=[chatbot])
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg_input])

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        css=CSS,
    )