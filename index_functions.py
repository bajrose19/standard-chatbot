import google.generativeai as genai

def generate_response_gemini(api_key, prompt, temperature=0.7, model="models/gemini-2.5-flash"):
    try:
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(model)

        response = gemini_model.generate_content(
            prompt,
            generation_config={"temperature": temperature}
        )

        return (response.text or "").strip()

    except Exception as e:
        return f"An error occurred: {str(e)}"
