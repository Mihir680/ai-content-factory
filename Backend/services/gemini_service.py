import os
import re
import time
import requests
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai_client = None
use_legacy = False

if gemini_api_key:
    try:
        from google import genai
        genai_client = genai.Client(api_key=gemini_api_key)
    except Exception:
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=gemini_api_key)
            genai_client = legacy_genai.GenerativeModel("gemini-2.0-flash")
            use_legacy = True
        except Exception:
            pass


def extract_topic_from_prompt(prompt: str) -> str:
    """Extracts target topic keyword from prompt string."""
    match = re.search(r"Topic:\s*(.+)", prompt, re.IGNORECASE)
    if match:
        return match.group(1).strip().split("\n")[0]
    return "this exciting topic"


def generate_text_via_groq(prompt: str) -> str:
    """Generates text via Groq API trying multiple fallback models."""
    if not groq_api_key:
        return ""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key.strip()}",
        "Content-Type": "application/json"
    }

    groq_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-70b-8192",
        "mixtral-8x7b-32768"
    ]

    for model_name in groq_models:
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a world-class YouTube content creator, viral scriptwriter, and Hollywood visual effects director."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        try:
            res = requests.post(url, json=payload, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                content = data["choices"][0]["message"]["content"]
                print(f"[Groq AI Success] Generated viral content using model: {model_name}!")
                return content
            else:
                print(f"[Groq Notice] Model {model_name} status {res.status_code}, trying next model...")
        except Exception as e:
            print(f"[Groq Error] {e}")

    return ""


def generate_text_via_pollinations(prompt: str) -> str:
    """Generates text via Pollinations Free Text AI API."""
    try:
        encoded_prompt = requests.utils.quote(prompt[:800])
        url = f"https://text.pollinations.ai/{encoded_prompt}?model=mistral"
        res = requests.get(url, timeout=10)
        if res.status_code == 200 and len(res.text.strip()) > 20:
            print("[Pollinations Text AI] Successfully generated free content!")
            return res.text.strip()
    except Exception as e:
        print(f"[Pollinations Text Error] {e}")
    return ""


def generate_text(prompt: str) -> str:
    """
    Multi-LLM Engine:
    1. Groq API (Multi-model retry)
    2. Google Gemini API
    3. Pollinations Free Text AI
    4. Smart Topic-Locked Fallback Generator
    """
    topic = extract_topic_from_prompt(prompt)

    # 1. Try Groq API first
    groq_output = generate_text_via_groq(prompt)
    if groq_output:
        return groq_output

    # 2. Try Gemini API
    if genai_client:
        for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                if use_legacy:
                    response = genai_client.generate_content(prompt)
                    return response.text
                else:
                    response = genai_client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    return response.text
            except Exception:
                pass

    # 3. Try Pollinations Text AI (Free zero-key LLM)
    pollinations_output = generate_text_via_pollinations(prompt)
    if pollinations_output:
        return pollinations_output

    # 4. Fallback
    return get_fallback_text(prompt, topic)


def get_fallback_text(prompt: str, topic: str):
    """Generates dynamic topic-matched fallback content."""
    clean_topic = topic.strip() if topic else "this topic"
    topic_lower = clean_topic.lower()
    
    if "script" in prompt.lower() or "director" in prompt.lower() or "narration" in prompt.lower():
        if "car" in topic_lower or "supercar" in topic_lower or "auto" in topic_lower or "vehicle" in topic_lower:
            return (
                "These 5 secret supercars are so expensive, only multi-billionaires can own them! "
                "Number 1: The $18 Million Bugatti La Voiture Noire, featuring a quad-turbo W16 engine. "
                "Number 2: The $30 Million Rolls-Royce Droptail, crafted with hand-carved wood veneer. "
                "Number 3: The Pagani Zonda HP Barchetta, built with a raw V12 screaming exhaust sound. "
                "Number 4: The Koenigsegg Jesko Absolut, reaching a mind-bending top speed of 330 miles per hour! "
                "Number 5: The $2.7 Million Mercedes-AMG One, powered by an actual Formula 1 hybrid engine! "
                "Which of these 5 secret hypercars would you pick? Subscribe for more mind-blowing car facts!"
            )
        else:
            return (
                f"These secret facts about {clean_topic} will blow your mind! "
                f"First: {clean_topic} is built with extreme precision and rare engineering. "
                f"Second: It reaches performance levels that normal people never get to see. "
                f"Third: Every single detail is designed for pure power and performance. "
                f"Fourth: Only a handful of people in the world can ever own this! "
                f"Which secret about {clean_topic} surprised you most? Subscribe now for more!"
            )

    elif "title" in prompt.lower():
        return f"Top 5 Secret Supercars Worth Millions That Only Billionaires Can Buy!\nThe Truth About {clean_topic}\nWhy {clean_topic} Changes Everything"
    elif "description" in prompt.lower():
        return f"Explore fascinating insights about {clean_topic}. Discover facts, news, and key details in this quick breakdown."
    elif "hashtag" in prompt.lower():
        clean_tag = re.sub(r"[^\w]", "", clean_topic)
        return f"#{clean_tag} #Trending #Supercars #Information #Viral"
    else:
        return f"Explore everything you need to know about {clean_topic}."