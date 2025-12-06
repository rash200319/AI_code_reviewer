# 🤖 AI Code Reviewer

An expert static analysis tool designed to review Python code, detect common code smells, and provide intelligent, actionable suggestions using **Groq Cloud LLM** for fast, accurate analysis. This project is built using Python's Abstract Syntax Tree (AST) for precise code analysis, features automated code fixes, and includes an interactive web dashboard for visualization.

---

## ✨ Features Completed (Weeks 1, 2 & 3)

### 1. 🔍 Static Analysis & Detection (Week 1)
* **AST Parsing:** Uses Python's built-in `ast` module to accurately parse code into a structure for reliable detection.
* **Code Smell Detection:** Implements the core logic to identify specific code smells, such as **Magic Numbers** (hardcoded numerical values).
* **Report Generation:** Generates a structured **JSON report** containing file metadata and detailed information about every detected issue (type, line, column, value, and message).

### 2. 🧠 AI/LLM Integration (Week 2 & 3)
* **Groq Cloud LLM (Week 3):** Upgraded from local Ollama to **Groq Cloud API** for significantly faster performance using the `Llama 3.1 8B Instant` model. This eliminates slow local inference while maintaining cost-effectiveness with generous free tier limits.
* **Intelligent Suggestions:** For every detected code smell, the tool sends the context to the LLM and generates a **concise, actionable, and friendly refactoring suggestion** which is added to the final report.
* **Robust Connection:** Implements reliable connection logic and error handling to communicate with the Groq API using environment variables for API key management.

### 3. 🔧 Automated Code Fixing (Week 3)
* **AutoFix Engine:** Automatically generates fix descriptions for detected code smells (e.g., Magic Numbers).
* **Patch Generation:** Creates structured patch data containing the fix information (constant name, value, line number, old code).
* **Fix Application:** Applies prepared fixes from the report back to the source code with proper file management.

### 4. 📊 Interactive Dashboard (Week 3)
* **Web-based UI:** Built with **Streamlit** for an intuitive, interactive dashboard to visualize code analysis results.
* **Results Visualization:** Displays metadata, detected issues, AI suggestions, and autofix statuses in a clean tabular format.
* **Real-time Feedback:** Shows fix descriptions and statuses for each issue identified in the code.

---

## 💻 Setup and Installation

### Prerequisites

1.  **Python 3.8+**
2.  **Groq API Key:** Sign up for a free Groq Cloud account at [https://groq.com](https://groq.com) and obtain your API key (free tier includes generous monthly credits for inference).

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
    ```
4.  **Set up environment variable for Groq API Key:**
    - **Windows (CMD):**
      ```bash
      set GROQ_API_KEY=your_groq_api_key_here
      ```
    - **Windows (PowerShell):**
      ```bash
      $env:GROQ_API_KEY="your_groq_api_key_here"
      ```
    - **Linux/macOS:**
      ```bash
      export GROQ_API_KEY=your_groq_api_key_here
      ```

---

## 🚀 Usage

### 1. Analyze a Python File and Generate Report

```bash
# Ensure the GROQ_API_KEY environment variable is set.
python -m cli.main <path_to_your_python_file>
```

**Example:**
```bash
python -m cli.main sample_project/example.py
```

This will generate a `code_reviewer_report.json` containing:
- Detected code smells (e.g., Magic Numbers)
- AI-powered suggestions from Groq LLM
- Automated fix descriptions and patch data

### 2. View Results in the Interactive Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard provides:
- 📊 Overview of analysis metadata and statistics
- 🔍 Detailed table of all detected issues with line numbers and descriptions
- 💡 AI suggestions for each issue
- 🔧 Fix status and autofix descriptions
- 📈 Visual representation of code quality metrics

### 3. Apply Automated Fixes (Week 3)

```bash
python -c "from core.autofix.fixer import Fixer; Fixer.apply_fixes_from_report('code_reviewer_report.json', '<path_to_file>')"
```

This applies the prepared fixes from the report back to your source code.

---

## 📁 Project Structure

```
AI_code_reviewer/
├── cli/
│   └── main.py                    # CLI entry point for code analysis
├── core/
│   ├── parser/
│   │   └── python_parser.py       # AST-based Python code parser
│   ├── detectors/
│   │   └── magic_number_detector.py  # Magic Number detection logic
│   ├── llm/
│   │   └── suggestion_generator.py   # Groq LLM integration for AI suggestions
│   ├── autofix/
│   │   └── fixer.py               # Automated fix generation & application
│   └── report/
│       └── (Report generation utilities)
├── dashboard/
│   ├── app.py                     # Streamlit dashboard application
│   └── ui/                        # Dashboard UI components
├── sample_project/
│   └── example.py                 # Sample code for testing
├── tests/
│   └── (Unit tests)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🛠️ Technology Stack

- **Python 3.8+** – Core language
- **AST Module** – Code parsing and analysis
- **Groq Cloud API** – Fast, cloud-based LLM with Llama 3.1 8B Instant
- **Streamlit** – Interactive web dashboard
- **FastAPI & Uvicorn** – (Optional) Backend server framework
- **Pytest** – Unit testing framework
- **Click** – Command-line interface utilities

---

## 🎯 Future Enhancements (Planned)

- [ ] Support for additional code smell detectors (Dead Code, Code Duplication, etc.)
- [ ] Multiple language support (JavaScript, Java, etc.)
- [ ] GitHub Actions integration for CI/CD pipelines
- [ ] Web API for remote analysis
- [ ] Configurable fix strategies and severity levels
- [ ] Performance profiling and optimization recommendations

---

## 📝 License

This project is open-source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request with your improvements.
