# Base LLM service interface
import os
from groq import Groq
from app.core.config import settings # Assuming you have a settings config, otherwise use os.getenv

class LLMService:
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )
        # Using Llama3 or Mixtral via Groq for speed
        self.model = "llama3-8b-8192" 

    def generate_summary(self, text: str, summary_type: str) -> str:
        """
        Generates a summary using Groq.
        summary_type: 'short' or 'medium'
        """
        
        # 1. Define Prompt Instructions based on type
        if summary_type.lower() == "short":
            instruction = "Provide a concise summary in 3-5 bullet points. Focus on the absolute key facts."
        else:
            instruction = "Provide a medium-length summary (2-3 paragraphs). Cover the main history, key concepts, and significant details."

        # 2. Construct the System and User Prompts
        system_prompt = (
            "You are an expert educational assistant named WikiSmart. "
            "Your goal is to summarize complex academic content into clear, easy-to-understand text. "
            "Do not add any conversational filler (like 'Here is the summary'). Just output the summary."
        )

        user_prompt = f"""
        Instructions: {instruction}
        
        Source Text:
        {text}
        """

        try:
            # 3. Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                model=self.model,
                temperature=0.5, # Balanced creativity/precision
                max_tokens=1024,
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            print(f"Error generating summary: {e}")
            raise e