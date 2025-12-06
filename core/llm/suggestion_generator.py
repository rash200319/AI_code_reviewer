# ai-code-reviewer/core/llm/suggestion_generator.py (GROQ CLOUD VERSION)
import os
from typing import Dict, Any, Optional
from groq import Groq

# Use the environment variable set above
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

class SuggestionGenerator:
    """
    Handles communication with the Groq Cloud LLM for fast suggestions.
    """
    # Using Llama 3 on Groq for excellent performance and code reasoning
    def __init__(self, model: str = "llama-3.1-8b-instant"): 
        self.model = model
        self.client = None
        
        if GROQ_API_KEY:
             try:
                self.client = Groq(api_key=GROQ_API_KEY)
                print(f"  ✅ Groq client initialized using model: {self.model}")
             except Exception as e:
                print(f"WARNING: Groq initialization failed. Error: {e}")
                self.client = None
        else:
            print("WARNING: GROQ_API_KEY not set. LLM functionality disabled.")


        self.system_prompt = (
            "You are an expert static analysis tool and code reviewer. "
            "Your task is to take a detected Python code smell and the surrounding code, "
            "and provide a concise, actionable, and friendly suggestion to fix the issue. "
            "DO NOT provide the fixed code, only the explanation and suggestion. Keep it under 50 words."
        )

    def generate_suggestion(self, issue: Dict[str, Any], file_content: str) -> Optional[str]:
        if not self.client:
            return "LLM service is not available (GROQ_API_KEY not set)."

        try:
            # Safely retrieve the context line
            context_line = file_content.splitlines()[issue['line'] - 1].strip()
        except IndexError:
            context_line = "Error loading context line."

        # --- CONSTRUCTING THE USER PROMPT ---
        user_prompt = f"""
        Analyze this issue detected in a Python file.

        Context Line (Line {issue['line']}):
        ---
        {context_line}
        ---

        Issue Details:
        - Type: {issue['type']}
        - Message: {issue['message']}
        - Detected Value: {issue.get('value', 'N/A')}

        Provide a single paragraph suggestion on how to refactor this code to fix the smell.
        """

        try:
            # --- GROQ API CALL ---
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3, 
            )
            
            # The response structure is simpler with Groq/OpenAI style APIs
            return completion.choices[0].message.content.strip()

        except Exception as e:
            return f"Error communicating with Groq: {e}"