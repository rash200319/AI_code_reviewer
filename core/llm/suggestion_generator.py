# ai-code-reviewer/core/llm/suggestion_generator.py (Revised for Robustness)
import os
from typing import Dict, Any, Optional

# --- Import errors separately (Crucial for the except block to work) ---
try:
    from ollama import Client, errors as ollama_errors
except ImportError:
    class FakeOllamaErrors:
        class RequestError(Exception): pass
    ollama_errors = FakeOllamaErrors()
    # No client initialization here

class SuggestionGenerator:
    def __init__(self, model: str = "deepseek-r1:8b"):
        self.model = model
        self.client = None
        self.system_prompt = (
            "You are an expert static analysis tool and code reviewer. "
            "Your task is to take a detected Python code smell and the surrounding code, "
            "and provide a concise, actionable, and friendly suggestion to fix the issue. "
            "DO NOT provide the fixed code, only the explanation and suggestion. Keep it under 50 words."
        )

    def _ensure_client(self):
        # We only try to initialize if the client is None
        if self.client is None:
            try:
                from ollama import Client
                self.client = Client(host="http://127.0.0.1:11434")
                self.client.list()  # Test connection
                print("✅ Ollama client connected!")
            except Exception as e:
                print(f"⚠️ Could not connect to Ollama: {e}")
                self.client = None

    def generate_suggestion(self, issue: Dict[str, Any], file_content: str) -> Optional[str]:
        self._ensure_client()
        if not self.client:
            return "LLM service is not available (Ollama server not running or connection failed)."

        # --- CONSTRUCTING THE USER PROMPT (same as before) ---
        try:
            context_line = file_content.splitlines()[issue['line'] - 1].strip()
        except IndexError:
            context_line = "Error loading context line."

        user_prompt = f"""
        Analyze this issue detected in a Python file.
        ... (rest of user_prompt) ...
        """
        
        try:
            # --- OLLAMA API CALL ---
            response_obj = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={'temperature': 0.3}
            )
            
            # --- CRITICAL FIX: Check if the message content exists ---
            if response_obj and 'message' in response_obj and 'content' in response_obj['message']:
                return response_obj['message']['content'].strip()
            else:
                # If the keys are missing or content is empty/None
                return "Error: LLM returned an empty or invalid response object."

        except ollama_errors.RequestError as e:
            return f"Error communicating with Ollama: Model '{self.model}' not found or Server issue: {e}"
        except Exception as e:
            # Catch the original 'NoneType' error here if it still happens
            return f"An unknown error occurred during Ollama call: {e}"