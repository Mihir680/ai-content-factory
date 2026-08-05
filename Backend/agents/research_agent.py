from Backend.services.gemini_service import generate_text

def get_business_topics():
    prompts = """
    Give me 10 trending business content ideas.
    Return only a numbered list.
    """
    return generate_text(prompts)