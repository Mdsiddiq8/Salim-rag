import json
import os

from dotenv import load_dotenv
from flask import Flask, Response, request, send_from_directory
from openai import OpenAI

load_dotenv()

app = Flask(__name__, static_folder=None)

DEFAULT_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def resolve_api_key(payload):
    return (payload.get("api_key") or "").strip() or DEFAULT_API_KEY


@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")


@app.route("/api/health")
def health():
    return {"status": "ok", "server_key_configured": bool(DEFAULT_API_KEY)}


@app.route("/api/models", methods=["POST"])
def models():
    payload = request.get_json(silent=True) or {}
    api_key = resolve_api_key(payload)
    if not api_key:
        return {"error": "No API key provided"}, 400

    try:
        client = OpenAI(api_key=api_key)
        model_list = client.models.list()
        chat_models = sorted(
            m.id
            for m in model_list.data
            if m.id.startswith("gpt") and "instruct" not in m.id
        )
        return {"models": chat_models}
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    api_key = resolve_api_key(payload)

    if not api_key:
        def error_stream():
            yield "data: " + json.dumps({"error": "No API key provided"}) + "\n\n"
            yield "data: [DONE]\n\n"
        return Response(error_stream(), mimetype="text/event-stream")

    messages = payload.get("messages") or []
    model = payload.get("model") or "gpt-4o-mini"
    temperature = payload.get("temperature", 0.7)
    max_tokens = payload.get("max_tokens", 4096)
    top_p = payload.get("top_p", 1.0)

    def generate():
        try:
            client = OpenAI(api_key=api_key)
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stream=True,
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield "data: " + json.dumps({"content": delta.content}) + "\n\n"
        except Exception as e:
            yield "data: " + json.dumps({"error": str(e)}) + "\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
