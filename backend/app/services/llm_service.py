# Base LLM service interface
import os
from groq import Groq
from app.core.config import settings
from google import genai
from google.genai import types

class LLMService:
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
            
        )

       
        self.model = "llama-3.1-8b-instant" 
        self.gemini_model_name = "gemini-3-flash-preview"
        self.google_api_key = settings.GOOGLE_API_KEY
         

    def generate_summary(self, text: str, summary_type: str) -> str:
        """
        Generates a summary using Groq.
        summary_type: 'short' or 'medium'
        """
        

        if summary_type.lower() == "short":
            instruction = "Provide a concise summary in 3-5 bullet points. Focus on the absolute key facts."
        else:
            instruction = "Provide a medium-length summary (2-3 paragraphs). Cover the main history, key concepts, and significant details."


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
                temperature=0.5,
                max_tokens=1024,
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            print(f"Error generating summary: {e}")
            raise e
        
    def get_translation(self, text: str, target_language: str) -> str:
     
        client = genai.Client(api_key=self.google_api_key)
        
        prompt = f"Translate the text to {target_language} : {text}"

        try:
            response = client.models.generate_content(
                model=self.gemini_model_name, # Pass the string name, not a model object
                config=types.GenerateContentConfig(
                    system_instruction="You are an expert translator",
                    temperature=1.0,
                    top_p=0.95,
                    top_k=60
                ),
                contents=prompt,
            )
            return response.text
        except Exception as e:
            print(f"Error generating translation: {e}")
            raise e