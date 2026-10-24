# GenAI Studio

A fully customizable, end-to-end Generative AI chat application powered by the OpenAI API. Bring your own API key, pick any model you have access to, and tune every generation parameter from the UI.

## Features

- **Streaming responses** — tokens render live as the model generates them.
- **Bring-your-own API key** — paste a key in the sidebar, or store one server-side in `.env` and leave the field blank.
- **Model picker** — choose from common GPT models, or hit "Refresh Models" to pull the exact list your account has access to.
- **Full generation controls** — system prompt, temperature, max tokens, top-p.
- **Markdown + syntax-highlighted code blocks** with one-click copy.
- **Light / dark / system theme toggle.**
- **Export chat** to JSON, or clear the conversation.
- **Responsive UI** — works on desktop and mobile.
- Chat history and settings persist locally in the browser (`localStorage`).

## Project structure

```
demo gen ai/
├── app.py            # Flask backend — /api/chat (streaming), /api/models, /api/health
├── index.html         # Frontend UI (single file, no build step)
├── requirements.txt   # Python dependencies
├── .env               # Your OpenAI API key (not committed — see .gitignore)
└── .gitignore
```

## Setup

1. **Install dependencies** (Python 3.9+):

   ```bash
   pip install -r requirements.txt
   ```

2. **Add your OpenAI API key** to `.env` in the project root:

   ```
   OPENAI_API_KEY=sk-...
   ```

   This is optional — you can instead paste a key directly into the sidebar in the browser. A key entered in the UI always overrides the server-side `.env` key for that request.

3. **Run the server:**

   ```bash
   python app.py
   ```

4. Open **http://127.0.0.1:5000** in your browser.

## Configuration (in the sidebar)

| Setting | Description |
|---|---|
| API Key | Overrides the server `.env` key for your session. Leave blank to use the server key. |
| Model | Any chat-capable OpenAI model (`gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, etc). Click "Refresh Models" to list exactly what your key can access. |
| System Prompt | Instructions sent before every conversation. |
| Temperature | 0–2, controls randomness. |
| Max Tokens | Upper bound on response length. |
| Top P | Nucleus sampling cutoff. |

## Security notes

- `.env` is listed in `.gitignore` — never commit it.
- The API key you type in the sidebar is stored only in your browser's `localStorage` and sent to your own local backend, which forwards it to OpenAI over HTTPS. It is never sent anywhere else.
- If a key is ever pasted into a chat log, IDE, or shared document, rotate it in the OpenAI dashboard.

## Customizing further

- **Swap providers**: `app.py` isolates all OpenAI calls in `/api/chat` and `/api/models` — point those at Azure OpenAI, Anthropic, or a local model server by changing the client construction.
- **Add features**: the frontend is a single static `index.html` with no build step, so UI changes are just edits to that file.
- **Persist chats server-side**: currently chat history lives in the browser only; swap in a database if you need multi-device sync.
