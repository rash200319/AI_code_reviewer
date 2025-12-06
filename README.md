# 🤖 AI Code Reviewer

An expert static analysis tool designed to review Python code, detect common code smells, and provide intelligent, actionable suggestions using a local Large Language Model (LLM). This project is built using Python's Abstract Syntax Tree (AST) for precise code analysis and Ollama for free, local AI enrichment.

---

## ✨ Features Completed (Weeks 1 & 2)

### 1. 🔍 Static Analysis & Detection (Week 1)
* **AST Parsing:** Uses Python's built-in `ast` module to accurately parse code into a structure for reliable detection.
* **Code Smell Detection:** Implements the core logic to identify specific code smells, such as **Magic Numbers** (hardcoded numerical values).
* **Report Generation:** Generates a structured **JSON report** containing file metadata and detailed information about every detected issue (type, line, column, value, and message).

### 2. 🧠 Local AI/LLM Integration (Week 2)
* **Free LLM Backend:** Successfully integrated with **Ollama** to use open-source LLMs (like `deepseek-r1:8b`) running locally on the user's machine. This eliminates the need for external cloud APIs, billing, or API keys for a fully cost-free solution.
* **Intelligent Suggestions:** For every detected code smell, the tool sends the context to the local LLM and generates a **concise, actionable, and friendly refactoring suggestion** which is added to the final report.
* **Robust Connection:** Implements reliable connection logic and error handling to communicate with the local Ollama server at `http://127.0.0.1:11434`.

---

## 💻 Setup and Installation

### Prerequisites

1.  **Python 3.8+**
2.  **Ollama Application:** Install the Ollama application for your operating system to run the local LLM server.
3.  **Model Download:** Once Ollama is installed, download the required code model:
    ```bash
    ollama run deepseek-r1:8b
    ```

### Project Setup

1.  **Clone the repository:** (Assume you have this step already done)
2.  **Create and activate a virtual environment (`venv`):**
    ```bash
    python -m venv venv
    venv\Scripts\activate.bat   # For Windows
    # source venv/bin/activate  # For Linux/macOS
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    # OR (if no requirements.txt):
    pip install ollama
    ```

---

## 🚀 Usage

To analyze a file and generate the report:

```bash
# Ensure the Ollama application is running in the background.
python -m cli.main <path_to_your_python_file>
```
example 
 - python -m cli.main sample_project/example.py