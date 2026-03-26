from flask import Flask, render_template, request, Response, jsonify
import ollama
import re
import subprocess
import time
import requests

app = Flask(__name__)

# 🧠 In-memory history
history = []


# 🚀 Start Ollama automatically
def start_ollama():
    try:
        requests.get("http://127.0.0.1:11434")
        print("✅ Ollama already running")
    except:
        print("🚀 Starting Ollama...")

        try:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            print("❌ Ollama not found. Add it to PATH or use full path.")
            return

        # Wait until server starts
        for i in range(10):
            try:
                requests.get("http://127.0.0.1:11434")
                print("✅ Ollama started")
                return
            except:
                time.sleep(1)

        print("❌ Failed to start Ollama")


# 📦 Ensure model exists
def ensure_model():
    try:
        ollama.chat(
            model="qwen2.5:3b",
            messages=[{"role": "user", "content": "hi"}]
        )
        print("✅ Model ready")
    except:
        print("⬇️ Pulling model...")
        subprocess.run(["ollama", "pull", "qwen2.5:3b"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    user_input = request.form.get("prompt", "")

    if not user_input.strip():
        return "⚠️ Enter something..."

    prompt = f"""
You are a chef.

Create a clean recipe for:
{user_input}

No markdown. Plain text only.

Format:
Recipe Name:
Ingredients:
Steps:
Cooking Time:
Tips:
"""

    def stream():
        full_text = ""

        try:
            response = ollama.chat(
                model='qwen2.5:3b',
                messages=[{'role': 'user', 'content': prompt}],
                stream=True
            )

            for chunk in response:
                if chunk.get('message') and chunk['message'].get('content'):
                    text = re.sub(r'[#*`]', '', chunk['message']['content'])
                    full_text += text
                    yield text

            # Save to history
            history.append({
                "prompt": user_input,
                "response": full_text
            })

        except Exception as e:
            yield f"\n\n⚠️ Error: {str(e)}\n"

    return Response(stream(), content_type='text/plain')


# 📜 Get history
@app.route("/history")
def get_history():
    return jsonify(history)


# 📌 Get item
@app.route("/history/<int:index>")
def get_item(index):
    if 0 <= index < len(history):
        return jsonify(history[index])
    return jsonify({"error": "Not found"})


# ❌ Delete one
@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_item(index):
    if 0 <= index < len(history):
        history.pop(index)
        return {"status": "deleted"}
    return {"error": "Not found"}


# 🧹 Clear all
@app.route("/clear", methods=["DELETE"])
def clear_history():
    history.clear()
    return {"status": "cleared"}


if __name__ == "__main__":
    start_ollama()     # 🚀 auto start
    ensure_model()     # 📦 ensure model exists
    app.run(debug=True)