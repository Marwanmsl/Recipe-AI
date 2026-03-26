# 🍽️ AI-Powered Recipe Generator

This project is a **web-based AI recipe generator** that uses a local Large Language Model (LLM) via **Ollama** to create structured cooking recipes from user input in real time.

Built with **Flask**, it provides a simple interface where users can enter any dish idea and instantly receive a clean, step-by-step recipe.

---

## 🚀 Features

### 🧠 AI Recipe Generation

* Uses **qwen2.5:3b** model via Ollama
* Converts user input into a structured recipe
* Outputs:

  * Recipe Name
  * Ingredients
  * Steps
  * Cooking Time
  * Tips

---

### ⚡ Real-Time Streaming Response

* Recipes are streamed token-by-token
* Users see results instantly as they are generated
* Improves responsiveness and user experience

---

### 🔄 Auto Model & Server Setup

* Automatically:

  * Starts Ollama server if not running
  * Downloads model if not available

---

### 📜 History Management

* Stores past prompts and generated recipes in memory
* API endpoints to:

  * View history
  * Retrieve specific items
  * Delete individual entries
  * Clear all history

---

## 🏗️ Architecture

```id="arch1"
User Input (Browser)
        │
        ▼
    Flask Server
        │
        ▼
 Prompt Formatting
        │
        ▼
   Ollama (LLM)
        │
        ▼
 Streaming Response
        │
        ▼
  Browser Display
```

---

## ⚙️ Tech Stack

* **Python**
* **Flask** – backend web framework
* **Ollama** – local LLM runtime
* **Qwen2.5:3B** – language model
* **HTML (Jinja2)** – frontend templating
* **JavaScript (optional)** – for handling streaming

---

## 🧩 Key Components

### `start_ollama()`

* Checks if Ollama server is running
* If not, starts it automatically using subprocess
* Waits until server becomes available

---

### `ensure_model()`

* Verifies that the required model exists
* If not, pulls it using:

```id="cmd1"
ollama pull qwen2.5:3b
```

---

### `/generate` Route

* Accepts user input
* Formats prompt for recipe generation
* Streams AI response back to client
* Cleans unwanted characters
* Stores result in history

---

### Streaming Logic

* Uses generator (`yield`) to send chunks progressively
* Enables real-time text output instead of waiting for full response

---

### History APIs

#### 📜 Get All History

```id="api1"
GET /history
```

#### 📌 Get Single Entry

```id="api2"
GET /history/<index>
```

#### ❌ Delete Entry

```id="api3"
DELETE /delete/<index>
```

#### 🧹 Clear History

```id="api4"
DELETE /clear
```

---

## 🔌 How It Works

1. User enters a dish (e.g., "chicken biryani")
2. Flask formats prompt for AI
3. Ollama processes using LLM
4. Response is streamed back
5. Result is saved in memory

---

## 🧪 Example Input

```id="input1"
chocolate cake
```

### Output (Generated)

* Recipe Name: Chocolate Cake
* Ingredients: ...
* Steps: ...
* Cooking Time: ...
* Tips: ...

---

## ⚠️ Limitations

* History is stored in memory (lost on restart)
* Requires Ollama installed locally
* Model size may affect performance on low-end systems

---

## 🔮 Future Improvements

* Save history to database
* Add user authentication
* Export recipes (PDF/print)
* Multi-language support
* Image generation for dishes

---

## ▶️ How to Run

```bash id="run1"
pip install flask ollama requests
python app.py
```

Make sure:

* Ollama is installed
* Model `qwen2.5:3b` is available (auto-downloaded if not)

---

## 💡 Use Cases

* Home cooking inspiration
* AI cooking assistants
* Recipe automation apps
* Learning cooking with AI

---

## 👨‍💻 Author

Built as a simple and powerful demonstration of integrating **local LLMs with web apps**.

---

## ⭐ Support

If you like this project:

* Star ⭐ the repo
* Share with others
* Contribute improvements

---
