import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.5-flash-lite"


def generate_text(prompt: str):

    for attempt in range(3):
        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            return response.text

        except Exception as e:

            print(f"Attempt {attempt+1} Failed:", e)

            if attempt < 2:
                time.sleep(5)
            else:
                raise